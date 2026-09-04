from decimal import Decimal, InvalidOperation
from typing import Any
from uuid import uuid4

from alpaca.data.historical.option import OptionHistoricalDataClient
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import OptionLatestQuoteRequest, StockLatestQuoteRequest
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import (
    AssetStatus,
    ContractType,
    OrderClass,
    OrderSide,
    OrderType,
    PositionIntent,
    TimeInForce,
)
from alpaca.trading.requests import (
    GetOptionContractsRequest,
    LimitOrderRequest,
    OptionLegRequest,
)

from lefa.config import Settings
from lefa.governance import AccountState, calculate_open_risk


class ReadOnlyAlpaca:
    """Paper telemetry adapter. Intentionally exposes no order methods."""

    def __init__(self, settings: Settings) -> None:
        api_key = settings.alpaca_api_key.get_secret_value().strip()
        secret_key = settings.alpaca_secret_key.get_secret_value().strip()
        if (
            not api_key
            or not secret_key
            or "your_" in api_key.lower()
            or "your_" in secret_key.lower()
        ):
            raise RuntimeError("ALPACA_CREDENTIALS_UNAVAILABLE")
        self._api_key = api_key
        self._secret_key = secret_key
        self._client = TradingClient(
            api_key,
            secret_key,
            paper=True,
        )

    def get_account(self) -> dict[str, Any]:
        account = self._client.get_account()
        return {
            "id": str(account.id),
            "account_number": str(account.account_number),
            "status": _enum_value(account.status),
            "account_blocked": account.account_blocked,
            "trading_blocked": account.trading_blocked,
            "trade_suspended_by_user": account.trade_suspended_by_user,
            "equity": str(account.equity),
            "last_equity": str(account.last_equity),
            "cash": str(account.cash),
            "buying_power": str(account.buying_power),
            "currency": str(getattr(account, "currency", "USD")),
            "options_level": getattr(
                account,
                "options_approved_level",
                getattr(account, "options_trading_level", None),
            ),
        }

    def get_positions(self) -> list[dict[str, Any]]:
        return [
            {
                "symbol": position.symbol,
                "qty": str(position.qty),
                "market_value": str(position.market_value),
                "unrealized_pl": str(position.unrealized_pl),
                "side": _enum_value(position.side),
            }
            for position in self._client.get_all_positions()
        ]

    def get_latest_quote(self, symbol: str) -> dict[str, str]:
        """Read one current stock quote from Alpaca's market-data API."""
        normalized_symbol = symbol.strip().upper()
        if not normalized_symbol:
            raise ValueError("ALPACA_SYMBOL_INVALID")

        quote = StockHistoricalDataClient(
            self._api_key,
            self._secret_key,
        ).get_stock_latest_quote(
            StockLatestQuoteRequest(symbol_or_symbols=normalized_symbol)
        ).get(normalized_symbol)
        if quote is None or quote.bid_price is None or quote.ask_price is None:
            raise ValueError("ALPACA_QUOTE_INVALID")
        try:
            bid_price = Decimal(str(quote.bid_price))
            ask_price = Decimal(str(quote.ask_price))
        except (InvalidOperation, TypeError, ValueError) as exc:
            raise ValueError("ALPACA_QUOTE_INVALID") from exc
        if bid_price <= 0 or ask_price <= 0 or bid_price > ask_price:
            raise ValueError("ALPACA_QUOTE_INVALID")
        return {
            "symbol": normalized_symbol,
            "bid_price": str(bid_price),
            "ask_price": str(ask_price),
            "mid_price": str((bid_price + ask_price) / 2),
            "timestamp": str(quote.timestamp),
        }

    def account_state(self) -> AccountState:
        account = self._client.get_account()
        equity = Decimal(str(account.equity))
        last_equity = Decimal(str(account.last_equity))
        open_risk = calculate_open_risk(self.get_positions())
        return AccountState(
            equity=equity,
            open_risk=open_risk,
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
        if (
            not api_key.strip()
            or not secret_key.strip()
            or "your_" in api_key.lower()
            or "your_" in secret_key.lower()
        ):
            raise RuntimeError("ALPACA_CREDENTIALS_UNAVAILABLE")

        self._client = TradingClient(api_key, secret_key, paper=True)

    def get_account(self) -> dict[str, Any]:
        acc = self._client.get_account()
        return {
            "id": str(acc.id),
            "account_number": str(acc.account_number),
            "status": _enum_value(acc.status),
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
        open_risk = calculate_open_risk(self.get_positions())
        return AccountState(
            equity=acc["equity"],
            open_risk=open_risk,
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
                "side": _enum_value(pos.side),
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
                "status": _enum_value(order.status),
                "submitted_at": str(order.submitted_at),
                "order_class": getattr(order, "order_class", "simple"),
            }
            for order in orders
        ]

    def get_option_contracts(
        self,
        underlying_symbol: str,
        contract_type: str = "put",
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """Fetch active option contracts for an underlying symbol from Alpaca."""
        normalized_symbol = underlying_symbol.strip().upper()
        normalized_type = contract_type.strip().lower()
        if not normalized_symbol or normalized_type not in {"put", "call"} or limit < 1:
            raise ValueError("ALPACA_OPTION_CONTRACTS_INVALID")
        request = GetOptionContractsRequest(
            underlying_symbols=[normalized_symbol],
            status=AssetStatus.ACTIVE,
            type=ContractType.PUT if normalized_type == "put" else ContractType.CALL,
            limit=limit,
        )
        response = self._client.get_option_contracts(request)
        contracts = (
            response.option_contracts
            if hasattr(response, "option_contracts")
            else response.get("option_contracts", [])
        )
        return [
            {
                "symbol": str(contract.symbol),
                "strike_price": str(contract.strike_price),
                "expiration_date": str(contract.expiration_date),
                "type": _enum_value(contract.type),
                "status": _enum_value(contract.status),
            }
            for contract in contracts
        ]

    def get_option_quotes(self, symbols: list[str]) -> dict[str, dict[str, str]]:
        """Read current option quotes for the supplied contract symbols."""
        normalized_symbols = [symbol.strip().upper() for symbol in symbols if symbol.strip()]
        if not normalized_symbols:
            raise ValueError("ALPACA_OPTION_SYMBOLS_INVALID")

        quotes = OptionHistoricalDataClient(
            self.settings.alpaca_api_key.get_secret_value(),
            self.settings.alpaca_secret_key.get_secret_value(),
        ).get_option_latest_quote(
            OptionLatestQuoteRequest(symbol_or_symbols=normalized_symbols)
        )
        result: dict[str, dict[str, str]] = {}
        for symbol, quote in quotes.items():
            if quote.bid_price is None or quote.ask_price is None:
                continue
            try:
                bid_price = Decimal(str(quote.bid_price))
                ask_price = Decimal(str(quote.ask_price))
            except (InvalidOperation, TypeError, ValueError):
                continue
            if bid_price <= 0 or ask_price <= 0 or bid_price > ask_price:
                continue
            normalized_quote_symbol = str(symbol).strip().upper()
            result[normalized_quote_symbol] = {
                "bid_price": str(bid_price),
                "ask_price": str(ask_price),
                "timestamp": str(quote.timestamp),
            }
        return result

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
        """Submit a defined-risk multi-leg options order to Alpaca Paper API.

        Payload matches Alpaca MCP V2 / REST `place_option_order` specification.
        LEFA currently submits only defined-risk multi-leg limit orders. Simple
        and non-limit orders need a separate side-aware request path.
        """
        normalized_order_class = order_class.lower()
        normalized_order_type = order_type.lower()
        if normalized_order_class != "mleg" or normalized_order_type != "limit":
            raise ValueError("ALPACA_OPTION_ORDER_PARAMETERS_UNSUPPORTED")
        if not legs or len(legs) < 2:
            raise ValueError("ALPACA_MLEG_LEGS_INVALID")
        if qty < 1:
            raise ValueError("ALPACA_OPTION_ORDER_PARAMETERS_INVALID")
        if limit_price is None:
            raise ValueError("ALPACA_OPTION_ORDER_PARAMETERS_INVALID")
        try:
            normalized_limit_price = Decimal(str(limit_price))
        except (InvalidOperation, TypeError, ValueError) as exc:
            raise ValueError("ALPACA_OPTION_ORDER_PARAMETERS_INVALID") from exc
        if normalized_limit_price <= 0:
            raise ValueError("ALPACA_OPTION_ORDER_PARAMETERS_INVALID")

        cid = client_order_id or f"lefa-opt-{uuid4().hex[:12]}"
        try:
            order_type_value = OrderType(normalized_order_type)
            time_in_force_value = TimeInForce(time_in_force.lower())
            order_class_value = OrderClass(normalized_order_class)
        except ValueError as exc:
            raise ValueError("ALPACA_ORDER_PARAMETERS_INVALID") from exc
        position_intents = {
            "sell_to_open": PositionIntent.SELL_TO_OPEN,
            "sell_to_close": PositionIntent.SELL_TO_CLOSE,
            "buy_to_open": PositionIntent.BUY_TO_OPEN,
            "buy_to_close": PositionIntent.BUY_TO_CLOSE,
        }
        native_legs = []
        for leg in legs or []:
            action = str(leg.get("action", "")).lower()
            if action not in position_intents:
                raise ValueError("ALPACA_OPTION_LEG_ACTION_INVALID")
            leg_symbol = str(leg.get("symbol", "")).strip().upper()
            if not leg_symbol:
                raise ValueError("ALPACA_OPTION_LEG_SYMBOL_INVALID")
            expected_side = "sell" if action.startswith("sell_") else "buy"
            side = str(leg.get("side", expected_side)).lower()
            if side != expected_side:
                raise ValueError("ALPACA_OPTION_LEG_SIDE_INVALID")
            try:
                ratio_qty = float(leg.get("ratio_qty", "1"))
            except (TypeError, ValueError) as exc:
                raise ValueError("ALPACA_OPTION_LEG_RATIO_INVALID") from exc
            if ratio_qty <= 0:
                raise ValueError("ALPACA_OPTION_LEG_RATIO_INVALID")
            native_legs.append(
                OptionLegRequest(
                    symbol=leg_symbol,
                    ratio_qty=ratio_qty,
                    side=OrderSide.SELL if side == "sell" else OrderSide.BUY,
                    position_intent=position_intents[action],
                )
            )
        order_request = LimitOrderRequest(
            type=order_type_value,
            time_in_force=time_in_force_value,
            order_class=order_class_value,
            qty=float(qty),
            client_order_id=cid,
            limit_price=float(normalized_limit_price),
            symbol=None,
            side=None,
            legs=native_legs,
        )
        raw_response = self._client.submit_order(order_request)
        order_id = _response_value(raw_response, "id", "order_id")
        status = _response_value(raw_response, "status")
        submitted_at = _response_value(raw_response, "submitted_at", "created_at")
        if not order_id or not status:
            raise ValueError("ALPACA_ORDER_RESPONSE_INVALID")
        return {
            "order_id": str(order_id),
            "client_order_id": cid,
            "status": _enum_value(status),
            "symbol": None,
            "order_class": normalized_order_class,
            "submitted_at": str(submitted_at),
        }

    def cancel_order(self, order_id: str) -> None:
        self._client.cancel_order_by_id(order_id)


def _enum_value(value: Any) -> str:
    return str(getattr(value, "value", value))


def _response_value(response: Any, *names: str) -> Any:
    for name in names:
        if isinstance(response, dict):
            value = response.get(name)
        else:
            value = getattr(response, name, None)
        if value is not None:
            return value
    return None
