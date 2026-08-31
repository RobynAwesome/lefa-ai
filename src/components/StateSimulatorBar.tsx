import React from 'react';
import { Smartphone, Monitor, Columns, Eye, Lock, Shield, Clock, Unlink, Sparkles, Activity, Beaker } from 'lucide-react';
import { SystemState, ViewportMode, DesignDirection, ExperienceMode } from '../types';

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
  currentState,
  onStateChange,
  activeDirection,
  onDirectionChange,
  viewportMode,
  onViewportChange,
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

  const isPreview = experienceMode === 'design-preview';

  return (
    <div className="w-full bg-[#121216]/95 border-b border-[#27272a] px-4 py-3 sticky top-0 z-40 backdrop-blur-md shadow-md text-xs font-mono">
      <div className="max-w-7xl mx-auto space-y-2.5">
        <div className="flex flex-col xl:flex-row items-center justify-between gap-3">
          <div className="flex items-center gap-1 bg-[#09090b] p-1 rounded-xl border border-[#d4af37]/35">
            <button
              onClick={() => onExperienceModeChange('runtime')}
              className={`px-3 py-1.5 rounded-lg transition-all cursor-pointer flex items-center gap-1.5 ${
                experienceMode === 'runtime'
                  ? 'bg-[#d4af37] text-black font-semibold shadow-sm'
                  : 'text-zinc-400 hover:text-zinc-200'
              }`}
            >
              <Activity className="w-3.5 h-3.5" />
              Runtime Truth
            </button>
            <button
              onClick={() => onExperienceModeChange('design-preview')}
              className={`px-3 py-1.5 rounded-lg transition-all cursor-pointer flex items-center gap-1.5 ${
                isPreview
                  ? 'bg-[#d97706]/25 border border-[#d97706]/55 text-[#fbbf24] font-semibold'
                  : 'text-zinc-400 hover:text-zinc-200 border border-transparent'
              }`}
            >
              <Beaker className="w-3.5 h-3.5" />
              Design Preview
            </button>
          </div>

          {isPreview ? (
            <div className="flex items-center gap-1 bg-[#18181b] p-1 rounded-xl border border-[#27272a] overflow-x-auto max-w-full">
              <button
                onClick={() => onDirectionChange('canvas-matrix')}
                className={`px-3 py-1.5 rounded-lg transition-all cursor-pointer flex items-center gap-1.5 whitespace-nowrap ${
                  activeDirection === 'canvas-matrix'
                    ? 'bg-[#d4af37] text-black font-semibold shadow-sm'
                    : 'text-zinc-400 hover:text-zinc-200'
                }`}
              >
                <Columns className="w-3.5 h-3.5" />
                Matrix
              </button>
              <button
                onClick={() => onDirectionChange('direction-a')}
                className={`px-3 py-1.5 rounded-lg transition-all cursor-pointer whitespace-nowrap ${
                  activeDirection === 'direction-a'
                    ? 'bg-[#d4af37] text-black font-semibold shadow-sm'
                    : 'text-zinc-400 hover:text-zinc-200'
                }`}
              >
                Living Companion
              </button>
              <button
                onClick={() => onDirectionChange('direction-b')}
                className={`px-3 py-1.5 rounded-lg transition-all cursor-pointer whitespace-nowrap ${
                  activeDirection === 'direction-b'
                    ? 'bg-[#d4af37] text-black font-semibold shadow-sm'
                    : 'text-zinc-400 hover:text-zinc-200'
                }`}
              >
                Living Ledger
              </button>
              <button
                onClick={() => onDirectionChange('direction-c')}
                className={`px-3 py-1.5 rounded-lg transition-all cursor-pointer whitespace-nowrap ${
                  activeDirection === 'direction-c'
                    ? 'bg-[#d4af37] text-black font-semibold shadow-sm'
                    : 'text-zinc-400 hover:text-zinc-200'
                }`}
              >
                Control Room
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-2 rounded-xl border border-[#d4af37]/30 bg-[#d4af37]/5 px-3 py-2 text-[10px] text-zinc-400">
              <Lock className="h-3.5 w-3.5 text-[#e5c158]" />
              Runtime state is receipt-derived. Manual state simulation is disabled.
            </div>
          )}

          <div className="flex items-center gap-2">
            {isPreview && activeDirection !== 'canvas-matrix' && (
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

            {isPreview && (
              <>
                <button
                  onClick={onOpenCodex}
                  className="px-2.5 py-1.5 rounded-lg bg-[#18181b] border border-[#27272a] hover:border-[#d4af37]/50 text-zinc-300 hover:text-[#fef08a] transition-colors cursor-pointer flex items-center gap-1.5"
                  title="LEFA Expression Grammar Codex"
                >
                  <Sparkles className="w-3.5 h-3.5 text-[#e5c158]" />
                  <span className="hidden sm:inline">Expressions</span>
                </button>

                <button
                  onClick={onOpenCritique}
                  className="px-2.5 py-1.5 rounded-lg bg-[#18181b] border border-[#d4af37]/40 hover:bg-[#d4af37]/10 text-[#fef08a] font-semibold transition-colors cursor-pointer flex items-center gap-1.5"
                  title="Divergence Critique & Convergence Matrix"
                >
                  <span className="w-2 h-2 rounded-full bg-[#d4af37] animate-pulse" />
                  <span>Critique</span>
                </button>
              </>
            )}

            <button
              onClick={onOpenDesignDoc}
              className="px-2.5 py-1.5 rounded-lg bg-[#18181b] border border-[#27272a] hover:border-[#d4af37]/50 text-zinc-300 hover:text-zinc-100 transition-colors cursor-pointer text-[11px]"
              title="DESIGN.md System Specification"
            >
              DESIGN.md
            </button>
          </div>
        </div>

        {isPreview && (
          <div className="flex flex-col lg:flex-row items-center justify-between gap-2 rounded-xl border border-[#d97706]/35 bg-[#d97706]/5 px-2 py-2">
            <span className="px-2 text-[10px] uppercase tracking-wider text-[#fbbf24]">
              Synthetic system-state simulator
            </span>
            <div className="flex items-center gap-1 overflow-x-auto max-w-full">
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
          </div>
        )}
      </div>
    </div>
  );
};
