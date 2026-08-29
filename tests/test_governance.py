from decimal import Decimal

from lefa.governance import AccountState, Decision, RiskPolicy, TradeProposal


def account(**overrides: Decimal) -> AccountState:
    values = {
        "equity": Decimal(100000),
        "open_risk": Decimal(0),
        "daily_pnl": Decimal(0),
    }
    values.update(overrides)
    return AccountState(**values)


def proposal(**overrides: object) -> TradeProposal:
    values: dict[str, object] = {
        "symbol": "SPY",
        "structure": "vertical_credit_spread",
        "maximum_loss": Decimal(500),
    }
    values.update(overrides)
    return TradeProposal(**values)


def test_approves_proposal_at_policy_boundary() -> None:
    receipt = RiskPolicy().evaluate(account(), proposal())
    assert receipt.decision is Decision.APPROVE


def test_rejects_trade_above_half_percent_equity() -> None:
    receipt = RiskPolicy().evaluate(account(), proposal(maximum_loss=Decimal("500.01")))
    assert receipt.decision is Decision.REJECT
    assert "trade_risk_limit_exceeded" in receipt.reasons


def test_rejects_disallowed_symbol_and_structure() -> None:
    receipt = RiskPolicy().evaluate(account(), proposal(symbol="NVDA", structure="iron_condor"))
    assert receipt.decision is Decision.REJECT
    assert receipt.reasons == ["symbol_not_allowed", "structure_not_allowed"]


def test_rejects_when_aggregate_open_risk_would_exceed_limit() -> None:
    receipt = RiskPolicy().evaluate(
        account(open_risk=Decimal(1750)), proposal(maximum_loss=Decimal(500))
    )
    assert "portfolio_risk_limit_exceeded" in receipt.reasons


def test_daily_loss_stop_fails_closed_at_boundary() -> None:
    receipt = RiskPolicy().evaluate(account(daily_pnl=Decimal(-1000)), proposal())
    assert "daily_loss_stop_active" in receipt.reasons
