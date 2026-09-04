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
| `lefa-core-live.vercel.app` | Public LEFA deployment target | DEPLOYMENT MUST BE VERIFIED |
| LEFA → Alpaca Paper path | `/api/bridge/status` and `/api/runtime/status` use LEFA's native server-side Alpaca adapters | ENVIRONMENT-DEPENDENT |
| Alpaca paper account readiness | Direct account verification succeeds only when rotated paper credentials are configured | HOLD / SETUP_NEEDED WITHOUT ENV |
| Browser execution authority | None; credentials and execution remain backend-only | ENFORCED |
| Runtime market telemetry | Runtime status exposes account truth and reports `WAITING_FOR_MARKET` until an admitted market observation is available | HOLD UNTIL OBSERVED |
| Featherless AI | Must be environment-configured server-side; provider failure may not masquerade as live reasoning | SECURITY / TRUTH HARDENING IN PROGRESS |

## Validated specimen — connection UX

The direct-Alpaca path keeps the human-facing connection projection small while the backend verifies provider truth:

```text
LEFA native Alpaca adapter
        ↓
LEFA backend projection
        ↓
READY | SETUP_NEEDED | UNAVAILABLE
        ↓
human-language next state
```

The projection is truthful only when the deployment has the required server-side paper credentials:

```text
GET /api/bridge/status
HTTP 200
bridge_state = VERIFIED | HOLD
experience.state = READY | SETUP_NEEDED | UNAVAILABLE
```

No fake success is permitted when credentials, account verification, or provider evidence are unavailable.

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
| Alpaca Paper API | Authoritative account, market-data, option-data, and order provider for this hackathon path |
| `RobynAwesome/Introduction-to-MCP` | Historical KPGS / PKA governance reference; not a runtime dependency |

Canonical transition law:

```text
trigger → evidence → invariant → authority → transition → receipt
```

## Active GitHub lanes

- **Direct-Alpaca hardening** — keep paper credentials server-side and rotate them outside source control.
- **Runtime truth** — show only provider-backed account and admitted market observations.
- **Submission proof** — capture Featherless reasoning, deterministic risk decisions, and Alpaca order receipts.

## Next safe execution order

1. Rotate/revoke any previously exposed provider credentials; deleting a current-tree value is not sufficient.
2. Configure fresh Alpaca Paper and Featherless credentials only in the deployment environment.
3. Replace any remaining hard-coded runtime telemetry with backend-derived presence/absence state.
4. Capture a provider-backed demo run showing account verification, market observation, risk decision, and Alpaca receipt.
5. Keep the submission narrative aligned with the implemented bull put vertical path.

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
