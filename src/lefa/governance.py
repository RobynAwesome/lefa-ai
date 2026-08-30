from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Decision(StrEnum):
    APPROVE = "approve"
    REJECT = "reject"
    HOLD = "hold"


class ExecutionJurisdiction(StrEnum):
    OBSERVE_ONLY = "observe_only"
    PAPER = "paper"
    LIVE = "live"


class ProofStageMaturity(StrEnum):
    SIMULATED = "simulated"
    PROCEDURAL = "procedural"
    EVIDENCED = "evidenced"
    INDEPENDENTLY_VALIDATED = "independently_validated"


class ProofStage(BaseModel):
    stage: str
    maturity: ProofStageMaturity
    evidence_ref: str | None = None


class AccountState(BaseModel):
    equity: Decimal = Field(gt=0)
    open_risk: Decimal = Field(ge=0)
    daily_pnl: Decimal


class TradeProposal(BaseModel):
    symbol: str
    structure: str
    maximum_loss: Decimal = Field(gt=0)


class GovernanceReceipt(BaseModel):
    receipt_id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    decision: Decision
    reasons: list[str]
    proposal: TradeProposal
    canonical_receipt_hash: str | None = None
    trace_id: str | None = None
    purity_score: float | None = Field(default=None, ge=0)
    canonical_proof_state: str | None = None
    execution_jurisdiction: ExecutionJurisdiction = ExecutionJurisdiction.OBSERVE_ONLY
    proof_depth: tuple[ProofStage, ...] = ()


class RiskPolicy(BaseModel):
    allowed_symbols: frozenset[str] = frozenset({"SPY"})
    allowed_structures: frozenset[str] = frozenset({"vertical_credit_spread"})
    max_trade_risk_fraction: Decimal = Decimal("0.005")
    max_open_risk_fraction: Decimal = Decimal("0.02")
    daily_loss_stop_fraction: Decimal = Decimal("0.01")

    def evaluate(self, account: AccountState, proposal: TradeProposal) -> GovernanceReceipt:
        reasons: list[str] = []
        if proposal.symbol not in self.allowed_symbols:
            reasons.append("symbol_not_allowed")
        if proposal.structure not in self.allowed_structures:
            reasons.append("structure_not_allowed")
        if proposal.maximum_loss > account.equity * self.max_trade_risk_fraction:
            reasons.append("trade_risk_limit_exceeded")
        if account.open_risk + proposal.maximum_loss > account.equity * self.max_open_risk_fraction:
            reasons.append("portfolio_risk_limit_exceeded")
        if account.daily_pnl <= -(account.equity * self.daily_loss_stop_fraction):
            reasons.append("daily_loss_stop_active")

        return GovernanceReceipt(
            decision=Decision.REJECT if reasons else Decision.APPROVE,
            reasons=reasons or ["all_policy_checks_passed"],
            proposal=proposal,
        )
