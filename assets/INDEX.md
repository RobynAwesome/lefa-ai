# LEFA AI — Visual Asset Registry

This folder is the governed registry for the visual identity of **LEFA AI**.

The rule is simple:

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
| `lefa-companion-root.jpg` | Companion identity root | **CANONICAL SOURCE — BINARY INGEST PENDING** | The hand-drawn black/white/gold companion image supplied during product discovery. This is the primary character/style reference for the interface. |
| `lefa-companion-motion.mp4` | Companion motion reference | **CANONICAL SOURCE — BINARY INGEST PENDING** | Short motion reference showing how the companion should feel when alive on-screen. Motion should remain restrained, intentional and state-driven. |
| `meet-lefa-readme-hero.png` | README/product hero | **GENERATED CANDIDATE — BINARY INGEST PENDING** | Marketing-style interpretation of the canonical companion for public introduction. Must not replace the root identity without acceptance. |
| `lefa-architecture-readme.png` | Backend visual explainer | **GENERATED CANDIDATE — BINARY INGEST PENDING** | Visual explanation of `User → LEFA → CRUD → ARK → BMP → MAO → SWFUS → Decision → Reveal`. Architecture is still discovery-stage and this image is illustrative, not an implementation receipt. |

## Naming law

Use lowercase kebab-case for new visual assets:

```text
lefa-[subject]-[purpose].[ext]
```

Examples:

```text
lefa-companion-root.jpg
lefa-companion-observe.mp4
lefa-companion-ledger.png
lefa-companion-reveal.png
lefa-architecture-readme.png
```

## Governance law

1. **Canonical assets are explicit.** Generated variants do not silently become canon.
2. **The companion is the interface anchor.** Do not reduce LEFA to a mascot beside a conventional dashboard.
3. **Aesthetic state must map to system state.** Animation, glow, posture, cards, symbols and transitions should eventually be driven by governed backend events.
4. **No fake financial truth.** Artwork may illustrate concepts, but balances, positions, returns, market state and outcomes must not be presented as live unless sourced from the real provider layer.
5. **Heavy architecture. Light interface.** Backend complexity should increase user confidence and simplicity, not visual clutter.
6. **Observe → Ledger → Reveal.** The product's visual language should make the system's behavior understandable without requiring the user to read the architecture.

## Binary ingest hold

The GitHub connector available in this session can create and update UTF-8 repository files, but it cannot write raw binary image/video files. The source and generated binary assets therefore remain **pending binary ingest** rather than being falsely recorded as uploaded.

Once a binary-capable Git write surface is available, place the files at the names above and remove the pending markers in this registry.
