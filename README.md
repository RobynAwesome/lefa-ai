<p align="center">
  <img src="./assets/readme/meet-lefa-readme-hero.svg" alt="Meet LEFA — governed financial intelligence companion" width="100%" />
</p>

<div align="center">
  <img src="https://img.shields.io/badge/STATUS-GOVERNED_POC_VALIDATED-111111?style=for-the-badge" alt="POC status" />
  <img src="https://img.shields.io/badge/ALPACA-OPTIONS_ALPHA_AGENTS-F2D16B?style=for-the-badge&logoColor=111111" alt="Alpaca AI Trading Agents Hackathon" />
  <img src="https://img.shields.io/badge/PARTNER-FEATHERLESS_AI-7C3AED?style=for-the-badge&logoColor=white" alt="Featherless AI Partner" />
  <img src="https://img.shields.io/badge/ZERO--TRUST-FORTIFIED-059669?style=for-the-badge&logoColor=white" alt="Zero-Trust Fortified" />
  <img src="https://img.shields.io/badge/PYTHON-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11+" />
</div>

<div align="center">
  <a href="https://github.com/RobynAwesome/lefa-ai/actions/workflows/ci.yml"><img src="https://github.com/RobynAwesome/lefa-ai/actions/workflows/ci.yml/badge.svg?branch=main" alt="ci" /></a>
  <a href="https://github.com/RobynAwesome/lefa-ai/actions/workflows/security-lint.yml"><img src="https://github.com/RobynAwesome/lefa-ai/actions/workflows/security-lint.yml/badge.svg?branch=main" alt="Security & Lint Gate" /></a>
  <a href="https://github.com/RobynAwesome/lefa-ai/actions/workflows/security-hardening.yml"><img src="https://github.com/RobynAwesome/lefa-ai/actions/workflows/security-hardening.yml/badge.svg?branch=main" alt="Zero-Trust Security Gate" /></a>
  <a href="https://github.com/RobynAwesome/lefa-ai/actions/workflows/mcp-boundary.yml"><img src="https://github.com/RobynAwesome/lefa-ai/actions/workflows/mcp-boundary.yml/badge.svg?branch=main" alt="MCP Boundary Verification" /></a>
  <a href="https://github.com/RobynAwesome/lefa-ai/actions/workflows/frontend-quality.yml"><img src="https://github.com/RobynAwesome/lefa-ai/actions/workflows/frontend-quality.yml/badge.svg?branch=main" alt="Frontend Quality Gate" /></a>
</div>

<p align="center">
  <strong>Your companion for governed financial intelligence.</strong><br/>
  <em>FI through AI, powered by SI.</em>
</p>

<p align="center">
  🇿🇦 <strong>Built in South Africa.</strong> · POC before narrative · receipts before claims · time reveals
</p>

---

<div align="center">
  <a href="https://lefa-core-live.vercel.app/"><img src="https://img.shields.io/badge/🚀_LAUNCH_LIVE_DEMO-lefa--core--live.vercel.app-22C55E?style=for-the-badge" alt="Launch Live Demo" /></a>
  <a href="./submission/one-page-writeup.md"><img src="https://img.shields.io/badge/📄_ONE--PAGE_WRITEUP-READ_PDF%2FMD-F2D16B?style=for-the-badge&logoColor=111111" alt="Read One-Page Writeup" /></a>
  <a href="#-options-alpha-strategy--risk-governance"><img src="https://img.shields.io/badge/⚡_OPTIONS_STRATEGY-DEFINED--RISK-3B82F6?style=for-the-badge" alt="Options Strategy" /></a>
  <a href="#-zero-trust-security-architecture"><img src="https://img.shields.io/badge/🛡️_ZERO--TRUST-NIST_800--207-7C3AED?style=for-the-badge" alt="Zero Trust Architecture" /></a>
</div>

---

## 👋 Meet LEFA

<p align="center">
  <a href="./assets/companion/lefa-companion-root.jpg">
    <img src="./assets/companion/lefa-companion-root.jpg" alt="Canonical hand-drawn LEFA companion source" width="38%" />
  </a>
  <a href="./assets/companion/lefa-companion-root.svg">
    <img src="./assets/companion/lefa-companion-root.svg" alt="Animated LEFA companion interface interpretation" width="38%" />
  </a>
</p>

<p align="center"><sub>Canonical source → animated interface interpretation. The drawing owns identity; the interface may evolve around it.</sub></p>

Most finance products introduce themselves with charts, balances and buttons.

**LEFA starts with a companion.**

You speak to **LEFA**. LEFA is the user-facing base intelligence. The complicated architecture underneath exists to help LEFA make a better decision — not to make the user learn the architecture.

> **You bring the human question. LEFA brings governed financial intelligence.**

