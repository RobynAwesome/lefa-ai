from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from lefa import bridge_api
from lefa.config import Settings


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
        },
        "experience": {
            "state": "READY" if bridge_state == "VERIFIED" else "SETUP_NEEDED",
            "headline": "Alpaca is ready"
            if bridge_state == "VERIFIED"
            else "Trading connection needs setup",
            "detail": "test",
        },
    }


def _patch_test_settings(monkeypatch) -> None:
    monkeypatch.setattr(
        bridge_api,
        "Settings",
        lambda: Settings(_env_file=None),
    )


def test_missing_credentials_fail_closed(monkeypatch) -> None:
    for name in (
        "ALPACA_API_KEY",
        "ALPACA_SECRET_KEY",
        "ALPACA_API_SECRET",
        "APCA_API_KEY_ID",
        "APCA_API_SECRET_KEY",
    ):
        monkeypatch.delenv(name, raising=False)
    _patch_test_settings(monkeypatch)

    response = TestClient(_app()).get("/api/bridge/status")
    body = response.json()

    assert response.status_code == 200
    assert body["bridge_state"] == "HOLD"
    assert body["experience"]["state"] == "SETUP_NEEDED"
    assert body["provider_observation"]["code"] == "PAPER_CREDENTIALS_UNAVAILABLE"
    assert "api_key" not in body["provider_observation"]


def test_invalid_live_configuration_fails_closed(monkeypatch) -> None:
    monkeypatch.setenv("ALPACA_PAPER_TRADE", "false")
    _patch_test_settings(monkeypatch)

    body = TestClient(_app()).get("/api/bridge/status").json()

    assert body["bridge_state"] == "HOLD"
    assert body["provider_observation"]["code"] == "PAPER_CONFIGURATION_INVALID"


def test_direct_alpaca_account_verifies_without_upstream(monkeypatch) -> None:
    monkeypatch.setenv("ALPACA_API_KEY", "test-paper-key")
    monkeypatch.setenv("ALPACA_SECRET_KEY", "test-paper-secret")
    _patch_test_settings(monkeypatch)

    class FakeReadOnlyAlpaca:
        def __init__(self, settings) -> None:
            assert settings.alpaca_paper is True

        def get_account(self) -> dict:
            return {
                "status": "ACTIVE",
                "account_blocked": False,
                "trading_blocked": False,
                "trade_suspended_by_user": False,
            }

    monkeypatch.setattr(bridge_api, "ReadOnlyAlpaca", FakeReadOnlyAlpaca)

    body = TestClient(_app()).get("/api/bridge/status").json()

    assert body["bridge_state"] == "VERIFIED"
    assert body["experience"]["state"] == "READY"
    assert body["experience"]["headline"] == "Alpaca is ready"
    assert body["provider_observation"]["code"] == "PAPER_ACCOUNT_OBSERVED"


def test_provider_failure_projects_to_unavailable(monkeypatch) -> None:
    monkeypatch.setenv("ALPACA_API_KEY", "test-paper-key")
    monkeypatch.setenv("ALPACA_SECRET_KEY", "test-paper-secret")
    _patch_test_settings(monkeypatch)

    class FailingReadOnlyAlpaca:
        def __init__(self, settings) -> None:
            pass

        def get_account(self) -> dict:
            raise ConnectionError("network down")

    monkeypatch.setattr(bridge_api, "ReadOnlyAlpaca", FailingReadOnlyAlpaca)

    body = TestClient(_app()).get("/api/bridge/status").json()

    assert body["bridge_state"] == "HOLD"
    assert body["experience"]["state"] == "UNAVAILABLE"
    assert body["provider_observation"]["code"] == "PAPER_PROVIDER_UNREACHABLE"


def test_malformed_provider_response_fails_closed(monkeypatch) -> None:
    monkeypatch.setenv("ALPACA_API_KEY", "test-paper-key")
    monkeypatch.setenv("ALPACA_SECRET_KEY", "test-paper-secret")
    _patch_test_settings(monkeypatch)

    class MalformedReadOnlyAlpaca:
        def __init__(self, settings) -> None:
            pass

        def get_account(self) -> dict:
            return {"status": "ACTIVE"}

    monkeypatch.setattr(bridge_api, "ReadOnlyAlpaca", MalformedReadOnlyAlpaca)

    body = TestClient(_app()).get("/api/bridge/status").json()

    assert body["bridge_state"] == "HOLD"
    assert body["experience"]["state"] == "SETUP_NEEDED"
    assert body["provider_observation"]["code"] == "PAPER_PROVIDER_RESPONSE_INVALID"


def test_inactive_account_cannot_be_verified(monkeypatch) -> None:
    monkeypatch.setenv("ALPACA_API_KEY", "test-paper-key")
    monkeypatch.setenv("ALPACA_SECRET_KEY", "test-paper-secret")
    _patch_test_settings(monkeypatch)

    class InactiveReadOnlyAlpaca:
        def __init__(self, settings) -> None:
            pass

        def get_account(self) -> dict:
            return {
                "status": "INACTIVE",
                "account_blocked": False,
                "trading_blocked": True,
                "trade_suspended_by_user": False,
            }

    monkeypatch.setattr(bridge_api, "ReadOnlyAlpaca", InactiveReadOnlyAlpaca)

    body = TestClient(_app()).get("/api/bridge/status").json()

    assert body["bridge_state"] == "HOLD"
    assert body["provider_observation"]["code"] == "ACCOUNT_INACTIVE"
    assert body["experience"]["state"] == "SETUP_NEEDED"


