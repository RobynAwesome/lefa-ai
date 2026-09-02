import React from 'react';
import { Activity, BookOpen, Layers, MessageSquare, Volume2, VolumeX } from 'lucide-react';
import type { DesignDirection, ExperienceMode, SystemState, ViewportMode } from '../types';

interface StateSimulatorBarProps {
  experienceMode: ExperienceMode;
  onExperienceModeChange: (mode: ExperienceMode) => void;
  currentState: SystemState;
  onStateChange: (state: SystemState) => void;
  activeDirection: DesignDirection;
  onDirectionChange: (dir: DesignDirection) => void;
  viewportMode: ViewportMode;
  onViewportChange: (mode: ViewportMode) => void;
  reducedMotion: boolean;
  onToggleReducedMotion: () => void;
  soundEnabled: boolean;
  onToggleSound: () => void;
  onOpenCritique: () => void;
  onOpenCodex: () => void;
  onOpenDesignDoc: () => void;
}

export const StateSimulatorBar: React.FC<StateSimulatorBarProps> = ({
  experienceMode,
  onExperienceModeChange,
  reducedMotion,
  onToggleReducedMotion,
  soundEnabled,
  onToggleSound,
  onOpenDesignDoc,
  onOpenCodex,
}) => {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-[#d4af37]/20 bg-[#0a0a0e]/95 px-4 py-3.5 text-xs shadow-xl backdrop-blur-xl sm:px-8">
      <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-gradient-to-br from-[#d4af37] to-[#854d0e] p-0.5 shadow-lg shadow-[#d4af37]/20">
            <img src="/lefa-companion-root.svg" alt="LEFA" className="h-full w-full object-contain" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-serif text-base font-bold tracking-wider text-zinc-100">LEFA AI</span>
              <span className="rounded-full border border-[#d4af37]/30 bg-[#d4af37]/15 px-2 py-0.5 text-[9px] font-medium uppercase tracking-[0.18em] text-[#fef08a]">
                Design Lab
              </span>
            </div>
            <span className="block text-[10px] text-zinc-500">Prototype controls — not live market truth</span>
          </div>
        </div>

        <div className="flex items-center gap-1.5 rounded-2xl border border-zinc-800/80 bg-black/60 p-1">
          <button
            onClick={() => onExperienceModeChange('runtime')}
            className={`flex cursor-pointer items-center gap-1.5 rounded-xl px-3.5 py-1.5 text-xs transition-all ${
              experienceMode === 'runtime'
                ? 'bg-gradient-to-r from-[#d4af37] to-[#b48a1e] font-semibold text-black shadow-md shadow-[#d4af37]/20'
                : 'text-zinc-300 hover:bg-white/[0.04] hover:text-white'
            }`}
          >
            <Activity className="h-3.5 w-3.5" />
            Back to LEFA
          </button>

          <button
            onClick={() => onExperienceModeChange('design-preview')}
            className={`flex cursor-pointer items-center gap-1.5 rounded-xl px-3.5 py-1.5 text-xs transition-all ${
              experienceMode === 'design-preview'
                ? 'border border-[#d4af37] bg-[#d4af37]/20 font-semibold text-[#fef08a]'
                : 'text-zinc-400 hover:text-zinc-200'
            }`}
          >
            <Layers className="h-3.5 w-3.5" />
            Design Lab
          </button>
        </div>

        <div className="flex items-center gap-2 text-xs">
          <button
            onClick={onToggleSound}
            className={`flex cursor-pointer items-center gap-1.5 rounded-xl border p-2 transition-all ${
              soundEnabled
                ? 'border-[#d4af37]/60 bg-[#d4af37]/20 text-[#fef08a]'
                : 'border-zinc-800 bg-zinc-900 text-zinc-400 hover:text-zinc-200'
            }`}
            title={soundEnabled ? 'Preview sound on' : 'Preview sound off'}
          >
            {soundEnabled ? (
              <Volume2 className="h-3.5 w-3.5 text-[#e5c158]" />
            ) : (
              <VolumeX className="h-3.5 w-3.5" />
            )}
          </button>

          <button
            onClick={onToggleReducedMotion}
            className={`cursor-pointer rounded-xl border px-2.5 py-1.5 text-[11px] transition-all ${
              reducedMotion
                ? 'border-zinc-700 bg-zinc-800 text-zinc-300'
                : 'border-zinc-800 bg-zinc-900 text-zinc-400 hover:text-zinc-200'
            }`}
          >
            {reducedMotion ? 'Static preview' : 'Motion preview'}
          </button>

          <button
            onClick={onOpenCodex}
            className="flex cursor-pointer items-center gap-1.5 rounded-xl border border-zinc-800 bg-zinc-900 px-3 py-1.5 text-[11px] text-zinc-300 transition-all hover:bg-zinc-800"
          >
            <MessageSquare className="h-3 w-3 text-[#e5c158]" />
            Expressions
          </button>

          <button
            onClick={onOpenDesignDoc}
            className="flex cursor-pointer items-center gap-1.5 rounded-xl border border-zinc-800 bg-zinc-900 px-3 py-1.5 text-[11px] text-zinc-300 transition-all hover:bg-zinc-800"
          >
            <BookOpen className="h-3 w-3 text-[#e5c158]" />
            Spec
          </button>
        </div>
      </div>
    </header>
  );
};