---

## ⚡ Options Alpha Strategy & Risk Governance

Built specifically for the **Alpaca AI Trading Agents Hackathon** (Track: *Options Alpha Agents*):

- **AI Logic**: when `FEATHERLESS_API_KEY` is configured, Featherless AI (`Qwen/Qwen2.5-7B-Instruct`) explains the real provider evidence supplied to it. If inference is unavailable, the camera-safe lane returns `HOLD`; it does not substitute canned reasoning.
- **Defined-Risk Alpha Structures (`src/lefa/alpha_structures.py`)**:
  - **Bull Put Vertical Spreads** (Moderately Bullish / High IV Premium Harvesting)
  - **Bear Call Vertical Spreads** (Moderately Bearish / High IV Premium Harvesting)
  - **Iron Condors** (Delta-Neutral Combined Volatility Premium Harvesting)
- **Delta Targeting**: the candidate selector requires short strikes to fall within `0.15–0.20` absolute delta.
- **Volatility Premium Gate**: a candidate is admitted only when $\frac{\text{ATM IV}}{\text{20-session RV}} \ge 1.15$.
- **Deterministic Risk Firewall**:
  - Max $3\%$ loss per structure relative to portfolio equity
  - $12\%$ aggregate-risk policy cap across all open exposures
  - $5\%$ competition-baseline drawdown circuit breaker
- **Alpaca Developer Stack**: official Alpaca MCP V2 server for protocol/tool observation plus `alpaca-py` / Alpaca Trading API for the separately governed paper-order boundary.

📄 **Full Architecture & Risk Specifications**: [Read the One-Page Hackathon Write-Up](./submission/one-page-writeup.md)

---

## 🛡️ Zero-Trust Security Architecture

LEFA operates under strict **Zero-Trust Architecture** (aligned with NIST SP 800-207 principles: *never trust, always verify, fail closed*).

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        ZERO-TRUST SECURITY STACK                       │
├────────────────────────────────────────────────────────────────────────┤
│ Layer 1: Secret Purge & Continuous Scanning (TruffleHog in CI)         │
│ Layer 2: Read-Only Alpaca MCP Boundary (ReadOnlyMCPProof Gate)         │
│ Layer 3: Execution Jurisdiction Firewall (LIVE Mode Inadmissible)      │
│ Layer 4: Cryptographic Runtime Truth (SHA-256 Receipts & Ark Ledger)   │
│ Layer 5: Defense-in-Depth HTTP Headers & DLP Response Sanitizer        │
│ Layer 6: Static Application Security Testing (Bandit SAST & pip-audit) │
└────────────────────────────────────────────────────────────────────────┘
```

1. **Defense-in-Depth HTTP Security Middleware (`src/lefa/security_middleware.py`)**:
   - Injects `Content-Security-Policy`, `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, and `Cache-Control: no-store` (ensures sensitive financial data is never persisted in browser caches).
   - Enforces CORS allowlist (`https://lefa-core-live.vercel.app`, `http://localhost:3000`), immediately rejecting unauthorized origins with `HTTP 403 Forbidden`.
   - Injects `X-LEFA-Execution-Authority: zero` and SHA-256 correlation IDs on every API response.
2. **Recursive Response DLP Sanitizer**:
   - Strips sensitive keywords (`secret`, `token`, `password`, `api_key`, `authorization`, `account_number`) recursively before payloads leave the server boundary.
3. **Execution Jurisdiction Firewall**:
   - `OBSERVE_ONLY`: Read-only market and account telemetry.
   - `PAPER`: Autonomous paper orders gated by dual-axis governance.
   - `LIVE`: Inadmissible; rejected at the orchestration layer.

---

## 🎭 Governing Product Law: Heavy Backend → Easy Immersive Interface

Codified in [`docs/HEAVY-BACKEND-EASY-IMMERSIVE.md`](./docs/HEAVY-BACKEND-EASY-IMMERSIVE.md):

> **Heavy Backend → Small Human State → Immersive Action**

LEFA serves non-technical humans. The backend absorbs technical complexity, schema drift, broker reconnection, and multi-leg risk evaluation. The interface projects simple, truthful human states:

| Human State | Semantic Meaning | Contextual Trigger |
|---|---|---|
| `Connecting` | Background verification active | Session initialization / MCP tool discovery |
| `Ready` | Provider witnessed, boundaries verified | Live paper telemetry authenticated |
| `Needs setup` | Environment setup required | Missing Alpaca or Featherless credentials |
| `Waiting` | Awaiting market evidence | Outside market hours or awaiting quotes |
| `Protected` | Risk firewall active | Candidate rejected or position limit reached |
| `Review needed` | Human authorization requested | Order submitted for confirmation |
| `Completed` | Transaction receipted | Order filled and confirmed on Alpaca |

