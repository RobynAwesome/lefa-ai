"""
LEFA AI — Web API
=================
FastAPI routes that bridge the governed Python backend to the React frontend.

Boundaries:
- /api/mcp/verify  — accepts sanitized runtime evidence, returns ReadOnlyMCPProof
- /api/snapshot    — returns a LEFASnapshot (fixture or live depending on proof state)
- No order, execution, or autonomous-trade routes exist here.
- Credentials are never accepted or forwarded through this API surface.
  The frontend sends only non-secret evidence (namespace, server_identity,
  paper_trade flag, tool_names, account_status flags).

I_AM_STATELESS_RENTER_NOT_LANDLORD
"""
from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from lefa.contracts import (
    AccountContext,
    ActivityEvent,
    AgentDecision,
    ConnectionState,
    DataSource,
    DecisionState,
    LEFASnapshot,
    MarketContext,
    MarketState,
    Provenance,
    ValidationState,
    ValidationStatus,
)
from lefa.mcp_observation import (
    MCPRuntimeEvidence,
    ReadOnlyMCPProof,
    evaluate_read_only_mcp_evidence,
)

app = FastAPI(
    title="LEFA AI Backend",
    description="Governed financial intelligence — observation only, no execution authority.",
    version="0.1.0",
)

# Allow the Vite dev server to call this API during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


# ---------------------------------------------------------------------------
# Request / Response shapes (frontend ↔ backend contract)
# ---------------------------------------------------------------------------


class MCPVerifyRequest(BaseModel):
    """
    Sanitized runtime facts the frontend collected during Alpaca MCP discovery.
    Credentials MUST NOT appear in this payload — the frontend must never
    forward API keys through this endpoint.
    """

    namespace: str | None = None
    server_identity: str | None = None
    server_version: str | None = None
    paper_trade: bool | None = None
    tool_names: list[str] = []
    account_status: str | None = None
    account_blocked: bool | None = None
    trading_blocked: bool | None = None
    auth_ok: bool = True
    network_ok: bool = True
    schema_ok: bool = True


class MCPVerifyResponse(BaseModel):
    status: str          # "ready" | "blocked"
    failures: list[str]  # MCPFailureCode values
    namespace: str | None
    server_identity: str | None
    paper_trade: bool | None
    readable_tool_names: list[str]
    observed_at: str     # ISO-8601


class SnapshotResponse(BaseModel):
    """Serialisable view of LEFASnapshot for the frontend."""
    connection_state: str
    account_status: str | None
    cash: str | None
    buying_power: str | None
    portfolio_equity: str | None
    provenance_source: str
    provenance_is_fixture: bool
    market_symbol: str
    market_state: str
    latest_price: str | None
    decision: dict | None
    validation_status: str | None
    activity_count: int


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.post("/api/mcp/verify", response_model=MCPVerifyResponse)
def verify_mcp_evidence(req: MCPVerifyRequest) -> MCPVerifyResponse:
    """
    Evaluate sanitized Alpaca MCP runtime evidence.
    Returns READY only when all fail-closed checks pass.
    This endpoint never touches credentials.
    """
    evidence = MCPRuntimeEvidence(
        namespace=req.namespace,
        server_identity=req.server_identity,
        server_version=req.server_version,
        paper_trade=req.paper_trade,
        tool_names=tuple(req.tool_names),
        account_status=req.account_status,
        account_blocked=req.account_blocked,
        trading_blocked=req.trading_blocked,
        auth_ok=req.auth_ok,
        network_ok=req.network_ok,
        schema_ok=req.schema_ok,
    )
    proof: ReadOnlyMCPProof = evaluate_read_only_mcp_evidence(evidence)
    return MCPVerifyResponse(
        status=proof.status.value,
        failures=[f.value for f in proof.failures],
        namespace=proof.namespace,
        server_identity=proof.server_identity,
        paper_trade=proof.paper_trade,
        readable_tool_names=list(proof.readable_tool_names),
        observed_at=proof.observed_at.isoformat(),
    )


@app.get("/api/snapshot", response_model=SnapshotResponse)
def get_snapshot(connected: bool = False) -> SnapshotResponse:
    """
    Return a LEFASnapshot.
    When connected=false (default), returns explicit fixture state with no
    believable live financial values — truthfulness mandate per Issue #3.
    When connected=true, returns the same fixture until live Alpaca MCP proof
    is implemented (Issue #2 live gate).
    """
    now = datetime.now(UTC)

    if not connected:
        # Disconnected — fully unpopulated, never fabricate live state
        prov = Provenance(
            source=DataSource.FIXTURE,
            observed_at=now,
            provider="fixture",
            is_fixture=True,
        )
        snapshot = LEFASnapshot(
            account=AccountContext(
                connection_state=ConnectionState.DISCONNECTED,
                account_status=None,
                cash=None,
                buying_power=None,
                portfolio_equity=None,
                provenance=prov,
            ),
            market=MarketContext(
                symbol="—",
                latest_price=None,
                market_state=MarketState.UNKNOWN,
                provenance=prov,
            ),
        )
    else:
        # Connected but live Alpaca proof not yet implemented — fixture with
        # explicit non-believable placeholder values per governed data contract.
        fresh_until = now + timedelta(seconds=30)
        prov = Provenance(
            source=DataSource.FIXTURE,
            observed_at=now,
            valid_until=fresh_until,
            provider="fixture-connected-placeholder",
            is_fixture=True,
        )
        snapshot = LEFASnapshot(
            account=AccountContext(
                connection_state=ConnectionState.FIXTURE,
                account_status="FIXTURE_ACTIVE",
                cash=Decimal("0.00"),
                buying_power=Decimal("0.00"),
                portfolio_equity=Decimal("0.00"),
                provenance=prov,
            ),
            market=MarketContext(
                symbol="FIXTURE",
                latest_price=None,
                market_state=MarketState.UNKNOWN,
                provenance=prov,
            ),
            activity=(
                ActivityEvent(
                    event_type="fixture_mode",
                    description=(
                        "Fixture mode active. "
                        "Live Alpaca MCP observation not yet proven (Issue #2). "
                        "No real account data is displayed."
                    ),
                ),
            ),
        )

    return SnapshotResponse(
        connection_state=snapshot.account.connection_state.value,
        account_status=snapshot.account.account_status,
        cash=str(snapshot.account.cash) if snapshot.account.cash is not None else None,
        buying_power=(
            str(snapshot.account.buying_power)
            if snapshot.account.buying_power is not None
            else None
        ),
        portfolio_equity=(
            str(snapshot.account.portfolio_equity)
            if snapshot.account.portfolio_equity is not None
            else None
        ),
        provenance_source=snapshot.account.provenance.source.value,
        provenance_is_fixture=snapshot.account.provenance.is_fixture,
        market_symbol=snapshot.market.symbol,
        market_state=snapshot.market.market_state.value,
        latest_price=(
            str(snapshot.market.latest_price)
            if snapshot.market.latest_price is not None
            else None
        ),
        decision=(
            {
                "decision_id": str(snapshot.decision.decision_id),
                "proposed_action": snapshot.decision.proposed_action,
                "instrument": snapshot.decision.instrument,
                "rationale_summary": snapshot.decision.rationale_summary,
                "state": snapshot.decision.state.value,
            }
            if snapshot.decision is not None
            else None
        ),
        validation_status=(
            snapshot.validation.status.value
            if snapshot.validation is not None
            else None
        ),
        activity_count=len(snapshot.activity),
    )


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "service": "lefa-ai-backend", "execution_authority": "none"}
