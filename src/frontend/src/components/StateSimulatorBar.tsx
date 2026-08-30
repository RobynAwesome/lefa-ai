import React from 'react';
import { Play, Pause, RotateCcw, Smartphone, Monitor, Columns, Eye, Lock, Shield, Clock, Unlink, Sparkles, Volume2, VolumeX } from 'lucide-react';
import { SystemState, ViewportMode, DesignDirection } from '../types';

interface StateSimulatorBarProps {
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
  currentState,
  onStateChange,
  activeDirection,
  onDirectionChange,
  viewportMode,
  onViewportChange,
  reducedMotion,
  onToggleReducedMotion,
  soundEnabled,
  onToggleSound,
  onOpenCritique,
  onOpenCodex,
  onOpenDesignDoc
}) => {
  const states: { id: SystemState; label: string; icon: React.ReactNode; kaomoji: string }[] = [
    { id: 'disconnected', label: 'Disconnected', icon: <Unlink className="w-3.5 h-3.5" />, kaomoji: 'ᓚᘏᗢ' },
    { id: 'observing', label: 'Observe', icon: <Eye className="w-3.5 h-3.5" />, kaomoji: '+_+' },
    { id: 'ledgered', label: 'Ledger', icon: <Lock className="w-3.5 h-3.5" />, kaomoji: '(●\'◡\'●)' },
    { id: 'hold', label: 'HOLD', icon: <Shield className="w-3.5 h-3.5" />, kaomoji: 'U_U' },
    { id: 'reveal', label: 'Reveal', icon: <Clock className="w-3.5 h-3.5" />, kaomoji: '(❁´◡`❁)' },
  ];

  return (
    <div className="w-full bg-[#121216]/95 border-b border-[#27272a] px-4 py-3 sticky top-0 z-40 backdrop-blur-md shadow-md text-xs font-mono">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-3">
        
        {/* Left: Direction Switcher Tabs */}
        <div className="flex items-center gap-1 bg-[#18181b] p-1 rounded-xl border border-[#27272a]">
          <button
            onClick={() => onDirectionChange('canvas-matrix')}
            className={`px-3 py-1.5 rounded-lg transition-all cursor-pointer flex items-center gap-1.5 ${
              activeDirection === 'canvas-matrix'
                ? 'bg-[#d4af37] text-black font-semibold shadow-sm'
                : 'text-zinc-400 hover:text-zinc-200'
            }`}
          >
            <Columns className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Canvas Matrix</span>
            <span className="sm:hidden">Matrix</span>
          </button>

          <button
            onClick={() => onDirectionChange('direction-a')}
            className={`px-3 py-1.5 rounded-lg transition-all cursor-pointer ${
              activeDirection === 'direction-a'
                ? 'bg-[#d4af37] text-black font-semibold shadow-sm'
                : 'text-zinc-400 hover:text-zinc-200'
            }`}
          >
            Dir A: Living Companion
          </button>

          <button
            onClick={() => onDirectionChange('direction-b')}
            className={`px-3 py-1.5 rounded-lg transition-all cursor-pointer ${
              activeDirection === 'direction-b'
                ? 'bg-[#d4af37] text-black font-semibold shadow-sm'
                : 'text-zinc-400 hover:text-zinc-200'
            }`}
          >
            Dir B: Living Ledger
          </button>

          <button
            onClick={() => onDirectionChange('direction-c')}
            className={`px-3 py-1.5 rounded-lg transition-all cursor-pointer ${
              activeDirection === 'direction-c'
                ? 'bg-[#d4af37] text-black font-semibold shadow-sm'
                : 'text-zinc-400 hover:text-zinc-200'
            }`}
          >
            Dir C: Control Room
          </button>
        </div>

        {/* Center: System State Journey Simulator */}
        <div className="flex items-center gap-1 bg-[#18181b] p-1 rounded-xl border border-[#27272a] overflow-x-auto max-w-full">
          <span className="text-[10px] text-zinc-500 px-2 font-mono uppercase tracking-wider hidden lg:inline">
            System State:
          </span>
          {states.map((s) => {
            const isActive = currentState === s.id;
            return (
              <button
                key={s.id}
                onClick={() => onStateChange(s.id)}
                className={`px-2.5 py-1 rounded-lg transition-all cursor-pointer flex items-center gap-1.5 whitespace-nowrap ${
                  isActive
                    ? 'bg-[#e5c158]/20 border border-[#e5c158]/60 text-[#fef08a] font-bold shadow-inner'
                    : 'text-zinc-400 hover:text-zinc-200 border border-transparent'
                }`}
              >
                {s.icon}
                <span>{s.label}</span>
                <span className="text-[10px] opacity-75 text-[#e5c158]">{s.kaomoji}</span>
              </button>
            );
          })}
        </div>

        {/* Right: Viewport & Exploration Modals Controls */}
        <div className="flex items-center gap-2">
          
          {/* Viewport switcher (when viewing individual direction) */}
          {activeDirection !== 'canvas-matrix' && (
            <div className="flex items-center bg-[#18181b] p-1 rounded-lg border border-[#27272a]">
              <button
                onClick={() => onViewportChange('mobile')}
                className={`p-1.5 rounded transition-colors cursor-pointer ${
                  viewportMode === 'mobile' ? 'bg-[#27272a] text-[#e5c158]' : 'text-zinc-400 hover:text-zinc-200'
                }`}
                title="Mobile (~390px)"
              >
                <Smartphone className="w-3.5 h-3.5" />
              </button>
              <button
                onClick={() => onViewportChange('desktop')}
                className={`p-1.5 rounded transition-colors cursor-pointer ${
                  viewportMode === 'desktop' ? 'bg-[#27272a] text-[#e5c158]' : 'text-zinc-400 hover:text-zinc-200'
                }`}
                title="Responsive Desktop"
              >
                <Monitor className="w-3.5 h-3.5" />
              </button>
            </div>
          )}

          {/* Expression Codex Button */}
          <button
            onClick={onOpenCodex}
            className="px-2.5 py-1.5 rounded-lg bg-[#18181b] border border-[#27272a] hover:border-[#d4af37]/50 text-zinc-300 hover:text-[#fef08a] transition-colors cursor-pointer flex items-center gap-1.5"
            title="LEFA Expression Grammar Codex"
          >
            <Sparkles className="w-3.5 h-3.5 text-[#e5c158]" />
            <span className="hidden sm:inline">Expressions</span>
          </button>

          {/* Critique & Recommendation Matrix Button */}
          <button
            onClick={onOpenCritique}
            className="px-2.5 py-1.5 rounded-lg bg-[#18181b] border border-[#d4af37]/40 hover:bg-[#d4af37]/10 text-[#fef08a] font-semibold transition-colors cursor-pointer flex items-center gap-1.5"
            title="Divergence Critique & Convergence Matrix"
          >
            <span className="w-2 h-2 rounded-full bg-[#d4af37] animate-pulse" />
            <span>Critique Matrix</span>
          </button>

          {/* DESIGN.md Specification Viewer */}
          <button
            onClick={onOpenDesignDoc}
            className="px-2.5 py-1.5 rounded-lg bg-[#18181b] border border-[#27272a] hover:border-[#d4af37]/50 text-zinc-300 hover:text-zinc-100 transition-colors cursor-pointer text-[11px]"
            title="DESIGN.md System Specification"
          >
            DESIGN.md
          </button>
        </div>

      </div>
    </div>
  );
};
