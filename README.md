<p align="center">
  <img src="./assets/readme/meet-lefa-readme-hero.svg" alt="Meet LEFA — governed financial intelligence companion" width="100%" />
</p>

<div align="center">
  <img src="https://img.shields.io/badge/STATUS-POC_VALIDATED-111111?style=for-the-badge" alt="POC status" />
  <img src="https://img.shields.io/badge/ALPACA-OPTIONS_ALPHA_AGENTS-F2D16B?style=for-the-badge&logoColor=111111" alt="Alpaca AI Trading Agents Hackathon" />
  <img src="https://img.shields.io/badge/PARTNER-FEATHERLESS_AI-7C3AED?style=for-the-badge&logoColor=white" alt="Featherless AI Partner" />
  <img src="https://img.shields.io/badge/PYTHON-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11+" />
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

- **AI Logic**: Featherless AI (`Qwen/Qwen2.5-7B-Instruct`) performs serverless, real-time market regime analysis and structure generation.
- **Options Strategy**: Automated defined-risk credit spreads (Bull Put & Bear Call spreads) and Iron Condors on liquid underlyings (`SPY`, `QQQ`, `AAPL`, `NVDA`).
- **Delta Targeting**: Short legs targeted at `0.15–0.20 delta` (~80–85% probability of OTM expiration).
- **Volatility Premium Gate**: Only trades when $\frac{\text{ATM IV}}{\text{20-Day RV}} \ge 1.15$.
- **Hard Risk Gates**: Zero naked short options, max $3\%$ loss per structure, $12\%$ aggregate portfolio risk cap, mandatory $5\text{ DTE}$ time stop, $50\%$ profit target, and $5\%$ drawdown circuit breaker.
- **Alpaca Developer Stack**: Alpaca MCP V2 server, Trading API, Alpaca CLI, and paper trading mode.

📄 **Full Architecture & Risk Specifications**: [Read the One-Page Hackathon Write-Up](./submission/one-page-writeup.md)

---

<p align="center">
  <img src="./assets/readme/lefa-observe-ledger-reveal.svg" alt="Animated LEFA Observe Ledger Time Reveal timeline" width="100%" />
</p>

LEFA does not treat a convincing first answer as reality.

**Observe** what is happening. **Ledger** what was known. Let **time** continue. **Reveal** what survived.

> **The frontend tells the story. The backend preserves the truth. Time decides what survives.**

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

The internal system does **not** replace LEFA's judgment. It filters unsupported certainty, preserves useful ambiguity, and returns better governed evidence to the base model.

<details>
<summary><strong>OPEN // Why the backend expands before it compresses</strong></summary>
<br/>

Human language can carry emotion, memory, contradiction, testimony, uncertainty and several valid meanings at once.

The ARK gives that ambiguity room to become **structured bloat** instead of prematurely flattening it into one intent. BMP then earns compression by stress-testing what should survive.

```text
HUMAN AMBIGUITY
      ↓
GOVERNED EXPANSION
      ↓
POC / FOC PRESSURE
      ↓
BMP FILTER + COMPRESSION
      ↓
BOUNDED DATA
```

**POC:** what can actually be supported.

**FOC:** what merely looks complete, plausible or polished.

</details>

---

## 🌱 Five agents. Five ecosystems. One LEFA.

<p align="center">
  <img src="./assets/readme/lefa-swfus-ecosystem.svg" alt="Animated LEFA SWFUS five-agent ecosystem" width="100%" />
</p>

The five internal agents do **not** talk to the user. They receive governed information from LEFA's backend and operate inside bounded ecosystems.

| Lane | Ecosystem | Core concern |
| :---: | :--- | :--- |
| **S** | Sovereign Ingestion | What may enter as governed signal? |
| **W** | Witness Isolation | What must be preserved independently as testimony? |
| **F** | Fluid Vectoring | What interpretations or directions remain plausible? |
| **U** | Unified Synchronization | What accepted state must align before action? |
| **S** | Severance Execution | What must be cut, held or rejected? |

> **Rich at the center. Minimal at the edges.**

The agent receives its identity, role, hierarchy and boundary. It does not need the entire city. It needs its ecosystem.

---

## 🧊 POC vs FOC

LEFA grows through one loop:

```text
POC → TEST → FEEDBACK → IMPROVE → NEXT POC
```

A model can sound intelligent and still be wrong. A market can disagree. A beautiful interface can look finished while the backend remains unproven.

So LEFA keeps receipts.

<details>
<summary><strong>OPEN // The hackathon proof</strong></summary>
<br/>

```text
CONNECT TO ALPACA PAPER ENVIRONMENT
                 ↓
OBSERVE REAL ACCOUNT / MARKET CONTEXT
                 ↓
PRESERVE SOURCE + TIME + PROVENANCE
                 ↓
LEFA RECEIVES GOVERNED FINDINGS
                 ↓
MAKE / EXPLAIN ONE GOVERNED DECISION
                 ↓
WAIT OR REPLAY TIME
                 ↓
COMPARE THESIS WITH OUTCOME
                 ↓
REVEAL
```

We are not claiming autonomous finance in one sprint.

The POC is smaller and harder to fake:

> **Can LEFA observe reality, preserve what it knew, make a bounded judgment, and remain accountable to what happens next?**

</details>

---

## 🎨 Heavy architecture. Light interface.

LEFA's visual identity is not decoration attached to a dashboard. The companion is the interface anchor.

- black, white and gold;
- calm, recognizable identity;
- circular / halo framing;
- motion maps to system state;
- financial truth must come from real providers, never invented UI values;
- the interface should become simpler as the backend becomes stronger.

Asset governance lives in [`./assets/INDEX.md`](./assets/INDEX.md).

---

## 🛠️ Current project seed

```text
lefa-ai/
├── assets/
│   ├── companion/
│   │   ├── lefa-companion-root.jpg  # canonical drawing source
│   │   └── lefa-companion-root.svg  # animated interface interpretation
│   ├── readme/
│   │   ├── meet-lefa-readme-hero.svg
│   │   ├── lefa-control-room.svg
│   │   ├── lefa-observe-ledger-reveal.svg
│   │   └── lefa-swfus-ecosystem.svg
│   └── INDEX.md
├── docs/
├── src/lefa/
├── tests/
├── .github/
├── .env.example
├── pyproject.toml
├── LEFA AI Logo.png
└── README.md
```

The code remains deliberately small while the architecture is being validated.

---

## ⚡ Run LEFA

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
cp .env.example .env
pytest
```

CLI:

```bash
lefa
```

Keep credentials in your local `.env`. Never commit them.

---

## 🏁 The question

LEFA is not being built merely to answer:

> "Can an LLM place a trade?"

The question is:

> **Can one human-facing intelligence receive messy human intent, use governed internal agents and real financial evidence, preserve uncertainty instead of inventing certainty, and make a decision that time can later validate?**

<p align="center">
  <strong>OBSERVE → LEDGER → REVEAL</strong><br/>
  <strong>FI through AI, powered by SI.</strong><br/>
  <em>Heavy architecture. Light interface.</em>
</p>
