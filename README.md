<p align="center">
  <img src="LEFA%20AI%20Logo.png" alt="LEFA AI logo" width="360" />
</p>

<h1 align="center">LEFA AI</h1>
<p align="center"><strong>AI trading agent being built for the Alpaca AI Trading Agents Hackathon.</strong></p>
<p align="center">POC first · unknown stays unknown · evidence decides what comes next.</p>

<div align="center">
  <img src="https://img.shields.io/badge/STATUS-POC-111111?style=for-the-badge" alt="POC status" />
  <img src="https://img.shields.io/badge/ALPACA-HACKATHON-FFD43B?style=for-the-badge" alt="Alpaca Hackathon" />
  <img src="https://img.shields.io/badge/PYTHON-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11+" />
</div>

---

> ## 👋 New here?
> **You do not need to understand trading infrastructure to understand LEFA AI.**
>
> LEFA is at the beginning of the build. This repository is the workbench for the hackathon — not a finished trading system and not a frozen architecture.

---

# 🧠 What is LEFA AI?

LEFA AI is our attempt to build an **AI trading agent around Alpaca** for the **Alpaca AI Trading Agents Hackathon**.

The important part right now is not pretending we already know the final agent.

We do not.

We are proving the smallest useful pieces, observing what the real environment gives us, collecting feedback, and using that evidence to decide the next build step.

```text
UNKNOWN
   ↓
TEST IT
   ↓
EVIDENCE
   ↓
POC
   ↓
FEEDBACK
   ↓
NEXT SMALLER / BETTER PROOF
```

**FOC does not get invented from an unknown and written backwards into the POC.**

---

# 🚪 What are we doing now?

The current job is simple:

```text
GET INTO THE HACKATHON / ALPACA ENVIRONMENT
                ↓
PROVE AUTHENTICATED CONNECTION
                ↓
SEE WHAT THE REAL ACCOUNT + TOOLS EXPOSE
                ↓
RECORD WHAT IS KNOWN / UNKNOWN
                ↓
BUILD THE FIRST REAL AGENT LOOP
```

That is the gate.

We are **not** choosing a final strategy, risk model, orchestration architecture, autonomous execution policy or product surface before this connection proof gives us evidence.

---

# ✅ What exists today?

This repository already has a small Python seed:

- a Python package and CLI;
- Alpaca SDK wiring;
- environment configuration;
- an experimental read-only account adapter;
- an experimental deterministic governance/risk module;
- tests and CI scaffolding.

Those pieces are useful **starting artifacts**.

They are **not automatically the final LEFA architecture**.

A seed can be changed, removed or replaced when the POC teaches us something better.

---

# ❓ What is still unknown?

These are valid project states — not gaps to fill with guesses:

| Question | State |
|---|---|
| Can we complete the intended Hackathon / Alpaca authenticated connection end-to-end? | `POC TO PROVE` |
| What authenticated account capabilities are actually available to LEFA? | `UNKNOWN` |
| What Alpaca tools / APIs will the agent use in the final build? | `UNKNOWN` |
| What trading strategy should LEFA prove first? | `UNKNOWN` |
| What should the final agent architecture look like? | `UNKNOWN` |
| What execution authority should the hackathon POC have? | `UNKNOWN` |
| What UI or operator surface is worth building? | `UNKNOWN` |

When one of these becomes knowable, we test it.

We do **not** promote it because an AI generated a convincing architecture diagram.

---

# 🔁 LEFA build law

```text
DO NOT KNOW?  → mark UNKNOWN
CAN TEST IT?  → run a POC
TEST WORKED?  → keep the evidence
TEST FAILED?  → keep the evidence
LEARNED MORE? → feed it back into the next POC
```

The repository should always make it easy to answer four questions:

1. **What are we trying to prove now?**
2. **What do we actually know?**
3. **What do we still not know?**
4. **What is the next smallest test?**

That is enough governance for the beginning.

---

# 🛠️ Run the current seed

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
cp .env.example .env
pytest
```

The current code also exposes:

```bash
lefa account
```

That command belongs to the existing seed. Whether it remains the final connection path is something the hackathon POC must prove.

Never commit credentials.

---

# 📍 Current checkpoint

For the live handoff — including what was tried, what is known, what is unknown and the next proof — read **[NOW.md](NOW.md)**.

---

<p align="center">
  <strong>Build what we can prove. Learn from what breaks. Let the POC teach the architecture.</strong>
</p>
