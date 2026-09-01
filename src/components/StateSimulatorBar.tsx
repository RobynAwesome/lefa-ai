import React from 'react';
import { Sparkles, Activity, Layers, Volume2, VolumeX, Eye, BookOpen, MessageSquare, Lock } from 'lucide-react';
import type { SystemState, ViewportMode, DesignDirection, ExperienceMode } from '../types';

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
    <header className="w-full bg-[#0a0a0e]/95 border-b border-[#d4af37]/20 px-4 sm:px-8 py-3.5 sticky top-0 z-50 backdrop-blur-xl shadow-xl font-sans text-xs">
      <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4">
        {/* Brand & Identity */}
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-[#d4af37] to-[#854d0e] flex items-center justify-center p-0.5 shadow-lg shadow-[#d4af37]/20">
            <img src="/lefa-companion-root.svg" alt="LEFA" className="w-full h-full object-contain" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-serif font-bold text-base text-zinc-100 tracking-wider">
                LEFA AI
              </span>
              <span className="text-[9px] font-mono px-2 py-0.5 rounded-full bg-[#d4af37]/15 text-[#fef08a] border border-[#d4af37]/30">
                LIVING COMPANION
              </span>
            </div>
            <span className="text-[10px] text-zinc-400 font-mono block">
              Governed Financial Intelligence
            </span>
          </div>
        </div>

        {/* Center Mode Controls */}
        <div className="flex items-center gap-1.5 p-1 rounded-2xl bg-black/60 border border-zinc-800/80">
          <button
            onClick={() => onExperienceModeChange('runtime')}
            className={`px-3.5 py-1.5 rounded-xl font-mono text-xs transition-all cursor-pointer flex items-center gap-1.5 ${
              experienceMode === 'runtime'
                ? 'bg-gradient-to-r from-[#d4af37] to-[#b48a1e] text-black font-semibold shadow-md shadow-[#d4af37]/20'
                : 'text-zinc-400 hover:text-zinc-200'
            }`}
          >
            <Activity className="w-3.5 h-3.5" />
            3D Living Room
          </button>

          <button
            onClick={() => onExperienceModeChange('design-preview')}
            className={`px-3.5 py-1.5 rounded-xl font-mono text-xs transition-all cursor-pointer flex items-center gap-1.5 ${
              experienceMode === 'design-preview'
                ? 'bg-[#d4af37]/20 border border-[#d4af37] text-[#fef08a] font-semibold'
                : 'text-zinc-400 hover:text-zinc-200'
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            Architecture Matrix
          </button>
        </div>

        {/* Right Tools & Audio/Motion Toggles */}
        <div className="flex items-center gap-2 font-mono text-xs">
          <button
            onClick={onToggleSound}
            className={`p-2 rounded-xl border transition-all cursor-pointer flex items-center gap-1.5 ${
              soundEnabled
                ? 'bg-[#d4af37]/20 border-[#d4af37]/60 text-[#fef08a]'
                : 'bg-zinc-900 border-zinc-800 text-zinc-400 hover:text-zinc-200'
            }`}
            title={soundEnabled ? 'Harmonic Chimes Active' : 'Mute Audio'}
          >
            {soundEnabled ? <Volume2 className="w-3.5 h-3.5 text-[#e5c158]" /> : <VolumeX className="w-3.5 h-3.5" />}
          </button>

          <button
            onClick={onToggleReducedMotion}
            className={`px-2.5 py-1.5 rounded-xl border transition-all cursor-pointer text-[11px] ${
              reducedMotion
                ? 'bg-zinc-800 border-zinc-700 text-zinc-300'
                : 'bg-zinc-900 border-zinc-800 text-zinc-400 hover:text-zinc-200'
            }`}
            title="Toggle 3D Orbit Motion"
          >
            {reducedMotion ? '2D Static' : '3D Orbit'}
          </button>

          <button
            onClick={onOpenCodex}
            className="px-3 py-1.5 rounded-xl bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 text-zinc-300 transition-all cursor-pointer flex items-center gap-1.5 text-[11px]"
          >
            <MessageSquare className="w-3 h-3 text-[#e5c158]" />
            <span>Expressions</span>
          </button>

          <button
            onClick={onOpenDesignDoc}
            className="px-3 py-1.5 rounded-xl bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 text-zinc-300 transition-all cursor-pointer flex items-center gap-1.5 text-[11px]"
          >
            <BookOpen className="w-3 h-3 text-[#e5c158]" />
            <span>Spec</span>
          </button>
        </div>
      </div>
    </header>
  );
};
