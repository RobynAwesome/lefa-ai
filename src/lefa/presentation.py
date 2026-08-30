from datetime import UTC, datetime
from decimal import Decimal

from pydantic import BaseModel

from lefa.contracts import ConnectionState, DataSource, LEFASnapshot


class UIAccountState(BaseModel):
    connection: str
    status: str
    cash: str | None = None
    buying_power: str | None = None
    portfolio_equity: str | None = None


class UIMarketState(BaseModel):
    symbol: str
    state: str
    latest_price: str | None = None


class UIStage(BaseModel):
    key: str
    label: str
    status: str
    detail: str


class UIProvenance(BaseModel):
    source: str
    provider: str
    observed_at: datetime
    valid_until: datetime | None = None
    freshness: str


class LEFAUIView(BaseModel):
    mode: str
    connection_label: str
    execution_authority: str
    observation_label: str
    truth_anchor: str
    account: UIAccountState
    market: UIMarketState
    stages: tuple[UIStage, ...]
    provenance: UIProvenance


def _money(value: Decimal | None, *, fixture: bool) -> str | None:
    if value is None or fixture:
        return None
    return format(value, "f")


def snapshot_to_ui_view(snapshot: LEFASnapshot, *, at: datetime | None = None) -> LEFAUIView:
    """Project one governed snapshot into the character-first UI truth surface.

    Fixture snapshots deliberately suppress numeric financial fields even if a future
    fixture is accidentally populated. This presentation boundary is therefore a
    second fail-closed layer behind ``FixtureProvider``.
    """

    account_provenance = snapshot.account.provenance
    market_provenance = snapshot.market.provenance
    fixture = account_provenance.is_fixture or market_provenance.is_fixture
    now = at or datetime.now(UTC)
    stale = market_provenance.is_stale(now)

    if fixture:
        connection_label = "Fixture mode — not live"
    elif snapshot.account.connection_state is ConnectionState.CONNECTED:
        connection_label = "Provider connected"
    elif snapshot.account.connection_state is ConnectionState.ERROR:
        connection_label = "Provider error"
    else:
        connection_label = "Not connected"

    latest_price = _money(snapshot.market.latest_price, fixture=fixture)
    observation_available = latest_price is not None and stale is not True
    observation_label = "Observation available" if observation_available else "Awaiting observation"

    if fixture:
        truth_anchor = "Fixture / non-live"
    elif stale is True:
        truth_anchor = "Stale — HOLD"
    elif market_provenance.source is DataSource.ALPACA:
        truth_anchor = "Provider evidence"
    else:
        truth_anchor = "Unknown"

    ledger_status = "preserved" if snapshot.decision is not None else "empty"
    ledger_detail = (
        "A governed decision artifact exists."
        if snapshot.decision is not None
        else "No governed decision receipt has been preserved yet."
    )
    reveal_status = "available" if snapshot.impact else "waiting"
    reveal_detail = (
        "Evidence-backed impact metrics are available."
        if snapshot.impact
        else "Nothing is eligible for outcome comparison yet."
    )

    freshness = "unknown"
    if stale is True:
        freshness = "stale"
    elif stale is False:
        freshness = "fresh"

    return LEFAUIView(
        mode=snapshot.account.connection_state.value,
        connection_label=connection_label,
        execution_authority="zero",
        observation_label=observation_label,
        truth_anchor=truth_anchor,
        account=UIAccountState(
            connection=snapshot.account.connection_state.value,
            status=snapshot.account.account_status or "unknown",
            cash=_money(snapshot.account.cash, fixture=fixture),
            buying_power=_money(snapshot.account.buying_power, fixture=fixture),
            portfolio_equity=_money(snapshot.account.portfolio_equity, fixture=fixture),
        ),
        market=UIMarketState(
            symbol=snapshot.market.symbol,
            state=snapshot.market.market_state.value,
            latest_price=latest_price,
        ),
        stages=(
            UIStage(
                key="observe",
                label="OBSERVE",
                status="ready" if observation_available else "awaiting",
                detail=observation_label,
            ),
            UIStage(
                key="ledger",
                label="LEDGER",
                status=ledger_status,
                detail=ledger_detail,
            ),
            UIStage(
                key="time",
                label="TIME",
                status="waiting",
                detail="Time may separate preserved evidence from later reality; no replay is claimed yet.",
            ),
            UIStage(
                key="reveal",
                label="REVEAL",
                status=reveal_status,
                detail=reveal_detail,
            ),
        ),
        provenance=UIProvenance(
            source=market_provenance.source.value,
            provider=market_provenance.provider,
            observed_at=market_provenance.observed_at,
            valid_until=market_provenance.valid_until,
            freshness=freshness,
        ),
    )
