from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, Field


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
