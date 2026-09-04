"""Direct Alpaca paper observations persisted to LEFA's Ark ledger.

This module retains the historical observer class name for callers, but it no
longer starts or delegates to an MCP server. All provider observations are made
by LEFA's native Python Alpaca adapters and fail closed when unavailable.
"""
from __future__ import annotations

from typing import Any

from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest

from lefa.alpaca import ReadOnlyAlpaca
from lefa.config import Settings


class AlpacaPaperObserver:
    """Read-only Alpaca paper observer that writes admitted facts to The Ark."""

    def __init__(
        self,
        ark_ledger: Any,
        server_command: str = "node",
        server_args: list[str] | None = None,
        settings: Settings | None = None,
    ) -> None:
        self.ark = ark_ledger
        self.server_command = server_command
        self.server_args = server_args or []
        self.settings = settings

    def _settings(self) -> Settings:
        try:
            settings = self.settings or Settings()
        except ValueError as exc:
            raise RuntimeError("CRITICAL GOVERNANCE FAILURE: Alpaca is not in Paper Trading mode.") from exc
        if not settings.alpaca_paper:
            raise RuntimeError("CRITICAL GOVERNANCE FAILURE: Alpaca is not in Paper Trading mode.")

        api_key = settings.alpaca_api_key.get_secret_value().strip()
        secret_key = settings.alpaca_secret_key.get_secret_value().strip()
        if (
            not api_key
            or not secret_key
            or "your_" in api_key.lower()
            or "your_" in secret_key.lower()
        ):
            raise RuntimeError("ALPACA_CREDENTIALS_UNAVAILABLE")
        return settings

    async def _execute_mcp_call(
        self,
        tool_name: str,
        args: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Execute one direct Alpaca observation; provider errors are propagated."""
        settings = self._settings()
        api_key = settings.alpaca_api_key.get_secret_value()
        secret_key = settings.alpaca_secret_key.get_secret_value()

        if tool_name in {"get_account", "get_account_info"}:
            response = ReadOnlyAlpaca(settings).get_account()
            response["provenance"] = {"source": "alpaca", "is_fixture": False}
            return response

        if tool_name in {"get_quote", "get_stock_bars"}:
            symbol = (args or {}).get("symbol", "SPY")
            if not isinstance(symbol, str) or not symbol.strip():
                raise ValueError("ALPACA_SYMBOL_INVALID")
            symbol = symbol.strip().upper()
            data_client = StockHistoricalDataClient(api_key, secret_key)
            quotes = data_client.get_stock_latest_quote(
                StockLatestQuoteRequest(symbol_or_symbols=symbol)
            )
            quote = quotes.get(symbol)
            if quote is None or quote.bid_price is None or quote.ask_price is None:
                raise ValueError("ALPACA_QUOTE_INVALID")
            return {
                "symbol": symbol,
                "bid_price": str(quote.bid_price),
                "ask_price": str(quote.ask_price),
                "timestamp": str(quote.timestamp),
                "provenance": {"source": "alpaca", "is_fixture": False},
            }

        if tool_name == "get_all_positions":
            return {
                "positions": ReadOnlyAlpaca(settings).get_positions(),
                "provenance": {"source": "alpaca", "is_fixture": False},
            }

        raise RuntimeError(f"Unknown read-only Alpaca observation: {tool_name}")

    async def observe_account(self) -> str:
        """Retrieve account telemetry from Alpaca and persist it to The Ark."""
        response = await self._execute_mcp_call("get_account")
        obs_id = self.ark.record_observation(
            source="Alpaca",
            observation_data={"tool": "get_account", "response": response},
        )
        return str(obs_id)

    async def observe_quote(self, symbol: str) -> str:
        """Retrieve a live market quote from Alpaca and persist it to The Ark."""
        response = await self._execute_mcp_call("get_quote", {"symbol": symbol})
        obs_id = self.ark.record_observation(
            source="Alpaca",
            observation_data={"tool": "get_quote", "response": response},
        )
        return str(obs_id)
