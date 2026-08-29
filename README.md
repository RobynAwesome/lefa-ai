<p align="center">
  <img src="LEFA%20AI%20Logo.png" alt="LEFA AI logo" width="360" />
</p>

<h1 align="center">LEFA AI</h1>
<p align="center"><strong>AI trading agent for the Alpaca AI Trading Agents Hackathon.</strong></p>
<p align="center">Built in South Africa 🇿🇦 · POC first · feedback makes the next build better.</p>

<div align="center">
  <img src="https://img.shields.io/badge/STATUS-POC-111111?style=for-the-badge" alt="POC status" />
  <img src="https://img.shields.io/badge/ALPACA-AI_TRADING_AGENTS-FFD43B?style=for-the-badge" alt="Alpaca AI Trading Agents Hackathon" />
  <img src="https://img.shields.io/badge/PYTHON-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11+" />
</div>

---

> ## 👋 New here?
> **You do not need to understand trading infrastructure to understand LEFA AI.**
>
> LEFA is a hackathon build. We are starting with one small proof: connect the agent to Alpaca, give it real context, let it make a governed decision, measure the result, and use that feedback to improve the next POC.

---

# 🧠 What is LEFA AI?

**LEFA AI is an AI trading agent being built for the Alpaca AI Trading Agents Hackathon.**

The idea is simple:

```text
MARKET + ACCOUNT CONTEXT
          ↓
       LEFA AI
          ↓
   PROPOSED ACTION
          ↓
     VALIDATION
          ↓
        ACTION
          ↓
      FEEDBACK
          ↓
      NEXT POC
```

We are not trying to build everything at once.

We are building the smallest useful trading-agent loop, proving it works, and then improving it from evidence.

---

# 🚪 First milestone

The first milestone is intentionally small:

```text
LOGIN TO THE HACKATHON / ALPACA ENVIRONMENT
                    ↓
CONNECT LEFA AI
                    ↓
READ THE CONTEXT LEFA NEEDS
                    ↓
MAKE ONE GOVERNED AGENT DECISION
                    ↓
MEASURE WHAT HAPPENED
                    ↓
FEED THE RESULT INTO THE NEXT POC
```

That gives us something real to build from.

---

# 🔁 How LEFA grows

LEFA uses a tight feedback loop:

```text
POC → TEST → FEEDBACK → IMPROVE → NEXT POC
```

A future design should come from what the previous proof taught us.

That keeps the hackathon build fast, understandable and grounded in working software.

---

# 🛠️ Current project seed

The repository currently includes:

- a Python package;
- a small CLI;
- Alpaca SDK integration;
- configuration support;
- governance experiments;
- tests and CI scaffolding.

The code is deliberately small so the team can change direction quickly as the POC develops.

---

# ⚡ Run LEFA

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
cp .env.example .env
pytest
```

CLI entry point:

```bash
lefa
```

Keep credentials in your local `.env` file. Never commit them.

---

# 🗂️ Repository map

```text
lefa-ai/
├── src/lefa/        # LEFA Python package
├── tests/           # POC tests
├── .github/         # CI and repository automation
├── .env.example     # environment template
├── pyproject.toml   # Python project configuration
└── README.md        # public front door
```

---

# 🏁 Hackathon direction

LEFA AI is being built to answer one practical question:

> **Can an AI trading agent turn live financial context into a useful, governed action and improve through feedback?**

The hackathon is where we prove it.

---

<p align="center">
  <strong>Connect → Decide → Validate → Act → Learn.</strong>
</p>
