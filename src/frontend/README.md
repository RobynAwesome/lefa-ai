# LEFA AI — Frontend

> **Design source:** `RobynAwesome/Lefa-ai-google-stitch`
> **Design system authority:** `DESIGN.md` at repository root
> **Constraint:** `I_AM_STATELESS_RENTER_NOT_LANDLORD`

React 19 + Vite + Tailwind v4 + Framer Motion frontend for the LEFA AI governed financial intelligence companion.

## Stack

| Item | Version |
|---|---|
| React | 19 |
| Vite | 6 |
| Tailwind CSS | 4 (Vite plugin) |
| Framer Motion | 12 (`motion/react`) |
| TypeScript | 5.8 |
| Lucide React | 0.546 |

## Structure

```
src/frontend/
├── index.html             — Cinzel + Plus Jakarta Sans + JetBrains Mono fonts
├── package.json
├── vite.config.ts         — proxies /api → Python backend on :8000
├── tsconfig.json
└── src/
    ├── App.tsx            — root, fetches /api/snapshot, passes to SnapshotBanner
    ├── main.tsx
    ├── index.css          — Tailwind import
    ├── types.ts           — SystemState, DesignDirection, ViewportMode, data types
    ├── api/
    │   └── lefa.ts        — governed API client (no credentials forwarded)
    ├── data/
    │   └── expressionGrammar.ts — kaomoji codex + mock fixtures
    └── components/
        ├── AlpacaConnectModal.tsx   — wired to /api/mcp/verify proof gate
        ├── SnapshotBanner.tsx       — governed account/market state display
        ├── CompanionAvatar.tsx      — LEFA portrait + state-reactive rings
        ├── CanvasMatrix.tsx         — 3-direction comparison canvas
        ├── DirectionA.tsx           — Living Companion (mobile-first radial)
        ├── DirectionB.tsx           — Living Ledger (temporal axis)
        ├── DirectionC.tsx           — Conversational Control Room
        ├── StateSimulatorBar.tsx    — top navigation + state controls
        ├── CritiqueModal.tsx        — design direction critique scores
        ├── ExpressionCodexModal.tsx — kaomoji expression codex
        └── DesignSystemSpec.tsx     — full design system documentation
```

## Companion portrait asset

`CompanionAvatar.tsx` expects:
```
src/assets/images/lefa_companion_portrait_<id>.jpg
```

Place the canonical LEFA AI portrait image here. The asset registry is governed by `assets/manifest.json` at the repository root. Generated assets are not canonical until explicitly admitted.

## Development

```bash
# Start Python backend first (port 8000)
cd ../..  && uvicorn lefa.web_api:app --reload --port 8000

# Start frontend dev server (port 3000)
cd src/frontend && npm install && npm run dev
```

## Governance

- All financial values come through `/api/snapshot` — never hardcoded.
- Fixture mode shows `—` / `null` — never invents balances.
- Credentials never pass through the API client.
- No execution authority exists in this layer.

`I_AM_STATELESS_RENTER_NOT_LANDLORD`
