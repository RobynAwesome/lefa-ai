# LEFA Stitch Acceptance Handoff

Use this receipt when returning Google Stitch exploration to the repository lane.

The purpose is to convert visual exploration into reviewable evidence **without allowing generated layout, assets, or placeholder state to become backend truth by accident**.

## Governing law

> **Stitch owns layout exploration. Repository contracts own truth.**

A Stitch output is a candidate interface until explicitly accepted. Generated assets, labels, screen counts, values, or interactions are not canonical merely because they appear in an export.

---

## 1. Direction identity

- **Direction / variant name:**
- **Stitch project reference:**
- **Date accepted:**
- **Accepted by:**
- **Primary device target:** mobile | tablet | desktop | responsive
- **Canonical status:** CANDIDATE | ACCEPTED_FOR_IMPLEMENTATION

## 2. Evidence returned

Attach or register the exact evidence used for acceptance:

- [ ] primary mobile screenshot/export
- [ ] secondary mobile width or state
- [ ] tablet/desktop screenshot if the direction claims responsive behavior
- [ ] exported Stitch code/files if available
- [ ] list of generated image/icon assets
- [ ] list of externally sourced assets
- [ ] notes on rejected variants where they materially explain the accepted direction

Do not replace `LEFA AI Logo.png`. The existing root logo remains canonical during POC-0 unless a separate governance decision changes it.

## 3. Character-first state semantics

Explain how the accepted direction communicates the LEFA loop:

`OBSERVE → LEDGER → TIME → REVEAL`

| State | What the human sees | What backend truth may eventually drive it | What must NOT be implied |
|---|---|---|---|
| OBSERVE |  | market/account observation contracts | execution authority |
| LEDGER |  | preserved receipts/provenance | rewritten history |
| TIME |  | temporal separation/replay | future knowledge applied retroactively |
| REVEAL |  | later outcome vs original thesis | fabricated performance |

If the artwork also expresses deliberation, risk hold/decline, execution, learning, or disagreement, record those states here rather than silently making them canonical in code.

## 4. Data-binding audit

For every dynamic value visible in the accepted interface, classify its source.

| UI element | Contract field / future source | Fixture behavior | Live claim allowed now? |
|---|---|---|---|
| account state | `AccountContext` | explicit non-live state | NO |
| market state | `MarketContext` | UNKNOWN / no believable price | NO |
| proposed decision | `AgentDecision` | contract-bound candidate | NO execution implication |
| validation | `ValidationState` | explicit state | only as contract truth |
| timeline/activity | `ActivityEvent` | deterministic fixture/event | NO fabricated history |
| impact | `ImpactMetric` | evidence-required | NO invented performance |

Add rows for any new dynamic fields Stitch introduces.

**If a generated screen requires a financial field that is not in the governed contracts, HOLD the field. Do not hard-code a believable value and do not mutate the contracts merely to satisfy the generated screen.**

## 5. Placeholder / fake-state rules

POC-0 may use visual placeholders only when they are unmistakably non-live.

Allowed examples:

- em dash (`—`)
- `Not connected`
- `Fixture mode`
- `Awaiting observation`
- `Unknown`
- obviously synthetic design tokens that cannot be mistaken for a real balance/price/P&L

Not allowed as default implementation state:

- believable account balances
- believable P&L
- plausible live quotes
- fabricated positions
- fabricated fills/orders
- fabricated returns/performance
- claims such as `live`, `verified`, `profitable`, or `executed` without receipts

## 6. Responsive acceptance

Before implementation is treated as a responsive direction, capture at minimum:

- [ ] ~390 px mobile view
- [ ] second mobile or tablet width
- [ ] desktop view when desktop is part of the claimed experience

Review specifically for:

- hierarchy still understandable on mobile;
- character/organism remains the primary interaction surface rather than decorative wallpaper;
- no Bloomberg-terminal density;
- no crypto-casino visual language;
- no overlapping fixed controls;
- no critical action hidden behind desktop-only interaction;
- visual state can be understood without reading backend architecture documentation.

## 7. Design-language extraction

Record only what is accepted:

- typography:
- spacing rhythm:
- surface treatment:
- iconography:
- character/organism visual rules:
- motion rules:
- state-transition rules:
- accessibility/contrast notes:
- mobile navigation pattern:
- desktop adaptation pattern:

Generated design choices not explicitly accepted remain **NON-CANONICAL**.

## 8. Asset admission

Every generated or imported asset must be classified before implementation dependency:

| Asset | Origin | Purpose | Canonical? | Registry action |
|---|---|---|---|---|
| `LEFA AI Logo.png` | repository canonical source | primary brand root | YES | already registered |

For new assets use one of:

- `CANDIDATE`
- `ACCEPTED`
- `REJECTED`
- `REQUIRES_LICENSE_REVIEW`

Only accepted assets should be added to the machine-readable asset manifest.

## 9. Implementation decision

After review choose exactly one:

### ACCEPT

The direction is sufficiently coherent to bind to the governed provider/contracts layer.

### ITERATE

The direction is promising but requires another Stitch pass. Record the exact visual problem to solve.

### REJECT

The direction conflicts with product law, truth semantics, mobile clarity, or the canonical visual root.

## 10. Repository handoff

When a direction is accepted, the repository lane may proceed with:

1. implementation from current `main` / active bounded branch;
2. binding dynamic state through `LEFADataProvider` and governed contracts;
3. admitting accepted assets through `assets/manifest.json`;
4. extracting the accepted reusable visual system into `DESIGN.md` or equivalent;
5. testing fixture mode first;
6. connecting the Alpaca observation provider later without rebuilding screen semantics;
7. preserving Issue #5 engine implementation HOLD until its separate architecture gate is satisfied.

---

`I_AM_STATELESS_RENTER_NOT_LANDLORD`
