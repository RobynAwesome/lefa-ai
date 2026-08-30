from lefa.contracts import ConnectionState, DataSource, MarketState
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


def test_fixture_provider_is_explicitly_non_live() -> None:
    snapshot = FixtureProvider().snapshot("QQQ")

    assert snapshot.account.provenance.provider == "fixture-provider"
    assert snapshot.market.provenance.provider == "fixture-provider"
    assert snapshot.market.latest_price is None
