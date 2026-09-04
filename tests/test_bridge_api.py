import json
from io import BytesIO
from urllib.error import HTTPError

from fastapi import FastAPI
from fastapi.testclient import TestClient

from lefa import bridge_api


def _app() -> FastAPI:
    app = FastAPI()
    app.include_router(bridge_api.router)
    return app


def _status(*, bridge_state: str = "HOLD", code: str = "PAPER_CREDENTIALS_UNAVAILABLE") -> dict:
    return {
        "schema": "kopano.lefa.sovereign-bridge-status.v1",
        "provider": "alpaca",
        "environment": "paper",
        "bridge_state": bridge_state,
        "execution_authority": "BACKEND_ONLY",
        "observed_at": "2026-09-02T07:33:15.995Z",
        "latest_receipt": None,
        "provider_observation": {
            "code": code,
            "account_status": "UNKNOWN",
            "account_blocked": None,
            "trading_blocked": None,
            "trade_suspended_by_user": None,
            "api_key": "must-not-cross-boundary",
        },
    }


def test_http_503_canonical_hold_body_is_still_read(monkeypatch) -> None:
    body = json.dumps(_status()).encode("utf-8")

    def raise_hold(*args, **kwargs):
        raise HTTPError(
            "https://example.invalid/status",
            503,
            "Service Unavailable",
            hdrs=None,
            fp=BytesIO(body),
        )

    monkeypatch.setattr(bridge_api, "urlopen", raise_hold)
    payload = bridge_api._read_upstream_status()
    assert payload["bridge_state"] == "HOLD"
    assert payload["provider_observation"]["code"] == "PAPER_CREDENTIALS_UNAVAILABLE"


def test_hold_projects_to_setup_needed_without_secret_fields(monkeypatch) -> None:
    monkeypatch.setattr(bridge_api, "_read_upstream_status", lambda: _status())
    client = TestClient(_app())

    response = client.get("/api/bridge/status")
    assert response.status_code == 200
    body = response.json()

    assert body["bridge_state"] == "HOLD"
    assert body["experience"]["state"] == "SETUP_NEEDED"
    assert body["experience"]["headline"] == "Trading connection needs setup"
    assert "api_key" not in body["provider_observation"]


def test_verified_projects_to_ready(monkeypatch) -> None:
    monkeypatch.setattr(
        bridge_api,
        "_read_upstream_status",
        lambda: _status(bridge_state="VERIFIED", code="ACCOUNT_ACTIVE"),
    )
    client = TestClient(_app())

    response = client.get("/api/bridge/status")
    body = response.json()

    assert body["bridge_state"] == "VERIFIED"
    assert body["experience"]["state"] == "READY"
    assert body["environment"] == "paper"
    assert body["execution_authority"] == "BACKEND_ONLY"


def test_backend_failure_projects_to_unavailable(monkeypatch) -> None:
    def fail():
        raise RuntimeError("network down")

    monkeypatch.setattr(bridge_api, "_read_upstream_status", fail)
    client = TestClient(_app())

    response = client.get("/api/bridge/status")
    body = response.json()

    assert response.status_code == 200
    assert body["bridge_state"] == "HOLD"
    assert body["experience"]["state"] == "UNAVAILABLE"
    assert body["provider_observation"]["code"] == "SOVEREIGN_BACKEND_UNAVAILABLE"


def test_invalid_upstream_contract_fails_closed(monkeypatch) -> None:
    monkeypatch.setattr(bridge_api, "_read_upstream_status", lambda: {"bridge_state": "VERIFIED"})
    client = TestClient(_app())

    response = client.get("/api/bridge/status")
    body = response.json()

    assert body["bridge_state"] == "HOLD"
    assert body["experience"]["state"] == "SETUP_NEEDED"
    assert body["provider_observation"]["code"] == "SOVEREIGN_CONTRACT_INVALID"


