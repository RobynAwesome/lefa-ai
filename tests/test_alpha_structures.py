"""
Unit tests for AlphaStructureEngine (Sprint 2 Options Alpha Structures).
Validates:
  1. Bull Put Spread formulation, delta checks, risk checks.
  2. Bear Call Spread formulation, delta checks, risk checks.
  3. Iron Condor combination and margin calculation.
  4. Alpaca legs payload conversion.
"""

from decimal import Decimal

import pytest

from lefa.alpha_structures import AlphaStructureEngine


def test_bear_call_spread_success():
    structure = AlphaStructureEngine.formulate_bear_call_spread(
        underlying="SPY",
        expiry="2026-09-25",
        dte=14,
        short_call_symbol="SPY260925C00595000",
        short_strike=Decimal("595.00"),
        short_delta=-0.17,
        long_call_symbol="SPY260925C00600000",
        long_strike=Decimal("600.00"),
        long_delta=0.08,
        net_credit=Decimal("1.25"),
        portfolio_equity=Decimal("100000.00"),
        iv_rv_ratio=1.28,
    )
    assert structure.name == "bear_call_spread"
    assert structure.max_loss == Decimal("375.00")  # (5.00 - 1.25) * 100
    assert structure.capital_at_risk_pct < Decimal("1.0")
    payload = structure.to_alpaca_legs_payload()
    assert len(payload) == 2
    assert payload[0]["side"] == "sell"
    assert payload[1]["side"] == "buy"


def test_bear_call_spread_rejects_low_iv_rv():
    with pytest.raises(ValueError, match="below minimum threshold"):
        AlphaStructureEngine.formulate_bear_call_spread(
            underlying="SPY",
            expiry="2026-09-25",
            dte=14,
            short_call_symbol="SPY260925C00595000",
            short_strike=Decimal("595.00"),
            short_delta=-0.17,
            long_call_symbol="SPY260925C00600000",
            long_strike=Decimal("600.00"),
            long_delta=0.08,
            net_credit=Decimal("1.25"),
            portfolio_equity=Decimal("100000.00"),
            iv_rv_ratio=1.05,  # Below 1.15
        )


def test_bear_call_spread_rejects_delta_out_of_bounds():
    with pytest.raises(ValueError, match="outside governed window"):
        AlphaStructureEngine.formulate_bear_call_spread(
            underlying="SPY",
            expiry="2026-09-25",
            dte=14,
            short_call_symbol="SPY260925C00595000",
            short_strike=Decimal("595.00"),
            short_delta=-0.28,  # > 0.20
            long_call_symbol="SPY260925C00600000",
            long_strike=Decimal("600.00"),
            long_delta=0.08,
            net_credit=Decimal("1.25"),
            portfolio_equity=Decimal("100000.00"),
            iv_rv_ratio=1.25,
        )


def test_iron_condor_combination():
    put_spread = AlphaStructureEngine.formulate_bull_put_spread(
        underlying="SPY",
        expiry="2026-09-25",
        dte=14,
        short_put_symbol="SPY260925P00585000",
        short_strike=Decimal("585.00"),
        short_delta=0.16,
        long_put_symbol="SPY260925P00580000",
        long_strike=Decimal("580.00"),
        long_delta=-0.08,
        net_credit=Decimal("1.20"),
        portfolio_equity=Decimal("100000.00"),
        iv_rv_ratio=1.30,
    )
    call_spread = AlphaStructureEngine.formulate_bear_call_spread(
        underlying="SPY",
        expiry="2026-09-25",
        dte=14,
        short_call_symbol="SPY260925C00605000",
        short_strike=Decimal("605.00"),
        short_delta=-0.16,
        long_call_symbol="SPY260925C00610000",
        long_strike=Decimal("610.00"),
        long_delta=0.08,
        net_credit=Decimal("1.10"),
        portfolio_equity=Decimal("100000.00"),
        iv_rv_ratio=1.30,
    )
    condor = AlphaStructureEngine.formulate_iron_condor(
        underlying="SPY",
        expiry="2026-09-25",
        dte=14,
        put_spread=put_spread,
        call_spread=call_spread,
        portfolio_equity=Decimal("100000.00"),
        iv_rv_ratio=1.30,
    )
    assert condor.name == "iron_condor"
    assert condor.net_credit == Decimal("2.30")  # 1.20 + 1.10
    # max loss = (5.00 - 2.30) * 100 = 270.00
    assert condor.max_loss == Decimal("270.00")
    assert len(condor.legs) == 4
    payload = condor.to_alpaca_legs_payload()
    assert len(payload) == 4
