import asyncio
import json
import logging
import os
from typing import Any, Dict
from uuid import UUID

from lefa.config import Settings

logger = logging.getLogger(__name__)


class AlpacaPaperObserver:
    """The Eye: Alpaca MCP & Trading API Observer.

    Connects to the official Alpaca Trading & Market Data APIs / MCP Server,
    strictly validating paper trading mode.
    Discovers market facts and persists raw observations directly into The Ark.
    """

    def __init__(
        self,
        ark_ledger: Any,
        server_command: str = "node",
        server_args: list[str] | None = None,
        settings: Settings | None = None,
    ) -> None:
        self.ark = ark_ledger
        self.server_command = server_command
        self.server_args = server_args or ["alpaca-mcp-server/index.js"]
        self.settings = settings or Settings()

    def _get_trading_client(self) -> Any:
        api_key = self.settings.alpaca_api_key.get_secret_value()
        secret_key = self.settings.alpaca_secret_key.get_secret_value()
        if not api_key or not secret_key or "your_" in api_key:
            return None

        try:
            from alpaca.trading.client import TradingClient

            return TradingClient(api_key, secret_key, paper=True)
        except Exception as exc:
            logger.debug("Could not instantiate TradingClient: %s", exc)
            return None

    async def _execute_mcp_call(self, tool_name: str, args: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """Execute an actual MCP or Trading API observation call.

        Enforces paper mode invariant. Uses live Alpaca REST SDK when credentials exist,
        falling back to clean simulated responses for offline test isolation.
        """
        # Ensure paper trading invariant is strictly enforced
        paper_env = os.getenv("ALPACA_PAPER_TRADE", "true").lower()
        if paper_env not in {"true", "1", "yes"}:
            raise RuntimeError("CRITICAL GOVERNANCE FAILURE: Alpaca is not in Paper Trading mode.")

        client = self._get_trading_client()

        if tool_name in {"get_account", "get_account_info"}:
            if client is not None:
                try:
                    acc = client.get_account()
                    return {
                        "id": str(acc.id),
                        "status": str(acc.status),
                        "equity": str(acc.equity),
                        "cash": str(acc.cash),
                        "buying_power": str(acc.buying_power),
                        "currency": str(getattr(acc, "currency", "USD")),
                        "options_level": getattr(acc, "options_approved_level", 3),
                        "_simulated": False,
                    }
                except Exception as exc:
                    logger.warning("Alpaca get_account API error, falling back: %s", exc)

            return {"status": "ACTIVE", "equity": "100000.00", "currency": "USD", "_simulated": True}

        elif tool_name in {"get_quote", "get_stock_bars"}:
            symbol = args.get("symbol", "SPY") if args else "SPY"
            if client is not None:
                try:
                    from alpaca.data.historical.stock import StockHistoricalDataClient
                    from alpaca.data.requests import StockLatestQuoteRequest

                    api_key = self.settings.alpaca_api_key.get_secret_value()
                    secret_key = self.settings.alpaca_secret_key.get_secret_value()
                    data_client = StockHistoricalDataClient(api_key, secret_key)
                    req = StockLatestQuoteRequest(symbol_or_symbols=symbol)
                    quote = data_client.get_stock_latest_quote(req)
                    q = quote[symbol]
                    return {
                        "symbol": symbol,
                        "bid_price": str(q.bid_price),
                        "ask_price": str(q.ask_price),
                        "timestamp": str(q.timestamp),
                        "_simulated": False,
                    }
                except Exception as exc:
                    logger.warning("Alpaca market quote error, falling back: %s", exc)

            return {"symbol": symbol, "bid_price": "595.10", "ask_price": "595.15", "_simulated": True}

        elif tool_name == "get_all_positions":
            if client is not None:
                try:
                    positions = client.get_all_positions()
                    return {
                        "positions": [
                            {"symbol": p.symbol, "qty": str(p.qty), "market_value": str(p.market_value)}
                            for p in positions
                        ],
                        "_simulated": False,
                    }
                except Exception as exc:
                    logger.warning("Alpaca positions error, falling back: %s", exc)
            return {"positions": [], "_simulated": True}

        elif tool_name == "place_option_order":
            if client is not None:
                try:
                    res = client.post("/orders", data=args or {})
                    return {"status": "submitted", "order": res, "_simulated": False}
                except Exception as exc:
                    logger.error("Alpaca order placement failed: %s", exc)
                    raise
            return {"status": "submitted", "order_id": "sim-order-101", "_simulated": True}

        else:
            raise RuntimeError(f"Unknown MCP tool: {tool_name}")

    async def observe_account(self) -> str:
        """Retrieve account telemetry from MCP / API and persist it to The Ark."""
        response = await self._execute_mcp_call("get_account")

        obs_id = self.ark.record_observation(
            source="AlpacaMCP",
            observation_data={"tool": "get_account", "response": response},
        )
        logger.info(f"Observed Account State. Ark T0 Receipt: {obs_id}")
        return str(obs_id)

    async def observe_quote(self, symbol: str) -> str:
        """Retrieve market data from MCP / API and persist to The Ark."""
        response = await self._execute_mcp_call("get_quote", {"symbol": symbol})

        obs_id = self.ark.record_observation(
            source="AlpacaMCP",
            observation_data={"tool": "get_quote", "response": response},
        )
        return str(obs_id)

