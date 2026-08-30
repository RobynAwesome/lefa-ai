from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from lefa.contracts import ConnectionState, DataSource, MarketState, Provenance
from lefa.providers import FixtureProvider


def test_fixture_provider_uses_governed_contracts_without_fake_financial_values() -> None:
    snapshot = FixtureProvider().snapshot("SPY")

    assert snapshot.account.connection_state is ConnectionState.FIXTURE
    assert snapshot.account.account_status == "fixture-only"
    assert snapshot.account.cash is None
    assert snapshot.account.buying_power is None
    assert snapshot.account.portfolio_equity is None

    assert snapshot.market.symbol == "SPY"
    assert snapshot.market.latest_price is None
    assert snapshot.market.market_state is MarketState.UNKNOWN

    assert snapshot.account.provenance.source is DataSource.FIXTURE
    assert snapshot.market.provenance.source is DataSource.FIXTURE
    assert snapshot.account.provenance.is_fixture is True
    assert snapshot.market.provenance.is_fixture is True
    assert snapshot.account.provenance.is_stale() is None
    assert snapshot.market.provenance.is_stale() is None


def test_fixture_provider_is_explicitly_non_live() -> None:
    snapshot = FixtureProvider().snapshot("QQQ")

    assert snapshot.account.provenance.provider == "fixture-provider"
    assert snapshot.market.provenance.provider == "fixture-provider"
    assert snapshot.market.latest_price is None


def test_provenance_rejects_fixture_flag_mismatch() -> None:
    with pytest.raises(ValidationError):
        Provenance(
            source=DataSource.FIXTURE,
            provider="fixture-provider",
            is_fixture=False,
        )

    with pytest.raises(ValidationError):
        Provenance(
            source=DataSource.CACHE,
            provider="cache-provider",
            is_fixture=True,
        )


def test_alpaca_provenance_requires_explicit_freshness_window() -> None:
    observed_at = datetime(2026, 8, 30, 14, 0, tzinfo=UTC)

    with pytest.raises(ValidationError):
        Provenance(
            source=DataSource.ALPACA,
            observed_at=observed_at,
            provider="alpaca-provider",
        )


def test_provenance_reports_freshness_deterministically() -> None:
    observed_at = datetime(2026, 8, 30, 14, 0, tzinfo=UTC)
    valid_until = observed_at + timedelta(seconds=30)
    provenance = Provenance(
        source=DataSource.ALPACA,
        observed_at=observed_at,
        valid_until=valid_until,
        provider="alpaca-provider",
    )

    assert provenance.is_stale(observed_at + timedelta(seconds=29)) is False
    assert provenance.is_stale(valid_until) is True


def test_provenance_rejects_invalid_or_naive_freshness_windows() -> None:
    observed_at = datetime(2026, 8, 30, 14, 0, tzinfo=UTC)

    with pytest.raises(ValidationError):
        Provenance(
            source=DataSource.ALPACA,
            observed_at=observed_at,
            valid_until=observed_at - timedelta(seconds=1),
            provider="alpaca-provider",
        )

    with pytest.raises(ValidationError):
        Provenance(
            source=DataSource.ALPACA,
            observed_at=datetime(2026, 8, 30, 14, 0),
            valid_until=datetime(2026, 8, 30, 14, 1),
            provider="alpaca-provider",
        )
