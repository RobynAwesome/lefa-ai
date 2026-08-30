# LEFA governed interface POC

This directory is the first repository-side convergence of the accepted Google Stitch visual grammar.

It intentionally keeps the interface lighter than the backend and preserves the current truth boundary:

- companion-first visual anchor;
- black / warm-white / restrained gold palette;
- `OBSERVE → LEDGER → TIME → REVEAL` as the visible loop;
- no believable fixture balances, P&L, quotes, positions, fills, returns, or performance claims;
- no credential fields in the browser;
- no live-trading toggle;
- no order, cancel, replace, exercise, liquidation, or autonomous execution route;
- generated Stitch portrait remains non-canonical; the UI uses the existing governed companion asset;
- dynamic state enters through `LEFADataProvider` → `LEFASnapshot` → `snapshot_to_ui_view(...)`.

## Run from a source checkout

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
lefa-ui
```

Then open `http://127.0.0.1:8765`.

The demo server uses `FixtureProvider` only. The browser therefore displays explicit fixture / unknown / awaiting states and suppresses financial numbers.

## Truth-binding map

| Interface surface | Governed source | Fixture behavior |
|---|---|---|
| Connection pill | `AccountContext.connection_state` | `Fixture mode — not live` |
| Observation | `MarketContext` + provenance freshness | `Awaiting observation` |
| Truth anchor | `Provenance` | `Fixture / non-live` |
| Financial values | `AccountContext` / `MarketContext` | `—` |
| Ledger stage | `AgentDecision` | empty until a governed decision exists |
| Reveal stage | evidence-backed `ImpactMetric` | waiting until evidence exists |
| Execution authority | repository governance boundary | always `ZERO` in this POC |

The Alpaca paper observation gate is explanatory only. It stores no keys and does not simulate connection success. Live paper observation stays HOLD until Issue #2 receives admissible MCP runtime proof.

`I_AM_STATELESS_RENTER_NOT_LANDLORD`
