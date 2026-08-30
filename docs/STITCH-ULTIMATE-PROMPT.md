# LEFA AI — Google Stitch Ultimate Prompt

**Status:** CANDIDATE DESIGN BRIEF — POC-0B
**Execution surface:** Google Stitch
**Source of truth:** `README.md`, `assets/INDEX.md`, Issue #4, Issue #3, `docs/STITCH-ACCEPTANCE-HANDOFF.md`
**Governance filter:** Introduction-to-MCP Black Mask / POC-vs-FOC / Servitude Triad

> **Stitch owns visual exploration. Repository contracts own truth.**

## Audit correction before prompting

The older POC-0 document remains useful for data/asset governance, but its original assumption of four conventional fintech screens and emerald-first styling is **not the active visual direction**.

Current visual canon is:

- companion-first rather than dashboard-first;
- black + white + gold;
- circular / halo framing;
- calm recognizable human companion;
- motion/state meaning rather than decoration;
- `OBSERVE → LEDGER → TIME → REVEAL`;
- heavy architecture, light interface;
- no believable fake financial truth.

Issue #4 explicitly supersedes the assumption that Stitch must begin with four conventional fintech screens. Treat screen count and layout as discovery outputs.

---

# Ultimate Stitch prompt

Design the first **LEFA AI** product experience for the **Alpaca AI Trading Agents Hackathon**.

LEFA is not a generic trading dashboard, chatbot skin, mascot beside charts, or crypto-style finance product. LEFA is a **human-facing governed financial intelligence companion**.

The public product idea must be understandable in seconds:

> **Your companion for governed financial intelligence.**
>
> **Observe → Ledger → Reveal.**
>
> **The frontend tells the story. The backend preserves the truth. Time decides what survives.**

Use the uploaded LEFA assets as source material. Preserve them rather than redesigning them:

1. the canonical **LEFA AI logo**;
2. the canonical **LEFA companion** visual — black hat, black clothing, geometric gold detail, circular/halo framing, calm human presence.

Do not replace either canonical identity with a newly generated logo, robot, orb, generic AI face, animal mascot, stock trader, cyberpunk avatar, or crypto character.

## 1. Design objective

Create an interface that feels like **meeting and working with LEFA**, not operating a terminal.

The companion should be the primary interaction surface. The finance UI should emerge around the companion only when needed.

The experience should feel:

- intelligent;
- calm;
- premium;
- human;
- slightly playful;
- technically credible;
- distinctly modern without becoming sterile;
- visually strong enough for public hackathon screenshots;
- simple enough for a non-technical person to understand without an architecture explanation.

Do not expose the heavy internal architecture in the main user journey. Internal concepts such as CRUD, ARK, BMP, MAO and SWFUS are backend concerns unless a separate optional “engine room” view is deliberately explored later.

## 2. Use Stitch as an exploration canvas — diverge before converging

Do **not** immediately commit to one dashboard layout.

On the infinite canvas, produce **three genuinely different visual directions** for the same LEFA product identity:

### Direction A — Living Companion

A character-first, mobile-native experience where LEFA occupies the visual center and system state appears around the companion as restrained cards, rings, text, and contextual controls.

### Direction B — Living Ledger

A temporal experience where observations, decisions, holds, receipts, and later outcomes form a beautiful chronological story around LEFA without becoming a spreadsheet or audit console.

### Direction C — Conversational Control Room

A minimal conversation-first interface where the user speaks/types to LEFA, with compact governed evidence surfaces appearing only when relevant.

For each direction, show:

- a ~390 px mobile composition;
- a responsive desktop adaptation;
- disconnected / first-visit state;
- observing state;
- ledgered / preserved state;
- hold / uncertainty state;
- reveal / later-outcome state.

Do not force a fixed number of pages. Discover whether LEFA works better as one living surface, a small flow, contextual overlays, or a few connected screens.

## 3. Canonical visual language

Use:

- near-black / black as the primary depth;
- warm white / off-white for clarity and breathing room;
- restrained metallic / warm gold for identity, state edges, halo, geometry, and high-value emphasis;
- clean typography with strong hierarchy;
- circular / halo geometry derived from the companion;
- geometric gold linework as a secondary motif;
- generous negative space;
- tactile, elegant surfaces without excessive glassmorphism;
- highly legible mobile typography;
- a premium fintech feel without looking like a bank app template.

Avoid introducing emerald/green as the dominant identity unless it already exists in an uploaded accepted asset. Green may only appear later when a real semantic state requires it and the design system accepts it.

