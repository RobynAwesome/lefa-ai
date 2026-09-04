"""Live Alpaca market-evidence helpers for LEFA's options agent.

No fixture, cached browser value, or hard-coded contract is admissible here. A
candidate exists only when current Alpaca stock data, option-chain greeks/quotes,
and completed daily bars support the declared strategy gates.
"""
from __future__ import annotations

import math
import statistics
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal

from alpaca.data.enums import DataFeed, OptionsFeed
from alpaca.data.historical.option import OptionHistoricalDataClient
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import OptionChainRequest, StockBarsRequest, StockSnapshotRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.enums import ContractType

from lefa.config import Settings


@dataclass(frozen=True)
class OptionLegEvidence:
    symbol: str
    expiry: date
    strike: Decimal
    delta: float
    bid: Decimal
    ask: Decimal
    implied_volatility: float

    @property
    def midpoint(self) -> Decimal:
        return (self.bid + self.ask) / Decimal("2")

    @property
    def relative_spread(self) -> Decimal:
        midpoint = self.midpoint
        if midpoint <= 0:
            return Decimal("999")
        return (self.ask - self.bid) / midpoint


@dataclass(frozen=True)
class CreditSpreadCandidate:
    underlying: str
    observed_at: str
    spot: Decimal
    realized_volatility: float
    atm_implied_volatility: float
    iv_rv_ratio: float
    short_leg: OptionLegEvidence
    long_leg: OptionLegEvidence
    net_credit: Decimal
    width: Decimal
    maximum_loss: Decimal
    dte: int

    @property
    def signed_alpaca_limit_price(self) -> Decimal:
        """Alpaca mleg uses a negative limit price for a credit."""
        return -self.net_credit

    @property
    def legs_payload(self) -> list[dict[str, str]]:
        return [
            {"symbol": self.short_leg.symbol, "ratio_qty": "1", "side": "sell"},
            {"symbol": self.long_leg.symbol, "ratio_qty": "1", "side": "buy"},
        ]


def _decimal(value: object) -> Decimal:
    return Decimal(str(value))


def parse_occ_contract(symbol: str) -> tuple[date, str, Decimal]:
    """Parse the standard OCC yymmdd/type/8-digit-strike suffix."""
    if len(symbol) < 16:
        raise ValueError(f"Invalid OCC option symbol: {symbol}")
    expiry_token = symbol[-15:-9]
    option_type = symbol[-9]
    strike_token = symbol[-8:]
    if option_type not in {"C", "P"} or not expiry_token.isdigit() or not strike_token.isdigit():
        raise ValueError(f"Invalid OCC option symbol: {symbol}")
    expiry = datetime.strptime(expiry_token, "%y%m%d").date()
    strike = Decimal(strike_token) / Decimal("1000")
    return expiry, option_type, strike


def realized_volatility(closes: list[Decimal], *, periods: int = 20) -> float:
    """Annualized close-to-close realized volatility from completed sessions."""
    if len(closes) < periods + 1:
        raise ValueError(f"Need at least {periods + 1} closes for realized volatility")
    window = closes[-(periods + 1) :]
    returns = [math.log(float(window[i] / window[i - 1])) for i in range(1, len(window))]
    if len(returns) < 2:
        raise ValueError("Insufficient returns for realized volatility")
    return statistics.stdev(returns) * math.sqrt(252)


def _snapshot_to_leg(symbol: str, snapshot: object) -> OptionLegEvidence | None:
    try:
        expiry, option_type, strike = parse_occ_contract(symbol)
        if option_type != "P":
            return None
        greeks = getattr(snapshot, "greeks", None)
        quote = getattr(snapshot, "latest_quote", None)
        iv = getattr(snapshot, "implied_volatility", None)
        delta = getattr(greeks, "delta", None) if greeks is not None else None
        bid = getattr(quote, "bid_price", None) if quote is not None else None
        ask = getattr(quote, "ask_price", None) if quote is not None else None
        if delta is None or iv is None or bid is None or ask is None:
            return None
        leg = OptionLegEvidence(
            symbol=symbol,
            expiry=expiry,
            strike=strike,
            delta=float(delta),
            bid=_decimal(bid),
            ask=_decimal(ask),
            implied_volatility=float(iv),
        )
        if leg.bid < 0 or leg.ask <= 0 or leg.ask < leg.bid or leg.implied_volatility <= 0:
            return None
        return leg
    except (TypeError, ValueError, ArithmeticError):
        return None


