# LEFA AI Engine Map (Canonical)

The backend responsibilities for LEFA are strictly bounded into discrete engines. This document canonizes their explicit responsibilities, authorities, and limits for the direct Alpaca Paper path.

## 1. The Eye (Observation Engine)
**Responsibility**: Sense Alpaca/account/market state and normalize evidence.
**Authority**: Strictly Read-Only.
**Limits**: 
- Must never gain execution authority.
- Must not evaluate risk or propose trades.
- Must preserve provider evidence and freshness metadata without inventing unavailable fields.

## 2. The Ark (Ledger & Temporal Engine)
**Responsibility**: The core Reality-to-Cloud (RTC) component. Preserves observations (`T0`), reasoning/decisions (`T1`), validation (`T2`), and later outcomes (`T3+`).
**Authority**: Append-Only Storage & Provenance when a persistence sink is configured.
**Limits**:
- **Future knowledge must not rewrite what the system knew in the past.**
- Cannot invent state.
- Exists to act as the cryptographic temporal truth for the KPGS pipeline.

## 3. The Brain (Risk & Validation Engine)
**Responsibility**: Deterministically approve, decline, or hold actions according to governed policy (e.g., `RiskPolicy`).
**Authority**: Risk metal-gate.
**Limits**:
- Cannot place trades (No execution authority).
- Cannot change its own policy without a canonical proposal going through KPGS orchestration.

## 4. The Hand (Execution Engine)
**Responsibility**: Own the narrow paper-trading action boundary.
**Authority**: Paper Execution (POC restricted).
**Limits**:
- No other engine receives implicit execution authority.
- Can only act if provided a valid deterministic approval from The Brain and a validated provider order payload.
- Executes paper-only Alpaca MLEG limit orders and reports success only with an Alpaca provider receipt.

## 5. The Face (Interface Projection Engine)
**Responsibility**: Translate governed temporal state from The Ark into the character-first visual experience.
**Authority**: Visual state mapping.
**Limits**:
- **Must not invent believable fake financial state.**
- The aesthetic must increase comprehension of the temporal loop (`OBSERVE → LEDGER → TIME → REVEAL`).

## 6. The Voice (Speech/Language Engine)
**Responsibility**: Translate audio to intent (STT) and state to audio (TTS) using Speechmatics.
**Authority**: Sensory mapping only.
**Limits**:
- **Must not hallucinate financial intent.** Audio transcripts must be preserved exactly as recognized.
- Cannot bypass **The Ark**. All recognized text is a `T0` event. All spoken text is a `T3` event.

---

## Architectural Principles (Dual-Axis Governance)

### 1. Dual-Axis Risk & Governance
Trading proposals must pass two entirely independent axes before execution eligibility:
1. **Financial Policy**: LEFA's deterministic `RiskPolicy.evaluate()` strictly governs financial risk (APPROVE/REJECT).
2. **Provider Truth**: Fresh Alpaca account, contract, quote, and order evidence establishes what can be claimed without overriding LEFA's risk.

### 2. Execution Jurisdiction
The orchestration result binds the proposal to a strict execution jurisdiction:
- `OBSERVE_ONLY`
- `PAPER`
- `LIVE` (Structurally unreachable for this POC; strictly fails closed).

### 3. Receipt Projections & Authority
**Receipts may travel. Authority does not.**
- `lefa-ai/receipts/`: Local projections when enabled, containing sanitized observations and decisions.
- Alpaca provider order receipts: authoritative evidence that an order was accepted by the paper broker.

### 4. Proof Depth
The `purity_score` determines the stage maturity (Proof Depth) of the KPGS pipeline:
- `SIMULATED` (design or fixture context only)
- `PROCEDURAL`
- `EVIDENCED`
- `INDEPENDENTLY_VALIDATED`
