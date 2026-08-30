from lefa.presentation import snapshot_to_ui_view
from lefa.providers import FixtureProvider


def test_fixture_ui_view_fails_closed_on_financial_state() -> None:
    view = snapshot_to_ui_view(FixtureProvider().snapshot("SPY"))

    assert view.mode == "fixture"
    assert view.connection_label == "Fixture mode — not live"
    assert view.execution_authority == "zero"
    assert view.observation_label == "Awaiting observation"
    assert view.truth_anchor == "Fixture / non-live"

    assert view.account.cash is None
    assert view.account.buying_power is None
    assert view.account.portfolio_equity is None
    assert view.market.latest_price is None

    assert [stage.key for stage in view.stages] == ["observe", "ledger", "time", "reveal"]
    assert view.stages[0].status == "awaiting"
    assert view.stages[1].status == "empty"
    assert view.stages[2].status == "waiting"
    assert view.stages[3].status == "waiting"


def test_fixture_ui_view_keeps_fixture_provenance_explicit() -> None:
    view = snapshot_to_ui_view(FixtureProvider().snapshot("QQQ"))

    assert view.provenance.source == "fixture"
    assert view.provenance.provider == "fixture-provider"
    assert view.provenance.freshness == "unknown"
    assert view.market.symbol == "QQQ"
