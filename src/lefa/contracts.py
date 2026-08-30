from datetime import UTC, date, datetime
from decimal import Decimal
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class DataSource(StrEnum):
    FIXTURE = "fixture"
    ALPACA = "alpaca"
    CACHE = "cache"


class ConnectionState(StrEnum):
    DISCONNECTED = "disconnected"
    FIXTURE = "fixture"
    CONNECTED = "connected"
    ERROR = "error"


class MarketState(StrEnum):
    OPEN = "open"
    CLOSED = "closed"
    UNKNOWN = "unknown"


class DecisionState(StrEnum):
    PROPOSED = "proposed"
    VALIDATED = "validated"
    HELD = "held"
    COMPLETED = "completed"


class ValidationStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    HELD = "held"


class Provenance(BaseModel):
    source: DataSource
    observed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    provider: str
    is_fixture: bool = False


class AccountContext(BaseModel):
    connection_state: ConnectionState
    account_status: str | None = None
    cash: Decimal | None = Field(default=None, ge=0)
    buying_power: Decimal | None = Field(default=None, ge=0)
    portfolio_equity: Decimal | None = Field(default=None, ge=0)
    provenance: Provenance


class MarketContext(BaseModel):
    symbol: str
    latest_price: Decimal | None = Field(default=None, gt=0)
    market_state: MarketState = MarketState.UNKNOWN
    provenance: Provenance


class AgentDecision(BaseModel):
    decision_id: UUID = Field(default_factory=uuid4)
    proposed_action: str
    instrument: str
    rationale_summary: str
    state: DecisionState = DecisionState.PROPOSED
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ValidationState(BaseModel):
    decision_id: UUID
    status: ValidationStatus = ValidationStatus.PENDING
    checks_performed: tuple[str, ...] = ()
    reason: str | None = None
    validated_at: datetime | None = None


class ActivityEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    event_type: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    related_id: UUID | None = None
    description: str


class ImpactMetric(BaseModel):
    metric_id: str
    metric_name: str
    measured_value: Decimal
    unit: str
    evidence_source: str
    measurement_date: date


class LEFASnapshot(BaseModel):
    account: AccountContext
    market: MarketContext
    decision: AgentDecision | None = None
    validation: ValidationState | None = None
    activity: tuple[ActivityEvent, ...] = ()
    impact: tuple[ImpactMetric, ...] = ()
