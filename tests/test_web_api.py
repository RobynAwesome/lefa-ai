"""
Tests for LEFA AI Web API — MCP proof, snapshot, and health surfaces.

Governance boundaries:
- No credentials in test fixtures.
- Browser-facing /api/mcp/status is backend-owned and fails closed until live proof exists.
- Fixture snapshots never return believable live financial values.
- /api/mcp/verify blocks non-paper mode and execution-tool reachability.
- Execution authority is always zero.
"""
from fastapi.testclient import TestClient

from lefa.web_api import app

client = TestClient(app)


def test_health_returns_ok() -> None:
    res = client.get("/api/health")
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "ok"
    assert body["execution_authority"] == "none"


def test_runtime_status_fails_closed_without_witnessed_evidence() -> None:
    """The UI must not be able to manufacture a successful Alpaca connection."""
    res = client.get("/api/mcp/status")
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "blocked"
    assert "missing_namespace" in body["failures"]
    assert "live_or_unproven_mode" in body["failures"]
    assert body["paper_trade"] is None


def test_verify_paper_mode_ready() -> None:
    """Valid sanitized paper-mode evidence passes the deterministic evaluator."""
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


def test_snapshot_disconnected_has_no_financial_values() -> None:
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
    res = client.get("/api/snapshot?connected=true")
    assert res.status_code == 200
    body = res.json()
    assert body["provenance_is_fixture"] is True
    assert body["cash"] == "0.00"
    assert body["buying_power"] == "0.00"
    assert body["portfolio_equity"] == "0.00"
    assert body["activity_count"] >= 1


def test_snapshot_has_no_execution_authority() -> None:
    for connected in [False, True]:
        res = client.get(f"/api/snapshot?connected={str(connected).lower()}")
        body = res.json()
        decision = body.get("decision")
        if decision is not None:
            assert decision["state"] not in ("completed",), (
                "Snapshot must not expose a completed execution decision"
            )
