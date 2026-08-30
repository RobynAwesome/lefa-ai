from datetime import UTC, datetime
from typing import Protocol

from lefa.contracts import (
    AccountContext,
    ConnectionState,
    DataSource,
    LEFASnapshot,
    MarketContext,
    MarketState,
    Provenance,
)


class LEFADataProvider(Protocol):
    """Single UI-facing boundary for governed LEFA state."""

    def snapshot(self, symbol: str) -> LEFASnapshot:
        """Return one contract-valid snapshot for the requested instrument."""


class FixtureProvider:
    """Deterministic non-live provider for UI work.

    The fixture intentionally contains no believable financial values. It exists to
    exercise the same contracts the future Alpaca provider must satisfy.
    """

    name = "fixture-provider"

    def snapshot(self, symbol: str) -> LEFASnapshot:
        observed_at = datetime.now(UTC)
        provenance = Provenance(
            source=DataSource.FIXTURE,
            observed_at=observed_at,
            provider=self.name,
            is_fixture=True,
        )
        return LEFASnapshot(
            account=AccountContext(
                connection_state=ConnectionState.FIXTURE,
                account_status="fixture-only",
                cash=None,
                buying_power=None,
                portfolio_equity=None,
                provenance=provenance,
            ),
            market=MarketContext(
                symbol=symbol,
                latest_price=None,
                market_state=MarketState.UNKNOWN,
                provenance=provenance,
            ),
        )
