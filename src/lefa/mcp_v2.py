"""Real Alpaca MCP V2 proof lane for LEFA.

This module launches Alpaca's official ``alpaca-mcp-server`` over MCP STDIO,
performs protocol discovery, and executes real paper-environment observation
tools. It is deliberately separate from LEFA's Alpaca Trading API broker so
MCP evidence can never be confused with REST/SDK execution.

Install the optional proof lane with::

    pip install -e ".[mcp]"

Then set the paper-account environment variables and run::

    lefa-mcp-proof --symbol SPY

Credentials are passed only to the MCP subprocess and are never printed.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
from typing import Any

from fastmcp import Client
from fastmcp.client.transports import StdioTransport

REQUIRED_TOOLS = {
    "get_account_info",
    "get_clock",
    "get_option_chain",
    "place_option_order",
}


def _secret_env() -> dict[str, str]:
    api_key = os.getenv("ALPACA_API_KEY", "").strip()
    secret_key = (
        os.getenv("ALPACA_SECRET_KEY", "") or os.getenv("ALPACA_API_SECRET", "")
    ).strip()
    if not api_key or not secret_key:
        raise RuntimeError(
            "ALPACA_API_KEY and ALPACA_SECRET_KEY are required for the MCP proof lane"
        )

    return {
        "ALPACA_API_KEY": api_key,
        "ALPACA_SECRET_KEY": secret_key,
        "ALPACA_PAPER_TRADE": "true",
        "ALPACA_TOOLSETS": "account,trading,assets,stock-data,options-data",
    }


def _tool_name(tool: Any) -> str:
    name = getattr(tool, "name", None)
    if isinstance(name, str):
        return name
    if isinstance(tool, dict) and isinstance(tool.get("name"), str):
        return str(tool["name"])
    return ""


def _safe_result_shape(result: Any) -> dict[str, Any]:
    """Describe an MCP result without dumping account/provider payloads."""

    content = getattr(result, "content", None)
    data = getattr(result, "data", None)
    return {
        "received": result is not None,
        "content_items": len(content) if isinstance(content, list) else None,
        "has_structured_data": data is not None,
    }


async def run_mcp_proof(symbol: str = "SPY") -> dict[str, Any]:
    """Discover Alpaca MCP V2 and execute two real observation tools."""

    env = {**os.environ, **_secret_env()}
    transport = StdioTransport(
        command="alpaca-mcp-server",
        args=[],
        env=env,
        keep_alive=False,
    )

    async with Client(transport) as client:
        tools = await client.list_tools()
        discovered = {_tool_name(tool) for tool in tools}
        missing = sorted(REQUIRED_TOOLS - discovered)
        if missing:
            raise RuntimeError(f"Alpaca MCP V2 missing required tools: {', '.join(missing)}")

        clock = await client.call_tool("get_clock", {})
        option_chain = await client.call_tool(
            "get_option_chain",
            {
                "underlying_symbol": symbol.upper(),
                "feed": "indicative",
                "limit": 5,
            },
        )

        server_name = None
        server_info = getattr(client, "server_info", None)
        if server_info is not None:
            server_name = getattr(server_info, "name", None)

        return {
            "proof": "ALPACA_MCP_V2_PROTOCOL_VERIFIED",
            "transport": "stdio",
            "server": server_name or "alpaca-mcp-server",
            "paper_mode": True,
            "symbol": symbol.upper(),
            "discovered_tool_count": len(discovered),
            "required_tools": sorted(REQUIRED_TOOLS),
            "missing_required_tools": missing,
            "calls": {
                "get_clock": _safe_result_shape(clock),
                "get_option_chain": _safe_result_shape(option_chain),
            },
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Prove LEFA's real Alpaca MCP V2 connection")
    parser.add_argument("--symbol", default="SPY", help="Underlying symbol for option-chain proof")
    args = parser.parse_args()
    result = asyncio.run(run_mcp_proof(args.symbol))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
