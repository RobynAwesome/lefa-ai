# LEFA AI — Options Alpha Agent: One-Page Hackathon Write-Up

**Project**: LEFA AI — Governed Autonomous Options Alpha Agent  
**Track**: Options Alpha Agents  
**Hackathon**: lablab.ai × Alpaca AI Trading Agents Hackathon  
**Repository**: https://github.com/RobynAwesome/lefa-ai  
**Demo**: https://lefa-core-live.vercel.app/  

## AI logic

LEFA separates **reasoning authority** from **execution authority**. Featherless AI may explain provider evidence and a defined-risk candidate, but it cannot place an order or override deterministic policy. Missing AI, missing market evidence, provider errors, existing unrehydrated risk, or a failed policy gate produce `HOLD` rather than a synthetic success.

```text
ALPACA MCP V2 OBSERVATION + TOOL DISCOVERY
              ↓
REAL ALPACA MARKET / OPTIONS EVIDENCE
              ↓
FEATHERLESS AI REASONING — OR HOLD
              ↓
DEFINED-RISK BULL-PUT VERTICAL CANDIDATE
              ↓
DETERMINISTIC RISK GATES
       APPROVE | HOLD | REJECT
              ↓
CONTENT-HASHED EXECUTION INTENT
              ↓
OPTIONAL ALPACA PAPER TRADING API WRITE
              ↓
INDEPENDENT PROVIDER ORDER RE-READ
              ↓
PROVIDER RECEIPT — OR HOLD → TIME / REVEAL
```

The LLM is treated as a **stateless renter**. Brokerage authority remains in deterministic code, and browser state is never accepted as brokerage truth.

## Options strategy and current proof boundary

The broader strategy design is defined-risk premium harvesting on liquid underlyings. The **current camera-safe execution POC** proves one bounded structure: a bull put vertical credit spread selected from real Alpaca evidence on `SPY`, `QQQ`, `AAPL`, or `NVDA`.

- **Entry evidence**: 7–21 DTE puts from the provider option chain.
- **Delta gate**: short put absolute delta must be `0.15–0.20`.
- **Volatility premium gate**: `ATM IV / 20-session RV >= 1.15`.
- **Protective leg**: same-expiry lower-strike long put is mandatory.
- **Credit calculation**: conservative credit uses short bid minus long ask.
- **Maximum loss**: `(spread width - net credit) × 100 × quantity`.
- **Liquidity check implemented today**: bid/ask sanity plus a bounded relative-spread threshold. The POC does not claim open-interest screening unless that evidence is added and receipted.

Bear-call spreads, iron condors, 50% profit-taking, and the 5 DTE lifecycle exit remain strategy design targets; this write-up does not present them as broker-receipted automation in the current demo lane.

## Deterministic risk gates

| Gate | Current implementation |
|---|---|
| Paper jurisdiction | `ALPACA_PAPER_TRADE=true`; `AlpacaPaperBroker` rejects non-paper configuration |
| Account truth | account must be active, unblocked, and options permission must be verified |
| Existing exposure | open positions or open orders cause the camera-safe runner to `HOLD` rather than assume zero risk |
| Max loss per structure | `<= 3%` of current verified equity |
| Aggregate-risk policy | `<= 12%` policy ceiling; no current-position risk is silently invented |
| Drawdown circuit breaker | halt at `>= 5%` drawdown from `LEFA_COMPETITION_BASELINE_EQUITY` (default `$100,000`) |
| Structure | defined-risk vertical with a real protective long |
| Provider success | no execution claim without Alpaca order ID plus a separate provider re-read of that order |

## Alpaca infrastructure

**MCP V2 observation is a real protocol lane, not a renamed REST call.** `lefa-mcp-proof` launches the official `alpaca-mcp-server==2.2.0` over STDIO using FastMCP, dynamically discovers tools, verifies required capabilities including `get_account_info`, `get_clock`, `get_option_chain`, and `place_option_order`, and executes observation calls such as `get_clock` and `get_option_chain` in the configured paper environment. Credentials are passed to the subprocess and are never intentionally printed by LEFA.

```bash
pip install -e ".[mcp]"
lefa-mcp-proof --symbol SPY
```

Execution is deliberately separate. `AlpacaPaperBroker` uses Alpaca-py's public `LimitOrderRequest`, `OptionLegRequest`, and `TradingClient.submit_order()` APIs. For the premium-selling lane, LEFA enforces Alpaca's multi-leg price sign: **negative limit price = credit**. A submitted order is then independently fetched from Alpaca before the demo can say `PROVIDER_RECEIPT_CONFIRMED`; a fill is never claimed unless the provider reports one.

Camera-safe evidence cycle, with no brokerage write:

```bash
python scripts/run_options_agent.py --symbol AUTO
```

Explicit governed **paper** execution request:

```bash
python scripts/run_options_agent.py --symbol AUTO --execute
```

## Human experience

The backend carries credentials, provider semantics, tool discovery, market evidence, risk mathematics and receipts. The browser receives a small truthful projection such as **Ready**, **Waiting for evidence**, **Needs setup**, or **On hold**. Provider failure does not become UI success.

**Heavy Backend → Small Human State → Immersive Action.**

LEFA's thesis is simple: **autonomous does not have to mean ungoverned — and execution-capable does not mean executed. Receipt before claim.**
