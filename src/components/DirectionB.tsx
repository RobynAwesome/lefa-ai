import React, { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Clock, ShieldCheck, History, GitCommit, FileText, Check, ChevronRight, Lock, Key, ArrowUpRight } from 'lucide-react';
import { SystemState, ViewportMode } from '../types';
import { CompanionAvatar } from './CompanionAvatar';
import { MOCK_OBSERVATION, MOCK_LEDGER_RECEIPT, MOCK_HOLD_RATIONALE, MOCK_REVEAL_DATA } from '../data/expressionGrammar';

interface DirectionBProps {
  state: SystemState;
  onStateChange: (state: SystemState) => void;
  viewportMode: ViewportMode;
  onOpenConnectModal: () => void;
  isAlpacaConnected: boolean;
  reducedMotion: boolean;
}

export const DirectionB: React.FC<DirectionBProps> = ({
  state,
  onStateChange,
  viewportMode,
  onOpenConnectModal,
  isAlpacaConnected,
  reducedMotion
}) => {
  const [selectedTimelineNode, setSelectedTimelineNode] = useState<'observe' | 'ledger' | 'hold' | 'reveal'>('ledger');

  const timelineSteps = [
    { id: 'observe', label: 'T₀ Observe', time: '14:30:00', state: 'observing' as SystemState },
    { id: 'ledger', label: 'T₁ Ledger Lock', time: '14:32:15', state: 'ledgered' as SystemState },
    { id: 'hold', label: 'T₂ Governed Hold', time: '14:35:00', state: 'hold' as SystemState },
    { id: 'reveal', label: 'T₃ Truth Reveal', time: '16:00:00', state: 'reveal' as SystemState },
  ];

  return (
    <div 
      className={`relative w-full min-h-[680px] bg-[#0a0a0d] text-[#f4f4f5] font-sans flex flex-col justify-between overflow-hidden rounded-2xl border border-[#27272a] shadow-2xl ${
        viewportMode === 'mobile' ? 'max-w-[390px] mx-auto' : 'w-full'
      }`}
      id="direction-b-surface"
    >
      {/* Background Architectural Grid Lines */}
      <div className="absolute inset-0 bg-[linear-gradient(to_bottom,rgba(212,175,55,0.03)_1px,transparent_1px)] bg-[size:100%_2rem] pointer-events-none" />

      {/* Top Header: Temporal Bar */}
      <header className="relative z-10 px-6 pt-5 pb-3 flex items-center justify-between border-b border-[#27272a]/60 bg-[#0a0a0d]/90 backdrop-blur-md">
        <div className="flex items-center gap-2.5">
          <div className="w-6 h-6 rounded-full border border-[#d4af37]/60 flex items-center justify-center bg-[#121216]">
            <History className="w-3.5 h-3.5 text-[#e5c158]" />
          </div>
          <div>
            <span className="text-xs font-semibold tracking-wider font-mono text-[#e5c158] uppercase">LEFA AI</span>
            <span className="text-[10px] text-zinc-500 block leading-tight">Living Ledger</span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button 
            onClick={onOpenConnectModal}
            className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-[#18181b] border border-[#27272a] hover:border-[#d4af37]/50 transition-colors text-[11px] font-mono text-zinc-300 cursor-pointer"
          >
            <span className={`w-1.5 h-1.5 rounded-full ${isAlpacaConnected ? 'bg-[#e5c158]' : 'bg-zinc-500'}`} />
            <span>{isAlpacaConnected ? 'Ledger Synced' : 'Awaiting Connection'}</span>
          </button>
        </div>
      </header>

      {/* Main Surface: Temporal Spine with Companion Sentinel */}
      <main className="relative z-10 flex-1 flex flex-col items-center px-6 py-4">
        
        {/* Temporal Navigation Rail */}
        <div className="w-full max-w-lg mb-4">
          <div className="p-1.5 rounded-xl bg-[#121216] border border-[#27272a] flex items-center justify-between font-mono text-[10px]">
            {timelineSteps.map((step) => {
              const isCurrent = state === step.state;
              return (
                <button
                  key={step.id}
                  onClick={() => onStateChange(step.state)}
                  className={`flex-1 py-1.5 px-2 rounded-lg transition-all text-center cursor-pointer ${
                    isCurrent 
                      ? 'bg-[#e5c158]/15 border border-[#e5c158]/50 text-[#fef08a] font-bold shadow-sm' 
                      : 'text-zinc-400 hover:text-zinc-200'
                  }`}
                >
                  <div className="truncate">{step.label}</div>
                  <div className="text-[9px] text-zinc-500 font-normal">{step.time}</div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Companion & Temporal Axis in Harmonious Split */}
        <div className={`w-full max-w-2xl flex flex-col ${viewportMode === 'desktop' ? 'md:flex-row items-center gap-8 my-auto' : 'items-center gap-4'}`}>
          
          {/* Companion Sentinel in Direction B */}
          <div className="flex-shrink-0 flex flex-col items-center">
            <CompanionAvatar 
              state={state} 
              size={viewportMode === 'mobile' ? 'md' : 'lg'} 
              reducedMotion={reducedMotion}
            />
            <div className="text-center mt-2">
              <span className="text-[11px] font-serif text-zinc-300">Guardian of Preserved Truth</span>
            </div>
          </div>

          {/* Temporal Ledger Card / Narrative Surface */}
          <div className="flex-1 w-full">
            <AnimatePresence mode="wait">
              
              {/* STATE 1: DISCONNECTED */}
              {state === 'disconnected' && (
                <motion.div
                  key="disconnected-b"
                  initial={{ opacity: 0, x: 10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -10 }}
                  className="p-5 rounded-2xl bg-[#121216] border border-[#27272a] space-y-4"
                >
                  <div className="space-y-1">
                    <span className="text-[10px] font-mono text-[#d4af37] tracking-wider uppercase">Unanchored State</span>
                    <h2 className="text-lg font-serif text-[#f4f4f5]">Truth Ledger Empty</h2>
                    <p className="text-xs text-zinc-400 leading-relaxed">
                      Without an authenticated connection to Alpaca, LEFA refuses to simulate historical records or fake trading receipts.
                    </p>
                  </div>

                  <div className="p-3 rounded-xl bg-[#0a0a0d] border border-[#27272a] space-y-1.5 text-xs font-mono text-zinc-400">
                    <div className="flex justify-between">
                      <span>Ledger Chain</span>
                      <span className="text-zinc-600">UNINITIALIZED</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Genesis Block</span>
                      <span className="text-zinc-600">—</span>
                    </div>
                  </div>

                  <button
                    onClick={onOpenConnectModal}
                    className="w-full py-2.5 px-4 rounded-xl bg-[#18181b] border border-[#d4af37]/60 hover:bg-[#d4af37]/10 text-[#fef08a] font-mono text-xs font-semibold flex items-center justify-center gap-2 cursor-pointer transition-colors"
                  >
                    <Key className="w-4 h-4 text-[#e5c158]" />
                    <span>Initialize Truth Bridge</span>
                  </button>
                </motion.div>
              )}

              {/* STATE 2: OBSERVING */}
              {state === 'observing' && (
                <motion.div
                  key="observing-b"
                  initial={{ opacity: 0, x: 10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -10 }}
                  className="p-5 rounded-2xl bg-[#121216] border border-[#d4af37]/40 space-y-3"
                >
                  <div className="flex items-center justify-between border-b border-[#27272a] pb-2">
                    <span className="text-xs font-mono text-[#e5c158] font-semibold">T₀: Stream Ingestion</span>
                    <span className="text-[10px] font-mono text-zinc-400">{MOCK_OBSERVATION.timestamp}</span>
                  </div>

                  <div className="space-y-1 text-xs">
                    <span className="text-zinc-400 block text-[11px]">Active Telemetry Ingest:</span>
                    <p className="text-zinc-200 font-medium">{MOCK_OBSERVATION.symbol} — {MOCK_OBSERVATION.marketRegime}</p>
                  </div>

                  <div className="space-y-1.5 pt-1">
                    {MOCK_OBSERVATION.sensedSignals.slice(0, 2).map((sig, idx) => (
                      <div key={idx} className="flex justify-between text-[11px] font-mono p-2 rounded bg-[#18181b] border border-[#27272a]">
                        <span className="text-zinc-400">{sig.label}</span>
                        <span className="text-zinc-200">{sig.value}</span>
                      </div>
                    ))}
                  </div>

                  <div className="pt-2 flex justify-end">
                    <button
                      onClick={() => onStateChange('ledgered')}
                      className="px-3 py-1.5 rounded-lg bg-[#e5c158]/20 border border-[#e5c158]/50 text-[#fef08a] text-xs font-mono flex items-center gap-1.5 cursor-pointer hover:bg-[#e5c158]/30"
                    >
                      <span>Commit to Ledger</span>
                      <ChevronRight className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </motion.div>
              )}

              {/* STATE 3: LEDGERED */}
              {state === 'ledgered' && (
                <motion.div
                  key="ledgered-b"
                  initial={{ opacity: 0, x: 10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -10 }}
                  className="p-5 rounded-2xl bg-[#121216] border border-[#e5c158]/50 shadow-[0_0_30px_rgba(212,175,55,0.12)] space-y-3"
                >
                  <div className="flex items-center justify-between border-b border-[#27272a] pb-2">
                    <div className="flex items-center gap-1.5">
                      <Lock className="w-3.5 h-3.5 text-[#e5c158]" />
                      <span className="text-xs font-mono text-[#e5c158] font-bold">T₁: Preserved Receipt Block</span>
                    </div>
                    <span className="text-[10px] font-mono bg-emerald-950/40 text-amber-200 border border-amber-500/30 px-2 py-0.5 rounded">
                      SEALED
                    </span>
                  </div>

                  <p className="text-xs text-zinc-300 leading-relaxed font-serif italic">
                    "{MOCK_LEDGER_RECEIPT.observedThesis}"
                  </p>

                  <div className="p-3 rounded-lg bg-[#09090b] border border-[#27272a] space-y-1 text-[11px] font-mono">
                    <div className="flex justify-between text-zinc-400">
                      <span>Hash Proof:</span>
                      <span className="text-[#e5c158]">{MOCK_LEDGER_RECEIPT.hash}</span>
                    </div>
                    <div className="flex justify-between text-zinc-400">
                      <span>Risk Gate:</span>
                      <span className="text-zinc-300">{MOCK_LEDGER_RECEIPT.riskParameters.volatilityGate}</span>
                    </div>
                  </div>

                  <div className="text-[10px] text-zinc-400 italic">
                    * Future price action cannot alter what was verified at this timestamp.
                  </div>
                </motion.div>
              )}

              {/* STATE 4: HOLD */}
              {state === 'hold' && (
                <motion.div
                  key="hold-b"
                  initial={{ opacity: 0, x: 10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -10 }}
                  className="p-5 rounded-2xl bg-[#14120e] border border-[#d97706]/50 space-y-3"
                >
                  <div className="flex items-center justify-between border-b border-[#27272a] pb-2">
                    <span className="text-xs font-mono text-[#fbbf24] font-bold">T₂: Governed Restraint</span>
                    <span className="text-[10px] font-mono text-[#fbbf24]">HOLD ACTIVE</span>
                  </div>

                  <p className="text-xs text-zinc-300">
                    {MOCK_HOLD_RATIONALE.reason}
                  </p>

                  <div className="p-3 rounded-lg bg-[#0c0c0f] border border-[#27272a] space-y-1.5 text-xs">
                    <span className="text-[10px] font-mono text-zinc-500 uppercase block">Execution Gate Blocked:</span>
                    <p className="text-[11px] text-amber-200/90 font-mono">
                      {MOCK_HOLD_RATIONALE.companionThought}
                    </p>
                  </div>

                  <div className="text-[10px] font-mono text-zinc-400 flex justify-between items-center pt-1">
                    <span>Capital Preserved: 100%</span>
                    <button
                      onClick={() => onStateChange('reveal')}
                      className="text-[#fbbf24] hover:underline cursor-pointer"
                    >
                      Audit at Reveal →
                    </button>
                  </div>
                </motion.div>
              )}

              {/* STATE 5: REVEAL */}
              {state === 'reveal' && (
                <motion.div
                  key="reveal-b"
                  initial={{ opacity: 0, x: 10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -10 }}
                  className="p-5 rounded-2xl bg-[#121216] border border-[#fef08a]/50 space-y-3"
                >
                  <div className="flex items-center justify-between border-b border-[#27272a] pb-2">
                    <span className="text-xs font-mono text-[#fef08a] font-bold">T₃: Retrospective Ledger Audit</span>
                    <span className="text-[10px] font-mono text-[#e5c158]">VERIFIED</span>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                    <div className="p-2.5 rounded bg-[#18181b] border border-[#27272a] space-y-1">
                      <span className="text-[10px] font-mono text-zinc-500 block">Original Ledger Thesis</span>
                      <p className="text-zinc-300 text-[11px]">{MOCK_REVEAL_DATA.projectedTrajectory}</p>
                    </div>
                    <div className="p-2.5 rounded bg-[#18181b] border border-[#27272a] space-y-1">
                      <span className="text-[10px] font-mono text-zinc-500 block">Subsequent Market Reality</span>
                      <p className="text-zinc-300 text-[11px]">{MOCK_REVEAL_DATA.realizedMarketTrajectory}</p>
                    </div>
                  </div>

                  <div className="p-2.5 rounded bg-[#09090b] border border-[#27272a] text-[11px] text-zinc-300">
                    <span className="text-[10px] font-mono text-[#e5c158] block mb-1">Preserved Governance Lesson:</span>
                    <ul className="list-disc list-inside space-y-0.5 text-zinc-400">
                      {MOCK_REVEAL_DATA.lessonsPreserved.slice(0, 2).map((l, i) => (
                        <li key={i}>{l}</li>
                      ))}
                    </ul>
                  </div>
                </motion.div>
              )}

            </AnimatePresence>
          </div>
        </div>
      </main>

      {/* Footer: Philosophy Statement */}
      <footer className="relative z-10 px-6 py-4 border-t border-[#27272a]/60 bg-[#0a0a0d]/95 flex items-center justify-between text-[11px] text-zinc-500 font-mono">
        <div>
          <span>The frontend tells the story. </span>
          <span className="text-zinc-300">The backend preserves the truth.</span>
        </div>
        <div className="text-[10px] text-[#d4af37]">
          Time decides what survives.
        </div>
      </footer>
    </div>
  );
};
