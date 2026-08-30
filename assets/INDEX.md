# LEFA AI — Visual Asset Registry

This folder is the governed registry for the visual identity of **LEFA AI**.

> **LEFA's interface may evolve. LEFA's identity must remain recognizable.**

## Canonical visual language

LEFA is introduced to the user as a **companion**, not as a finance dashboard.

The visual language is anchored in:

- black;
- white;
- gold;
- a calm human companion;
- black hat;
- black clothing with gold geometric detail;
- circular / halo framing;
- simple silhouette before UI complexity;
- motion that represents real system state rather than decoration.

## Asset registry

| Asset | Role | State | Notes |
|---|---|---|---|
| `../LEFA AI Logo.png` | Product logo | **CANONICAL** | Existing repository logo. Do not silently replace. |
| `companion/lefa-companion-root.svg` | Companion identity root | **CANONICAL VISUAL** | Self-contained SVG. Primary companion/style reference for public surfaces. |
| `readme/meet-lefa-readme-hero.svg` | README hero | **PUBLIC PRESENTATION** | Animated full-width product introduction. |
| `readme/lefa-observe-ledger-reveal.svg` | Product behavior visual | **PUBLIC EXPLAINER** | Animated Observe → Ledger → Time → Reveal timeline. |
| `readme/lefa-control-room.svg` | Backend control-room visual | **PUBLIC EXPLAINER** | Animated Human → LEFA → CRUD → ARK → BMP → SWFUS route. |
| `readme/lefa-swfus-ecosystem.svg` | Agent ecosystem visual | **PUBLIC EXPLAINER** | Animated five-agent / five-ecosystem topology around LEFA. |
| `readme/lefa-architecture-readme.svg` | Legacy architecture visual | **REFERENCE** | Earlier architecture explainer retained as a reference asset; the current README uses the newer animated control-room and SWFUS visuals. |
| `lefa-companion-motion.mp4` | Companion motion reference | **SOURCE — INGEST PENDING** | Canonical motion reference still waiting for a binary-capable ingest path. |

## Folder map

```text
assets/
├── companion/
│   ├── lefa-companion-root.svg
│   ├── CANONICAL.md
│   └── README.md
├── readme/
│   ├── meet-lefa-readme-hero.svg
│   ├── lefa-observe-ledger-reveal.svg
│   ├── lefa-control-room.svg
│   ├── lefa-swfus-ecosystem.svg
│   ├── lefa-architecture-readme.svg
│   └── README.md
├── INDEX.md
└── README.md
```

## Naming law

Use lowercase kebab-case for visual assets:

```text
lefa-[subject]-[purpose].[ext]
```

## Governance law

1. **Canonical assets are explicit.** Generated variants do not silently become canon.
2. **The companion is the interface anchor.** Do not reduce LEFA to a mascot beside a conventional dashboard.
3. **Aesthetic state must map to system state.** Animation, glow, posture, cards, symbols and transitions should eventually be driven by governed backend events.
4. **No fake financial truth.** Artwork may illustrate concepts, but balances, positions, returns, market state and outcomes must not be presented as live unless sourced from the real provider layer.
5. **Heavy architecture. Light interface.** Backend complexity should increase user confidence and simplicity, not visual clutter.
6. **Observe → Ledger → Reveal.** The product's visual language should make system behavior understandable without requiring the user to read the architecture.
7. **README assets must be GitHub-renderable.** Prefer self-contained SVG primitives and `./assets/...` relative paths. Do not depend on embedded base64 raster payloads inside SVG wrappers.

## Current hold

Only the motion reference remains pending repository ingest. The still companion identity and the public animated README explainer surfaces are repository-addressable and wired into the README.
