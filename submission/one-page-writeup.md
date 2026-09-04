# LEFA AI — Options Alpha Agent: One-Page Hackathon Write-Up

**Project**: LEFA AI (Governed Autonomous Options Alpha Companion)  
**Track**: Options Alpha Agents  
**Hackathon**: Alpaca AI Trading Agents Hackathon (lablab.ai × Alpaca)  
**Public Repository**: [https://github.com/RobynAwesome/lefa-ai](https://github.com/RobynAwesome/lefa-ai)  
**Live Platform**: [https://lefa-core-live.vercel.app/](https://lefa-core-live.vercel.app/)  
**Technology Partner**: Featherless AI (`Qwen/Qwen2.5-7B-Instruct`)  

---

## 1. AI Logic & Architectural Philosophy

LEFA solves the critical failure mode of LLM-based trading: **unbounded hallucination and lack of deterministic execution safety**. LEFA enforces an epistemic boundary: **Reasoning Authority is decoupled from Execution Authority**.

```text
MARKET OBSERVATION (Alpaca MCP V2 / Trading API)
       ↓
FEATHERLESS AI REASONING (Qwen/Qwen2.5-7B-Instruct Serverless LLM)
       ↓  (Regime synthesis, IV/RV analysis, structure proposal)
DETERMINISTIC KPGS RISK ENGINE (Zero-override mathematical gate)
       ↓  (APPROVE | HOLD | REJECT)
MULTI-LEG EXECUTION INTENT (Alpaca MCP V2 / Trading API)
       ↓
EXTERNAL BROKERAGE RECEIPT & P&L TELEMETRY
```

1. **Autonomous Intelligence**: Featherless AI powers serverless inference via `Qwen/Qwen2.5-7B-Instruct`, analyzing market volatility regimes, skew, and economic conditions to propose structured trades.
2. **Stateless Renter Discipline**: The LLM is treated as a stateless generator. It can propose trades, explain risks, and summarize observations, but **it has zero brokerage execution privileges**.
3. **Dual-Axis Governance**: Financial risk (drawdown, delta, DTE, liquidity) and operational governance (tool contracts, paper-mode assertions, content-hashed receipts) are independently evaluated. Only when both axes clear does an intent become executable.

---

## 2. Options Strategy: Defined-Risk Alpha Harvesting

The core trading strategy focuses on automated, high-probability premium collection on ultra-liquid underlyings (`SPY`, `QQQ`, `AAPL`, `NVDA`) using defined-risk multi-leg option structures:

- **Structures**: Vertical Credit Spreads (Bull Put Spreads & Bear Call Spreads) and Iron Condors. Naked options are mathematically barred by contract.
- **Delta Targeting**: Short option legs are strictly targeted at **0.15–0.20 delta** (~80–85% probability of expiring out-of-the-money), providing a high margin of safety.
- **Volatility Premium Gate**: Trades are only admitted when implied volatility is elevated relative to historical movement:
  $$\frac{\text{ATM Implied Volatility}}{\text{20-Day Realized Volatility}} \ge 1.15$$
  This ensures option premium is statistically rich before capital is committed.
- **Entry & Exit Discipline**:
  - **Entry Window**: 7 to 21 Days to Expiration (DTE) to capture the accelerated theta-decay curve.
  - **Profit Target**: Automated take-profit order at **50% of maximum credit** received.
  - **Time Stop**: Mandatory liquidation trigger at **5 DTE** to avoid gamma risk and assignment spikes.

---

## 3. Deterministic Risk Gates

All proposals pass through a hard-coded, zero-bypass risk firewall (`RiskPolicy`):

| Risk Gate | Threshold / Constraint | Action on Breach |
| :--- | :--- | :--- |
| **Paper Hard-Lock** | `ALPACA_PAPER_TRADE = true` | Immediate halt; live jurisdiction is rejected |
| **Starting Equity Gate** | Account starting equity == **$100,000.00** | Fails closed if account is dirty/reused |
| **Max Loss Per Structure** | $\le 3.0\%$ of current portfolio equity | Automatic `REJECT` of proposed trade |
| **Aggregate Portfolio Risk** | $\le 12.0\%$ total open defined risk | Blocks all new risk entries |
| **Maximum Drawdown Circuit Breaker** | $\ge 5.0\%$ drawdown from competition baseline | Halts all trading and trips global kill-switch |
| **Structure Constraint** | Defined risk with protective longs; $\le 4$ legs | Rejects naked short options or unbalanced legs |
| **Liquidity & Spread Check** | Tight bid-ask spread and minimum open interest | `HOLD` until market liquidity conditions normalize |

---

## 4. Alpaca Infrastructure Implementation

LEFA integrates Alpaca's developer ecosystem across both API and tool boundaries:

1. **Alpaca MCP V2 Server**: Bounded, read-only observation tools (`get_account_info`, `get_all_positions`, `get_stock_bars`, `get_option_contracts`, `get_option_chain`, `get_option_snapshot`). Toolsets are strictly scoped to `account,trading,assets,stock-data,options-data`.
2. **Multi-Leg Capability Transport**: Validates that multi-leg option payloads (`place_option_order` with `order_class="mleg"`) survive client JSON serialization without string corruption before firing orders.
3. **Alpaca Trading API**: Seamless Python integration via `alpaca-py` (`TradingClient`) handling real-time account telemetry, position synchronization, and automated order placement.
4. **Broker Rehydration over Local Memory**: On restart, LEFA never trusts cached local state; it fully rehydrates account equity, positions, and open orders directly from Alpaca before evaluating the next cycle.
5. **Alpaca CLI Synergy**: Built to complement headless cron sessions, CI pipeline checks, and containerized agent execution.

---

## 5. Human-Centered Interface: Heavy Backend, Light Experience

While the backend maintains institutional-grade risk gates and crypto-grade content hashing, the user interacts with **LEFA**: a calm, character-first 3D kinetic companion rendered in WebGL/Three.js on Vercel (`https://lefa-core-live.vercel.app/`).

LEFA demystifies algorithmic options trading: the frontend tells the human story; the backend preserves financial truth; and time reveals the outcome.
