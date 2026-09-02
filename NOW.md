# LEFA NOW

**Updated:** 2026-09-02T10:55:00+02:00  
**Authority:** Human owner + repository/runtime evidence  
**Stateless-renter law:** `I_AM_STATELESS_RENTER_NOT_LANDLORD`  
**Truth law:** `REALITY_STATE > INDEX_STATE` · `RECEIPT OR HOLD`

## Current product law

> **Heavy Backend → Small Human State → Immersive Action**

LEFA may carry complex provider, KPGS, risk, receipt, reconciliation and AI state behind the interface. Primary UX must expose only the smallest truthful state and useful next action. Simplifying the UI must never simplify away reality.

## Production truth

| Surface | Current evidence | Governed state |
|---|---|---|
| `lefa-core-live.vercel.app` | Production deployment from merge `b18b741cf3d57609200541dbcc8c750f85231cf0` | READY |
| LEFA → Sovereign Hub bridge | `/api/bridge/status` returns canonical Hub state server-to-server | WORKING |
| Alpaca paper account readiness | Sovereign Hub currently reports paper credentials unavailable | HOLD / SETUP_NEEDED |
| Browser execution authority | None; credentials and execution remain backend-only | ENFORCED |
| Runtime market telemetry | Current primary runtime UI still contains hard-coded/demo market values and simulator controls | FOC_FLAGGED — DO NOT TREAT AS LIVE |
| Backend snapshot | Explicit fixture-only surface; not admissible as live market/account truth | HOLD FOR REAL OBSERVATION |
| Featherless AI | Must be environment-configured server-side; provider failure may not masquerade as live reasoning | SECURITY / TRUTH HARDENING IN PROGRESS |

## Validated specimen — connection UX

Issue #12 / PR #13 removed the dead human-facing MCP verification seam and introduced the production bridge projection:

```text
Sovereign Hub technical truth
        ↓
LEFA backend projection
        ↓
READY | SETUP_NEEDED | UNAVAILABLE
        ↓
human-language next state
```

Production evidence after merge:

```text
GET /api/bridge/status
HTTP 200
bridge_state = HOLD
experience.state = SETUP_NEEDED
```

This is correct while the Hub lacks configured Alpaca paper credentials. No fake success is permitted.

## Active failure seeds

### P0 — committed AI credential exposure

A Featherless credential-like value was committed in source, scripts and prior NOW continuity. Current remediation branch:

`forge/purge-featherless-secret`

Required closure:

- current tree contains no real credential literal;
- Featherless configuration is environment-only;
- diagnostic scripts fail closed without configuration;
- inference outage/configuration failure is explicit instead of synthetic success;
- affected provider credential is rotated/revoked outside source control;
- historical Git commits are treated as exposed even after current-tree cleanup.

**Never place the credential value in issues, docs, chat, logs or fixtures.**

### P0 — runtime screen truth drift

`src/components/RuntimeCompanionView.tsx` currently presents hard-coded market data and permits manual runtime state cycling. The backend `/api/snapshot` explicitly remains fixture-only and the runtime screen does not consume it.

This creates a forbidden state:

```text
UI LOOKS LIVE
    !=
BACKEND HAS LIVE EVIDENCE
```

Next correction must:

- remove hard-coded price/regime/ATR/admissibility claims from primary runtime;
- remove manual `observing → ledgered → hold → reveal` simulation from primary runtime;
- keep simulator/design controls only in an explicit lab/design-preview context;
- drive connection state from `/api/bridge/status`;
- show market/account values only when backend provenance is non-fixture and fresh;
- render missing evidence as a calm user state, not invented telemetry;
- disable or contextualize AI market reasoning when no admitted market observation exists.

## Repository topology

| Repository | Authority |
|---|---|
| `RobynAwesome/lefa-ai` | User-facing LEFA runtime + Python contracts/orchestration/projection boundary |
| `RobynAwesome/kopano-sovereign-hub` | Server-side Alpaca PAPER observation and execution jurisdiction |
| `RobynAwesome/Introduction-to-MCP` | KPGS / PKA / governance transition authority |

Canonical transition law:

```text
trigger → evidence → invariant → authority → transition → receipt
```

## Active GitHub lanes

- **#15** — purge credential-like literals and restore repository-wide Python hygiene/security.
- **#16** — apply Heavy Backend → Easy Immersive Interface across all LEFA workflows.
- **#2** — Alpaca MCP/runtime proof admission remains separate from presentation success.

## Next safe execution order

1. Merge P0 Featherless current-tree purge only after CI proves env-only behavior and no secret literal remains.
2. Rotate/revoke the previously committed Featherless credential at the provider; Git history means deletion from main is not sufficient.
3. Seed a bounded runtime-truth branch from clean main.
4. Replace hard-coded runtime telemetry with backend-derived presence/absence state.
5. Add a real server-side market observation contract before displaying price/regime/ATR as current truth.
6. Continue Issue #16 surface-by-surface: onboarding, risk HOLD, ledger/reveal, AI, voice, errors, settings and mobile.

## Invariants

```text
SIMPLE UI ≠ SIMPLE GOVERNANCE
HUMAN FRIENDLY ≠ FALSE SUCCESS
IMMERSIVE ≠ DECORATIVE
AI DOES THE WORK ≠ AI HIDES CONSEQUENCES
MODEL MEMORY != GROUND TRUTH
CURRENT / REALITY STATE > INDEX STATE
NO POC PROMOTION WITHOUT RECEIPTS
INSUFFICIENTLY KNOWABLE → HOLD
```
