import React, { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Shield, Lock, Eye, Compass, ArrowRight, CheckCircle2, AlertTriangle, Clock, RefreshCw, Key, ExternalLink } from 'lucide-react';
import { SystemState, ViewportMode } from '../types';
import { CompanionAvatar } from './CompanionAvatar';
import { MOCK_OBSERVATION, MOCK_LEDGER_RECEIPT, MOCK_HOLD_RATIONALE, MOCK_REVEAL_DATA } from '../data/expressionGrammar';

interface DirectionAProps {
  state: SystemState;
  onStateChange: (state: SystemState) => void;
  viewportMode: ViewportMode;
  onOpenConnectModal: () => void;
  isAlpacaConnected: boolean;
  reducedMotion: boolean;
}

export const DirectionA: React.FC<DirectionAProps> = ({
  state,
  onStateChange,
  viewportMode,
  onOpenConnectModal,
  isAlpacaConnected,
  reducedMotion
}) => {
  const [activeContextSurface, setActiveContextSurface] = useState<'evidence' | 'receipt' | 'thesis' | null>(null);

  return (
    <div 
      className={`relative w-full min-h-[680px] bg-[#0c0c0f] text-[#f4f4f5] font-sans flex flex-col justify-between overflow-hidden rounded-2xl border border-[#27272a] shadow-2xl ${
        viewportMode === 'mobile' ? 'max-w-[390px] mx-auto' : 'w-full'
      }`}
      id="direction-a-surface"
    >
      {/* Background Subtle Radial Atmosphere */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-b from-[#d4af37]/10 via-[#c5a059]/5 to-transparent rounded-full blur-3xl pointer-events-none" />
      
      {/* Subtle Geometric Framing Grid */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#18181b_1px,transparent_1px),linear-gradient(to_bottom,#18181b_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_40%,#000_70%,transparent_100%)] opacity-30 pointer-events-none" />

      {/* Top Header: Governed Status Bar */}
      <header className="relative z-10 px-6 pt-5 pb-3 flex items-center justify-between border-b border-[#27272a]/60 bg-[#0c0c0f]/80 backdrop-blur-md">
        <div className="flex items-center gap-2.5">
          <div className="w-6 h-6 rounded-full border border-[#d4af37]/60 flex items-center justify-center bg-[#121216]">
            <span className="w-2 h-2 rounded-full bg-[#d4af37]" />
          </div>
          <div>
            <span className="text-xs font-semibold tracking-wider font-mono text-[#e5c158] uppercase">LEFA AI</span>
            <span className="text-[10px] text-zinc-500 block leading-tight">Living Companion</span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {/* Connection Status Pill */}
          <button 
            onClick={onOpenConnectModal}
            className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-[#18181b] border border-[#27272a] hover:border-[#d4af37]/50 transition-colors text-[11px] font-mono text-zinc-300"
          >
            <span className={`w-1.5 h-1.5 rounded-full ${isAlpacaConnected ? 'bg-[#e5c158]' : 'bg-zinc-500'}`} />
            <span>{isAlpacaConnected ? 'Alpaca Synced' : 'Not Connected'}</span>
          </button>
        </div>
      </header>

      {/* Main Core Surface: LEFA Living Companion at Visual Center */}
      <main className="relative z-10 flex-1 flex flex-col items-center justify-center px-6 py-6">
        
        {/* State Banner Pill */}
        <div className="mb-4">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-mono tracking-wide bg-[#18181b]/80 border border-[#3f3f46] text-zinc-300">
            {state === 'disconnected' && 'Mode: Disconnected / Awaiting Key'}
            {state === 'observing' && 'Mode: Passive Telemetry Sensing'}
            {state === 'ledgered' && 'Mode: Immutable Thesis Preserved'}
            {state === 'hold' && 'Mode: Governed Uncertainty (HOLD)'}
            {state === 'reveal' && 'Mode: Retrospective Truth Reveal'}
          </span>
        </div>

        {/* The Central Companion Visual Centerpiece */}
        <div className="my-2 relative">
          <CompanionAvatar 
            state={state} 
            size={viewportMode === 'mobile' ? 'lg' : 'xl'} 
            reducedMotion={reducedMotion}
          />
        </div>

        {/* Dynamic Contextual Surfaces that Blossom Around LEFA */}
        <div className="w-full max-w-md mt-4">
          <AnimatePresence mode="wait">
            
            {/* STATE 1: DISCONNECTED / FIRST USE */}
            {state === 'disconnected' && (
              <motion.div
                key="disconnected"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="text-center space-y-4"
              >
                <div className="space-y-1.5">
                  <h1 className="text-xl sm:text-2xl font-serif text-[#f4f4f5] tracking-wide font-normal">
                    Meet LEFA
                  </h1>
                  <p className="text-xs sm:text-sm text-zinc-400 font-light max-w-xs mx-auto leading-relaxed">
                    Your companion for governed financial intelligence.
                  </p>
                </div>

                <div className="p-3.5 rounded-xl bg-[#121216] border border-[#27272a] text-left space-y-2 text-xs">
                  <div className="flex justify-between text-zinc-400 font-mono text-[11px]">
                    <span>Current Status</span>
                    <span className="text-zinc-500">Awaiting observation</span>
                  </div>
                  <div className="flex justify-between text-zinc-400 font-mono text-[11px]">
                    <span>Truth Anchor</span>
                    <span className="text-zinc-500">—</span>
                  </div>
                  <div className="flex justify-between text-zinc-400 font-mono text-[11px]">
                    <span>Execution Authority</span>
                    <span className="text-[#e5c158]">Zero (Observation Only)</span>
                  </div>
                </div>

                <div className="pt-1">
                  <button
                    onClick={onOpenConnectModal}
                    className="w-full py-3 px-5 rounded-xl bg-gradient-to-r from-[#d4af37] via-[#e5c158] to-[#c5a059] text-black font-semibold text-xs sm:text-sm tracking-wide shadow-lg shadow-[#d4af37]/20 hover:brightness-110 active:scale-[0.98] transition-all flex items-center justify-center gap-2 cursor-pointer"
                  >
                    <Key className="w-4 h-4 text-black" />
                    <span>Connect Alpaca Paper Account</span>
                    <ArrowRight className="w-4 h-4 text-black" />
                  </button>
                  <p className="text-[10px] text-zinc-500 mt-2 font-mono">
                    Alpaca AI Trading Agents Hackathon • Built in South Africa
                  </p>
                </div>
              </motion.div>
            )}

            {/* STATE 2: OBSERVING */}
            {state === 'observing' && (
              <motion.div
                key="observing"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="space-y-3"
              >
                <div className="p-4 rounded-xl bg-[#121216]/90 border border-[#d4af37]/30 backdrop-blur-md space-y-3">
                  <div className="flex items-center justify-between border-b border-[#27272a] pb-2">
                    <div className="flex items-center gap-2">
                      <Eye className="w-4 h-4 text-[#e5c158] animate-pulse" />
                      <span className="text-xs font-semibold font-mono text-[#e5c158]">
                        Active Perception Matrix
                      </span>
                    </div>
                    <span className="text-[10px] font-mono text-zinc-400">
                      {MOCK_OBSERVATION.symbol}
                    </span>
                  </div>

                  <p className="text-xs text-zinc-300 leading-relaxed">
                    {MOCK_OBSERVATION.thesisSummary}
                  </p>

                  <div className="grid grid-cols-2 gap-2 pt-1">
                    {MOCK_OBSERVATION.sensedSignals.map((signal, idx) => (
                      <div key={idx} className="p-2 rounded-lg bg-[#18181b] border border-[#27272a] text-[11px]">
                        <span className="text-[10px] text-zinc-500 block truncate">{signal.label}</span>
                        <span className="font-mono text-zinc-200 font-medium truncate block">{signal.value}</span>
                      </div>
                    ))}
                  </div>

                  <div className="pt-1 flex items-center justify-between text-[10px] font-mono text-zinc-500">
                    <span>* Observation never implies trade authority</span>
                    <button 
                      onClick={() => onStateChange('ledgered')}
                      className="text-[#e5c158] hover:underline cursor-pointer flex items-center gap-1"
                    >
                      Preserve thesis <ArrowRight className="w-3 h-3" />
                    </button>
                  </div>
                </div>
              </motion.div>
            )}

            {/* STATE 3: LEDGERED */}
            {state === 'ledgered' && (
              <motion.div
                key="ledgered"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="space-y-3"
              >
                <div className="p-4 rounded-xl bg-[#121216]/95 border border-[#e5c158]/40 shadow-[0_4px_20px_rgba(212,175,55,0.15)] space-y-3">
                  <div className="flex items-center justify-between border-b border-[#27272a] pb-2">
                    <div className="flex items-center gap-2">
                      <Lock className="w-4 h-4 text-[#e5c158]" />
                      <span className="text-xs font-semibold font-mono text-[#e5c158]">
                        Cryptographic Receipt Locked
                      </span>
                    </div>
                    <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-[#e5c158]/10 text-[#e5c158] border border-[#e5c158]/30">
                      IMMUTABLE
                    </span>
                  </div>

                  <div className="p-2.5 rounded bg-[#09090b] border border-[#27272a] space-y-1 font-mono text-[11px]">
                    <div className="flex justify-between text-zinc-400">
                      <span>Receipt ID:</span>
                      <span className="text-zinc-200">{MOCK_LEDGER_RECEIPT.receiptId}</span>
                    </div>
                    <div className="flex justify-between text-zinc-400">
                      <span>SHA-256 Hash:</span>
                      <span className="text-[#e5c158] truncate max-w-[170px]">{MOCK_LEDGER_RECEIPT.hash}</span>
                    </div>
                  </div>

                  <p className="text-xs text-zinc-300 italic border-l-2 border-[#d4af37] pl-2.5 py-0.5">
                    "{MOCK_LEDGER_RECEIPT.observedThesis}"
                  </p>

                  <div className="text-[10px] font-mono text-zinc-400 flex items-center justify-between pt-1">
                    <span>Drawdown Cap: {MOCK_LEDGER_RECEIPT.riskParameters.maxDrawdownCap}</span>
                    <button 
                      onClick={() => onStateChange('hold')}
                      className="text-[#e5c158] hover:underline cursor-pointer"
                    >
                      Simulate market shift →
                    </button>
                  </div>
                </div>
              </motion.div>
            )}

            {/* STATE 4: HOLD / GOVERNED UNCERTAINTY */}
            {state === 'hold' && (
              <motion.div
                key="hold"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="space-y-3"
              >
                <div className="p-4 rounded-xl bg-[#14120e] border border-[#d97706]/40 space-y-3 shadow-lg">
                  <div className="flex items-center justify-between border-b border-[#27272a] pb-2">
                    <div className="flex items-center gap-2">
                      <Shield className="w-4 h-4 text-[#fbbf24]" />
                      <span className="text-xs font-semibold font-mono text-[#fbbf24]">
                        Governed Restraint (HOLD)
                      </span>
                    </div>
                    <span className="text-[10px] font-mono text-[#fbbf24] bg-[#fbbf24]/10 px-2 py-0.5 rounded border border-[#fbbf24]/30">
                      Uncertainty: {MOCK_HOLD_RATIONALE.uncertaintyScore}%
                    </span>
                  </div>

                  <p className="text-xs text-zinc-300">
                    {MOCK_HOLD_RATIONALE.reason}
                  </p>

                  <div className="p-2.5 rounded bg-[#0c0c0f] border border-[#27272a] space-y-1 text-[11px] text-zinc-400">
                    <span className="text-[10px] font-mono text-zinc-500 uppercase block">Catalysts for Hold:</span>
                    {MOCK_HOLD_RATIONALE.triggers.slice(0, 2).map((t, idx) => (
                      <div key={idx} className="flex items-start gap-1.5">
                        <span className="text-[#fbbf24]">•</span>
                        <span>{t}</span>
                      </div>
                    ))}
                  </div>

                  <div className="flex items-center justify-between text-[10px] font-mono text-zinc-400 pt-1">
                    <span className="text-amber-200/80">HOLD is intelligence, not failure.</span>
                    <button 
                      onClick={() => onStateChange('reveal')}
                      className="text-[#fbbf24] hover:underline cursor-pointer"
                    >
                      Fast-forward to Reveal →
                    </button>
                  </div>
                </div>
              </motion.div>
            )}

            {/* STATE 5: REVEAL */}
            {state === 'reveal' && (
              <motion.div
                key="reveal"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="space-y-3"
              >
                <div className="p-4 rounded-xl bg-[#121216] border border-[#fef08a]/40 space-y-3 shadow-xl">
                  <div className="flex items-center justify-between border-b border-[#27272a] pb-2">
                    <div className="flex items-center gap-2">
                      <Clock className="w-4 h-4 text-[#fef08a]" />
                      <span className="text-xs font-semibold font-mono text-[#fef08a]">
                        Temporal Truth Comparison
                      </span>
                    </div>
                    <span className="text-[10px] font-mono text-zinc-400">THEN vs NOW</span>
                  </div>

                  <div className="space-y-2 text-xs">
                    <div className="p-2 rounded bg-[#18181b] border border-[#27272a]">
                      <span className="text-[10px] text-zinc-500 font-mono block">THEN (Preserved Thesis)</span>
                      <p className="text-zinc-300 text-[11px]">{MOCK_REVEAL_DATA.projectedTrajectory}</p>
                    </div>

                    <div className="p-2 rounded bg-[#18181b] border border-[#27272a]">
                      <span className="text-[10px] text-zinc-500 font-mono block">NOW (Realized Market Path)</span>
                      <p className="text-zinc-300 text-[11px]">{MOCK_REVEAL_DATA.realizedMarketTrajectory}</p>
                    </div>
                  </div>

                  <p className="text-xs text-amber-100/90 italic bg-[#d4af37]/10 p-2 rounded border border-[#d4af37]/20">
                    "{MOCK_REVEAL_DATA.companionReflection}"
                  </p>

                  <div className="pt-1 flex items-center justify-between text-[10px] font-mono text-zinc-500">
                    <span>Immutable truth recorded</span>
                    <button 
                      onClick={() => onStateChange('observing')}
                      className="text-[#e5c158] hover:underline cursor-pointer flex items-center gap-1"
                    >
                      New Cycle <RefreshCw className="w-3 h-3" />
                    </button>
                  </div>
                </div>
              </motion.div>
            )}

          </AnimatePresence>
        </div>
      </main>

      {/* Footer: Provenance & Restrained Navigation */}
      <footer className="relative z-10 px-6 py-4 border-t border-[#27272a]/60 bg-[#0c0c0f]/90 flex flex-col sm:flex-row items-center justify-between gap-2 text-[11px] text-zinc-500 font-mono">
        <div className="flex items-center gap-2">
          <span>Observe</span>
          <span className="text-[#d4af37]">→</span>
          <span>Ledger</span>
          <span className="text-[#d4af37]">→</span>
          <span>Reveal</span>
        </div>
        <div className="text-zinc-600 text-[10px]">
          Transfer capability home.
        </div>
      </footer>
    </div>
  );
};
