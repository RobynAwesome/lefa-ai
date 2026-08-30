import React from 'react';
import { motion } from 'motion/react';
import { Sparkles, ArrowRight, Smartphone, Monitor, CheckCircle, AlertTriangle } from 'lucide-react';
import { SystemState, ViewportMode, DesignDirection } from '../types';
import { DirectionA } from './DirectionA';
import { DirectionB } from './DirectionB';
import { DirectionC } from './DirectionC';
import { DIRECTION_CRITIQUES } from '../data/expressionGrammar';

interface CanvasMatrixProps {
  state: SystemState;
  onStateChange: (state: SystemState) => void;
  onSelectDirection: (dir: DesignDirection) => void;
  onOpenConnectModal: () => void;
  isAlpacaConnected: boolean;
  reducedMotion: boolean;
  onOpenCritiqueModal: () => void;
}

export const CanvasMatrix: React.FC<CanvasMatrixProps> = ({
  state,
  onStateChange,
  onSelectDirection,
  onOpenConnectModal,
  isAlpacaConnected,
  reducedMotion,
  onOpenCritiqueModal
}) => {
  return (
    <div className="w-full max-w-7xl mx-auto px-4 py-8 space-y-12">
      
      {/* Canvas Header Hero */}
      <div className="text-center space-y-3 max-w-3xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#121216] border border-[#d4af37]/40 text-xs font-mono text-[#e5c158]">
          <span className="w-2 h-2 rounded-full bg-[#d4af37]" />
          <span>Alpaca AI Trading Agents Hackathon • Canonical Multi-Direction Canvas</span>
        </div>

        <h1 className="text-3xl sm:text-4xl font-serif text-[#f4f4f5] tracking-wide font-normal">
          Three Divergent Explorations of LEFA
        </h1>

        <p className="text-xs sm:text-sm text-zinc-400 font-light leading-relaxed">
          The frontend tells the story. The backend preserves the truth. Time decides what survives.
          Explore the three core architectural directions built around the same canonical LEFA identity.
        </p>

        <div className="pt-2 flex flex-wrap items-center justify-center gap-3">
          <button
            onClick={onOpenCritiqueModal}
            className="px-4 py-2 rounded-xl bg-gradient-to-r from-[#d4af37] via-[#e5c158] to-[#c5a059] text-black font-semibold text-xs font-mono flex items-center gap-2 hover:brightness-110 cursor-pointer shadow-lg shadow-[#d4af37]/20"
          >
            <span>Review Direction Critique & Recommendation</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* 3-Column Comparative Board */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
        
        {/* DIRECTION A CARD */}
        <div className="space-y-4">
          <div className="p-4 rounded-2xl bg-[#121216] border border-[#27272a] flex items-center justify-between">
            <div>
              <span className="text-[10px] font-mono text-[#d4af37] uppercase tracking-wider block">Direction A</span>
              <h3 className="text-base font-serif text-zinc-100 font-medium">Living Companion</h3>
            </div>
            <button
              onClick={() => onSelectDirection('direction-a')}
              className="text-xs font-mono px-3 py-1.5 rounded-lg bg-[#18181b] border border-[#d4af37]/50 text-[#fef08a] hover:bg-[#d4af37]/20 transition-colors cursor-pointer"
            >
              Focus View →
            </button>
          </div>

          <div className="bg-[#09090b] p-3 rounded-2xl border border-[#27272a]/60 shadow-xl">
            <DirectionA 
              state={state} 
              onStateChange={onStateChange} 
              viewportMode="mobile" 
              onOpenConnectModal={onOpenConnectModal} 
              isAlpacaConnected={isAlpacaConnected} 
              reducedMotion={reducedMotion} 
            />
          </div>

          <div className="p-4 rounded-xl bg-[#121216] border border-[#27272a] space-y-2 text-xs">
            <div className="font-mono text-[10px] text-[#e5c158] uppercase">Strongest Idea:</div>
            <p className="text-zinc-300 text-[11px] leading-relaxed">
              {DIRECTION_CRITIQUES[0].strongestIdea}
            </p>
          </div>
        </div>

        {/* DIRECTION B CARD */}
        <div className="space-y-4">
          <div className="p-4 rounded-2xl bg-[#121216] border border-[#27272a] flex items-center justify-between">
            <div>
              <span className="text-[10px] font-mono text-[#d4af37] uppercase tracking-wider block">Direction B</span>
              <h3 className="text-base font-serif text-zinc-100 font-medium">Living Ledger</h3>
            </div>
            <button
              onClick={() => onSelectDirection('direction-b')}
              className="text-xs font-mono px-3 py-1.5 rounded-lg bg-[#18181b] border border-[#d4af37]/50 text-[#fef08a] hover:bg-[#d4af37]/20 transition-colors cursor-pointer"
            >
              Focus View →
            </button>
          </div>

          <div className="bg-[#09090b] p-3 rounded-2xl border border-[#27272a]/60 shadow-xl">
            <DirectionB 
              state={state} 
              onStateChange={onStateChange} 
              viewportMode="mobile" 
              onOpenConnectModal={onOpenConnectModal} 
              isAlpacaConnected={isAlpacaConnected} 
              reducedMotion={reducedMotion} 
            />
          </div>

          <div className="p-4 rounded-xl bg-[#121216] border border-[#27272a] space-y-2 text-xs">
            <div className="font-mono text-[10px] text-[#e5c158] uppercase">Strongest Idea:</div>
            <p className="text-zinc-300 text-[11px] leading-relaxed">
              {DIRECTION_CRITIQUES[1].strongestIdea}
            </p>
          </div>
        </div>

        {/* DIRECTION C CARD */}
        <div className="space-y-4">
          <div className="p-4 rounded-2xl bg-[#121216] border border-[#27272a] flex items-center justify-between">
            <div>
              <span className="text-[10px] font-mono text-[#d4af37] uppercase tracking-wider block">Direction C</span>
              <h3 className="text-base font-serif text-zinc-100 font-medium">Control Room</h3>
            </div>
            <button
              onClick={() => onSelectDirection('direction-c')}
              className="text-xs font-mono px-3 py-1.5 rounded-lg bg-[#18181b] border border-[#d4af37]/50 text-[#fef08a] hover:bg-[#d4af37]/20 transition-colors cursor-pointer"
            >
              Focus View →
            </button>
          </div>

          <div className="bg-[#09090b] p-3 rounded-2xl border border-[#27272a]/60 shadow-xl">
            <DirectionC 
              state={state} 
              onStateChange={onStateChange} 
              viewportMode="mobile" 
              onOpenConnectModal={onOpenConnectModal} 
              isAlpacaConnected={isAlpacaConnected} 
              reducedMotion={reducedMotion} 
            />
          </div>

          <div className="p-4 rounded-xl bg-[#121216] border border-[#27272a] space-y-2 text-xs">
            <div className="font-mono text-[10px] text-[#e5c158] uppercase">Strongest Idea:</div>
            <p className="text-zinc-300 text-[11px] leading-relaxed">
              {DIRECTION_CRITIQUES[2].strongestIdea}
            </p>
          </div>
        </div>

      </div>

      {/* Synthesis Footnote */}
      <div className="p-6 rounded-2xl bg-[#121216] border border-[#d4af37]/30 flex flex-col md:flex-row items-center justify-between gap-4 text-xs font-mono">
        <div className="space-y-1 text-center md:text-left">
          <div className="text-sm font-serif text-zinc-100">Governed Design Convergence</div>
          <p className="text-zinc-400 text-[11px]">
            No direction is discarded blindly. Select your preferred direction or review the synthesis matrix to guide the next interactive prototype stage.
          </p>
        </div>
        <button
          onClick={onOpenCritiqueModal}
          className="px-4 py-2 rounded-xl bg-[#18181b] border border-[#d4af37] text-[#fef08a] font-semibold hover:bg-[#d4af37]/20 transition-colors cursor-pointer whitespace-nowrap"
        >
          View Convergence Matrix →
        </button>
      </div>

    </div>
  );
};
