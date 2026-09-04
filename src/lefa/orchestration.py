from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any, Protocol

from lefa.governance import (
    AccountState,
    Decision,
    ExecutionJurisdiction,
    GovernanceReceipt,
    ProofStage,
    ProofStageMaturity,
    RiskPolicy,
    TradeProposal,
)


class CanonicalOrchestratorProtocol(Protocol):
    def orchestrate_task(self, **kwargs: Any) -> Any: ...


class CanonicalBridgeUnavailable(RuntimeError):
    """Raised only by strict callers when the upstream KPGS bridge cannot be loaded."""


def _load_kpgs() -> tuple[CanonicalOrchestratorProtocol, Any]:
    try:
        from kopano.canonical_data_governance_orchestrator import (
            CanonicalDataGovernanceOrchestrator,
        )
        from kopano.mmao_mao_identity_mesh import DeviceOperatingMode
    except ImportError as exc:
        raise CanonicalBridgeUnavailable(
            "kopano-core is not importable; canonical governance cannot be proven"
        ) from exc

    return CanonicalDataGovernanceOrchestrator(), DeviceOperatingMode.LAPTOP_BLACK_BEAST


def _read(result: Any, field: str, default: Any = None) -> Any:
    if isinstance(result, dict):
        return result.get(field, default)
    return getattr(result, field, default)


def _proof_depth(result: Any) -> tuple[ProofStage, ...]:
    """Project upstream completion into explicit maturity without inventing evidence."""
    upstream = _read(result, "proof_depth")
    if upstream:
        return tuple(ProofStage.model_validate(item) for item in upstream)

    # The current KPGS orchestrator returns pipeline outputs but not per-stage maturity.
    # Treat pipeline completion as procedural unless an upstream result explicitly
    # supplies evidence-backed maturity states.
    return tuple(
        ProofStage(stage=f"stage_{stage}", maturity=ProofStageMaturity.PROCEDURAL)
        for stage in range(1, 9)
    )