```text
SIMPLE UI ≠ SIMPLE GOVERNANCE
HUMAN FRIENDLY ≠ FALSE SUCCESS
IMMERSIVE ≠ DECORATIVE
AI DOES THE WORK ≠ AI HIDES CONSEQUENCES
```

---

## 🧠 What moves under LEFA?

<p align="center">
  <img src="./assets/readme/lefa-control-room.svg" alt="Animated LEFA backend control room" width="100%" />
</p>

The public experience stays light. The backend is intentionally heavy.

```text
HUMAN
  ↓
LEFA — base identity / final decision-maker
  ↓
CRUD — capture the event
  ↓
ARK — governed structured bloat
  ↓
BMP — stress-test, filter and compress
  ↓
MAO — route bounded responsibility
  ↓
SWFUS — five internal ecosystems
  ↓
EVIDENCE + RECEIPTS + UNCERTAINTY
  ↓
LEFA
  ↓
DECISION / EXPLANATION
```

---

## 🌱 Five agents. Five ecosystems. One LEFA.

<p align="center">
  <img src="./assets/readme/lefa-swfus-ecosystem.svg" alt="Animated LEFA SWFUS five-agent ecosystem" width="100%" />
</p>

| Lane | Ecosystem | Core concern |
| :---: | :--- | :--- |
| **S** | Sovereign Ingestion | What may enter as governed signal? |
| **W** | Witness Isolation | What must be preserved independently as testimony? |
| **F** | Fluid Vectoring | What interpretations or directions remain plausible? |
| **U** | Unified Synchronization | What accepted state must align before action? |
| **S** | Severance Execution | What must be cut, held or rejected? |

---

## 🛠️ Project Structure & Skills

```text
lefa-ai/
├── .github/workflows/
│   ├── ci.yml                    # Primary CI pipeline (backend, MCP, frontend)
│   ├── security-lint.yml         # TruffleHog secret scan + global Ruff lint/format
│   ├── security-hardening.yml    # Bandit SAST scan + pip-audit + jurisdiction gate
│   ├── mcp-boundary.yml          # Alpaca MCP tool audit + read-only boundary tests
│   ├── frontend-quality.yml      # Strict TypeScript check + Vite production build
│   └── dependency-audit.yml      # Weekly supply chain vulnerability audit
├── assets/                       # Governed brand, companion, and interface artwork
├── docs/
│   └── HEAVY-BACKEND-EASY-IMMERSIVE.md  # Product system projection law
├── skills/
│   └── kpgs-rtc-learning/        # Evolved 24-RTC learning skill under KPGS rules
├── src/lefa/
│   ├── alpha_structures.py       # Bull Put, Bear Call, Iron Condor options alpha
│   ├── security_middleware.py    # Zero-Trust headers, CORS 403, and DLP sanitizer
│   ├── orchestration.py          # Dual-axis trading orchestrator
│   ├── governance.py             # RiskPolicy, Decision, and ExecutionJurisdiction
│   ├── mcp_observation.py        # ReadOnlyMCPProof evaluator
│   └── web_api.py               # Governed FastAPI serverless backend
├── tests/                        # Full regression suite (76/76 passing)
├── pyproject.toml                # Hatchling build specification
├── package.json                  # React 19 + Vite 6 + Tailwind 4 + Three.js
└── README.md
```

---

## ⚡ Run LEFA

```bash
# Set up Python environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e '.[dev,mcp]'
cp .env.example .env

# Run full regression test suite (76 tests)
pytest -v --tb=short

# Run repository-wide lint and format check
ruff check .
ruff format --check .

# Frontend strict typecheck and production build
npx tsc --noEmit
npm run build
```

Base CLI:
```bash
lefa
```

Real Alpaca MCP V2 protocol proof:
```bash
lefa-mcp-proof --symbol SPY
```

Options Alpha Agent Cycle (Camera-Safe / No Broker Write):
```bash
python scripts/run_options_agent.py --symbol AUTO
```

Explicit Alpaca **Paper** Execution Request after all gates clear:
```bash
python scripts/run_options_agent.py --symbol AUTO --execute
```

---

## 🏁 The Question

LEFA is not being built merely to answer:

> "Can an LLM place a trade?"

The question is:

> **Can one human-facing intelligence receive messy human intent, use governed internal agents and real financial evidence, preserve uncertainty instead of inventing certainty, and make a decision that time can later validate?**

<p align="center">
  <strong>OBSERVE → LEDGER → REVEAL</strong><br/>
  <strong>FI through AI, powered by SI.</strong><br/>
  <em>Heavy architecture. Light interface.</em>
</p>
