from fastapi import FastAPI
from fastapi.testclient import TestClient

from lefa import bridge_api


def _app() -> FastAPI:
    app = FastAPI()
    app.include_router(bridge_api.router)
    return app


def _ready_account() -> dict:
    return {
        "id": "paper-account-test",
        "status": "AccountStatus.ACTIVE",
        "account_blocked": False,
        "trading_blocked": False,
        "trade_suspended_by_user": False,
    }


class _ReadyBroker:
    def __init__(self, settings) -> None:
        self.settings = settings

    def get_account(self) -> dict:
        return _ready_account()


class _FailingBroker:
    def __init__(self, settings) -> None:
        self.settings = settings

    def get_account(self) -> dict:
        raise RuntimeError("provider unavailable")


def _configure_credentials(monkeypatch) -> None:
    monkeypatch.setenv("ALPACA_API_KEY", "test-paper-key")
    monkeypatch.setenv("ALPACA_SECRET_KEY", "test-paper-secret")
    monkeypatch.setenv("ALPACA_PAPER_TRADE", "true")


def test_missing_api_key_fails_closed_inside_lefa(monkeypatch) -> None:
    monkeypatch.setenv("ALPACA_API_KEY", "")
    monkeypatch.setenv("ALPACA_SECRET_KEY", "test-paper-secret")

    body = TestClient(_app()).get("/api/bridge/status").json()

    assert body["bridge_state"] == "HOLD"
    assert body["provider_observation"]["code"] == "PAPER_API_KEY_UNAVAILABLE"
    assert body["experience"]["state"] == "SETUP_NEEDED"


def test_missing_secret_fails_closed_inside_lefa(monkeypatch) -> None:
    monkeypatch.setenv("ALPACA_API_KEY", "test-paper-key")
    monkeypatch.setenv("ALPACA_SECRET_KEY", "")

    body = TestClient(_app()).get("/api/bridge/status").json()

    assert body["bridge_state"] == "HOLD"
    assert body["provider_observation"]["code"] == "PAPER_SECRET_KEY_UNAVAILABLE"


def test_direct_alpaca_account_observation_projects_ready(monkeypatch) -> None:
    _configure_credentials(monkeypatch)
    monkeypatch.setattr(bridge_api, "AlpacaPaperBroker", _ReadyBroker)

    response = TestClient(_app()).get("/api/bridge/status")
    body = response.json()

    assert response.status_code == 200
    assert body["bridge_state"] == "VERIFIED"
    assert body["environment"] == "paper"
    assert body["provider_observation"]["code"] == "PAPER_ACCOUNT_OBSERVED"
    assert body["experience"]["state"] == "READY"
    assert body["latest_receipt"]["account_id"] == "paper-account-test"
    assert "secret" not in str(body).lower()


def test_restricted_account_remains_hold(monkeypatch) -> None:
    _configure_credentials(monkeypatch)

    class RestrictedBroker(_ReadyBroker):
        def get_account(self) -> dict:
            account = _ready_account()
            account["trading_blocked"] = True
            return account

    monkeypatch.setattr(bridge_api, "AlpacaPaperBroker", RestrictedBroker)
    body = TestClient(_app()).get("/api/bridge/status").json()

    assert body["bridge_state"] == "HOLD"
    assert body["provider_observation"]["code"] == "PAPER_ACCOUNT_RESTRICTED"
    assert body["provider_observation"]["trading_blocked"] is True


def test_provider_failure_becomes_human_unavailable(monkeypatch) -> None:
    _configure_credentials(monkeypatch)
    monkeypatch.setattr(bridge_api, "AlpacaPaperBroker", _FailingBroker)

    body = TestClient(_app()).get("/api/bridge/status").json()

    assert body["bridge_state"] == "HOLD"
    assert body["experience"]["state"] == "UNAVAILABLE"
    assert body["provider_observation"]["code"] == "ALPACA_ACCOUNT_UNAVAILABLE"


def test_runtime_hold_is_small_human_state_without_provider_details(monkeypatch) -> None:
    monkeypatch.setattr(
        bridge_api,
        "_current_bridge_status",
        lambda: bridge_api._hold_payload(
            "PAPER_API_KEY_UNAVAILABLE",
            detail="LEFA's Alpaca paper connection still needs setup.",
        ),
    )

    body = TestClient(_app()).get("/api/runtime/status").json()

    assert body["schema"] == "kopano.lefa.runtime-status.v1"
    assert body["state"] == "SETUP_NEEDED"
    assert body["connection"]["state"] == "SETUP_NEEDED"
    assert body["market"]["state"] == "WAITING_FOR_EVIDENCE"
    assert body["market"]["symbol"] is None
    assert body["market"]["latest_price"] is None
    assert "provider_observation" not in body
    assert "execution_authority" not in body


def test_verified_account_does_not_promote_to_fake_market_truth(monkeypatch) -> None:
    _configure_credentials(monkeypatch)
    monkeypatch.setattr(bridge_api, "AlpacaPaperBroker", _ReadyBroker)

    body = TestClient(_app()).get("/api/runtime/status").json()

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


def test_runtime_ai_state_reflects_server_configuration(monkeypatch) -> None:
    _configure_credentials(monkeypatch)
    monkeypatch.setattr(bridge_api, "AlpacaPaperBroker", _ReadyBroker)
    client = TestClient(_app())

    monkeypatch.delenv("FEATHERLESS_API_KEY", raising=False)
    unavailable = client.get("/api/runtime/status").json()
    assert unavailable["ai"]["state"] == "UNAVAILABLE"

    monkeypatch.setenv("FEATHERLESS_API_KEY", "test-only-key")
    available = client.get("/api/runtime/status").json()
    assert available["ai"]["state"] == "AVAILABLE"


def test_module_has_no_sovereign_runtime_fallback() -> None:
    assert not hasattr(bridge_api, "DEFAULT_SOVEREIGN_STATUS_URL")
    assert not hasattr(bridge_api, "_read_upstream_status")
    assert not hasattr(bridge_api, "_upstream_url")