class CanonicalTradingOrchestrator:
    """
    Translation boundary between LEFA-native deterministic risk semantics and KPGS.

    This legacy adapter may evaluate and ledger a proposal. The hackathon options runner
    does not depend on it or on an external execution service. Any caller that uses the
    compatibility execution method still submits only through the provided direct paper
    broker and the narrow defined-risk MLEG order shape.
    """

    def __init__(
        self,
        risk_policy: RiskPolicy | None = None,
        canonical_orchestrator: CanonicalOrchestratorProtocol | None = None,
        operating_mode: Any = None,
        submitting_agent_id: str = "LEFA_AI",
    ) -> None:
        self.risk_policy = risk_policy or RiskPolicy()
        self._canonical_orchestrator = canonical_orchestrator
        self._operating_mode = operating_mode
        self.submitting_agent_id = submitting_agent_id

    def evaluate(
        self,
        account: AccountState,
        proposal: TradeProposal,
        *,
        jurisdiction: ExecutionJurisdiction = ExecutionJurisdiction.PAPER,
    ) -> GovernanceReceipt:
        risk_receipt = self.risk_policy.evaluate(account, proposal)
        risk_receipt.execution_jurisdiction = jurisdiction

        if risk_receipt.decision is Decision.REJECT:
            risk_receipt.reasons.append("canonical_orchestration_skipped_after_risk_reject")
            return risk_receipt

        if jurisdiction is ExecutionJurisdiction.LIVE:
            return risk_receipt.model_copy(
                update={
                    "decision": Decision.HOLD,
                    "reasons": [*risk_receipt.reasons, "live_jurisdiction_not_admissible"],
                }
            )

        try:
            orchestrator, operating_mode = self._resolve_bridge()
            result = orchestrator.orchestrate_task(
                task_title=f"LEFA trade proposal: {proposal.symbol} {proposal.structure}",
                submitting_agent_id=self.submitting_agent_id,
                operating_mode=operating_mode,
                raw_code_proposal=proposal.model_dump_json(),
                human_testimony_claim=(
                    "LEFA deterministic RiskPolicy approved this proposal for canonical review."
                ),
                real_api_surface={
                    "disallowed_inventions": [],
                    "verified_exports": [
                        "RiskPolicy",
                        "GovernanceReceipt",
                        "CanonicalTradingOrchestrator",
                    ],
                },
            )
        except (
            CanonicalBridgeUnavailable,
            ImportError,
            KeyError,
            PermissionError,
            RuntimeError,
        ) as exc:
            return risk_receipt.model_copy(
                update={
                    "decision": Decision.HOLD,
                    "reasons": [
                        *risk_receipt.reasons,
                        f"canonical_bridge_hold:{type(exc).__name__}",
                    ],
                }
            )

        receipt_hash = _read(result, "receipt_hash")
        trace_id = _read(result, "trace_id")
        proof_state = _read(result, "rtcp_proof_state")
        recycled_status = _read(result, "recycled_status")
        purity_score = _read(result, "btth_purity_score")

        canonical_state = str(proof_state or "").upper()
        recycled_state = str(recycled_status or "").upper()
        if (
            any(marker in canonical_state for marker in ("HOLD", "FAIL", "REJECT"))
            or recycled_state.startswith("RECYCLED")
        ):
            return risk_receipt.model_copy(
                update={
                    "decision": Decision.HOLD,
                    "reasons": [*risk_receipt.reasons, "canonical_governance_not_admissible"],
                    "canonical_receipt_hash": str(receipt_hash) if receipt_hash else None,
                    "trace_id": str(trace_id) if trace_id else None,
                    "purity_score": float(purity_score) if purity_score is not None else None,
                    "canonical_proof_state": str(proof_state) if proof_state is not None else None,
                    "proof_depth": _proof_depth(result),
                }
            )

        if not receipt_hash or not trace_id:
            return risk_receipt.model_copy(
                update={
                    "decision": Decision.HOLD,
                    "reasons": [*risk_receipt.reasons, "canonical_receipt_incomplete"],
                    "canonical_proof_state": proof_state,
                    "proof_depth": _proof_depth(result),
                }
            )

        return risk_receipt.model_copy(
            update={
                "canonical_receipt_hash": str(receipt_hash),
                "trace_id": str(trace_id),
                "purity_score": float(purity_score) if purity_score is not None else None,
                "canonical_proof_state": str(proof_state) if proof_state is not None else None,
                "proof_depth": _proof_depth(result),
                "reasons": [*risk_receipt.reasons, "canonical_governance_receipted"],
            }
        )

    def project_receipt(self, receipt: GovernanceReceipt) -> dict[str, Any]:
        """Return a local, sanitized projection; canonical authority remains upstream."""
        return {
            "receipt_id": str(receipt.receipt_id),
            "decision": receipt.decision.value,
            "reasons": list(receipt.reasons),
            "proposal": receipt.proposal.model_dump(mode="json"),
            "canonical_receipt_hash": receipt.canonical_receipt_hash,
            "trace_id": receipt.trace_id,
            "purity_score": receipt.purity_score,
            "canonical_proof_state": receipt.canonical_proof_state,
            "execution_jurisdiction": receipt.execution_jurisdiction.value,
            "proof_depth": [stage.model_dump(mode="json") for stage in receipt.proof_depth],
        }

    def execute_approved_order(
        self,
        receipt: GovernanceReceipt,
        broker: Any,
        *,
        legs: list[dict[str, Any]] | None = None,
        limit_price: Decimal | None = None,
        qty: int = 1,
    ) -> dict[str, Any]:
        """Execute an approved trade proposal on the provided paper broker.

        Requires:
        - receipt.decision == Decision.APPROVE
        - receipt.execution_jurisdiction == ExecutionJurisdiction.PAPER
        - at least two option legs and a positive limit price
        """
        if receipt.decision != Decision.APPROVE:
            raise ValueError(f"Cannot execute order with non-approved receipt decision: {receipt.decision}")
        if receipt.execution_jurisdiction != ExecutionJurisdiction.PAPER:
            raise ValueError(f"Execution prohibited outside PAPER jurisdiction: {receipt.execution_jurisdiction}")
        if not legs or len(legs) < 2:
            raise ValueError("DEFINED_RISK_MLEG_REQUIRED")
        if qty < 1:
            raise ValueError("ORDER_QUANTITY_INVALID")
        if limit_price is None:
            raise ValueError("ORDER_LIMIT_PRICE_REQUIRED")
        try:
            normalized_limit_price = Decimal(str(limit_price))
        except (InvalidOperation, TypeError, ValueError) as exc:
            raise ValueError("ORDER_LIMIT_PRICE_INVALID") from exc
        if normalized_limit_price <= 0:
            raise ValueError("ORDER_LIMIT_PRICE_INVALID")

        order_result = broker.place_option_order(
            order_class="mleg",
            order_type="limit",
            time_in_force="day",
            legs=legs,
            limit_price=normalized_limit_price,
            qty=qty,
            client_order_id=f"lefa-{str(receipt.receipt_id)[:12]}",
        )
        return {
            "receipt_id": str(receipt.receipt_id),
            "canonical_receipt_hash": receipt.canonical_receipt_hash,
            "order_id": order_result.get("order_id"),
            "status": order_result.get("status"),
            "submitted_at": order_result.get("submitted_at"),
            "symbol": receipt.proposal.symbol,
            "structure": receipt.proposal.structure,
        }

    def _resolve_bridge(self) -> tuple[CanonicalOrchestratorProtocol, Any]:
        if self._canonical_orchestrator is not None:
            return self._canonical_orchestrator, self._operating_mode
        return _load_kpgs()
