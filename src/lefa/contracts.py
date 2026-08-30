from datetime import UTC, date, datetime
from decimal import Decimal
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator


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
    valid_until: datetime | None = None
    provider: str
    is_fixture: bool = False

    @model_validator(mode="after")
    def validate_truth_boundary(self) -> "Provenance":
        if self.observed_at.tzinfo is None or self.observed_at.utcoffset() is None:
            raise ValueError("observed_at must be timezone-aware")

        if self.valid_until is not None:
            if self.valid_until.tzinfo is None or self.valid_until.utcoffset() is None:
                raise ValueError("valid_until must be timezone-aware")
            if self.valid_until < self.observed_at:
                raise ValueError("valid_until cannot be earlier than observed_at")

        if self.source is DataSource.FIXTURE and not self.is_fixture:
            raise ValueError("fixture provenance must declare is_fixture=true")
        if self.source is not DataSource.FIXTURE and self.is_fixture:
            raise ValueError("non-fixture provenance cannot declare is_fixture=true")

        if self.source is DataSource.ALPACA and self.valid_until is None:
            raise ValueError("Alpaca provenance requires an explicit freshness window")

        return self

    def is_stale(self, at: datetime | None = None) -> bool | None:
        """Return freshness without inventing a window when none was supplied."""

        if self.valid_until is None:
            return None

        reference_time = at or datetime.now(UTC)
        if reference_time.tzinfo is None or reference_time.utcoffset() is None:
            raise ValueError("freshness comparison time must be timezone-aware")
        return reference_time >= self.valid_until


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
