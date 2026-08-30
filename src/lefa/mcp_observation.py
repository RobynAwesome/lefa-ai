from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, Field, model_validator


class MCPProofStatus(StrEnum):
    READY = "ready"
    BLOCKED = "blocked"


class MCPFailureCode(StrEnum):
    MISSING_NAMESPACE = "missing_namespace"
    AUTH_FAILURE = "auth_failure"
    SCHEMA_DRIFT = "schema_drift"
    LIVE_OR_UNPROVEN_MODE = "live_or_unproven_mode"
    NETWORK_FAILURE = "network_failure"
    ACCOUNT_BLOCKED = "account_blocked"
    ORDER_TOOL_REACHABLE = "order_tool_reachable"


class MCPObservationKind(StrEnum):
    ACCOUNT = "account"
    ASSET = "asset"
    CLOCK = "clock"
    MARKET_QUOTE = "market_quote"
    OPTION_CHAIN = "option_chain"


class MCPReceiptFailure(StrEnum):
    PROOF_NOT_READY = "proof_not_ready"
    TOOL_NOT_DISCOVERED = "tool_not_discovered"
    EXECUTION_TOOL = "execution_tool"
    SYMBOL_REQUIRED = "symbol_required"
    SENSITIVE_FIELD = "sensitive_field"


FORBIDDEN_TOOL_TOKENS: tuple[str, ...] = (
    "order",
    "cancel",
    "replace",
    "liquidate",
    "exercise",
)


class MCPRuntimeEvidence(BaseModel):
    """Sanitized runtime facts discovered from an Alpaca MCP session.

    This model intentionally stores only non-secret proof material. Credentials,
    raw MCP config, account numbers, and full payload dumps do not belong here.
    """

    namespace: str | None = None
    server_identity: str | None = None
    server_version: str | None = None
    paper_trade: bool | None = None
    tool_names: tuple[str, ...] = ()
    account_status: str | None = None
    account_blocked: bool | None = None
    trading_blocked: bool | None = None
    auth_ok: bool = True
    network_ok: bool = True
    schema_ok: bool = True
    observed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ReadOnlyMCPProof(BaseModel):
    status: MCPProofStatus
    failures: tuple[MCPFailureCode, ...]
    namespace: str | None
    server_identity: str | None
    server_version: str | None
    paper_trade: bool | None
    observed_at: datetime
    readable_tool_names: tuple[str, ...]

    @property
    def is_ready(self) -> bool:
        return self.status is MCPProofStatus.READY


class MCPObservationReceipt(BaseModel):
    """Normalized, non-secret receipt for one read-only Alpaca MCP observation."""

    proof: ReadOnlyMCPProof
    kind: MCPObservationKind
    source_tool: str
    observed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    symbol: str | None = None
    summary: dict[str, str | bool | int] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_receipt_boundary(self) -> "MCPObservationReceipt":
        if not self.proof.is_ready:
            raise ValueError(MCPReceiptFailure.PROOF_NOT_READY.value)
        if self.source_tool not in self.proof.readable_tool_names:
            raise ValueError(MCPReceiptFailure.TOOL_NOT_DISCOVERED.value)
        if _has_forbidden_tool((self.source_tool,)):
            raise ValueError(MCPReceiptFailure.EXECUTION_TOOL.value)
        if self.kind in (
            MCPObservationKind.ASSET,
            MCPObservationKind.MARKET_QUOTE,
            MCPObservationKind.OPTION_CHAIN,
        ) and not self.symbol:
            raise ValueError(MCPReceiptFailure.SYMBOL_REQUIRED.value)
        if _has_sensitive_summary_key(self.summary):
            raise ValueError(MCPReceiptFailure.SENSITIVE_FIELD.value)

        return self


def evaluate_read_only_mcp_evidence(evidence: MCPRuntimeEvidence) -> ReadOnlyMCPProof:
    """Evaluate whether sanitized Alpaca MCP evidence can enter the LEFA proof lane."""

    failures: list[MCPFailureCode] = []

    if not evidence.namespace:
        failures.append(MCPFailureCode.MISSING_NAMESPACE)
    if not evidence.auth_ok:
        failures.append(MCPFailureCode.AUTH_FAILURE)
    if not evidence.network_ok:
        failures.append(MCPFailureCode.NETWORK_FAILURE)
    if not evidence.schema_ok:
        failures.append(MCPFailureCode.SCHEMA_DRIFT)
    if evidence.paper_trade is not True:
        failures.append(MCPFailureCode.LIVE_OR_UNPROVEN_MODE)
    if evidence.account_status is not None and evidence.account_status.lower() != "active":
        failures.append(MCPFailureCode.ACCOUNT_BLOCKED)
    if evidence.account_blocked is True or evidence.trading_blocked is True:
        failures.append(MCPFailureCode.ACCOUNT_BLOCKED)
    if _has_forbidden_tool(evidence.tool_names):
        failures.append(MCPFailureCode.ORDER_TOOL_REACHABLE)

    return ReadOnlyMCPProof(
        status=MCPProofStatus.BLOCKED if failures else MCPProofStatus.READY,
        failures=tuple(failures),
        namespace=evidence.namespace,
        server_identity=evidence.server_identity,
        server_version=evidence.server_version,
        paper_trade=evidence.paper_trade,
        observed_at=evidence.observed_at,
        readable_tool_names=evidence.tool_names,
    )


def _has_forbidden_tool(tool_names: tuple[str, ...]) -> bool:
    normalized_names = (" ".join(tool_names)).lower().replace("-", "_")
    return any(token in normalized_names for token in FORBIDDEN_TOOL_TOKENS)


def _has_sensitive_summary_key(summary: dict[str, str | bool | int]) -> bool:
    sensitive_tokens = (
        "secret",
        "token",
        "password",
        "api_key",
        "key_id",
        "authorization",
        "oauth",
        "account_id",
        "account_number",
    )
    normalized_keys = " ".join(summary.keys()).lower().replace("-", "_")
    return any(token in normalized_keys for token in sensitive_tokens)
