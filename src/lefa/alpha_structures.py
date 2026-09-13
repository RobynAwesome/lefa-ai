"""
LEFA AI — Defined-Risk Options Alpha Structures
===============================================
Institutional Options Alpha strategy formulation under KPGS Governance.
Implements:
  1. Bull Put Spread (Credit) — Moderately Bullish / High IV
  2. Bear Call Spread (Credit) — Moderately Bearish / High IV
  3. Iron Condor (Credit) — Delta-Neutral Volatility Premium Harvesting

All structures strictly adhere to:
  - IV/RV ratio >= 1.15
  - Target absolute delta between 0.15 and 0.20
  - Maximum capital at risk <= 3.0% of portfolio equity
  - Zero synthetic market data (RECEIPT OR HOLD)

I_AM_STATELESS_RENTER_NOT_LANDLORD
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any


@dataclass(frozen=True)
class OptionLeg:
    symbol: str
    ratio_qty: int
    side: str  # "buy" or "sell"
    strike: Decimal
    option_type: str  # "call" or "put"
    delta: float


@dataclass(frozen=True)
class GovernedSpreadStructure:
    name: str  # "bull_put_spread" | "bear_call_spread" | "iron_condor"
    underlying: str
    expiry: str
    dte: int
    legs: list[OptionLeg]
    net_credit: Decimal
    max_loss: Decimal
    capital_at_risk_pct: Decimal
    delta_net: float
    iv_rv_ratio: float

    def to_alpaca_legs_payload(self) -> list[dict[str, Any]]:
        return [
            {
                "symbol": leg.symbol,
                "ratio_qty": leg.ratio_qty,
                "side": leg.side,
            }
            for leg in self.legs
        ]


class AlphaStructureEngine:
    """Deterministic options spread formulation engine."""

    MIN_IV_RV_RATIO: float = 1.15
    MIN_DELTA: float = 0.15
    MAX_DELTA: float = 0.20
    MAX_TRADE_RISK_PCT: Decimal = Decimal("3.0")

    @classmethod
    def formulate_bear_call_spread(
        cls,
        underlying: str,
        expiry: str,
        dte: int,
        short_call_symbol: str,
        short_strike: Decimal,
        short_delta: float,
        long_call_symbol: str,
        long_strike: Decimal,
        long_delta: float,
        net_credit: Decimal,
        portfolio_equity: Decimal,
        iv_rv_ratio: float,
    ) -> GovernedSpreadStructure:
        """Formulate a governed Bear Call Spread (Sell lower strike call, Buy higher strike call)."""
        if iv_rv_ratio < cls.MIN_IV_RV_RATIO:
            raise ValueError(
                f"IV/RV ratio {iv_rv_ratio:.2f} below minimum threshold {cls.MIN_IV_RV_RATIO}"
            )

        if not (cls.MIN_DELTA <= abs(short_delta) <= cls.MAX_DELTA):
            raise ValueError(
                f"Short call delta {short_delta} outside governed window [{cls.MIN_DELTA}, {cls.MAX_DELTA}]"
            )

        spread_width = long_strike - short_strike
        if spread_width <= 0:
            raise ValueError("Long call strike must be higher than short call strike")

        max_loss = (spread_width - net_credit) * 100
        risk_pct = (max_loss / portfolio_equity) * 100
        if risk_pct > cls.MAX_TRADE_RISK_PCT:
            raise ValueError(
                f"Trade risk {risk_pct:.2f}% exceeds {cls.MAX_TRADE_RISK_PCT}% ceiling"
            )

        legs = [
            OptionLeg(
                symbol=short_call_symbol,
                ratio_qty=1,
                side="sell",
                strike=short_strike,
                option_type="call",
                delta=short_delta,
            ),
            OptionLeg(
                symbol=long_call_symbol,
                ratio_qty=1,
                side="buy",
                strike=long_strike,
                option_type="call",
                delta=long_delta,
            ),
        ]

        return GovernedSpreadStructure(
            name="bear_call_spread",
            underlying=underlying,
            expiry=expiry,
            dte=dte,
            legs=legs,
            net_credit=net_credit,
            max_loss=max_loss,
            capital_at_risk_pct=risk_pct,
            delta_net=short_delta + long_delta,
            iv_rv_ratio=iv_rv_ratio,
        )

    @classmethod
    def formulate_bull_put_spread(
        cls,
        underlying: str,
        expiry: str,
        dte: int,
        short_put_symbol: str,
        short_strike: Decimal,
        short_delta: float,
        long_put_symbol: str,
        long_strike: Decimal,
        long_delta: float,
        net_credit: Decimal,
        portfolio_equity: Decimal,
        iv_rv_ratio: float,
    ) -> GovernedSpreadStructure:
        """Formulate a governed Bull Put Spread (Sell higher strike put, Buy lower strike put)."""
        if iv_rv_ratio < cls.MIN_IV_RV_RATIO:
            raise ValueError(
                f"IV/RV ratio {iv_rv_ratio:.2f} below minimum threshold {cls.MIN_IV_RV_RATIO}"
            )

        if not (cls.MIN_DELTA <= abs(short_delta) <= cls.MAX_DELTA):
            raise ValueError(
                f"Short put delta {short_delta} outside governed window [{cls.MIN_DELTA}, {cls.MAX_DELTA}]"
            )

        spread_width = short_strike - long_strike
        if spread_width <= 0:
            raise ValueError("Short put strike must be higher than long put strike")

        max_loss = (spread_width - net_credit) * 100
        risk_pct = (max_loss / portfolio_equity) * 100
        if risk_pct > cls.MAX_TRADE_RISK_PCT:
            raise ValueError(
                f"Trade risk {risk_pct:.2f}% exceeds {cls.MAX_TRADE_RISK_PCT}% ceiling"
            )

        legs = [
            OptionLeg(
                symbol=short_put_symbol,
                ratio_qty=1,
                side="sell",
                strike=short_strike,
                option_type="put",
                delta=short_delta,
            ),
            OptionLeg(
                symbol=long_put_symbol,
                ratio_qty=1,
                side="buy",
                strike=long_strike,
                option_type="put",
                delta=long_delta,
            ),
        ]

        return GovernedSpreadStructure(
            name="bull_put_spread",
            underlying=underlying,
            expiry=expiry,
            dte=dte,
            legs=legs,
            net_credit=net_credit,
            max_loss=max_loss,
            capital_at_risk_pct=risk_pct,
            delta_net=short_delta + long_delta,
            iv_rv_ratio=iv_rv_ratio,
        )

    @classmethod
    def formulate_iron_condor(
        cls,
        underlying: str,
        expiry: str,
        dte: int,
        put_spread: GovernedSpreadStructure,
        call_spread: GovernedSpreadStructure,
        portfolio_equity: Decimal,
        iv_rv_ratio: float,
    ) -> GovernedSpreadStructure:
        """Combine Bull Put and Bear Call spreads into a delta-neutral Iron Condor."""
        total_credit = put_spread.net_credit + call_spread.net_credit
        # Margin requirement: standard broker rule requires margin for only the wider spread width
        put_width = put_spread.legs[0].strike - put_spread.legs[1].strike
        call_width = call_spread.legs[1].strike - call_spread.legs[0].strike
        max_spread_width = max(put_width, call_width)

        max_loss = (max_spread_width - total_credit) * 100
        risk_pct = (max_loss / portfolio_equity) * 100

        if risk_pct > cls.MAX_TRADE_RISK_PCT:
            raise ValueError(
                f"Iron Condor risk {risk_pct:.2f}% exceeds {cls.MAX_TRADE_RISK_PCT}% ceiling"
            )

        combined_legs = put_spread.legs + call_spread.legs
        combined_delta = put_spread.delta_net + call_spread.delta_net

        return GovernedSpreadStructure(
            name="iron_condor",
            underlying=underlying,
            expiry=expiry,
            dte=dte,
            legs=combined_legs,
            net_credit=total_credit,
            max_loss=max_loss,
            capital_at_risk_pct=risk_pct,
            delta_net=combined_delta,
            iv_rv_ratio=iv_rv_ratio,
        )
