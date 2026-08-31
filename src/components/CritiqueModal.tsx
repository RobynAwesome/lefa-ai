import React, { useState } from 'react';
import { motion } from 'motion/react';
import { X, CheckCircle, AlertTriangle, Sparkles, ArrowRight, ShieldCheck, Scale, Award } from 'lucide-react';
import { DIRECTION_CRITIQUES } from '../data/expressionGrammar';
import { DesignDirection } from '../types';

interface CritiqueModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectDirection: (dir: DesignDirection) => void;
}

export const CritiqueModal: React.FC<CritiqueModalProps> = ({
  isOpen,
  onClose,
  onSelectDirection
}) => {
  const [selectedDirectionForConvergence, setSelectedDirectionForConvergence] = useState<DesignDirection>('direction-a');

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md overflow-y-auto">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.95 }}
        className="relative w-full max-w-5xl bg-[#0e0e12] border border-[#d4af37]/40 rounded-3xl shadow-2xl overflow-hidden my-8"
      >
        {/* Modal Header */}
        <div className="p-6 border-b border-[#27272a] flex items-center justify-between bg-[#121216]">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full border border-[#d4af37] flex items-center justify-center bg-[#18181b]">
              <Scale className="w-4 h-4 text-[#e5c158]" />
            </div>
            <div>
              <h2 className="text-xl font-serif text-[#f4f4f5]">
                Divergence Critique & Convergence Matrix
              </h2>
              <p className="text-xs text-zinc-400 font-mono">
                Comparative analysis of Directions A, B, and C for LEFA AI
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 rounded-xl bg-[#18181b] text-zinc-400 hover:text-white border border-[#27272a] cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 space-y-8 max-h-[75vh] overflow-y-auto font-sans">
          
          {/* Top Recommendation Banner */}
          <div className="p-5 rounded-2xl bg-gradient-to-r from-[#d4af37]/15 via-[#18181b] to-[#121216] border border-[#d4af37]/50 space-y-2">
            <div className="flex items-center gap-2 text-xs font-mono text-[#fef08a]">
              <Award className="w-4 h-4 text-[#d4af37]" />
              <span className="font-bold tracking-wide uppercase">Convergence Recommendation for Hackathon Evaluation</span>
            </div>
            <p className="text-xs sm:text-sm text-zinc-200 leading-relaxed">
              <strong>The Unified Synthesis:</strong> Use <strong>Direction A (Living Companion)</strong> as the primary mobile anchor and visual soul of LEFA; integrate <strong>Direction B's</strong> immutable temporal receipt timeline for the ledger lock/reveal phases, and expose <strong>Direction C's</strong> natural language governance prompts as the conversational overlay.
            </p>
          </div>

          {/* 3-Direction In-Depth Critique Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {DIRECTION_CRITIQUES.map((critique) => (
              <div 
                key={critique.directionId} 
                className="p-5 rounded-2xl bg-[#121216] border border-[#27272a] flex flex-col justify-between space-y-4 hover:border-[#d4af37]/40 transition-colors"
              >
                <div className="space-y-3">
                  <div>
                    <span className="text-[10px] font-mono text-[#d4af37] uppercase tracking-wider block">
                      {critique.subtitle}
                    </span>
                    <h3 className="text-base font-serif text-zinc-100 font-medium">
                      {critique.title}
                    </h3>
                  </div>

                  <p className="text-xs text-zinc-400 italic">
                    "{critique.philosophy}"
                  </p>

                  <div className="space-y-2 pt-2 text-xs">
                    <div className="p-2.5 rounded-lg bg-[#18181b] border border-[#27272a]">
                      <span className="text-[10px] font-mono text-emerald-400 block font-semibold mb-0.5">
                        ✓ STRONGEST IDEA:
                      </span>
                      <p className="text-zinc-300 text-[11px] leading-relaxed">
                        {critique.strongestIdea}
                      </p>
                    </div>

                    <div className="p-2.5 rounded-lg bg-[#18181b] border border-[#27272a]">
                      <span className="text-[10px] font-mono text-amber-400 block font-semibold mb-0.5">
                        ⚠ BIGGEST WEAKNESS:
                      </span>
                      <p className="text-zinc-300 text-[11px] leading-relaxed">
                        {critique.biggestWeakness}
                      </p>
                    </div>
                  </div>

                  {/* Criteria Scores */}
                  <div className="space-y-1.5 pt-2 border-t border-[#27272a] text-[11px] font-mono">
                    <div className="flex justify-between text-zinc-400">
                      <span>Human Warmth</span>
                      <span className="text-[#e5c158]">{critique.scoreCard.humanWarmth}%</span>
                    </div>
                    <div className="flex justify-between text-zinc-400">
                      <span>Governance Clarity</span>
                      <span className="text-[#e5c158]">{critique.scoreCard.governanceClarity}%</span>
                    </div>
                    <div className="flex justify-between text-zinc-400">
                      <span>Mobile Efficiency</span>
                      <span className="text-[#e5c158]">{critique.scoreCard.mobileEfficiency}%</span>
                    </div>
                    <div className="flex justify-between text-zinc-400">
                      <span>Temporal Truth</span>
                      <span className="text-[#e5c158]">{critique.scoreCard.temporalContinuity}%</span>
                    </div>
                  </div>
                </div>

                <div className="pt-2 border-t border-[#27272a]">
                  <div className="text-[10px] font-mono text-zinc-500 mb-2">
                    Verdict: {critique.recommendation}
                  </div>
                  <button
                    onClick={() => {
                      onSelectDirection(critique.directionId);
                      onClose();
                    }}
                    className="w-full py-2 rounded-xl bg-[#18181b] border border-[#d4af37]/50 hover:bg-[#d4af37]/20 text-[#fef08a] font-mono text-xs font-semibold cursor-pointer transition-colors"
                  >
                    Explore {critique.title.split(':')[0]} →
                  </button>
                </div>
              </div>
            ))}
          </div>

          {/* Convergence Decision Framework */}
          <div className="p-5 rounded-2xl bg-[#14120e] border border-[#27272a] space-y-3 font-mono text-xs">
            <h4 className="text-sm font-serif text-[#f4f4f5]">Non-Negotiable Principles That Survive Convergence:</h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-[11px] text-zinc-300">
              <div className="p-2 rounded bg-[#18181b] border border-[#27272a] flex items-start gap-2">
                <CheckCircle className="w-3.5 h-3.5 text-[#e5c158] shrink-0 mt-0.5" />
                <span><strong>No Fake Financial Truth:</strong> Disconnected states remain strictly unpopulated; zero fake balances.</span>
              </div>
              <div className="p-2 rounded bg-[#18181b] border border-[#27272a] flex items-start gap-2">
                <CheckCircle className="w-3.5 h-3.5 text-[#e5c158] shrink-0 mt-0.5" />
                <span><strong>HOLD is Intelligence:</strong> Pausing is framed as mathematical vigilance, never system error.</span>
              </div>
              <div className="p-2 rounded bg-[#18181b] border border-[#27272a] flex items-start gap-2">
                <CheckCircle className="w-3.5 h-3.5 text-[#e5c158] shrink-0 mt-0.5" />
                <span><strong>Observe → Ledger → Reveal:</strong> Immutable receipts must freeze what was known at T₀.</span>
              </div>
              <div className="p-2 rounded bg-[#18181b] border border-[#27272a] flex items-start gap-2">
                <CheckCircle className="w-3.5 h-3.5 text-[#e5c158] shrink-0 mt-0.5" />
                <span><strong>Canonical Identity:</strong> Black + Warm White + Restrained Metallic Gold halo framing preserved.</span>
              </div>
            </div>
          </div>

        </div>

        {/* Footer */}
        <div className="p-4 border-t border-[#27272a] bg-[#121216] flex items-center justify-between text-xs font-mono">
          <span className="text-zinc-500">Built in South Africa • Alpaca AI Trading Agents Hackathon</span>
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-[#d4af37] text-black font-semibold hover:bg-[#e5c158] cursor-pointer"
          >
            Done Reviewing
          </button>
        </div>

      </motion.div>
    </div>
  );
};
