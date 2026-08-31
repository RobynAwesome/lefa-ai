import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import {
  Shield,
  Activity,
  Lock,
  Sparkles,
  Zap,
  Volume2,
  CheckCircle2,
  AlertTriangle,
  RefreshCw,
  TrendingUp,
  Cpu,
  Eye,
  Layers,
} from 'lucide-react';
import type { SovereignBridgeStatus, SystemState } from '../types';
import { Aether3DScene } from './Aether3DScene';
import { getAIExplanation, getDualAxisExplanation } from '../api/lefa';

interface RuntimeCompanionViewProps {
  bridgeStatus: SovereignBridgeStatus | null;
  onOpenConnectModal: () => void;
  reducedMotion?: boolean;
}

const STATE_CONFIG: Record<
  SystemState,
  {
    title: string;
    kaomoji: string;
    description: string;
    color: string;
    border: string;
    badge: string;
  }
> = {
  disconnected: {
    title: 'Dormant Observer',
    kaomoji: '(,,•́ . •̀,,)',
    description: 'Awaiting Alpaca Paper bridge connection. Observation mode ready.',
    color: 'text-zinc-400',
    border: 'border-zinc-700/50',
    badge: 'bg-zinc-800/80 text-zinc-300',
  },
  observing: {
    title: 'Active Sensing (SPY)',
    kaomoji: '(・_・;)',
    description: 'Streaming live tick feeds. Ingesting market microstructure & regime data.',
    color: 'text-emerald-400',
    border: 'border-emerald-500/40',
    badge: 'bg-emerald-500/20 text-emerald-300',
  },
  ledgered: {
    title: 'Immutable Thesis Locked',
    kaomoji: '( `･ω･´ )',
    description: 'Pre-execution thesis committed to The Ark ledger (T0-T1). Zero drift permitted.',
    color: 'text-[#fef08a]',
    border: 'border-[#d4af37]/50',
    badge: 'bg-[#d4af37]/20 text-[#fef08a]',
  },
  hold: {
    title: 'Dual-Axis Hold Active',
    kaomoji: 'ψ( ` ∇ ´ )ψ',
    description: 'Risk policy threshold reached or market regime uncertain. Execution blocked.',
    color: 'text-orange-400',
    border: 'border-orange-500/50',
    badge: 'bg-orange-500/20 text-orange-300',
  },
  reveal: {
    title: 'Post-Market Truth Reveal',
    kaomoji: '╰(*°▽°*)╯',
    description: 'Ex-post evaluation complete. Comparing initial thesis against realized path.',
    color: 'text-cyan-400',
    border: 'border-cyan-500/50',
    badge: 'bg-cyan-500/20 text-cyan-300',
  },
};