def test_runtime_hold_is_small_human_state_without_provider_details(monkeypatch) -> None:
    monkeypatch.setattr(bridge_api, "_check_direct_alpaca_status", lambda: _status())

    body = TestClient(_app()).get("/api/runtime/status").json()

    assert body["schema"] == "kopano.lefa.runtime-status.v1"
    assert body["state"] == "SETUP_NEEDED"
    assert body["connection"]["state"] == "SETUP_NEEDED"
    assert body["market"]["state"] == "WAITING_FOR_EVIDENCE"
    assert body["market"]["symbol"] is None
    assert body["market"]["latest_price"] is None
    assert "provider_observation" not in body
    assert "execution_authority" not in body


def test_verified_account_waits_for_real_market_evidence(monkeypatch) -> None:
    monkeypatch.setattr(
        bridge_api,
        "_check_direct_alpaca_status",
        lambda: _status(bridge_state="VERIFIED", code="PAPER_ACCOUNT_OBSERVED"),
    )
    monkeypatch.setattr(bridge_api, "_read_market_observation", lambda: None)

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


def test_runtime_reports_fresh_alpaca_quote(monkeypatch) -> None:
    monkeypatch.setattr(
        bridge_api,
        "_check_direct_alpaca_status",
        lambda: _status(bridge_state="VERIFIED", code="PAPER_ACCOUNT_OBSERVED"),
    )
    _patch_test_settings(monkeypatch)

    class FakeReadOnlyAlpaca:
        def __init__(self, settings) -> None:
            pass

        def get_latest_quote(self, symbol: str) -> dict[str, str]:
            assert symbol == "SPY"
            return {
                "symbol": "SPY",
                "bid_price": "100.00",
                "ask_price": "101.00",
                "timestamp": datetime.now(UTC).isoformat(),
            }

    monkeypatch.setattr(bridge_api, "ReadOnlyAlpaca", FakeReadOnlyAlpaca)

    body = TestClient(_app()).get("/api/runtime/status").json()

    assert body["market"]["state"] == "OBSERVED"
    assert body["market"]["symbol"] == "SPY"
    assert body["market"]["latest_price"] == "100.50"
    assert body["market"]["observed_at"]


@pytest.mark.parametrize(
    "quote",
    [
        None,
        {},
        {
            "symbol": "SPY",
            "bid_price": "10",
            "ask_price": "9",
            "timestamp": "2000-01-01T00:00:00Z",
        },
        {
            "symbol": "SPY",
            "bid_price": "0",
            "ask_price": "9",
            "timestamp": "2000-01-01T00:00:00Z",
        },
        {"symbol": "SPY", "bid_price": "10", "ask_price": "11"},
        {
            "symbol": "SPY",
            "bid_price": "10",
            "ask_price": "11",
            "timestamp": "2099-01-01T00:00:00Z",
        },
    ],
)
def test_runtime_rejects_missing_malformed_invalid_or_stale_quote(monkeypatch, quote) -> None:
    monkeypatch.setattr(
        bridge_api,
        "_check_direct_alpaca_status",
        lambda: _status(bridge_state="VERIFIED", code="PAPER_ACCOUNT_OBSERVED"),
    )
    _patch_test_settings(monkeypatch)

    class FakeReadOnlyAlpaca:
        def __init__(self, settings) -> None:
            pass

        def get_latest_quote(self, symbol: str):
            return quote

    monkeypatch.setattr(bridge_api, "ReadOnlyAlpaca", FakeReadOnlyAlpaca)

    body = TestClient(_app()).get("/api/runtime/status").json()

    assert body["market"]["state"] == "WAITING_FOR_EVIDENCE"
    assert body["market"]["symbol"] is None
    assert body["market"]["latest_price"] is None


def test_runtime_rejects_quote_provider_failure(monkeypatch) -> None:
    monkeypatch.setattr(
        bridge_api,
        "_check_direct_alpaca_status",
        lambda: _status(bridge_state="VERIFIED", code="PAPER_ACCOUNT_OBSERVED"),
    )
    _patch_test_settings(monkeypatch)

    class FailingReadOnlyAlpaca:
        def __init__(self, settings) -> None:
            pass

        def get_latest_quote(self, symbol: str):
            raise ConnectionError("market data unavailable")

    monkeypatch.setattr(bridge_api, "ReadOnlyAlpaca", FailingReadOnlyAlpaca)

    body = TestClient(_app()).get("/api/runtime/status").json()

    assert body["market"]["state"] == "WAITING_FOR_EVIDENCE"


def test_runtime_ai_state_reflects_server_configuration(monkeypatch) -> None:
    monkeypatch.setattr(
        bridge_api,
        "_check_direct_alpaca_status",
        lambda: _status(bridge_state="VERIFIED", code="PAPER_ACCOUNT_OBSERVED"),
    )
    monkeypatch.setattr(bridge_api, "_read_market_observation", lambda: None)
    client = TestClient(_app())

    monkeypatch.delenv("FEATHERLESS_API_KEY", raising=False)
    assert client.get("/api/runtime/status").json()["ai"]["state"] == "UNAVAILABLE"

    monkeypatch.setenv("FEATHERLESS_API_KEY", "test-only-key")
    assert client.get("/api/runtime/status").json()["ai"]["state"] == "AVAILABLE"
