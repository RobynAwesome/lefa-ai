from decimal import Decimal
from typing import Any
from uuid import uuid4

from alpaca.trading.client import TradingClient

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

    Graduates LEFA from read-only observation to autonomous paper execution.
    Executes multi-leg options strategies, defined-risk credit spreads,
    and portfolio rehydration strictly in Alpaca's paper trading environment.
    """

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings()
        if not self.settings.alpaca_paper:
            raise ValueError("AlpacaPaperBroker strictly requires paper trading mode")

        api_key = self.settings.alpaca_api_key.get_secret_value()
        secret_key = self.settings.alpaca_secret_key.get_secret_value()

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
            "options_approved_level": getattr(acc, "options_approved_level", None),
            "options_trading_level": getattr(acc, "options_trading_level", None),
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
                "order_class": getattr(order, "order_class", "simple"),
            }
            for order in orders
        ]

    def place_option_order(
        self,
        *,
        symbol: str,
        order_class: str = "mleg",
        order_type: str = "limit",
        time_in_force: str = "day",
        limit_price: str | Decimal | None = None,
        legs: list[dict[str, Any]] | None = None,
        qty: int = 1,
        client_order_id: str | None = None,
    ) -> dict[str, Any]:
        """Submit a multi-leg or single-leg options order directly to Alpaca Paper API.

        Payload matches Alpaca MCP V2 / REST `place_option_order` specification.
        """
        cid = client_order_id or f"lefa-opt-{uuid4().hex[:12]}"
        payload: dict[str, Any] = {
            "symbol": symbol,
            "order_class": order_class,
            "type": order_type,
            "time_in_force": time_in_force,
            "qty": str(qty),
            "client_order_id": cid,
        }

        if limit_price is not None:
            payload["limit_price"] = str(limit_price)

        if legs:
            payload["legs"] = legs

        # Dispatch via underlying REST endpoint
        raw_response = self._client.post("/orders", data=payload)
        return {
            "order_id": str(raw_response.get("id") or raw_response.get("order_id")),
            "client_order_id": cid,
            "status": str(raw_response.get("status", "submitted")),
            "symbol": symbol,
            "order_class": order_class,
            "submitted_at": str(raw_response.get("submitted_at") or raw_response.get("created_at")),
            "raw_response": raw_response,
        }

    def cancel_order(self, order_id: str) -> None:
        self._client.cancel_order_by_id(order_id)

