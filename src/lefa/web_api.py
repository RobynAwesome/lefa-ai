"""
LEFA AI — Web API
=================
FastAPI routes that bridge the governed Python backend to the React frontend.

Boundaries:
- /api/mcp/status  — backend-owned runtime proof status for the UI
- /api/mcp/verify  — pure evaluator for sanitized evidence (tests/internal tooling)
- /api/snapshot    — governed snapshot surface; fixture until live proof exists
- No order, execution, or autonomous-trade routes exist here.
- Credentials are never accepted or forwarded through this API surface.

I_AM_STATELESS_RENTER_NOT_LANDLORD
"""
from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from lefa.contracts import (
    AccountContext,
    ActivityEvent,
    ConnectionState,
    DataSource,
    LEFASnapshot,
    MarketContext,
    MarketState,
    Provenance,
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class MCPVerifyRequest(BaseModel):
    """Sanitized, non-secret Alpaca MCP facts for deterministic evaluation."""

    namespace: str | None = None
    server_identity: str | None = None
    server_version: str | None = None
    paper_trade: bool | None = None
    tool_names: list[str] = Field(default_factory=list)
    account_status: str | None = None
    account_blocked: bool | None = None
    trading_blocked: bool | None = None
    auth_ok: bool = True
    network_ok: bool = True
    schema_ok: bool = True


class MCPVerifyResponse(BaseModel):
    status: str
    failures: list[str]
    namespace: str | None
    server_identity: str | None
    paper_trade: bool | None
    readable_tool_names: list[str]
    observed_at: str


class SnapshotResponse(BaseModel):
    """Serializable view of LEFASnapshot for the frontend."""

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


def _proof_response(proof: ReadOnlyMCPProof) -> MCPVerifyResponse:
    return MCPVerifyResponse(
        status=proof.status.value,
        failures=[failure.value for failure in proof.failures],
        namespace=proof.namespace,
        server_identity=proof.server_identity,
        paper_trade=proof.paper_trade,
        readable_tool_names=list(proof.readable_tool_names),
        observed_at=proof.observed_at.isoformat(),
    )


def _current_runtime_evidence() -> MCPRuntimeEvidence:
    """Return backend-owned runtime evidence.

    Issue #2 is still HOLD: live Alpaca MCP discovery has not yet been witnessed in
    this runtime. Returning an empty evidence object deliberately fails closed.
    Replace this seam only when local credential-backed discovery produces a
    sanitized receipt.
    """

    return MCPRuntimeEvidence()


@app.get("/api/mcp/status", response_model=MCPVerifyResponse)
def get_mcp_status() -> MCPVerifyResponse:
    """Expose backend-owned read-only Alpaca MCP proof state to the UI."""

    proof = evaluate_read_only_mcp_evidence(_current_runtime_evidence())
    return _proof_response(proof)


@app.post("/api/mcp/verify", response_model=MCPVerifyResponse)
def verify_mcp_evidence(req: MCPVerifyRequest) -> MCPVerifyResponse:
    """Deterministically evaluate supplied sanitized evidence.

    This endpoint is an evaluator, not a connection authority. The user-facing UI
    reads /api/mcp/status, whose evidence is owned by the backend runtime.
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
    proof = evaluate_read_only_mcp_evidence(evidence)
    return _proof_response(proof)


@app.get("/api/snapshot", response_model=SnapshotResponse)
def get_snapshot(connected: bool = False) -> SnapshotResponse:
    """Return a governed LEFASnapshot.

    The connected flag is presentation state only. Until Issue #2 supplies real
    backend-owned Alpaca observation evidence, every snapshot remains explicitly
    fixture-sourced and therefore cannot masquerade as live account truth.
    """

    now = datetime.now(UTC)

    if not connected:
        provenance = Provenance(
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
                provenance=provenance,
            ),
            market=MarketContext(
                symbol="—",
                latest_price=None,
                market_state=MarketState.UNKNOWN,
                provenance=provenance,
            ),
        )
    else:
        fresh_until = now + timedelta(seconds=30)
        provenance = Provenance(
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
                provenance=provenance,
            ),
            market=MarketContext(
                symbol="FIXTURE",
                latest_price=None,
                market_state=MarketState.UNKNOWN,
                provenance=provenance,
            ),
            activity=(
                ActivityEvent(
                    event_type="fixture_mode",
                    description=(
                        "Fixture mode active. Live Alpaca MCP observation is not yet "
                        "proven (Issue #2). No real account data is displayed."
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
    return {
        "status": "ok",
        "service": "lefa-ai-backend",
        "execution_authority": "none",
        "ai_inference_provider": "Featherless AI (Lablab.ai Hackathon Partner)",
    }


class AIExplainRequest(BaseModel):
    symbol: str = "SPY"
    price: str | None = None
    market_state: str = "open"
    decision_action: str | None = None
    rationale: str | None = None
    custom_prompt: str | None = None


class AIExplainResponse(BaseModel):
    explanation: str
    model: str
    provider: str


@app.post("/api/ai/explain", response_model=AIExplainResponse)
def explain_market_state(req: AIExplainRequest) -> AIExplainResponse:
    """Generate governed natural language explanation via Featherless AI open-source inference."""
    from lefa.featherless import FeatherlessReasoner

    reasoner = FeatherlessReasoner()
    if req.custom_prompt:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are LEFA AI, the Governed Financial Intelligence Companion. "
                    "Provide clear, professional, risk-aware explanations."
                ),
            },
            {"role": "user", "content": req.custom_prompt},
        ]
        explanation = reasoner.complete(messages, max_tokens=150)
    else:
        explanation = reasoner.explain_market_observation(
            symbol=req.symbol,
            price=req.price,
            market_state=req.market_state,
            decision_action=req.decision_action,
            rationale=req.rationale,
        )

    return AIExplainResponse(
        explanation=explanation,
        model=reasoner.model,
        provider="Featherless AI",
    )


@app.get("/api/ai/dual-axis-explainer", response_model=AIExplainResponse)
def get_dual_axis_explanation() -> AIExplainResponse:
    """Return live Featherless AI explanation of LEFA's dual-axis governance architecture."""
    from lefa.featherless import FeatherlessReasoner

    reasoner = FeatherlessReasoner()
    explanation = reasoner.explain_dual_axis_governance()
    return AIExplainResponse(
        explanation=explanation,
        model=reasoner.model,
        provider="Featherless AI",
    )

