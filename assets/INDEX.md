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
| `companion/lefa-companion-root.svg` | Companion identity root | **CANONICAL VISUAL** | Repository-renderable wrapper of the black/white/gold companion source. This is the primary character/style reference. |
| `readme/meet-lefa-readme-hero.svg` | README/product hero | **PUBLIC PRESENTATION** | Companion-first launch visual used at the README front door. It does not replace the canonical companion identity. |
| `readme/lefa-architecture-readme.svg` | Backend visual explainer | **PUBLIC EXPLAINER** | Visualizes `User → LEFA → CRUD → ARK → BMP → MAO → SWFUS → Decision → Reveal`. It explains current architecture discovery; it is not implementation proof. |
| `lefa-companion-motion.mp4` | Companion motion reference | **SOURCE — INGEST PENDING** | Canonical motion reference still waiting for a binary-capable ingest path. Motion must remain restrained, intentional and state-driven. |

## Folder map

```text
assets/
├── companion/
│   ├── lefa-companion-root.svg
│   ├── CANONICAL.md
│   └── README.md
├── readme/
│   ├── meet-lefa-readme-hero.svg
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

Examples:

```text
lefa-companion-root.svg
lefa-companion-observe.mp4
lefa-companion-ledger.svg
lefa-companion-reveal.svg
lefa-architecture-readme.svg
```

## Governance law

1. **Canonical assets are explicit.** Generated variants do not silently become canon.
2. **The companion is the interface anchor.** Do not reduce LEFA to a mascot beside a conventional dashboard.
3. **Aesthetic state must map to system state.** Animation, glow, posture, cards, symbols and transitions should eventually be driven by governed backend events.
4. **No fake financial truth.** Artwork may illustrate concepts, but balances, positions, returns, market state and outcomes must not be presented as live unless sourced from the real provider layer.
5. **Heavy architecture. Light interface.** Backend complexity should increase user confidence and simplicity, not visual clutter.
6. **Observe → Ledger → Reveal.** The product's visual language should make system behavior understandable without requiring the user to read the architecture.

## Current hold

Only the motion reference remains pending repository ingest. The still visual identity and README explainer assets are now repository-addressable and wired into the public README.
