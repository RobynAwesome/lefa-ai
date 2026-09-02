import React, { useCallback, useEffect, useState } from 'react';
import { motion } from 'motion/react';
import {
  Brain,
  CheckCircle2,
  FlaskConical,
  Lock,
  Radar,
  RefreshCw,
  ShieldCheck,
  Sparkles,
  WifiOff,
} from 'lucide-react';
import type { SovereignBridgeStatus, SystemState } from '../types';
import { getDualAxisExplanation, getRuntimeStatus } from '../api/lefa';
import type { RuntimeStatusResponse } from '../api/lefa';
import { Aether3DScene } from './Aether3DScene';

interface RuntimeCompanionViewProps {
  bridgeStatus: SovereignBridgeStatus | null;
  onOpenConnectModal: () => void;
  onOpenLab: () => void;
  reducedMotion?: boolean;
}

const unavailableRuntime: RuntimeStatusResponse = {
  schema: 'kopano.lefa.runtime-status.v1',
  state: 'UNAVAILABLE',
  headline: 'LEFA is reconnecting',
  detail: 'The secure service is temporarily out of reach. Your experience remains protected.',
  observed_at: '',
  connection: {
    state: 'UNAVAILABLE',
    label: 'Alpaca paper trading',
  },
  market: {
    state: 'WAITING_FOR_EVIDENCE',
    symbol: null,
    latest_price: null,
    market_state: 'unknown',
    observed_at: null,
  },
  decision: { state: 'NO_DECISION' },
  ai: {
    state: 'UNAVAILABLE',
    label: 'AI explanation',
  },
};

function visualStateFor(runtime: RuntimeStatusResponse): SystemState {
  return runtime.state === 'WAITING_FOR_MARKET' ? 'observing' : 'disconnected';
}

function connectionCopy(state: RuntimeStatusResponse['connection']['state']) {
  if (state === 'READY') {
    return {
      label: 'Ready',
      detail: 'Your secure paper connection is available.',
      icon: CheckCircle2,
      tone: 'text-emerald-300',
      surface: 'border-emerald-500/25 bg-emerald-500/8',
    };
  }
  if (state === 'SETUP_NEEDED') {
    return {
      label: 'Needs setup',
      detail: 'LEFA is waiting for the secure trading connection.',
      icon: Lock,
      tone: 'text-amber-300',
      surface: 'border-amber-500/25 bg-amber-500/8',
    };
  }
  return {
    label: 'Unavailable',
    detail: 'The trading service cannot be reached right now.',
    icon: WifiOff,
    tone: 'text-zinc-300',
    surface: 'border-zinc-700/70 bg-zinc-900/60',
  };
}

