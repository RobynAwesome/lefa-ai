# LEFA Product Law — Heavy Backend, Easy Immersive Interface

## Failure seed

A production connection modal truthfully exposed internal governance details (`schema`, namespace failure codes, execution authority and manual proof verification) to the person using LEFA.

The information was correct, but the responsibility was placed on the wrong side of the interface.

## Law

> **Heavy Backend → Small Human State → Immersive Action**

KPGS, KC, Alpaca adapters and LEFA backend may carry large proof surfaces. The human-facing interface should project only the minimum state required to understand what is happening and what to do next.

## Separation

### Backend / SI responsibility

May know and preserve:

- credentials and provider reachability;
- MCP namespace/schema/tool discovery;
- canonical receipts and hashes;
- Alpaca account restrictions and entitlements;
- paper/live jurisdiction;
- deterministic risk decisions;
- execution transport and provider order IDs;
- detailed HOLD reasons;
- retry/recovery/reconciliation state.

### Human / HI experience

Should normally see only:

- **Connecting** — LEFA is doing the work.
- **Ready** — the capability can be used.
- **Setup needed** — the capability is not ready, but the product remains usable where safe.
- **Unavailable** — a temporary service problem exists.

Technical detail is available only when the person explicitly enters an advanced/debug/receipt view.

## Interaction rule

A user action should describe the human goal, not the infrastructure mechanism.

Prefer:

- `Connect Alpaca`
- `Continue`
- `Try again`
- `Review decision`

Avoid as primary UI:

- `Verify Paper Bridge`
- schema identifiers;
- namespace names;
- raw provider error codes;
- transport names;
- execution-authority constants.

## Runtime pattern

```text
HUMAN INTENT
    ↓
SIMPLE LEFA ACTION
    ↓
LEFA BACKEND ORCHESTRATION
    ↓
KC / KPGS / PROVIDER EVIDENCE
    ↓
DETERMINISTIC GOVERNANCE
    ↓
SMALL EXPERIENCE STATE
    ↓
IMMERSIVE NEXT ACTION
```

## Governance invariant

Simplifying the interface must never simplify away truth.

```text
SIMPLE UI ≠ SIMPLE GOVERNANCE
HIDDEN COMPLEXITY ≠ HIDDEN RISK
HUMAN FRIENDLY ≠ FALSE SUCCESS
```

A backend HOLD remains HOLD. LEFA changes only its projection, not its meaning.

## First application

Issue #12 applies this law to the Alpaca connection experience:

- the browser stops consuming the dead POC MCP evidence seam;
- LEFA backend checks Sovereign Hub server-to-server;
- canonical provider HOLD remains inspectable behind the boundary;
- the modal automatically resolves to Connecting / Ready / Setup needed / Unavailable;
- no browser execution authority is introduced.

This document is the reusable seed for applying the same law across the rest of LEFA.