def select_credit_spread(
    *,
    underlying: str,
    spot: Decimal,
    realized_vol: float,
    chain: dict[str, object],
    today: date,
    quantity: int = 1,
    min_iv_rv_ratio: float = 1.15,
    max_relative_spread: Decimal = Decimal("0.50"),
) -> CreditSpreadCandidate | None:
    """Select a truthful bull-put spread or return ``None``.

    Selection requires a 7-21 DTE put, short-leg absolute delta 0.15-0.20,
    same-expiry protective long, positive conservative credit, usable quotes,
    and ATM IV / 20-day RV >= the strategy threshold.
    """
    if realized_vol <= 0 or quantity < 1:
        return None

    legs = [leg for symbol, snap in chain.items() if (leg := _snapshot_to_leg(symbol, snap))]
    legs = [leg for leg in legs if 7 <= (leg.expiry - today).days <= 21]
    if not legs:
        return None

    short_candidates = [
        leg
        for leg in legs
        if leg.delta < 0
        and 0.15 <= abs(leg.delta) <= 0.20
        and leg.relative_spread <= max_relative_spread
    ]
    short_candidates.sort(
        key=lambda leg: (abs(abs(leg.delta) - 0.17), abs((leg.expiry - today).days - 14))
    )

    for short_leg in short_candidates:
        same_expiry = [leg for leg in legs if leg.expiry == short_leg.expiry]
        atm_candidates = [leg for leg in same_expiry if leg.implied_volatility > 0]
        if not atm_candidates:
            continue
        atm = min(atm_candidates, key=lambda leg: abs(leg.strike - spot))
        ratio = atm.implied_volatility / realized_vol
        if ratio < min_iv_rv_ratio:
            continue

        protective = [
            leg
            for leg in same_expiry
            if leg.strike < short_leg.strike and leg.relative_spread <= max_relative_spread
        ]
        protective.sort(key=lambda leg: short_leg.strike - leg.strike)
        for long_leg in protective:
            width = short_leg.strike - long_leg.strike
            if width <= 0:
                continue
            # Conservative executable credit: sell short at bid, buy protection at ask.
            net_credit = (short_leg.bid - long_leg.ask).quantize(Decimal("0.01"))
            if net_credit <= Decimal("0.00") or net_credit >= width:
                continue
            maximum_loss = ((width - net_credit) * Decimal("100") * quantity).quantize(
                Decimal("0.01")
            )
            return CreditSpreadCandidate(
                underlying=underlying,
                observed_at=datetime.now(UTC).isoformat(),
                spot=spot,
                realized_volatility=realized_vol,
                atm_implied_volatility=atm.implied_volatility,
                iv_rv_ratio=ratio,
                short_leg=short_leg,
                long_leg=long_leg,
                net_credit=net_credit,
                width=width,
                maximum_loss=maximum_loss,
                dte=(short_leg.expiry - today).days,
            )
    return None


class AlpacaOptionsMarket:
    """Read live stock/options evidence from Alpaca using the LEFA paper credentials."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings()
        api_key = self.settings.alpaca_api_key.get_secret_value().strip()
        secret_key = self.settings.alpaca_secret_key.get_secret_value().strip()
        if not api_key or not secret_key:
            raise ValueError("Alpaca paper credentials are required for market evidence")
        self._stock = StockHistoricalDataClient(api_key, secret_key)
        self._options = OptionHistoricalDataClient(api_key, secret_key)

    def latest_spot(self, symbol: str) -> Decimal:
        snapshots = self._stock.get_stock_snapshot(
            StockSnapshotRequest(symbol_or_symbols=symbol, feed=DataFeed.IEX)
        )
        snapshot = snapshots.get(symbol)
        if snapshot is None:
            raise RuntimeError(f"Alpaca returned no stock snapshot for {symbol}")
        latest_trade = getattr(snapshot, "latest_trade", None)
        price = getattr(latest_trade, "price", None) if latest_trade is not None else None
        if price is None or _decimal(price) <= 0:
            raise RuntimeError(f"Alpaca returned no usable latest trade for {symbol}")
        return _decimal(price)

    def completed_closes(self, symbol: str, *, sessions: int = 21) -> list[Decimal]:
        now = datetime.now(UTC)
        bars = self._stock.get_stock_bars(
            StockBarsRequest(
                symbol_or_symbols=symbol,
                timeframe=TimeFrame.Day,
                start=now - timedelta(days=60),
                end=now,
                feed=DataFeed.IEX,
            )
        )
        symbol_bars = list(bars[symbol])
        completed = [bar for bar in symbol_bars if bar.timestamp.date() < now.date()]
        closes = [_decimal(bar.close) for bar in completed]
        if len(closes) < sessions:
            raise RuntimeError(
                f"Alpaca returned only {len(closes)} completed sessions for {symbol}; need {sessions}"
            )
        return closes[-sessions:]

    def option_chain(self, symbol: str, *, spot: Decimal) -> dict[str, object]:
        today = datetime.now(UTC).date()
        request = OptionChainRequest(
            underlying_symbol=symbol,
            feed=OptionsFeed.INDICATIVE,
            type=ContractType.PUT,
            strike_price_gte=float(spot * Decimal("0.75")),
            strike_price_lte=float(spot * Decimal("1.02")),
            expiration_date_gte=today + timedelta(days=7),
            expiration_date_lte=today + timedelta(days=21),
        )
        chain = self._options.get_option_chain(request)
        if not isinstance(chain, dict) or not chain:
            raise RuntimeError(f"Alpaca returned no option chain for {symbol}")
        return chain

    def candidate(self, symbol: str, *, quantity: int = 1) -> CreditSpreadCandidate | None:
        symbol = symbol.upper()
        spot = self.latest_spot(symbol)
        closes = self.completed_closes(symbol)
        rv = realized_volatility(closes)
        chain = self.option_chain(symbol, spot=spot)
        return select_credit_spread(
            underlying=symbol,
            spot=spot,
            realized_vol=rv,
            chain=chain,
            today=datetime.now(UTC).date(),
            quantity=quantity,
        )
