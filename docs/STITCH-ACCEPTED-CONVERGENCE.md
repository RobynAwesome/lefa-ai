# LEFA Stitch Accepted Convergence — 2026-08-30

## Decision

**ACCEPT FOR GOVERNED IMPLEMENTATION**, with explicit semantic pruning.

Human approval was given after repository audit of `RobynAwesome/Lefa-ai-google-stitch` against Issues #3 and #4 plus the merged truth-boundary work from PR #6 and the read-only receipt layer from PR #7.

The accepted result is **not** a wholesale code import. The repository accepts the visual grammar that survived truth review and rejects generated behavior that implied unproven capability.

## Accepted visual convergence

The three Stitch directions converge as follows:

1. **Direction A — Living Companion** supplies the primary mobile / human anchor. LEFA remains the optical center rather than a mascot beside a dashboard.
2. **Direction B — Living Ledger** supplies the temporal `THEN → NOW` / preserved-receipt logic underneath the companion experience.
3. **Direction C — Conversational Control Room** supplies the low-friction interaction model and inline governed evidence surfaces, but does not become a generic chatbot shell.

Canonical visible loop:

`OBSERVE → LEDGER → TIME → REVEAL`

Accepted visual language:

- obsidian black / warm white / restrained metallic gold;
- amber reserved for governed HOLD / uncertainty;
- circular / halo framing around LEFA;
- semantic motion only;
- mobile-first clarity with desktop expansion;
- kaomoji may communicate protocol state, never profit;
- heavy architecture, light interface.

## Explicitly rejected from the Stitch export

The following generated behavior is **FOC / non-canonical** and must not cross into implementation:

- hard-coded Alpaca-looking credentials;
- browser-side credential collection for this POC;
- one-second timeout pretending to verify Alpaca connectivity;
- claims such as `Alpaca Paper Sandbox Connected`, `real-time market streams`, or `Verified` without admissible runtime receipts;
- a `Live Trading` toggle;
- believable fabricated NVDA prices, volatility, liquidity, drawdown, consensus, returns, or performance metrics;
- fake cryptographic receipt identifiers / hashes presented as truth;
- claims that HOLD reduced drawdown by a numeric percentage without evidence;
- treating the generated Stitch portrait as canonical merely because it exists.

## Asset decision

The generated Stitch portrait remains **CANDIDATE / NOT ADMITTED**.

The implementation slice uses the existing governed repository companion asset at:

`assets/companion/lefa-companion-root.svg`

The root `LEFA AI Logo.png` remains canonical. No generated asset is added to `assets/manifest.json` in this slice.

## Data-binding decision

The accepted interface must bind through:

`LEFADataProvider → LEFASnapshot → snapshot_to_ui_view(...) → browser`

The presentation layer is fail-closed:

- fixture financial numbers are suppressed even if a future fixture is accidentally populated;
- stale provider evidence produces `HOLD` semantics rather than current-truth semantics;
- execution authority is explicitly `ZERO`;
- account / market / provenance labels derive from governed contracts;
- LEDGER remains empty until a real governed decision artifact exists;
- REVEAL remains waiting until evidence-backed impact exists.

## Alpaca connection decision

The Stitch connection modal is replaced by an **UNPROVEN PAPER OBSERVATION GATE**.

Current gate law:

- read-only observation only;
- no browser credential persistence;
- no simulated success;
- no order-capable route;
- live paper observation remains HOLD until Issue #2 receives admissible MCP runtime evidence.

## Implementation receipt

Branch: `feat/stitch-governed-convergence`

Initial bounded implementation adds:

- `src/lefa/presentation.py` — governed UI projection boundary;
- `src/lefa/demo_server.py` — stdlib source-checkout demo server using `FixtureProvider` only;
- `ui/index.html` — companion-first shell;
- `ui/lefa.css` — accepted black / gold visual language and responsive layout;
- `ui/lefa.js` — contract-derived UI binding;
- `ui/README.md` — truth-binding map and run instructions;
- `tests/test_presentation.py` — regression checks for fixture suppression and explicit provenance;
- `lefa-ui` console entry point.

## HOLD remains

- live Alpaca MCP runtime proof;
- order / execution authority;
- generated portrait canonization;
- Issue #5 engine architecture / SWFUS implementation.

`I_AM_STATELESS_RENTER_NOT_LANDLORD`
