import pytest
from pydantic import ValidationError

from lefa.mcp_observation import (
    MCPFailureCode,
    MCPObservationKind,
    MCPObservationReceipt,
    MCPProofStatus,
    MCPRuntimeEvidence,
    evaluate_read_only_mcp_evidence,
)


def ready_evidence(**overrides: object) -> MCPRuntimeEvidence:
    values: dict[str, object] = {
        "namespace": "alpaca",
        "server_identity": "official-alpaca-mcp",
        "server_version": "runtime-discovered",
        "paper_trade": True,
        "tool_names": (
            "get_account",
            "get_asset",
            "get_clock",
            "get_stock_quote",
            "get_option_chain",
        ),
        "account_status": "ACTIVE",
        "account_blocked": False,
        "trading_blocked": False,
    }
    values.update(overrides)
    return MCPRuntimeEvidence(**values)


def test_accepts_sanitized_read_only_paper_evidence() -> None:
    proof = evaluate_read_only_mcp_evidence(ready_evidence())

    assert proof.status is MCPProofStatus.READY
    assert proof.failures == ()
    assert proof.paper_trade is True
    assert proof.is_ready is True


def test_missing_namespace_fails_closed() -> None:
    proof = evaluate_read_only_mcp_evidence(ready_evidence(namespace=None))

    assert proof.status is MCPProofStatus.BLOCKED
    assert MCPFailureCode.MISSING_NAMESPACE in proof.failures


def test_auth_failure_fails_closed() -> None:
    proof = evaluate_read_only_mcp_evidence(ready_evidence(auth_ok=False))

    assert proof.status is MCPProofStatus.BLOCKED
    assert MCPFailureCode.AUTH_FAILURE in proof.failures


def test_schema_drift_fails_closed() -> None:
    proof = evaluate_read_only_mcp_evidence(ready_evidence(schema_ok=False))

    assert proof.status is MCPProofStatus.BLOCKED
    assert MCPFailureCode.SCHEMA_DRIFT in proof.failures


def test_live_or_unproven_mode_fails_closed() -> None:
    for paper_trade in (False, None):
        proof = evaluate_read_only_mcp_evidence(ready_evidence(paper_trade=paper_trade))

        assert proof.status is MCPProofStatus.BLOCKED
        assert MCPFailureCode.LIVE_OR_UNPROVEN_MODE in proof.failures


def test_network_failure_fails_closed() -> None:
    proof = evaluate_read_only_mcp_evidence(ready_evidence(network_ok=False))

    assert proof.status is MCPProofStatus.BLOCKED
    assert MCPFailureCode.NETWORK_FAILURE in proof.failures


def test_blocked_account_fails_closed() -> None:
    proof = evaluate_read_only_mcp_evidence(
        ready_evidence(account_status="INACTIVE", account_blocked=True, trading_blocked=True)
    )

    assert proof.status is MCPProofStatus.BLOCKED
    assert MCPFailureCode.ACCOUNT_BLOCKED in proof.failures


def test_order_authority_is_rejected_even_in_paper_mode() -> None:
    proof = evaluate_read_only_mcp_evidence(
        ready_evidence(tool_names=("get_account", "submit_order", "cancel_order"))
    )

    assert proof.status is MCPProofStatus.BLOCKED
    assert MCPFailureCode.ORDER_TOOL_REACHABLE in proof.failures


def test_accepts_normalized_account_observation_receipt() -> None:
    proof = evaluate_read_only_mcp_evidence(ready_evidence())

    receipt = MCPObservationReceipt(
        proof=proof,
        kind=MCPObservationKind.ACCOUNT,
        source_tool="get_account",
        summary={
            "account_status": "ACTIVE",
            "account_blocked": False,
            "trading_blocked": False,
        },
    )

    assert receipt.kind is MCPObservationKind.ACCOUNT
    assert receipt.source_tool == "get_account"
    assert receipt.summary["account_status"] == "ACTIVE"


def test_observation_receipt_requires_ready_proof() -> None:
    proof = evaluate_read_only_mcp_evidence(ready_evidence(paper_trade=None))

    with pytest.raises(ValidationError, match="proof_not_ready"):
        MCPObservationReceipt(
            proof=proof,
            kind=MCPObservationKind.ACCOUNT,
            source_tool="get_account",
        )


def test_observation_receipt_requires_discovered_tool() -> None:
    proof = evaluate_read_only_mcp_evidence(ready_evidence())

    with pytest.raises(ValidationError, match="tool_not_discovered"):
        MCPObservationReceipt(
            proof=proof,
            kind=MCPObservationKind.ACCOUNT,
            source_tool="unknown_account_reader",
        )


def test_observation_receipt_rejects_execution_tool_even_if_supplied_manually() -> None:
    proof = evaluate_read_only_mcp_evidence(
        ready_evidence(tool_names=("get_account", "submit_order"), paper_trade=True)
    ).model_copy(update={"status": MCPProofStatus.READY, "failures": ()})

    with pytest.raises(ValidationError, match="execution_tool"):
        MCPObservationReceipt(
            proof=proof,
            kind=MCPObservationKind.ACCOUNT,
            source_tool="submit_order",
        )


def test_symbol_receipts_require_symbol() -> None:
    proof = evaluate_read_only_mcp_evidence(ready_evidence())

    with pytest.raises(ValidationError, match="symbol_required"):
        MCPObservationReceipt(
            proof=proof,
            kind=MCPObservationKind.MARKET_QUOTE,
            source_tool="get_stock_quote",
        )


def test_observation_receipt_rejects_sensitive_summary_keys() -> None:
    proof = evaluate_read_only_mcp_evidence(ready_evidence())

    with pytest.raises(ValidationError, match="sensitive_field"):
        MCPObservationReceipt(
            proof=proof,
            kind=MCPObservationKind.ACCOUNT,
            source_tool="get_account",
            summary={"account_id": "must-not-enter-receipts"},
        )
