# LEFA AI — MVP POC-0: Stitch + Data & Asset Governance

**Status:** Active plan  
**Project:** Alpaca AI Trading Agents Hackathon  
**POC rule:** Connect → Observe → Decide → Validate → Act → Learn  
**Build rule:** POC → Test → Feedback → Improve → Next POC

## 1. Purpose

LEFA AI begins with the visual MVP in **Google Stitch**, but the product must control its **data, assets, copy, and state contracts from day one**.

The goal is to avoid a common AI-generated-UI failure mode: a prototype invents fields and hard-coded numbers, implementation copies them, then the team later has to replace mock data across many components when the real Alpaca connection arrives.

For LEFA AI, **the UI adapts to canonical contracts — the contracts do not get rewritten to fit generated UI.**

This is a hackathon side quest with a larger value-transfer objective: validate useful agentic-finance patterns using global infrastructure, then carry the engineering knowledge and capability back into South African technology-building and apprenticeship work. We do not claim outcomes that have not yet been measured.

---

## 2. POC-0 outcome

POC-0 is successful when we have:

1. one canonical LEFA AI visual identity;
2. one controlled asset registry;
3. explicit UI data contracts before frontend implementation;
4. Stitch designs for four responsive MVP screens;
5. a clean boundary between **fixture data** and **live Alpaca data**;
6. no component-level hard-coded financial values pretending to be live;
7. a clear handoff into the first Alpaca-connected POC.

POC-0 does **not** require a final trading strategy or final architecture.

---

## 3. Canonical visual identity

The existing repository asset **`LEFA AI Logo.png`** is the current brand source of truth.

### Logo rules

- Do not regenerate or redesign the logo during POC-0.
- Do not create alternate AI-generated versions and silently replace the canonical file.
- Stitch receives the existing logo as visual context.
- The full logo is used on welcome / impact surfaces.
- A compact mark may later be derived from the canonical logo, but must be registered as a separate governed asset.
- Any rename, compression, crop, SVG conversion, or derivative must be performed intentionally and recorded in the asset registry.

### Initial design language

- deep emerald green;
- charcoal / near-black surfaces;
- restrained gold accent;
- geometric shield language;
- strong, clean typography;
- premium fintech feel without crypto-casino aesthetics;
- mobile-first responsive layout.

---

## 4. Asset governance from day one

The implementation phase should move toward this controlled structure:

```text
assets/
  brand/
    lefa-logo.png
  icons/
  illustrations/
  manifest.json
```

The current root logo remains canonical until a dedicated refactor moves it and updates every reference atomically.

### `manifest.json` responsibility

Every shipped asset should eventually have a registry entry containing at minimum:

```json
{
  "id": "brand.logo.primary",
  "path": "assets/brand/lefa-logo.png",
  "role": "Primary LEFA AI brand logo",
  "source": "canonical",
  "variant": "full",
  "status": "active"
}
```

### Asset law

**No component may depend on an invented filename or an unregistered generated asset.**

If Stitch, an image model, or another AI tool proposes a new visual asset, it is a candidate until explicitly accepted into the registry.

---

## 5. Data governance before UI implementation

Stitch may generate visual placeholders, but **Stitch does not define LEFA's financial data model**.

Before implementing the generated screens, define the minimum contracts that the UI is allowed to consume.

### Initial MVP contracts

#### `AccountContext`

Represents the account information required by the UI after Alpaca is connected.

Minimum conceptual fields:

- connection state;
- account status;
- buying-power / cash context when available;
- portfolio-equity context when available;
- data timestamp / freshness.

#### `MarketContext`

Represents the market information currently being observed.

Minimum conceptual fields:

- symbol / instrument identity;
- latest observed price context;
- market state;
- observation timestamp;
- provenance / source.

#### `AgentDecision`

Represents a LEFA proposal before action.

Minimum conceptual fields:

- decision ID;
- proposed action;
- instrument;
- rationale summary;
- decision state;
- creation timestamp.

#### `ValidationState`

Represents whether a proposal has passed the current POC's governance checks.

Minimum conceptual fields:

- decision ID;
- validation status;
- checks performed;
- rejection / hold reason when applicable;
- validation timestamp.

#### `ActivityEvent`

Represents observable events in the LEFA lifecycle.

Minimum conceptual fields:

- event ID;
- event type;
- timestamp;
- related decision or action ID;
- short human-readable description.

#### `ImpactMetric`

Represents measured hackathon-to-ecosystem value transfer without inventing social outcomes.

Minimum conceptual fields:

- metric ID;
- metric name;
- measured value;
- unit;
- evidence source;
- measurement date.

These are starting contracts, not a declaration of final architecture. Alpaca connection feedback may refine them.

---

## 6. Fixture data is allowed; disposable mock data is not

We still need deterministic data to build and test screens before every live integration exists. The difference is governance.

### Allowed

- fixtures generated from or validated against the same contracts used by live data;
- one centralized fixture source;
- clearly labeled fixture mode;
- deterministic values for repeatable UI tests;
- contract tests proving fixture and live providers expose the same shape.

### Not allowed

- hard-coded balances, P&L, quotes, positions, or account states inside React/UI components;
- random numbers generated merely to make dashboards look alive;
- AI-generated fields that do not exist in the canonical contract;
- copying fake financial numbers from Stitch screenshots into production code;
- separate "mock component" trees that later need to be rebuilt for real data;
- silent fallback from failed live data to realistic-looking fake data.

