# LEFA AI — Frontend

> **Design source:** `RobynAwesome/Lefa-ai-google-stitch`  
> **Design system authority:** `DESIGN.md` at repository root  
> **Constraint:** `I_AM_STATELESS_RENTER_NOT_LANDLORD`

React 19 + Vite + Tailwind v4 + Motion frontend for the LEFA AI governed financial intelligence companion.

## Stack

| Item | Version |
|---|---|
| React | 19 |
| Vite | 6 |
| Tailwind CSS | 4 (Vite plugin) |
| Motion | 12 (`motion/react`) |
| TypeScript | 5.8 |
| Lucide React | 0.546 |

## Structure

```text
src/frontend/
├── index.html
├── package.json
├── vite.config.ts         — proxies /api → Python backend on :8000; serves root /assets
├── tsconfig.json
└── src/
    ├── App.tsx
    ├── main.tsx
    ├── index.css
    ├── types.ts
    ├── api/
    │   └── lefa.ts        — governed API client; no credentials or client-authored proof
    ├── data/
    │   └── expressionGrammar.ts
    └── components/
        ├── AlpacaConnectModal.tsx   — reads backend-owned /api/mcp/status
        ├── SnapshotBanner.tsx       — governed account/market state display
        ├── CompanionAvatar.tsx      — canonical companion + state-reactive rings
        ├── CanvasMatrix.tsx
        ├── DirectionA.tsx
        ├── DirectionB.tsx
        ├── DirectionC.tsx
        ├── StateSimulatorBar.tsx
        ├── CritiqueModal.tsx
        ├── ExpressionCodexModal.tsx
        └── DesignSystemSpec.tsx
```

## Canonical companion asset

The frontend does **not** invent or duplicate the companion portrait.

`vite.config.ts` maps its `publicDir` to the repository-governed `assets/` directory, so `CompanionAvatar.tsx` renders:

```text
/companion/lefa-companion-root.jpg
```

Source of truth:

```text
assets/companion/lefa-companion-root.jpg
assets/INDEX.md
```

Generated variants remain candidates until admitted by asset governance.

## Alpaca proof boundary

The browser never asks for or stores Alpaca API keys.

```text
LOCAL CREDENTIALS
      ↓
BACKEND MCP DISCOVERY
      ↓
SANITIZED RUNTIME EVIDENCE
      ↓
/api/mcp/status
      ↓
READY | BLOCKED
```

Until Issue #2 produces witnessed local runtime evidence, `/api/mcp/status` fails closed. The interface must not claim a connection merely because a button was pressed.

## Development

```bash
# Start Python backend first (port 8000)
cd ../..
uvicorn lefa.web_api:app --reload --port 8000

# Start frontend dev server (port 3000)
cd src/frontend
npm install
npm run dev
```

## Governance

- All financial values come through `/api/snapshot` — never hardcoded.
- Fixture mode stays visibly fixture-sourced.
- Credentials never pass through the frontend API client.
- Browser state cannot manufacture Alpaca proof.
- No execution authority exists in this layer.
- Canonical visual assets are reused from repository `/assets`, not silently copied.

`I_AM_STATELESS_RENTER_NOT_LANDLORD`