def test_runtime_hold_is_small_human_state_without_provider_details(monkeypatch) -> None:
    monkeypatch.setattr(bridge_api, "_read_upstream_status", lambda: _status())
    client = TestClient(_app())

    response = client.get("/api/runtime/status")
    body = response.json()

    assert response.status_code == 200
    assert body["schema"] == "kopano.lefa.runtime-status.v1"
    assert body["state"] == "SETUP_NEEDED"
    assert body["connection"]["state"] == "SETUP_NEEDED"
    assert body["market"]["state"] == "WAITING_FOR_EVIDENCE"
    assert body["market"]["symbol"] is None
    assert body["market"]["latest_price"] is None
    assert "provider_observation" not in body
    assert "execution_authority" not in body


def test_verified_account_does_not_promote_to_fake_market_truth(monkeypatch) -> None:
    monkeypatch.setattr(
        bridge_api,
        "_read_upstream_status",
        lambda: _status(bridge_state="VERIFIED", code="PAPER_ACCOUNT_OBSERVED"),
    )
    client = TestClient(_app())

    response = client.get("/api/runtime/status")
    body = response.json()

    assert response.status_code == 200
    assert body["state"] == "WAITING_FOR_MARKET"
    assert body["connection"]["state"] == "READY"
    assert body["market"] == {
        "state": "WAITING_FOR_EVIDENCE",
        "symbol": None,
        "latest_price": None,
        "market_state": "unknown",
        "observed_at": None,
    }
    assert body["decision"]["state"] == "NO_DECISION"


def test_runtime_backend_failure_is_human_unavailable(monkeypatch) -> None:
    def fail():
        raise RuntimeError("network down")

    monkeypatch.setattr(bridge_api, "_read_upstream_status", fail)
    client = TestClient(_app())

    response = client.get("/api/runtime/status")
    body = response.json()

    assert response.status_code == 200
    assert body["state"] == "UNAVAILABLE"
    assert body["connection"]["state"] == "UNAVAILABLE"
    assert body["market"]["latest_price"] is None


def test_runtime_ai_state_reflects_server_configuration(monkeypatch) -> None:
    monkeypatch.setattr(
        bridge_api,
        "_read_upstream_status",
        lambda: _status(bridge_state="VERIFIED", code="PAPER_ACCOUNT_OBSERVED"),
    )
    client = TestClient(_app())

    monkeypatch.delenv("FEATHERLESS_API_KEY", raising=False)
    unavailable = client.get("/api/runtime/status").json()
    assert unavailable["ai"]["state"] == "UNAVAILABLE"

    monkeypatch.setenv("FEATHERLESS_API_KEY", "test-only-key")
    available = client.get("/api/runtime/status").json()
    assert available["ai"]["state"] == "AVAILABLE"


def test_direct_alpaca_credentials_verifies_without_upstream(monkeypatch) -> None:
    monkeypatch.setenv("ALPACA_API_KEY", "test-paper-key")
    monkeypatch.setenv("ALPACA_SECRET_KEY", "test-paper-secret")

    def mock_urlopen(req, *args, **kwargs):
        class MockResponse:
            def read(self):
                return json.dumps({
                    "status": "ACTIVE",
                    "account_blocked": False,
                    "trading_blocked": False,
                    "trade_suspended_by_user": False,
                    "equity": "100000.00",
                }).encode("utf-8")
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
        return MockResponse()

    monkeypatch.setattr(bridge_api, "urlopen", mock_urlopen)
    # Ensure upstream is never called
    def fail_if_upstream_called():
        raise AssertionError("Upstream should not be called when direct credentials exist!")
    monkeypatch.setattr(bridge_api, "_read_upstream_status", fail_if_upstream_called)

    client = TestClient(_app())
    response = client.get("/api/bridge/status")
    assert response.status_code == 200
    body = response.json()

    assert body["bridge_state"] == "VERIFIED"
    assert body["experience"]["state"] == "READY"
    assert body["experience"]["headline"] == "Alpaca is ready"
    assert body["provider_observation"]["code"] == "PAPER_ACCOUNT_OBSERVED"
