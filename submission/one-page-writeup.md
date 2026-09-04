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
MARKET OBSERVATION (LEFA native Alpaca Paper API adapters)
       ↓
FEATHERLESS AI ADVISORY REASONING (Qwen/Qwen2.5-7B-Instruct)
       ↓  (Evidence-bounded explanation and structure context)
DETERMINISTIC LEFA RISK ENGINE (Zero-override mathematical gate)
       ↓  (APPROVE | HOLD | REJECT)
VALIDATED MLEG PAPER ORDER (Alpaca Trading API)
       ↓
ALPACA PROVIDER RECEIPT
```

1. **Autonomous Intelligence**: Featherless AI powers serverless inference via `Qwen/Qwen2.5-7B-Instruct`, explaining the supplied live account, quote, contract, and option-quote evidence without inventing unavailable Greeks or volatility facts.
2. **Stateless Renter Discipline**: The LLM is treated as a stateless generator. It can propose trades, explain risks, and summarize observations, but **it has zero brokerage execution privileges**.
3. **Dual-Axis Governance**: Financial risk (daily loss, open risk, trade risk, and defined-risk structure validation) and operational truth (paper-mode assertions, fresh provider evidence, and provider receipts) are independently evaluated. Only when both axes clear does an order become executable.

---

## 2. Options Strategy: Defined-Risk Alpha Harvesting

The current runner focuses on conservative premium collection on supported underlyings (`SPY`, `QQQ`, `AAPL`, `NVDA`) using one defined-risk multi-leg option structure:

- **Structure**: A same-expiration bull put vertical, selected only from active contracts with valid two-sided option quotes. Naked options are rejected.
- **Pricing**: The conservative entry credit is the short-put bid less the long-put ask. Maximum loss is the quoted spread width less credit, multiplied by 100 and quantity.
- **Evidence boundary**: The current implementation does not claim delta targeting, IV/RV gating, DTE exits, profit targets, bear call spreads, or iron condors.

---

## 3. Deterministic Risk Gates

All proposals pass through a hard-coded, zero-bypass risk firewall (`RiskPolicy`):

| Risk Gate | Threshold / Constraint | Action on Breach |
| :--- | :--- | :--- |
| **Paper Hard-Lock** | `ALPACA_PAPER_TRADE = true` | Immediate halt; live jurisdiction is rejected |
| **Max Loss Per Structure** | $\le 3.0\%$ of current portfolio equity | Automatic `REJECT` of proposed trade |
| **Aggregate Portfolio Risk** | $\le 12.0\%$ total open defined risk | Blocks all new risk entries |
| **Daily-Loss Stop** | $\ge 5.0\%$ loss from the previous equity observation | Halts the cycle and returns `HOLD` |
| **Structure Constraint** | Two valid protective-leg MLEG entries with positive limit credit | Rejects naked, malformed, or incomplete orders |
| **Evidence Constraint** | Active account, fresh underlying quote, active contracts, two-sided option quotes, and live Featherless rationale | Returns `HOLD` when any required evidence is unavailable |

---

## 4. Alpaca Infrastructure Implementation

LEFA keeps the hackathon-critical path self-contained in its Python backend:

1. **Direct provider observation**: `ReadOnlyAlpaca` reads the paper account, positions, stock quote, option contracts, and option quotes directly from Alpaca.
2. **Defined-risk execution**: `AlpacaPaperBroker` accepts only validated `mleg` limit orders with at least two option legs and a positive credit.
3. **Broker rehydration over local memory**: Each cycle re-reads account equity and positions from Alpaca before evaluating risk.
4. **Fail-closed behavior**: Missing credentials, provider failures, malformed data, unavailable contracts or quotes, missing reasoning, and invalid orders produce `HOLD`; no order is reported as submitted without an Alpaca receipt.

---

## 5. Human-Centered Interface: Heavy Backend, Light Experience

While the backend maintains institutional-grade risk gates and crypto-grade content hashing, the user interacts with **LEFA**: a calm, character-first 3D kinetic companion rendered in WebGL/Three.js on Vercel (`https://lefa-core-live.vercel.app/`).

LEFA demystifies algorithmic options trading: the frontend tells the human story; the backend preserves financial truth; and time reveals the outcome.