### Provider boundary

The UI should conceptually depend on a provider boundary:

```text
UI
 ↓
Canonical LEFA contracts
 ↓
Data provider
 ├── Fixture provider (POC/testing)
 └── Alpaca provider (live/paper environment)
```

The screen should not care which provider supplied the valid contract.

---

## 7. Data provenance and freshness

Financial context must always be distinguishable by provenance.

Every data object that can affect a LEFA decision should be able to answer:

- Where did this value come from?
- When was it observed?
- Is it fixture, cached, delayed, or live/paper-environment data?
- What POC produced or consumed it?

A visually polished dashboard with ambiguous provenance is considered a failed POC.

---

## 8. The four Stitch screens

### Screen 1 — Welcome / Connect

Purpose: establish LEFA and enter the Alpaca connection flow.

Required content:

- canonical LEFA AI logo;
- "Governed AI for market decisions.";
- dominant **Connect Alpaca** CTA;
- Alpaca AI Trading Agents Hackathon context;
- restrained impact statement: **Build globally. Transfer capability home.**

No fake account balance should appear before connection.

### Screen 2 — Agent Dashboard

Purpose: show the minimum context required to understand what LEFA is observing and doing.

Required regions:

- connection/account context;
- market context;
- LEFA agent status;
- current decision;
- activity stream.

All dynamic regions must map to canonical contracts.

### Screen 3 — Decision Review

Purpose: make a proposed action understandable before execution.

Required regions:

- proposed action;
- supporting market context;
- validation state;
- current risk/context information supported by the POC;
- human controls;
- visible proposed / validated / completed states.

Do not invent risk metrics merely because a generated dashboard template contains them.

### Screen 4 — Learning / Impact

Purpose: make the feedback and value-transfer loop visible.

Required content:

```text
POC → TEST → FEEDBACK → IMPROVE → NEXT POC
```

Show measured engineering outputs and evidence. Do not claim jobs, capital, users, or social impact until those values have evidence.

---

## 9. Google Stitch operating prompt

Use this as the first design prompt after uploading the canonical logo:

> Design a responsive web application MVP called LEFA AI for the Alpaca AI Trading Agents Hackathon. Use the uploaded LEFA AI logo as the canonical visual identity and do not redesign it. Build four responsive screens: Welcome / Connect, Agent Dashboard, Decision Review, and Learning / Impact. Use deep emerald green, charcoal/near-black, restrained gold accents, geometric shield forms, and strong clean typography. Prioritize mobile-first clarity and make the application understandable within five seconds. The UX sequence is Connect → Observe → Decide → Validate → Act → Learn. Do not invent realistic financial values or fake live-data states. Use clearly labeled structural placeholders for dynamic data regions because all implemented values will later come from governed LEFA data contracts. Avoid Bloomberg-terminal density, excessive charts, giant gradients, crypto-casino aesthetics, excessive glassmorphism, and desktop sidebars squeezed onto mobile. Produce a coherent design system suitable for later implementation and DESIGN.md capture.

---

## 10. Implementation law for AI-generated frontend work

When generated UI is brought into the repository:

1. **Extract layout and design — not invented data semantics.**
2. Replace every generated dynamic literal with a canonical contract binding immediately.
3. If a desired UI field has no contract, stop and decide whether the contract actually needs it.
4. Do not let AI silently rename domain concepts between screens.
5. Keep fixture and live providers interchangeable at the same boundary.
6. Add test IDs / state tests around important decision states rather than screenshot-only validation.
7. Any new asset must be registered before becoming a dependency.
8. Any measured impact claim must carry evidence/provenance.

This prevents AI variability from becoming application state.

---

## 11. POC-0 execution order

```text
CANONICAL LOGO
      ↓
ASSET RULES + REGISTRY CONTRACT
      ↓
UI DATA CONTRACTS
      ↓
STITCH — 4 RESPONSIVE SCREENS
      ↓
DESIGN REVIEW
      ↓
IMPLEMENT UI AGAINST CONTRACTS
      ↓
FIXTURE PROVIDER
      ↓
ALPACA PROVIDER
      ↓
FIRST CONNECTED LEFA POC
      ↓
TEST → FEEDBACK → NEXT POC
```

---

## 12. Acceptance criteria

POC-0 is complete only when:

- [ ] `LEFA AI Logo.png` is treated as the canonical source asset during Stitch design.
- [ ] Four Stitch screens exist and are responsive.
- [ ] No screen depends on believable fake live financial data.
- [ ] Asset-registry structure has been decided before adding generated assets.
- [ ] Minimum UI contracts are implemented before binding the frontend.
- [ ] Fixture data validates against the exact same contracts used by the Alpaca provider.
- [ ] Dynamic values are not hard-coded inside UI components.
- [ ] Data provenance/freshness can be represented.
- [ ] The implementation can switch fixture → Alpaca provider without rebuilding the screens.
- [ ] The first connected POC produces feedback for the next POC.

---

## 13. Immediate next action

**Open Google Stitch, upload the canonical `LEFA AI Logo.png`, run the governed prompt above, and produce the four-screen visual POC.**

The first screenshots become design feedback — not implementation truth. Contracts and registered assets remain the source of truth.