export const RuntimeCompanionView: React.FC<RuntimeCompanionViewProps> = ({
  bridgeStatus,
  onOpenConnectModal,
  reducedMotion = false,
}) => {
  const isConnected = bridgeStatus?.bridge_state === 'VERIFIED';
  const [activeState, setActiveState] = useState<SystemState>(
    isConnected ? 'observing' : 'disconnected'
  );

  // Live AI reasoning states
  const [aiExplanation, setAiExplanation] = useState<string>(
    'LEFA AI is observing SPY at $598.50 under a strict 2% max-allocation risk policy. No rogue execution is permitted.'
  );
  const [isLoadingAI, setIsLoadingAI] = useState<boolean>(false);
  const [aiModel, setAiModel] = useState<string>('Qwen/Qwen2.5-7B-Instruct');

  // Trigger live AI explanation on demand
  const handleAskAI = async () => {
    setIsLoadingAI(true);
    try {
      const res = await getAIExplanation({
        symbol: 'SPY',
        price: '598.50',
        market_state: activeState,
        decision_action: activeState === 'hold' ? 'HOLD' : 'OBSERVE',
        rationale:
          'Governed financial evaluation under Alpaca Paper trading hackathon constraints.',
      });
      setAiExplanation(res.explanation);
      setAiModel(res.model);
    } catch {
      setAiExplanation(
        'Dual-axis governance policy enforced. Market observation maintained under paper jurisdiction.'
      );
    } finally {
      setIsLoadingAI(false);
    }
  };

  const handleExplainDualAxis = async () => {
    setIsLoadingAI(true);
    try {
      const res = await getDualAxisExplanation();
      setAiExplanation(res.explanation);
      setAiModel(res.model);
    } catch {
      setAiExplanation(
        'Dual-axis governance pairs deterministic risk policies with cryptographic provenance.'
      );
    } finally {
      setIsLoadingAI(false);
    }
  };

  const currentCfg = STATE_CONFIG[activeState];

  return (
    <div className="w-full max-w-6xl mx-auto space-y-6 sm:space-y-8 animate-fadeIn">
      {/* 1. HERO COMPANION CONTAINER */}
      <div className="relative rounded-3xl bg-gradient-to-b from-[#121218]/90 to-[#0c0c10]/95 border border-[#d4af37]/30 shadow-2xl p-6 sm:p-8 backdrop-blur-xl overflow-hidden">
        {/* Subtle decorative grid background */}
        <div className="absolute inset-0 bg-[radial-gradient(#d4af37_1px,transparent_1px)] [background-size:24px_24px] opacity-5 pointer-events-none" />

        {/* Top Status Strip */}
        <div className="flex flex-wrap items-center justify-between gap-3 pb-4 border-b border-zinc-800/80">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-2xl bg-gradient-to-br from-[#d4af37]/20 to-[#d4af37]/5 border border-[#d4af37]/40 flex items-center justify-center text-[#e5c158]">
              <Sparkles className="w-4 h-4" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-lg font-serif text-zinc-100 tracking-wide">LEFA AI</h2>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-[#d4af37]/15 text-[#fef08a] border border-[#d4af37]/30">
                  v1.0 Hackathon
                </span>
              </div>
              <p className="text-xs text-zinc-400 font-sans">
                Governed Financial Intelligence Companion • Observe → Ledger → Reveal
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2.5">
            <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-zinc-900/80 border border-zinc-700/60 text-xs font-mono">
              <span
                className={`w-2 h-2 rounded-full ${
                  isConnected ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'
                }`}
              />
              <span className="text-zinc-300">
                {isConnected ? 'Alpaca Paper: VERIFIED' : 'Paper Bridge: DORMANT'}
              </span>
            </div>

            <button
              onClick={onOpenConnectModal}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-medium transition-all duration-200 cursor-pointer flex items-center gap-1.5 ${
                isConnected
                  ? 'bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-600'
                  : 'bg-gradient-to-r from-[#d4af37] to-[#b48a1e] hover:brightness-110 text-black font-semibold shadow-lg shadow-[#d4af37]/20'
              }`}
            >
              <Lock className="w-3.5 h-3.5" />
              {isConnected ? 'Bridge Details' : 'Connect Alpaca'}
            </button>
          </div>
        </div>

        {/* 3D Aether Core & Real-time Companion Persona */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center pt-4">
          {/* Left: 3D Living Orb */}
          <div className="lg:col-span-7 flex flex-col items-center justify-center">
            <Aether3DScene state={activeState} reducedMotion={reducedMotion} />
            <div className="text-center mt-[-10px] z-10">
              <span className="text-2xl sm:text-3xl font-mono text-[#fef08a] select-none tracking-widest drop-shadow-[0_0_12px_rgba(212,175,55,0.4)]">
                {currentCfg.kaomoji}
              </span>
              <p className="text-xs font-serif text-zinc-300 mt-1">{currentCfg.title}</p>
            </div>
          </div>

          {/* Right: State Selector & Companion Narration */}
          <div className="lg:col-span-5 space-y-4">
            <div className="p-4 rounded-2xl bg-black/40 border border-zinc-800/80 space-y-3">
              <div className="flex items-center justify-between text-xs">
                <span className="text-zinc-400 font-mono flex items-center gap-1.5">
                  <Activity className="w-3.5 h-3.5 text-[#e5c158]" /> Companion State
                </span>
                <span className={`text-[10px] font-mono px-2 py-0.5 rounded-full ${currentCfg.badge}`}>
                  {activeState.toUpperCase()}
                </span>
              </div>
              <p className="text-xs text-zinc-300 leading-relaxed font-sans">
                {currentCfg.description}
              </p>

              {/* State Cycle Pill Buttons */}
              <div className="pt-2">
                <span className="text-[10px] font-mono text-zinc-500 uppercase tracking-wider block mb-2">
                  Simulate T0-T3 Protocol Cycle:
                </span>
                <div className="grid grid-cols-3 gap-1.5 text-[11px] font-mono">
                  {(['observing', 'ledgered', 'hold', 'reveal', 'disconnected'] as SystemState[]).map(
                    (st) => (
                      <button
                        key={st}
                        onClick={() => setActiveState(st)}
                        className={`px-2 py-1.5 rounded-lg border transition-all cursor-pointer text-center ${
                          activeState === st
                            ? 'bg-[#d4af37]/20 border-[#d4af37] text-[#fef08a] font-semibold'
                            : 'bg-zinc-900/60 border-zinc-800 text-zinc-400 hover:text-zinc-200 hover:border-zinc-700'
                        }`}
                      >
                        {st}
                      </button>
                    )
                  )}
                </div>
              </div>
            </div>

            {/* Quick Live Actions */}
            <div className="flex gap-2">
              <button
                onClick={handleAskAI}
                disabled={isLoadingAI}
                className="flex-1 py-2.5 px-3 rounded-xl bg-[#d4af37]/15 hover:bg-[#d4af37]/25 border border-[#d4af37]/40 text-[#fef08a] text-xs font-mono flex items-center justify-center gap-1.5 transition-all cursor-pointer"
              >
                <Cpu className={`w-3.5 h-3.5 ${isLoadingAI ? 'animate-spin' : ''}`} />
                {isLoadingAI ? 'Reasoning...' : 'Ask AI Reasoner'}
              </button>
              <button
                onClick={handleExplainDualAxis}
                disabled={isLoadingAI}
                className="py-2.5 px-3 rounded-xl bg-zinc-900/90 hover:bg-zinc-800 border border-zinc-700 text-zinc-300 text-xs font-mono flex items-center gap-1.5 transition-all cursor-pointer"
                title="Explain Dual-Axis Governance"
              >
                <Layers className="w-3.5 h-3.5 text-[#e5c158]" /> Dual-Axis Law
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* 2. THREE COMPACT, PERFECTLY ALIGNED TELEMETRY CARDS */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6">
        {/* Card 1: Market Sensing (SPY) */}
        <div className="rounded-2xl bg-[#0f0f14]/90 border border-zinc-800/80 p-5 space-y-4 hover:border-zinc-700/80 transition-all">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
                <TrendingUp className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-sm font-serif text-zinc-100">Market Sensing</h3>
                <p className="text-[10px] font-mono text-zinc-400">S&P 500 ETF (SPY)</p>
              </div>
            </div>
            <span className="text-xs font-mono font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
              $598.50
            </span>
          </div>

          <div className="space-y-2 text-xs font-mono">
            <div className="flex justify-between py-1 border-b border-zinc-800/60">
              <span className="text-zinc-500">Regime:</span>
              <span className="text-zinc-200">Balanced Trend</span>
            </div>
            <div className="flex justify-between py-1 border-b border-zinc-800/60">
              <span className="text-zinc-500">Volatility (ATR):</span>
              <span className="text-zinc-200">1.14 (Normal)</span>
            </div>
            <div className="flex justify-between py-1">
              <span className="text-zinc-500">Paper Jurisdiction:</span>
              <span className="text-emerald-400 font-semibold">ADMISSIBLE</span>
            </div>
          </div>
        </div>

        {/* Card 2: Dual-Axis Governance Policy */}
        <div className="rounded-2xl bg-[#0f0f14]/90 border border-zinc-800/80 p-5 space-y-4 hover:border-zinc-700/80 transition-all">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-xl bg-[#d4af37]/10 border border-[#d4af37]/30 flex items-center justify-center text-[#e5c158]">
                <Shield className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-sm font-serif text-zinc-100">Dual-Axis Risk Policy</h3>
                <p className="text-[10px] font-mono text-zinc-400">Deterministic Invariant</p>
              </div>
            </div>
            <span className="text-xs font-mono text-[#fef08a] bg-[#d4af37]/10 px-2 py-0.5 rounded-full border border-[#d4af37]/20">
              Max 2.0% Cap
            </span>
          </div>

          <div className="space-y-2 text-xs font-mono">
            <div className="flex justify-between py-1 border-b border-zinc-800/60">
              <span className="text-zinc-500">Execution Authority:</span>
              <span className="text-amber-400 font-semibold">ZERO (Observe Only)</span>
            </div>
            <div className="flex justify-between py-1 border-b border-zinc-800/60">
              <span className="text-zinc-500">KPGS Audit Ledger:</span>
              <span className="text-zinc-200">E1_PROVENANCE_SEALED</span>
            </div>
            <div className="flex justify-between py-1">
              <span className="text-zinc-500">Memory Discipline:</span>
              <span className="text-emerald-400">NO_MALLOC_ZERO_DRIFT</span>
            </div>
          </div>
        </div>

        {/* Card 3: Featherless AI Serverless Engine */}
        <div className="rounded-2xl bg-[#0f0f14]/90 border border-zinc-800/80 p-5 space-y-4 hover:border-zinc-700/80 transition-all">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
                <Cpu className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-sm font-serif text-zinc-100">Featherless AI</h3>
                <p className="text-[10px] font-mono text-zinc-400">Official Partner Engine</p>
              </div>
            </div>
            <span className="text-xs font-mono text-cyan-300 bg-cyan-500/10 px-2 py-0.5 rounded-full border border-cyan-500/20">
              21.9k Models
            </span>
          </div>

          <div className="space-y-2 text-xs font-mono">
            <div className="flex justify-between py-1 border-b border-zinc-800/60">
              <span className="text-zinc-500">Active Model:</span>
              <span className="text-zinc-200 truncate max-w-[140px]">{aiModel}</span>
            </div>
            <div className="flex justify-between py-1 border-b border-zinc-800/60">
              <span className="text-zinc-500">Inference Mode:</span>
              <span className="text-cyan-400">Serverless Open-Source</span>
            </div>
            <div className="flex justify-between py-1">
              <span className="text-zinc-500">Fallback Safety:</span>
              <span className="text-emerald-400">Deterministic Closed</span>
            </div>
          </div>
        </div>
      </div>

      {/* 3. LIVE AI NARRATIVE EXPLANATION BANNER */}
      <div className="p-5 rounded-2xl bg-gradient-to-r from-[#121218] via-[#16161f] to-[#121218] border border-[#d4af37]/40 shadow-xl space-y-2">
        <div className="flex items-center justify-between text-xs font-mono text-[#fef08a]">
          <span className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-[#e5c158]" />
            <span>LEFA Companion Live Synthesis (Featherless AI)</span>
          </span>
          <span className="text-[10px] text-zinc-400">{aiModel}</span>
        </div>
        <p className="text-xs sm:text-sm text-zinc-200 leading-relaxed font-sans italic">
          "{aiExplanation}"
        </p>
      </div>
    </div>
  );
};