## 4. LEFA expression grammar — explore this as interface language

LEFA should have a **textual expression layer** inspired by kaomoji / emoticons. These are not random decoration. Explore them as tiny state signatures, conversational reactions, loading moments, microcopy, tooltips, empty states, transition labels, or optional companion captions.

Candidate expression vocabulary to explore:

- `╰(*°▽°*)╯` — delight / energetic completion
- `(^///^)` — bashful warmth / human connection
- `(❁´◡\`❁)` — calm satisfaction / gentle welcome
- `(●'◡'●)` — friendly attentive presence
- `☆*: .｡. o(≧▽≦)o .｡.:☆` — rare celebration / major milestone
- `(*/ω＼*)` — shy/playful acknowledgment
- `(┬┬﹏┬┬)` — strong disappointment / something genuinely failed
- `ಥ_ಥ` — sadness / empathy / failed expectation
- `ᓚᘏᗢ` — playful cat signature / easter-egg-scale delight
- `^_~` — playful confirmation
- `U_U` — quiet pause / reflective hold
- `O.O` — surprise / unexpected observation
- `OwO` — playful curiosity
- `UwU` — soft playful warmth
- `^o^` — upbeat positive reaction
- `~_~` — uncertainty / unease
- `X_X` — failed process / unavailable state
- `¬_¬` — skepticism / “this needs checking”
- `+_+` — high-focus processing / analysis
- `T_T` — disappointment
- `;_;` — softer sadness
- `^^;` — awkward uncertainty / cautious caveat

Treat this as a **candidate expression grammar**, not fixed product canon.

Important semantic rule:

**Expressions communicate LEFA's interaction/system mood, never investment performance.**

For example, a delighted expression may mean “receipt preserved” or “connection completed”; it must never visually imply that a trade is profitable unless real evidence supports that claim.

Use these expressions sparingly and intentionally. LEFA should feel alive, not childish or noisy. Explore how this grammar can make a financial intelligence companion feel warm and memorable while preserving trust.

## 5. Core state story

The interface must make this loop visible without requiring the user to read documentation:

### OBSERVE

LEFA is sensing account / market context.

Possible visual behavior:

- halo slowly wakes or pulses;
- subtle radial sensing lines;
- companion remains calm;
- microcopy such as `Observing… +_+`;
- evidence surfaces appear progressively.

Do not imply execution authority.

### LEDGER

LEFA preserves what was known at that moment.

Possible visual behavior:

- a ring locks into place;
- an observation becomes a compact receipt/timeline object;
- timestamp/provenance is visible when expanded;
- microcopy such as `Preserved. (●'◡'●)`.

Do not rewrite previous state using future information.

### TIME

The system waits, revisits, or replays later reality.

Possible visual behavior:

- halo arc / timeline orbit;
- restrained temporal transitions;
- clear distinction between “then” and “now”.

### REVEAL

LEFA compares the original thesis/decision with later reality.

Possible visual behavior:

- split or layered then-vs-now view;
- receipt expands into outcome comparison;
- companion reacts according to evidence, not aesthetics alone.

Do not fabricate performance or claim success simply because the reveal animation looks satisfying.

## 6. First-use / connection experience

The first visit should not dump the user into charts.

Start with LEFA.

Suggested content hierarchy:

- canonical companion / logo;
- **Meet LEFA**;
- `Your companion for governed financial intelligence.`;
- primary CTA: **Connect Alpaca**;
- secondary low-emphasis context: `Alpaca AI Trading Agents Hackathon`;
- small origin mark: `Built in South Africa.`;
- optional line: `Build globally. Transfer capability home.`

Before connection, do not display fake balances, fake quotes, fake positions, fake P&L, fake returns, fake orders, or fake “live” badges.

Use honest states such as:

- `Not connected`
- `Awaiting observation`
- `—`
- `Unknown`
- `Fixture mode` when relevant to implementation previews

## 7. Financial context behavior

When financial information appears, it should be subordinate to the user’s question and LEFA’s reasoning state.

Prefer contextual surfaces such as:

- one market observation card;
- one account-context card;
- one proposed decision / hold card;
- one receipt / provenance affordance;
- one reveal comparison.

Avoid:

- Bloomberg-terminal density;
- giant wall-of-metrics dashboards;
- fake candlestick charts;
- crypto-casino visuals;
- neon-green “profit” language;
- generic SaaS left-nav + 12 KPI cards;
- dozens of widgets just because fintech templates contain them;
- hard-coded realistic money values;
- fabricated activity feeds;
- meaningless decorative charts.

