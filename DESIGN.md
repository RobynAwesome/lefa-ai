# DESIGN.md — LEFA AI Governed Design Specification

## 1. Product Identity & Core Philosophy
- **Identity**: LEFA is a human-facing governed financial intelligence companion designed for the **Alpaca AI Trading Agents Hackathon**.
- **Not a**: Generic trading dashboard, chatbot skin, mascot beside charts, crypto casino, or conventional banking application.
- **Core Loop**: **Observe → Ledger → Time → Reveal**.
- **First Principle**: *The frontend tells the story. The backend preserves the truth. Time decides what survives.*
- **Provenance**: Built in South Africa. Build globally. Transfer capability home. (Present with quiet dignity, never over-marketed).

---

## 2. Visual Language & Chromatic Tokens
The palette is rooted in **Obsidian Black + Warm White + Restrained Metallic Gold**, with subtle Amber reserved strictly for governed uncertainty (HOLD).

| Semantic Role | Token | Hex | Optical Purpose |
| :--- | :--- | :--- | :--- |
| **Canvas** | `--bg-obsidian` | `#09090B` | Deep, low-fatigue space with subtle geometric grid |
| **Surfaces** | `--surface-dark` | `#121216` | Card enclosures, modal dialogs, ledger blocks |
| **Borders** | `--border-subtle` | `#27272A` | Structural dividers (1px, 60-80% opacity) |
| **Metallic Gold** | `--gold-metallic` | `#D4AF37` | Canonical halo rings, primary actions, sensory nodes |
| **Auric Highlight** | `--gold-auric` | `#FEF08A` / `#E5C158` | Verified cryptographic hashes, active perception |
| **Governed Hold** | `--amber-hold` | `#D97706` / `#FBBF24` | Uncertainty state (HOLD is intelligence, not failure) |
| **Warm White** | `--text-warm-white` | `#F4F4F5` / `#ECEAE2` | High-contrast WCAG AA readable text |

> **Anti-Slop Prohibitions**:
> - NO emerald green dominance; NO generic fintech neon green.
> - NO purple-to-blue gradients; NO cyan glowing neon text.
> - NO fake candlestick charts or fake balances.

---

## 3. Typographic Hierarchy
| Role | Family | Fallbacks | Usage |
| :--- | :--- | :--- | :--- |
| **Display Headings** | \`Cinzel\` | \`Cormorant Garamond, Georgia, serif\` | Dignified, editorial presence |
| **Body Text** | \`Plus Jakarta Sans\` | \`Inter, sans-serif\` | Clean readability (14-16px, 1.5-1.7 line height) |
| **Telemetry & Code** | \`JetBrains Mono\` | \`Space Grotesk, monospace\` | Cryptographic hashes, receipts, timestamps |

---

## 4. Semantic Motion Signatures
Every motion maps directly to real system state:
1. **Halo Pulse (\`4s linear\`)** → Sensory intake during **OBSERVE** (no execution authority).
2. **Ring Closure & Lock Snap** → Cryptographic sealing during **LEDGER** (receipt hash generated).
3. **Orbital Arc / Dial Rotation** → Passage of **TIME** (separating THEN from NOW).
4. **Radial Bloom & Unfold** → Retrospective truth comparison during **REVEAL**.
5. **Reduced-Motion Alternatives**: Fully WCAG compliant toggle replaces animations with crisp high-contrast status borders.

---

## 5. Candidate Expression Grammar & Guardrails
Kaomoji serve as micro-interaction signatures:
- \`Observing… +_+\`: Sensory intake without authority.
- \`Preserved. (●'◡'●)\`: Cryptographic hash sealed.
- \`Need more evidence. ¬_¬\` / \`Holding this one. U_U\`: Governed uncertainty (Intelligence, not error).
- \`Something changed. O.O\`: Regime shift alert.
- \`╰(*°▽°*)╯\`: API connection verified.

> **CRITICAL GUARDRAIL**: An expression may **never** imply financial profitability unless verified by backend ledger data. Delighted expressions represent *protocol integrity*, not *stock market gains*.

---

## 6. Divergence Critique & Convergence Synthesis

### Direction A: Living Companion (Mobile-First Radial Anchor)
- **Strongest Idea**: Uncompromised emotional gravity; LEFA is the living center.
- **Biggest Weakness**: Circular constraints require pagination for dense data.
- **Surviving Element**: The central companion anchor and mobile-native layout.

### Direction B: Living Ledger (Temporal Orbit)
- **Strongest Idea**: Exceptional temporal clarity; solves the hardest problem in AI finance (distinguishing what was known THEN vs NOW).
- **Biggest Weakness**: Higher cognitive load for first-time non-technical users.
- **Surviving Element**: The immutable receipt artifact and Then-vs-Now orbital scrubber.

### Direction C: Conversational Control Room (Governed Dialogue)
- **Strongest Idea**: Zero friction for natural user inquiry with inline evidence cards.
- **Biggest Weakness**: Risk of feeling like a chatbot if evidence cards are not visibly governed.
- **Surviving Element**: Inline governed evidence cards and voice prompt flow.

---

## 7. First-Use & Truthfulness Mandate
Before Alpaca is connected, the UI displays only truthful states:
- **Status**: *Not connected*
- **Observation**: *Awaiting observation*
- **Truth Anchor**: *Unknown* / *—*
- **Execution Authority**: *Zero*
- **Balance / P&L**: Unpopulated (Never fabricated).
