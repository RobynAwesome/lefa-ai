# Heavy Backend → Easy Immersive Interface

> **Product Law** — validated by Issue #12 / PR #13, promoted by Issue #16.  
> **Invariant**: `SIMPLE UI ≠ SIMPLE GOVERNANCE`  
> **Author**: LEFA Architecture  
> **Status**: Active  

---

## Governing Principle

LEFA serves non-technical humans. KPGS/AI/SI carries technical complexity, proof depth,
state reconciliation, provider semantics and failure recovery **behind the interaction boundary**.

This document does not remove governance detail. It moves detail to the correct layer.

---

## The Three Layers

```
┌─────────────────────────────────────────────────┐
│  LAYER 1: HEAVY BACKEND                        │
│  Provider transport, KPGS receipts, MCP         │
│  sessions, risk policy evaluation, SHA-256      │
│  hashes, execution jurisdiction, schema drift   │
│  detection, fail-closed gates.                  │
├─────────────────────────────────────────────────┤
│  LAYER 2: SMALL HUMAN STATE                     │
│  Connecting · Ready · Needs setup · Waiting     │
│  Protected · Not available yet · Review needed  │
│  Completed                                      │
├─────────────────────────────────────────────────┤
│  LAYER 3: IMMERSIVE ACTION                      │
│  The single next action the human can take.     │
│  Context-aware, device-adapted, truthful.       │
│  Full receipt available on advanced path.        │
└─────────────────────────────────────────────────┘
```

---

## Human Experience Test

For every primary user surface, ask:

1. **What is the human trying to accomplish?**
2. **What complexity can LEFA/KPGS resolve without asking the human to understand it?**
3. **What is the smallest truthful state the human needs now?**
4. **What single next action is useful?**
5. **Where is the full technical receipt preserved for advanced inspection/audit?**

---

## Projection Rules

### Backend MAY retain vocabulary such as:
- Schema/version identifiers
- Namespaces/tool contracts
- Provider transport details
- Exact KPGS receipt/hash state
- Execution jurisdiction codes
- Entitlement/restriction codes
- Deterministic gate reasons
- Reconciliation metadata

### Primary UI SHOULD prefer human states such as:
- `Connecting` — background verification in progress
- `Ready` — provider observed, boundaries active
- `Needs setup` — missing credentials; plain language instructions
- `Waiting` — awaiting market evidence
- `Protected` — risk gate active, HOLD state
- `Not available yet` — capability not deployed
- `Review needed` — human approval required
- `Completed` — action receipted

The exact vocabulary should be **contextual**; do not build a generic status taxonomy.

---

## Interaction Invariant

```
SIMPLE UI        ≠  SIMPLE GOVERNANCE
HUMAN FRIENDLY   ≠  FALSE SUCCESS
IMMERSIVE        ≠  DECORATIVE
AI DOES THE WORK ≠  AI HIDES CONSEQUENCES
```

**Immersion** means continuity, low cognitive overhead and context-aware action —
not visual spectacle alone.

---

## First Validated Specimen

**Issue #12 / PR #13**:
```
PAPER_CREDENTIALS_UNAVAILABLE → SETUP_NEEDED → "Trading connection needs setup"
```

The provider/KPGS truth remains inspectable while the person receives a seamless next state.

---

## Surfaces to Audit (Issue #16)

| # | Surface | Backend Responsibility | Human State |
|---|---------|----------------------|-------------|
| 1 | Onboarding / first-run | Credential detection, account verification | `Needs setup` or `Ready` |
| 2 | Alpaca connection | MCP session, paper mode enforcement | `Connecting` → `Ready` |
| 3 | Strategy observation | Market data ingestion, IV/RV calculation | `Waiting` or opportunity card |
| 4 | Risk approval / HOLD | RiskPolicy evaluation, deterministic gates | `Protected` with reason |
| 5 | Trade lifecycle | Order submission, receipt confirmation | `Review needed` → `Completed` |
| 6 | Receipts / ledger | SHA-256 hashing, OBSERVE→LEDGER→TIME→REVEAL | Timeline view |
| 7 | AI reasoning | Featherless inference, fail-closed on error | Plain-language summary |
| 8 | Voice interaction | Interruption recovery, state preservation | Calm audio feedback |
| 9 | Loading / retries / outages | Provider health, network failure detection | `Connecting` with context |
| 10 | Permissions / jurisdiction | Execution boundary enforcement | `Not available yet` |
| 11 | Settings / setup | Environment validation | Guided setup flow |
| 12 | Empty states | Missing data detection | Contextual empty message |
| 13 | Mobile navigation | Responsive layout, thumb-reach zones | Same semantic state |
| 14 | Advanced / debug / receipt | Full governance evidence | Inspector panel |

---

## Zero-Trust Integration

This product law operates **within** the zero-trust security framework:

1. **Security headers** (CSP, HSTS, X-Frame-Options) protect every response
2. **CORS allowlist** restricts API access to trusted origins
3. **Response sanitization** strips forbidden keys before any data reaches the frontend
4. **Execution authority** is always `zero` at the API boundary
5. **Runtime truth enforcement** prevents synthetic market data in the UI

```
I_AM_STATELESS_RENTER_NOT_LANDLORD
REALITY_STATE > INDEX_STATE
RECEIPT OR HOLD
```
