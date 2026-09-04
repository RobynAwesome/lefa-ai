from decimal import Decimal
from typing import Any
from uuid import uuid4

from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderClass, OrderSide, TimeInForce
from alpaca.trading.requests import LimitOrderRequest, OptionLegRequest

from lefa.config import Settings
from lefa.governance import AccountState


class ReadOnlyAlpaca:
    """Paper telemetry adapter. Intentionally exposes no order methods."""

    def __init__(self, settings: Settings) -> None:
        self._client = TradingClient(
            settings.alpaca_api_key.get_secret_value(),
            settings.alpaca_secret_key.get_secret_value(),
            paper=True,
        )

    def account_state(self) -> AccountState:
        account = self._client.get_account()
        equity = Decimal(str(account.equity))
        last_equity = Decimal(str(account.last_equity))
        return AccountState(
            equity=equity,
            open_risk=Decimal(0),
            daily_pnl=equity - last_equity,
        )


class AlpacaPaperBroker:
    """Governed Alpaca Paper Trading Broker.

    Paper mode is mandatory. Multi-leg option orders use Alpaca-py's public
    ``submit_order`` API and request models; no private transport methods are used.
    """

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings()
        if not self.settings.alpaca_paper:
            raise ValueError("AlpacaPaperBroker strictly requires paper trading mode")

        api_key = self.settings.alpaca_api_key.get_secret_value()
        secret_key = self.settings.alpaca_secret_key.get_secret_value()
        if not api_key or not secret_key:
            raise ValueError("Alpaca paper credentials are required")

        self._client = TradingClient(api_key, secret_key, paper=True)

    def get_account(self) -> dict[str, Any]:
        acc = self._client.get_account()
        return {
            "id": str(acc.id),
            "account_number": str(acc.account_number),
            "status": str(acc.status),
            "equity": Decimal(str(acc.equity)),
            "last_equity": Decimal(str(acc.last_equity)),
            "cash": Decimal(str(acc.cash)),
            "buying_power": Decimal(str(acc.buying_power)),
            "account_blocked": bool(getattr(acc, "account_blocked", False)),
            "trading_blocked": bool(getattr(acc, "trading_blocked", False)),
            "trade_suspended_by_user": bool(getattr(acc, "trade_suspended_by_user", False)),
            "options_approved_level": getattr(acc, "options_approved_level", None),
            "options_trading_level": getattr(acc, "options_trading_level", None),
        }

    def get_clock(self) -> dict[str, Any]:
        clock = self._client.get_clock()
        return {
            "timestamp": str(clock.timestamp),
            "is_open": bool(clock.is_open),
            "next_open": str(clock.next_open),
            "next_close": str(clock.next_close),
        }

    def account_state(self) -> AccountState:
        acc = self.get_account()
        daily_pnl = acc["equity"] - acc["last_equity"]
        return AccountState(
            equity=acc["equity"],
            open_risk=Decimal("0.00"),
            daily_pnl=daily_pnl,
        )

    def get_positions(self) -> list[dict[str, Any]]:
        positions = self._client.get_all_positions()
        return [
            {
                "symbol": pos.symbol,
                "qty": str(pos.qty),
                "market_value": str(pos.market_value),
                "unrealized_pl": str(pos.unrealized_pl),
                "side": str(pos.side),
            }
            for pos in positions
        ]

    def get_orders(self, status: str = "open") -> list[dict[str, Any]]:
        orders = self._client.get_orders(status=status)
        return [
            {
                "id": str(order.id),
                "client_order_id": str(order.client_order_id),
                "symbol": str(order.symbol),
                "status": str(order.status),
                "submitted_at": str(order.submitted_at),
                "order_class": str(getattr(order, "order_class", "simple")),
            }
            for order in orders
        ]

    def place_option_order(
        self,
        *,
        symbol: str | None = None,
        order_class: str = "mleg",
        order_type: str = "limit",
        time_in_force: str = "day",
        limit_price: str | Decimal | None = None,
        legs: list[dict[str, Any]] | None = None,
        qty: int = 1,
        client_order_id: str | None = None,
    ) -> dict[str, Any]:
        """Submit a governed multi-leg credit order to Alpaca Paper.

        Alpaca defines an mleg limit price as **negative for a credit** and positive
        for a debit. LEFA's premium-selling lane therefore rejects non-negative
        prices instead of silently reversing the economic meaning of the order.
        """

        if order_class != "mleg" or order_type != "limit" or time_in_force != "day":
            raise ValueError("LEFA options execution supports only DAY limit mleg paper orders")
        if not legs or not 2 <= len(legs) <= 4:
            raise ValueError("Multi-leg option execution requires 2 to 4 legs")
        if qty < 1:
            raise ValueError("Order quantity must be at least 1")
        if limit_price is None:
            raise ValueError("A signed Alpaca mleg limit price is required")

        signed_limit = Decimal(str(limit_price))
        if signed_limit >= 0:
            raise ValueError("LEFA credit spreads require a negative Alpaca mleg limit price")

        option_legs: list[OptionLegRequest] = []
        for leg in legs:
            leg_symbol = str(leg.get("symbol", "")).strip()
            if not leg_symbol:
                raise ValueError("Every option leg requires a provider contract symbol")
            side_raw = str(leg.get("side", "")).lower()
            if side_raw not in {"buy", "sell"}:
                raise ValueError("Every option leg requires side='buy' or side='sell'")
            ratio_qty = float(leg.get("ratio_qty", 1))
            if ratio_qty <= 0:
                raise ValueError("Option leg ratio_qty must be positive")
            option_legs.append(
                OptionLegRequest(
                    symbol=leg_symbol,
                    ratio_qty=ratio_qty,
                    side=OrderSide.BUY if side_raw == "buy" else OrderSide.SELL,
                )
            )

        cid = client_order_id or f"lefa-opt-{uuid4().hex[:12]}"
        request = LimitOrderRequest(
            qty=float(qty),
            time_in_force=TimeInForce.DAY,
            order_class=OrderClass.MLEG,
            limit_price=float(signed_limit),
            legs=option_legs,
            client_order_id=cid,
        )
        order = self._client.submit_order(order_data=request)

        order_id = getattr(order, "id", None)
        if order_id is None and isinstance(order, dict):
            order_id = order.get("id") or order.get("order_id")
        if not order_id:
            raise RuntimeError("Alpaca returned no provider order ID")

        status = getattr(order, "status", None)
        submitted_at = getattr(order, "submitted_at", None)
        if isinstance(order, dict):
            status = status or order.get("status")
            submitted_at = submitted_at or order.get("submitted_at") or order.get("created_at")

        return {
            "order_id": str(order_id),
            "client_order_id": cid,
            "status": str(status or "UNKNOWN"),
            "symbol": symbol,
            "order_class": "mleg",
            "signed_limit_price": str(signed_limit),
            "submitted_at": str(submitted_at) if submitted_at is not None else None,
        }

    def cancel_order(self, order_id: str) -> None:
        self._client.cancel_order_by_id(order_id)