## 8. Human controls and governance

LEFA should communicate that it may:

- observe;
- reason;
- preserve evidence;
- propose;
- hold / decline;
- later reveal outcomes.

The interface must make **HOLD** feel like an intelligent result, not an error state.

Explore a visual language where uncertainty can be beautiful and legible:

- `Need more evidence. ¬_¬`
- `Holding this one. U_U`
- `Something changed. O.O`

Do not create controls that imply live autonomous trading in this design POC.

## 9. Motion principles

Motion must map to state.

Explore restrained motion such as:

- halo pulse = observation;
- ring lock = ledger receipt preserved;
- orbit / arc progression = time;
- controlled reveal / unfold = outcome comparison;
- subtle companion posture / expression change = system mood;
- small gold geometry changes = governance state.

Avoid perpetual particle storms, decorative stock tickers, excessive parallax, random glowing, and motion that has no semantic meaning.

Provide a reduced-motion alternative.

## 10. Mobile-first law

Design the product from the phone outward.

At ~390 px:

- LEFA remains the primary visual anchor;
- the main action remains visible;
- no desktop sidebar is squeezed onto mobile;
- no horizontal data overflow;
- financial context collapses gracefully;
- touch targets are comfortable;
- important state is understandable within five seconds;
- expressions remain readable but subtle;
- the user can move between conversation, evidence, and reveal without hunting.

Then adapt the same system to desktop. Desktop may gain breathing room and simultaneous context, but not extra conceptual complexity merely because there is more space.

## 11. Accessibility and trust

Create accessible contrast and readable typography.

Use the eventual design system to support WCAG-aware color semantics.

Do not rely on color alone to distinguish:

- observing;
- held;
- validated;
- rejected;
- revealed.

Use labels, icons, form, motion, and text together.

Never visually imply that a state is “verified,” “live,” “profitable,” or “executed” without a real backend receipt.

## 12. Public-build aesthetics

The product must produce screenshots that can stand on their own publicly.

A viewer should be able to look at one frame and understand:

1. this is LEFA;
2. LEFA is a companion, not a dashboard;
3. LEFA is observing / preserving / revealing financial reasoning;
4. the product is serious about truth;
5. the personality is warm and memorable.

Do not place the social mission as a giant charity banner in the core interaction. Keep the product credible globally. The South African origin and capability-transfer mission may appear as restrained provenance / impact context.

## 13. Deliverables from this first Stitch run

Do not code the final app yet.

Produce on the canvas:

1. **three divergent visual directions** A/B/C;
2. mobile ~390 px and desktop adaptation for each;
3. canonical logo + companion preserved in each;
4. at least four visual states: disconnected, observe, hold/uncertain, reveal;
5. at least one subtle use of the candidate expression grammar in each direction;
6. a short critique of each direction: strongest idea, biggest risk, what should be combined or rejected;
7. a recommended direction, but **do not delete the alternatives**;
8. after I choose a direction, be ready to build an interactive prototype from that direction;
9. after convergence, extract the accepted design rules into **DESIGN.md**.

## 14. Final non-negotiables

- Preserve the canonical LEFA logo.
- Preserve the canonical companion identity.
- Black + white + gold is the current visual root.
- Companion-first, not dashboard-first.
- Heavy architecture, light interface.
- `OBSERVE → LEDGER → TIME → REVEAL` must be felt visually.
- No believable fake financial truth.
- No autonomous-trading theater.
- No generated asset becomes canonical merely because Stitch created it.
- Aesthetic ambition is encouraged aggressively, but realism contains it.
- Explore before converging.
- Mobile first.
- Make LEFA unforgettable without making LEFA noisy.

**Start by placing the uploaded companion at the center of the canvas and generate the three divergent directions around that identity.**

---

## Introduction-to-MCP Black Mask preflight

Before accepting any Stitch output, inspect:

- **Doctrine:** Does the interface preserve current LEFA product law?
- **Assets:** Did Stitch preserve rather than replace canonical identity?
- **Truth:** Did it invent financial state?
- **POC vs FOC:** Is the direction proving a usable interface idea or merely looking finished?
- **Aesthetics + Realism:** Does beauty increase comprehension while remaining evidence-bound?
- **Mobile:** Does the 390 px experience still work?
- **State semantics:** Does motion/expression map to meaning?
- **Generated assets:** Are they still candidates until accepted?
- **Unknowns:** Are unresolved ideas left as candidate/HOLD rather than silently canonized?

Return accepted visual evidence through `docs/STITCH-ACCEPTANCE-HANDOFF.md`.
