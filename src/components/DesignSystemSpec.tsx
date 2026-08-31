import React, { useState } from 'react';
import { motion } from 'motion/react';
import { X, Copy, Check, FileText, Palette, Type, Layers, Activity, Eye, ShieldAlert } from 'lucide-react';

interface DesignSystemSpecProps {
  isOpen: boolean;
  onClose: () => void;
}

export const DesignSystemSpec: React.FC<DesignSystemSpecProps> = ({
  isOpen,
  onClose
}) => {
  const [copied, setCopied] = useState(false);

  const designDocMarkdown = `# DESIGN.md — LEFA AI Governed Design Specification

## 1. Brand Essence & Core Philosophy
- **Identity**: Human-facing governed financial intelligence companion.
- **Core Loop**: **Observe → Ledger → Time → Reveal**.
- **First Principle**: *The frontend tells the story. The backend preserves the truth. Time decides what survives.*
- **South African Provenance**: Built in South Africa. Build globally. Transfer capability home. (Present but restrained; never a charity banner).

---

## 2. Color Palette & Chromatic Rules
| Semantic Role | Token Name | Hex Code | Purpose |
| :--- | :--- | :--- | :--- |
| Primary Canvas | \`--bg-obsidian\` | \`#09090B\` / \`#0C0C0F\` | Deep rich atmospheric canvas |
| Surface Container | \`--surface-dark\` | \`#121216\` | Structured cards & modal frames |
| Metallic Gold (Bright) | \`--gold-auric\` | \`#FEF08A\` / \`#E5C158\` | Active telemetry, verified hashes |
| Metallic Gold (Deep) | \`--gold-base\` | \`#D4AF37\` / \`#C5A059\` | Celestial halo linework & accents |
| Governed Restraint | \`--amber-hold\` | \`#D97706\` / \`#FBBF24\` | HOLD uncertainty state (Not failure) |
| Warm White Text | \`--text-warm-white\` | \`#F4F4F5\` / \`#ECEAE2\` | High contrast, calm typography |

> **Anti-Slop Color Directives**:
> - NO emerald green dominance; NO generic fintech neon green.
> - NO purple-to-blue gradients; NO cyan glowing neon text.
> - Maximum brightness difference between background & card: ≤ 7-12%.

---

## 3. Typographic Hierarchy
- **Display Headings**: \`Cinzel\` / \`Cormorant Garamond\` (Editorial, dignified, wise presence).
- **Body & Dialogue**: \`Plus Jakarta Sans\` (14-16px, 1.5-1.7 line height, max 65-75ch width).
- **Telemetry & Hashes**: \`JetBrains Mono\` / \`Space Grotesk\` (Cryptographic proofs, state tags).

---

## 4. Semantic Motion Signatures
Every animation maps strictly to verified system state:
1. **Halo Pulse (\`4s linear\`)** → Sensed sensory intake (Passive Observe).
2. **Ring Closure & Lock Snap** → Cryptographic commit to immutable ledger.
3. **Orbital Arc / Dial Rotation** → Passage of time (Then vs Now).
4. **Controlled Radial Bloom** → Retrospective truth comparison (Reveal).
5. **Reduced-Motion Support**: All animations gracefully fallback to static high-contrast borders and badge states.

---

## 5. Candidate Expression Grammar Guardrails
Kaomoji are used as micro-interaction signatures:
- \`Observing… +_+\`: Sensory intake without authority.
- \`Preserved. (●'◡'●)\`: Cryptographic hash sealed.
- \`Need more evidence. ¬_¬\` / \`Holding this one. U_U\`: Governed uncertainty (Intelligence, not error).
- \`Something changed. O.O\`: Regime shift alert.

> **CRITICAL GUARDRAIL**: An expression may **never** imply financial profitability unless verified by backend ledger data. Delighted expressions represent *protocol integrity*, not *stock market gains*.
`;

  const handleCopy = () => {
    navigator.clipboard.writeText(designDocMarkdown);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md overflow-y-auto font-sans">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.95 }}
        className="relative w-full max-w-4xl bg-[#0e0e12] border border-[#d4af37]/40 rounded-3xl shadow-2xl overflow-hidden my-8"
      >
        {/* Header */}
        <div className="p-5 border-b border-[#27272a] flex items-center justify-between bg-[#121216]">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full border border-[#d4af37] flex items-center justify-center bg-[#18181b]">
              <FileText className="w-4 h-4 text-[#e5c158]" />
            </div>
            <div>
              <h2 className="text-xl font-serif text-[#f4f4f5]">DESIGN.md Living Specification</h2>
              <p className="text-xs text-zinc-400 font-mono">Canonical tokens, rules, motion signatures & guardrails</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleCopy}
              className="px-3 py-1.5 rounded-xl bg-[#18181b] border border-[#27272a] hover:border-[#d4af37]/50 text-zinc-300 hover:text-[#fef08a] text-xs font-mono flex items-center gap-1.5 cursor-pointer"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? 'Copied' : 'Copy Spec'}</span>
            </button>

            <button
              onClick={onClose}
              className="p-1.5 rounded-xl bg-[#18181b] text-zinc-400 hover:text-white border border-[#27272a] cursor-pointer"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Content Viewer */}
        <div className="p-6 space-y-6 max-h-[70vh] overflow-y-auto font-mono text-xs text-zinc-300 bg-[#09090b]">
          
          {/* Visual Palette Preview */}
          <div className="space-y-2">
            <span className="text-[10px] uppercase text-[#d4af37] tracking-wider block">Visual Chromatic Palette</span>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
              <div className="p-3 rounded-xl bg-[#09090b] border border-[#27272a] space-y-1">
                <div className="w-full h-8 rounded-lg bg-[#09090b] border border-zinc-700" />
                <span className="text-[11px] text-zinc-300 block font-bold">Obsidian Black</span>
                <span className="text-[10px] text-zinc-500">#09090B (Canvas)</span>
              </div>
              <div className="p-3 rounded-xl bg-[#121216] border border-[#27272a] space-y-1">
                <div className="w-full h-8 rounded-lg bg-[#121216] border border-zinc-700" />
                <span className="text-[11px] text-zinc-300 block font-bold">Deep Slate</span>
                <span className="text-[10px] text-zinc-500">#121216 (Surfaces)</span>
              </div>
              <div className="p-3 rounded-xl bg-[#18181b] border border-[#27272a] space-y-1">
                <div className="w-full h-8 rounded-lg bg-[#d4af37]" />
                <span className="text-[11px] text-zinc-300 block font-bold">Metallic Gold</span>
                <span className="text-[10px] text-zinc-500">#D4AF37 (Geometry)</span>
              </div>
              <div className="p-3 rounded-xl bg-[#18181b] border border-[#27272a] space-y-1">
                <div className="w-full h-8 rounded-lg bg-[#d97706]" />
                <span className="text-[11px] text-zinc-300 block font-bold">Restraint Amber</span>
                <span className="text-[10px] text-zinc-500">#D97706 (HOLD)</span>
              </div>
            </div>
          </div>

          <div className="p-4 rounded-xl bg-[#121216] border border-[#27272a] space-y-4">
            <pre className="whitespace-pre-wrap font-mono text-[11px] text-zinc-300 leading-relaxed">
              {designDocMarkdown}
            </pre>
          </div>

        </div>

        {/* Footer */}
        <div className="p-4 border-t border-[#27272a] bg-[#121216] flex items-center justify-between text-xs font-mono">
          <span className="text-zinc-500">Extracted for Alpaca AI Trading Agents Hackathon</span>
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-[#d4af37] text-black font-semibold hover:bg-[#e5c158] cursor-pointer"
          >
            Close Document
          </button>
        </div>

      </motion.div>
    </div>
  );
};
