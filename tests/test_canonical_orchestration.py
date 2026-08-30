from dataclasses import dataclass
from decimal import Decimal

from lefa.governance import (
    AccountState,
    Decision,
    ExecutionJurisdiction,
    ProofStageMaturity,
    TradeProposal,
)
from lefa.orchestration import CanonicalTradingOrchestrator


def account() -> AccountState:
    return AccountState(
        equity=Decimal("100000"),
        open_risk=Decimal("0"),
        daily_pnl=Decimal("0"),
    )


def proposal(maximum_loss: str = "500") -> TradeProposal:
    return TradeProposal(
        symbol="SPY",
        structure="vertical_credit_spread",
        maximum_loss=Decimal(maximum_loss),
    )


@dataclass
class CanonicalResult:
    trace_id: str = "TRACE-123"
    receipt_hash: str = "sha256:abc"
    btth_purity_score: float = 1.0
    rtcp_proof_state: str = "POC_VALIDATED"


class FakeCanonical:
    def orchestrate_task(self, **kwargs: object) -> CanonicalResult:
        return CanonicalResult()


class BrokenCanonical:
    def orchestrate_task(self, **kwargs: object) -> CanonicalResult:
        raise PermissionError("stage gate failed")


class IncompleteCanonical:
    def orchestrate_task(self, **kwargs: object) -> dict[str, object]:
        return {"rtcp_proof_state": "HOLD"}


class RecycledCanonical:
    def orchestrate_task(self, **kwargs: object) -> dict[str, object]:
        return {
            "trace_id": "TRACE-RECYCLED",
            "receipt_hash": "sha256:recycled",
            "btth_purity_score": 1.0,
            "rtcp_proof_state": "POC_VALIDATED",
            "recycled_status": "RECYCLED_FOC_PURGED",
        }


class HeldCanonical:
    def orchestrate_task(self, **kwargs: object) -> dict[str, object]:
        return {
            "trace_id": "TRACE-HOLD",
            "receipt_hash": "sha256:hold",
            "rtcp_proof_state": "HOLD",
            "recycled_status": "POC_VERIFIED",
        }


def test_risk_rejection_short_circuits_canonical_bridge() -> None:
    class MustNotRun:
        def orchestrate_task(self, **kwargs: object) -> object:
            raise AssertionError("canonical bridge must not run after risk rejection")

    receipt = CanonicalTradingOrchestrator(canonical_orchestrator=MustNotRun()).evaluate(
        account(), proposal("500.01")
    )
    assert receipt.decision is Decision.REJECT
    assert "canonical_orchestration_skipped_after_risk_reject" in receipt.reasons


def test_canonical_approval_augments_risk_receipt_without_replacing_it() -> None:
    receipt = CanonicalTradingOrchestrator(
        canonical_orchestrator=FakeCanonical(),
        operating_mode="TEST",
    ).evaluate(account(), proposal())

    assert receipt.decision is Decision.APPROVE
    assert receipt.canonical_receipt_hash == "sha256:abc"
    assert receipt.trace_id == "TRACE-123"
    assert receipt.purity_score == 1.0
    assert receipt.execution_jurisdiction is ExecutionJurisdiction.PAPER
    assert receipt.reasons[0] == "all_policy_checks_passed"
    assert "canonical_governance_receipted" in receipt.reasons


def test_bridge_failure_becomes_hold_not_false_approval() -> None:
    receipt = CanonicalTradingOrchestrator(
        canonical_orchestrator=BrokenCanonical(),
        operating_mode="TEST",
    ).evaluate(account(), proposal())

    assert receipt.decision is Decision.HOLD
    assert "canonical_bridge_hold:PermissionError" in receipt.reasons


def test_incomplete_canonical_receipt_fails_closed_to_hold() -> None:
    receipt = CanonicalTradingOrchestrator(
        canonical_orchestrator=IncompleteCanonical(),
        operating_mode="TEST",
    ).evaluate(account(), proposal())

    assert receipt.decision is Decision.HOLD
    assert "canonical_governance_not_admissible" in receipt.reasons


def test_live_jurisdiction_is_representable_but_not_admissible() -> None:
    receipt = CanonicalTradingOrchestrator(
        canonical_orchestrator=FakeCanonical(),
        operating_mode="TEST",
    ).evaluate(
        account(),
        proposal(),
        jurisdiction=ExecutionJurisdiction.LIVE,
    )

    assert receipt.decision is Decision.HOLD
    assert "live_jurisdiction_not_admissible" in receipt.reasons
    assert receipt.execution_jurisdiction is ExecutionJurisdiction.LIVE


def test_current_upstream_pipeline_defaults_to_procedural_proof_depth() -> None:
    receipt = CanonicalTradingOrchestrator(
        canonical_orchestrator=FakeCanonical(),
        operating_mode="TEST",
    ).evaluate(account(), proposal())

    assert len(receipt.proof_depth) == 8
    assert {stage.maturity for stage in receipt.proof_depth} == {
        ProofStageMaturity.PROCEDURAL
    }


def test_receipt_projection_is_local_and_sanitized() -> None:
    orchestrator = CanonicalTradingOrchestrator(
        canonical_orchestrator=FakeCanonical(),
        operating_mode="TEST",
    )
    receipt = orchestrator.evaluate(account(), proposal())
    projection = orchestrator.project_receipt(receipt)

    assert projection["canonical_receipt_hash"] == "sha256:abc"
    assert projection["execution_jurisdiction"] == "paper"
    assert "account" not in projection


def test_recycled_canonical_result_is_held_even_with_receipt_hash() -> None:
    receipt = CanonicalTradingOrchestrator(
        canonical_orchestrator=RecycledCanonical(),
        operating_mode="TEST",
    ).evaluate(account(), proposal())

    assert receipt.decision is Decision.HOLD
    assert "canonical_governance_not_admissible" in receipt.reasons
    assert receipt.canonical_receipt_hash == "sha256:recycled"


def test_explicit_canonical_hold_survives_translation() -> None:
    receipt = CanonicalTradingOrchestrator(
        canonical_orchestrator=HeldCanonical(),
        operating_mode="TEST",
    ).evaluate(account(), proposal())

    assert receipt.decision is Decision.HOLD
    assert receipt.canonical_proof_state == "HOLD"
    assert "canonical_governance_not_admissible" in receipt.reasons
