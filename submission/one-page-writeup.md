# LEFA AI — Options Alpha Agent: One-Page Hackathon Write-Up

**Project**: LEFA AI — Governed Autonomous Options Alpha Agent  
**Track**: Options Alpha Agents  
**Hackathon**: lablab.ai × Alpaca AI Trading Agents Hackathon  
**Repository**: https://github.com/RobynAwesome/lefa-ai  
**Demo**: https://lefa-core-live.vercel.app/  

## AI logic

LEFA separates **reasoning authority** from **execution authority**. AI may analyze observations and propose an options structure, but it cannot bypass deterministic risk policy. A proposal becomes executable only after the KPGS risk engine returns `APPROVE`.

```text
ALPACA MCP V2 OBSERVATION + TOOL DISCOVERY
              ↓
FEATHERLESS AI REASONING
              ↓
DEFINED-RISK OPTIONS PROPOSAL
              ↓
DETERMINISTIC KPGS RISK GATES
       APPROVE | HOLD | REJECT
              ↓
ALPACA PAPER TRADING API EXECUTION
              ↓
BROKER ORDER RECEIPT → TIME → P&L / REVEAL
```

The LLM is treated as a **stateless renter**: it may propose and explain, but brokerage authority remains in deterministic code. LEFA rehydrates account state from Alpaca rather than trusting browser state or cached UI values.

## Options strategy

LEFA targets defined-risk premium structures on liquid underlyings such as `SPY`, `QQQ`, `AAPL`, and `NVDA`.

- **Structures**: bull put spreads, bear call spreads, and iron condors; naked short options are rejected.
- **Delta target**: short legs around `0.15–0.20` delta when market evidence supports the structure.
- **Volatility premium gate**: ATM implied volatility must be rich relative to realized volatility (`IV / 20-day RV >= 1.15`).
- **Entry window**: 7–21 DTE.
- **Profit target**: 50% of maximum credit.
- **Time stop**: exit by 5 DTE to reduce gamma/assignment risk.

## Deterministic risk gates

| Gate | Constraint |
|---|---|
| Paper jurisdiction | `ALPACA_PAPER_TRADE=true`; live mode rejected |
| Competition baseline | fresh paper account; starting equity must be `$100,000.00` |
| Max loss per structure | `<= 3%` of equity |
| Aggregate defined risk | `<= 12%` of equity |
| Drawdown circuit breaker | halt at `>= 5%` drawdown from baseline |
| Structure | protective long required; no naked shorts; max 4 legs |
| Liquidity | hold/reject when spread/open-interest evidence is insufficient |

## Alpaca infrastructure

**Real MCP V2 usage is a separate proof lane, not a renamed REST call.** `lefa-mcp-proof` launches Alpaca's official `alpaca-mcp-server==2.2.0` over MCP STDIO using FastMCP, performs live protocol discovery, verifies required tools including `get_account_info`, `get_clock`, `get_option_chain`, and `place_option_order`, then calls `get_clock` and `get_option_chain` against the configured paper environment. Credentials are passed only to the MCP subprocess and never printed.

Install and run the proof lane:

```bash
pip install -e ".[mcp]"
lefa-mcp-proof --symbol SPY
```

Order execution is intentionally separate: LEFA's `AlpacaPaperBroker` uses `alpaca-py` / Alpaca Trading API to rehydrate the paper account, positions and orders, resolve active option contracts, and submit governed multi-leg paper orders. This separation lets MCP satisfy AI/tool observation while deterministic LEFA code owns the final brokerage boundary and provider receipt.

## Human experience

The backend carries credentials, tool discovery, risk mathematics, receipts and provider failure states. The browser does not. The live Three.js interface projects only small human states such as **Connecting**, **Ready**, **Waiting for evidence**, or **On hold**.

**Heavy Backend → Small Human State → Immersive Action.**

LEFA's thesis is simple: **autonomous does not have to mean ungoverned.**
