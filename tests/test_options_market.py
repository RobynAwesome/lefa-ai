from datetime import date
from decimal import Decimal
from types import SimpleNamespace

from lefa.options_market import parse_occ_contract, select_credit_spread


def _snapshot(*, delta: float, bid: float, ask: float, iv: float) -> SimpleNamespace:
    return SimpleNamespace(
        greeks=SimpleNamespace(delta=delta),
        latest_quote=SimpleNamespace(bid_price=bid, ask_price=ask),
        implied_volatility=iv,
    )


def test_parse_occ_contract() -> None:
    expiry, option_type, strike = parse_occ_contract("SPY260918P00100000")
    assert expiry == date(2026, 9, 18)
    assert option_type == "P"
    assert strike == Decimal(100)


def test_select_credit_spread_uses_provider_quotes_and_negative_credit_limit() -> None:
    chain = {
        "SPY260918P00100000": _snapshot(delta=-0.50, bid=3.00, ask=3.20, iv=0.30),
        "SPY260918P00095000": _snapshot(delta=-0.17, bid=1.50, ask=1.60, iv=0.28),
        "SPY260918P00090000": _snapshot(delta=-0.08, bid=0.50, ask=0.60, iv=0.27),
    }

    candidate = select_credit_spread(
        underlying="SPY",
        spot=Decimal(100),
        realized_vol=0.20,
        chain=chain,
        today=date(2026, 9, 5),
    )

    assert candidate is not None
    assert candidate.short_leg.symbol == "SPY260918P00095000"
    assert candidate.long_leg.symbol == "SPY260918P00090000"
    assert candidate.net_credit == Decimal("0.90")
    assert candidate.width == Decimal(5)
    assert candidate.maximum_loss == Decimal("410.00")
    assert candidate.signed_alpaca_limit_price == Decimal("-0.90")
    assert candidate.iv_rv_ratio == 1.5


def test_select_credit_spread_holds_when_iv_rv_gate_fails() -> None:
    chain = {
        "SPY260918P00100000": _snapshot(delta=-0.50, bid=3.00, ask=3.20, iv=0.20),
        "SPY260918P00095000": _snapshot(delta=-0.17, bid=1.50, ask=1.60, iv=0.20),
        "SPY260918P00090000": _snapshot(delta=-0.08, bid=0.50, ask=0.60, iv=0.20),
    }

    candidate = select_credit_spread(
        underlying="SPY",
        spot=Decimal(100),
        realized_vol=0.20,
        chain=chain,
        today=date(2026, 9, 5),
    )

    assert candidate is None