export const RuntimeCompanionView: React.FC<RuntimeCompanionViewProps> = ({
  bridgeStatus,
  onOpenConnectModal,
  onOpenLab,
  reducedMotion = false,
}) => {
  const [runtime, setRuntime] = useState<RuntimeStatusResponse | null>(null);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [aiExplanation, setAiExplanation] = useState<string | null>(null);
  const [aiModel, setAiModel] = useState<string | null>(null);
  const [isLoadingAI, setIsLoadingAI] = useState(false);

  const refreshRuntime = useCallback(async () => {
    setIsRefreshing(true);
    try {
      const status = await getRuntimeStatus();
      setRuntime(status);
    } catch {
      setRuntime(unavailableRuntime);
    } finally {
      setIsRefreshing(false);
    }
  }, []);

  useEffect(() => {
    void refreshRuntime();
    const interval = window.setInterval(() => void refreshRuntime(), 30_000);
    return () => window.clearInterval(interval);
  }, [refreshRuntime, bridgeStatus?.observed_at]);

  const current = runtime ?? unavailableRuntime;
  const visualState = visualStateFor(current);
  const connection = connectionCopy(current.connection.state);
  const ConnectionIcon = connection.icon;
  const marketAvailable = current.market.symbol !== null && current.market.latest_price !== null;
  const aiAvailable = current.ai.state === 'AVAILABLE';

  const explainProtection = async () => {
    setIsLoadingAI(true);
    setAiExplanation(null);
    try {
      const response = await getDualAxisExplanation();
      setAiExplanation(response.explanation);
      setAiModel(response.model);
    } catch {
      setAiExplanation("AI explanation isn't available right now. LEFA's core protections remain active without it.");
      setAiModel(null);
    } finally {
      setIsLoadingAI(false);
    }
  };

  return (
    <div className="mx-auto w-full max-w-6xl space-y-5 sm:space-y-6 animate-fadeIn">
      <section className="relative overflow-hidden rounded-[32px] border border-[#d4af37]/25 bg-gradient-to-b from-[#13131a]/95 via-[#0f0f14]/95 to-[#0a0a0e]/95 p-5 shadow-2xl backdrop-blur-xl sm:p-8">
        <div className="pointer-events-none absolute inset-0 opacity-[0.045] bg-[radial-gradient(#d4af37_1px,transparent_1px)] [background-size:26px_26px]" />
        <div className="pointer-events-none absolute left-1/2 top-[-180px] h-[360px] w-[560px] -translate-x-1/2 rounded-full bg-[#d4af37]/10 blur-[120px]" />

        <div className="relative z-10 flex flex-wrap items-center justify-between gap-4 border-b border-white/[0.07] pb-5">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-2xl border border-[#d4af37]/35 bg-[#d4af37]/10 text-[#f0cf69]">
              <Sparkles className="h-4 w-4" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="font-serif text-lg tracking-wide text-zinc-50">LEFA AI</h1>
                <span className="rounded-full border border-white/10 bg-white/[0.04] px-2 py-0.5 text-[9px] font-medium uppercase tracking-[0.2em] text-zinc-400">
                  Paper
                </span>
              </div>
              <p className="mt-0.5 text-xs text-zinc-500">Governed financial intelligence</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => void refreshRuntime()}
              disabled={isRefreshing}
              className="flex h-9 w-9 items-center justify-center rounded-xl border border-white/10 bg-white/[0.035] text-zinc-400 transition hover:border-white/20 hover:text-zinc-100 disabled:opacity-60"
              aria-label="Refresh LEFA status"
              title="Refresh"
            >
              <RefreshCw className={`h-3.5 w-3.5 ${isRefreshing ? 'animate-spin' : ''}`} />
            </button>
            <button
              onClick={onOpenConnectModal}
              className="rounded-xl bg-gradient-to-r from-[#d4af37] to-[#e2c35e] px-4 py-2.5 text-xs font-semibold text-black shadow-lg shadow-[#d4af37]/10 transition hover:brightness-110 active:scale-[0.99]"
            >
              {current.connection.state === 'READY' ? 'Connection' : 'Check connection'}
            </button>
          </div>
        </div>

        <div className="relative z-10 grid items-center gap-5 pt-5 lg:grid-cols-12 lg:gap-8">
          <div className="lg:col-span-7">
            <Aether3DScene state={visualState} reducedMotion={reducedMotion} />
            <div className="relative z-10 -mt-3 text-center">
              <p className="text-[10px] font-medium uppercase tracking-[0.28em] text-[#d9bc58]/70">
                {current.state === 'WAITING_FOR_MARKET' ? 'Listening' : 'Protected'}
              </p>
            </div>
          </div>

          <div className="space-y-5 lg:col-span-5">
            <motion.div
              key={current.state}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-3"
            >
              <div className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.04] px-3 py-1.5 text-[10px] uppercase tracking-[0.18em] text-zinc-400">
                <span
                  className={`h-1.5 w-1.5 rounded-full ${
                    current.state === 'WAITING_FOR_MARKET' ? 'bg-emerald-400 animate-pulse' : 'bg-amber-300'
                  }`}
                />
                {current.state === 'WAITING_FOR_MARKET'
                  ? 'Ready to observe'
                  : current.state === 'SETUP_NEEDED'
                    ? 'Setup needed'
                    : 'Reconnecting'}
              </div>
              <h2 className="max-w-md font-serif text-3xl leading-tight text-zinc-50 sm:text-4xl">
                {current.headline}
              </h2>
              <p className="max-w-md text-sm leading-6 text-zinc-400">{current.detail}</p>
            </motion.div>

            <div className="rounded-2xl border border-white/[0.07] bg-black/25 p-4">
              <div className="flex items-start gap-3">
                <Radar className="mt-0.5 h-4 w-4 shrink-0 text-[#e2c35e]" />
                <div>
                  <p className="text-sm font-medium text-zinc-200">
                    {marketAvailable ? 'Fresh market evidence received' : 'Waiting for market evidence'}
                  </p>
                  <p className="mt-1 text-xs leading-5 text-zinc-500">
                    {marketAvailable
                      ? 'LEFA is displaying only facts received from the governed backend.'
                      : 'No price or market claim will appear here until the backend can prove it.'}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="grid gap-3 md:grid-cols-3 sm:gap-4">
        <article className={`rounded-2xl border p-5 ${connection.surface}`}>
          <div className="flex items-center justify-between">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl border border-white/10 bg-black/20">
              <ConnectionIcon className={`h-4 w-4 ${connection.tone}`} />
            </div>
            <span className={`text-xs font-semibold ${connection.tone}`}>{connection.label}</span>
          </div>
          <h3 className="mt-4 text-sm font-semibold text-zinc-100">Trading connection</h3>
          <p className="mt-1.5 text-xs leading-5 text-zinc-500">{connection.detail}</p>
        </article>

        <article className="rounded-2xl border border-white/[0.07] bg-[#101015]/90 p-5">
          <div className="flex items-center justify-between">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl border border-white/10 bg-black/20 text-[#e2c35e]">
              <Radar className="h-4 w-4" />
            </div>
            <span className="text-xs font-semibold text-zinc-400">
              {marketAvailable ? 'Observed' : 'Waiting'}
            </span>
          </div>
          <h3 className="mt-4 text-sm font-semibold text-zinc-100">Market evidence</h3>
          <p className="mt-1.5 text-xs leading-5 text-zinc-500">
            {marketAvailable
              ? 'Fresh evidence is available from the backend.'
              : 'LEFA has not admitted a fresh market observation yet.'}
          </p>
        </article>

        <article className="rounded-2xl border border-white/[0.07] bg-[#101015]/90 p-5">
          <div className="flex items-center justify-between">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl border border-white/10 bg-black/20 text-cyan-300">
              <Brain className="h-4 w-4" />
            </div>
            <span className={`text-xs font-semibold ${aiAvailable ? 'text-cyan-300' : 'text-zinc-500'}`}>
              {aiAvailable ? 'Available' : 'Unavailable'}
            </span>
          </div>
          <h3 className="mt-4 text-sm font-semibold text-zinc-100">AI explanation</h3>
          <p className="mt-1.5 text-xs leading-5 text-zinc-500">
            {aiAvailable
              ? 'Ask LEFA to explain how its protections work. Market reasoning waits for market evidence.'
              : 'Core governance keeps working even when AI explanation is offline.'}
          </p>
        </article>
      </section>

      <section className="overflow-hidden rounded-2xl border border-[#d4af37]/20 bg-gradient-to-r from-[#111116] via-[#15151c] to-[#111116]">
        <div className="flex flex-col gap-4 p-5 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-start gap-3">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-[#d4af37]/25 bg-[#d4af37]/8 text-[#e2c35e]">
              <ShieldCheck className="h-4 w-4" />
            </div>
            <div>
              <h3 className="text-sm font-semibold text-zinc-100">Want the simple explanation?</h3>
              <p className="mt-1 max-w-2xl text-xs leading-5 text-zinc-500">
                LEFA can explain how it protects decisions without pretending it has market facts that have not arrived.
              </p>
            </div>
          </div>
          <button
            onClick={() => void explainProtection()}
            disabled={isLoadingAI || !aiAvailable}
            className="rounded-xl border border-[#d4af37]/35 bg-[#d4af37]/10 px-4 py-2.5 text-xs font-medium text-[#f3da87] transition hover:bg-[#d4af37]/15 disabled:cursor-not-allowed disabled:border-white/10 disabled:bg-white/[0.03] disabled:text-zinc-600"
          >
            {isLoadingAI ? 'Explaining…' : aiAvailable ? 'Explain protection' : 'AI unavailable'}
          </button>
        </div>

        {aiExplanation && (
          <motion.div
            initial={{ opacity: 0, y: 5 }}
            animate={{ opacity: 1, y: 0 }}
            className="border-t border-white/[0.06] px-5 py-4"
          >
            <p className="text-sm leading-6 text-zinc-300">{aiExplanation}</p>
            {aiModel && <p className="mt-2 text-[10px] text-zinc-600">Explained by LEFA AI</p>}
          </motion.div>
        )}
      </section>

      <div className="flex justify-center pb-2">
        <button
          onClick={onOpenLab}
          className="flex items-center gap-2 rounded-full px-3 py-2 text-[11px] text-zinc-600 transition hover:bg-white/[0.03] hover:text-zinc-400"
        >
          <FlaskConical className="h-3.5 w-3.5" />
          Open design lab
        </button>
      </div>
    </div>
  );
};
