# NOW — LEFA AI

## Why this file exists

This is the current handoff for LEFA AI.

It records **what is actually known now** so the next person or agent does not invent a future architecture and treat it as project truth.

---

## Current phase

`ALPACA AI TRADING AGENTS HACKATHON → BUILD START → POC`

We are at the beginning.

The immediate goal is **not** to optimize a trading strategy.

The immediate goal is to prove the Hackathon / Alpaca connection and learn what the real authenticated environment exposes.

---

## Known

- The `RobynAwesome/lefa-ai` repository exists.
- A Python project seed exists.
- The seed currently contains Alpaca SDK wiring, a CLI, configuration, a read-only account adapter, governance/risk experiments, tests and CI scaffolding.
- Those artifacts are useful implementation experiments.
- They are **not automatically final product decisions**.

---

## Unknown

- The final authenticated connection path LEFA should use for the hackathon.
- Which authenticated Alpaca account capabilities are available end-to-end in the intended build environment.
- Which Alpaca APIs / tools belong in the first real agent loop.
- The first trading strategy worth proving.
- The final agent architecture.
- The final execution policy.
- The final operator / UI surface.

`UNKNOWN` is valid state.

Do not convert unknowns into FOC assumptions.

---

## Next proof

1. Complete the intended Hackathon / Alpaca login or authenticated connection.
2. Prove that LEFA can reach the authenticated Alpaca environment.
3. Record exactly what account data, market data and actions are available.
4. Record failures and missing capabilities without filling them with guesses.
5. Use that evidence to define the **smallest first agent loop**.
6. Build and test that loop.

Nothing further becomes canon before this proof feeds back into the build.

---

## Feedback loop

```text
UNKNOWN
   ↓
TEST
   ↓
EVIDENCE
   ↓
POC
   ↓
FEEDBACK
   ↓
CHANGE / KEEP / REMOVE
   ↓
NEXT POC
```

A failed POC is still useful if it tells us what the system cannot do.

A generated idea is not evidence.

---

## Anti-drift rule

If a future agent cannot prove a claim from the repository, the real environment or a recorded test:

**mark it UNKNOWN and work backwards to the next POC.**

Do not make LEFA look complete before LEFA is complete.
