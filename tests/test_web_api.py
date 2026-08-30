"""
Tests for LEFA AI Web API — /api/mcp/verify, /api/snapshot, /api/health.

Governance boundaries:
- No credentials in test fixtures.
- Fixture mode snapshot never returns believable financial values.
- /api/mcp/verify blocks non-paper mode.
- Execution authority is always zero.
"""
import pytest
from fastapi.testclient import TestClient

from lefa.web_api import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# /api/health
# ---------------------------------------------------------------------------


def test_health_returns_ok() -> None:
    res = client.get("/api/health")
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "ok"
    assert body["execution_authority"] == "none"


# ---------------------------------------------------------------------------
# /api/mcp/verify
# ---------------------------------------------------------------------------


def test_verify_paper_mode_ready() -> None:
    """Valid paper-mode evidence passes the proof gate."""
    res = client.post(
        "/api/mcp/verify",
        json={
            "namespace": "alpaca-paper",
            "server_identity": "alpaca-mcp",
            "server_version": "1.0.0",
            "paper_trade": True,
            "tool_names": ["get_account", "get_clock", "get_latest_quote"],
            "account_status": "ACTIVE",
            "account_blocked": False,
            "trading_blocked": False,
            "auth_ok": True,
            "network_ok": True,
            "schema_ok": True,
        },
    )
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "ready"
    assert body["failures"] == []
    assert body["paper_trade"] is True


def test_verify_live_mode_blocked() -> None:
    """Live mode (paper_trade=False) must be blocked."""
    res = client.post(
        "/api/mcp/verify",
        json={
            "namespace": "alpaca-live",
            "paper_trade": False,
            "tool_names": ["get_account"],
            "auth_ok": True,
            "network_ok": True,
            "schema_ok": True,
        },
    )
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "blocked"
    assert "live_or_unproven_mode" in body["failures"]


def test_verify_missing_namespace_blocked() -> None:
    """Missing namespace must fail the proof gate."""
    res = client.post(
        "/api/mcp/verify",
        json={
            "namespace": None,
            "paper_trade": True,
            "tool_names": ["get_account"],
            "auth_ok": True,
            "network_ok": True,
            "schema_ok": True,
        },
    )
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "blocked"
    assert "missing_namespace" in body["failures"]


def test_verify_order_tool_reachable_blocked() -> None:
    """If an order-placement tool is discoverable the gate must block."""
    res = client.post(
        "/api/mcp/verify",
        json={
            "namespace": "alpaca-paper",
            "paper_trade": True,
            "tool_names": ["get_account", "create_order"],
            "auth_ok": True,
            "network_ok": True,
            "schema_ok": True,
        },
    )
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "blocked"
    assert "order_tool_reachable" in body["failures"]


def test_verify_auth_failure_blocked() -> None:
    """Auth failure evidence must block."""
    res = client.post(
        "/api/mcp/verify",
        json={
            "namespace": "alpaca-paper",
            "paper_trade": True,
            "tool_names": ["get_account"],
            "auth_ok": False,
            "network_ok": True,
            "schema_ok": True,
        },
    )
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "blocked"
    assert "auth_failure" in body["failures"]


# ---------------------------------------------------------------------------
# /api/snapshot
# ---------------------------------------------------------------------------


def test_snapshot_disconnected_has_no_financial_values() -> None:
    """Truthfulness mandate: disconnected snapshot must not fabricate balances."""
    res = client.get("/api/snapshot?connected=false")
    assert res.status_code == 200
    body = res.json()
    assert body["connection_state"] == "disconnected"
    assert body["cash"] is None
    assert body["buying_power"] is None
    assert body["portfolio_equity"] is None
    assert body["latest_price"] is None
    assert body["provenance_is_fixture"] is True


def test_snapshot_fixture_connected_non_believable() -> None:
    """Connected fixture mode must not expose real-looking account values."""
    res = client.get("/api/snapshot?connected=true")
    assert res.status_code == 200
    body = res.json()
    # Must still be fixture — live Alpaca proof not yet implemented
    assert body["provenance_is_fixture"] is True
    # Cash must be zero (explicit fixture), never a random believable balance
    assert body["cash"] == "0.00"
    assert body["buying_power"] == "0.00"
    assert body["portfolio_equity"] == "0.00"
    # Activity must explain fixture mode
    assert body["activity_count"] >= 1


def test_snapshot_has_no_execution_authority() -> None:
    """The snapshot endpoint must never surface an order/execution decision."""
    for connected in [False, True]:
        res = client.get(f"/api/snapshot?connected={str(connected).lower()}")
        body = res.json()
        decision = body.get("decision")
        if decision is not None:
            # If a decision exists, it must not be in a state that implies execution
            assert decision["state"] not in ("completed",), (
                "Snapshot must not expose a completed execution decision"
            )
