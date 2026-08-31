import React from 'react';
import {
  Activity,
  AlertTriangle,
  Clock3,
  FileCheck2,
  Link2,
  LockKeyhole,
  Radar,
  ShieldCheck,
} from 'lucide-react';
import type { SovereignBridgeStatus, SystemState } from '../types';

interface RuntimeCompanionViewProps {
  bridgeStatus: SovereignBridgeStatus | null;
  onOpenConnectModal: () => void;
  reducedMotion: boolean;
}

function runtimeVisualState(status: SovereignBridgeStatus | null): SystemState {
  if (!status) return 'disconnected';
  if (status.bridge_state !== 'VERIFIED') return 'hold';
  if (!status.latest_receipt) return 'hold';
  if (status.latest_receipt.evaluation.decision === 'HOLD') return 'hold';
  return 'ledgered';
}

function stateCopy(state: SystemState, status: SovereignBridgeStatus | null) {
  const receipt = status?.latest_receipt ?? null;

  if (state === 'disconnected') {
    return {
      eyebrow: 'AWAITING PROVIDER EVIDENCE',
      title: 'LEFA is ready. Reality is not connected yet.',
      body: 'Runtime remains empty until the sovereign paper bridge proves its provider boundary. No browser credentials. No synthetic fallback.',
      kaomoji: 'ᓚᘏᗢ',
    };
  }

  if (state === 'hold' && status?.bridge_state === 'VERIFIED' && !receipt) {
    return {
      eyebrow: 'PROVIDER VERIFIED • RECEIPT MISSING',
      title: 'Observation exists. Decision truth does not — HOLD.',
      body: 'Alpaca PAPER is observable through the sovereign boundary, but no canonical decision receipt has been published. The interface refuses to invent one.',
      kaomoji: 'U_U',
    };
  }

  if (state === 'hold' && receipt) {
    return {
      eyebrow: 'CANONICAL DECISION • HOLD',
      title: 'LEFA is preserving uncertainty instead of forcing action.',
      body: 'A governed receipt exists and its deterministic decision is HOLD. The frontend reflects that receipt without promoting it to execution.',
      kaomoji: 'U_U',
    };
  }

  return {
    eyebrow: `CANONICAL DECISION • ${receipt?.evaluation.decision ?? 'PRESERVED'}`,
    title: 'A governed decision has been preserved.',
    body: 'The receipt is ledgered. Time and later reality still decide what survives; provider reachability and decision approval are not order execution.',
    kaomoji: "(●'◡'●)",
  };
}

function stateAura(state: SystemState) {
  if (state === 'hold') return 'border-[#d97706]/65 shadow-[0_0_70px_rgba(217,119,6,0.16)]';
  if (state === 'ledgered') return 'border-[#e5c158]/70 shadow-[0_0_80px_rgba(229,193,88,0.16)]';
  return 'border-[#d4af37]/35 shadow-[0_0_60px_rgba(212,175,55,0.10)]';
}

export const RuntimeCompanionView: React.FC<RuntimeCompanionViewProps> = ({
  bridgeStatus,
  onOpenConnectModal,
  reducedMotion,
}) => {
  const receipt = bridgeStatus?.latest_receipt ?? null;
  const state = runtimeVisualState(bridgeStatus);
  const copy = stateCopy(state, bridgeStatus);
  const providerVerified = bridgeStatus?.bridge_state === 'VERIFIED';
  const observation = bridgeStatus?.provider_observation;

  const observeStatus = providerVerified ? 'VERIFIED' : 'AWAITING';
  const ledgerStatus = receipt ? 'PRESERVED' : providerVerified ? 'HOLD' : 'EMPTY';

  return (
    <section className="w-full max-w-6xl mx-auto" aria-label="LEFA adaptive runtime companion">
      <div className="overflow-hidden rounded-[28px] border border-[#27272a] bg-[#0c0c0f] shadow-2xl">
        <header className="flex flex-col gap-3 border-b border-[#27272a] bg-[#101014]/95 px-4 py-4 sm:flex-row sm:items-center sm:justify-between sm:px-6">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-full border border-[#d4af37]/45 bg-[#18181b]">
              <Activity className="h-4 w-4 text-[#e5c158]" />
            </div>
            <div>
              <div className="text-xs font-semibold tracking-[0.16em] text-[#e5c158]">LEFA AI</div>
              <div className="text-[10px] font-mono text-zinc-500">Adaptive Runtime Companion • receipt-derived</div>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2 text-[10px] font-mono">
            <span className={`rounded-full border px-2.5 py-1 ${providerVerified ? 'border-[#d4af37]/45 bg-[#d4af37]/10 text-[#fef08a]' : 'border-[#3f3f46] bg-[#18181b] text-zinc-400'}`}>
              ALPACA {providerVerified ? 'PAPER VERIFIED' : 'UNVERIFIED'}
            </span>
            <span className="rounded-full border border-[#3f3f46] bg-[#18181b] px-2.5 py-1 text-zinc-400">
              EXECUTION: BACKEND ONLY
            </span>
          </div>
        </header>

        <div className="grid gap-0 lg:grid-cols-[minmax(0,1.15fr)_minmax(320px,0.85fr)]">
          <main className="relative flex min-h-[620px] flex-col items-center justify-center overflow-hidden border-b border-[#27272a] px-5 py-10 text-center lg:border-b-0 lg:border-r">
            <div className="pointer-events-none absolute inset-0 bg-[linear-gradient(to_right,#18181b_1px,transparent_1px),linear-gradient(to_bottom,#18181b_1px,transparent_1px)] bg-[size:4rem_4rem] opacity-20 [mask-image:radial-gradient(ellipse_68%_58%_at_50%_44%,#000_68%,transparent_100%)]" />
            <div className={`pointer-events-none absolute h-[430px] w-[430px] rounded-full border ${stateAura(state)}`} />
            <div className={`pointer-events-none absolute h-[500px] w-[500px] rounded-full border border-dashed ${state === 'hold' ? 'border-[#d97706]/20' : 'border-[#d4af37]/15'} ${!reducedMotion ? 'animate-[spin_48s_linear_infinite]' : ''}`} />

            <div className="relative z-10 mb-5 rounded-full border border-[#27272a] bg-[#121216]/90 px-3 py-1.5 text-[10px] font-mono tracking-[0.12em] text-zinc-400">
              {copy.eyebrow}
            </div>

            <div className={`relative z-10 w-[250px] overflow-hidden rounded-full border-2 bg-[#f7f7f4] sm:w-[300px] ${stateAura(state)}`}>
              <img
                src="/lefa-companion-root.svg"
                alt="Canonical LEFA companion"
                className="block h-auto w-full"
              />
            </div>

            <div className="relative z-10 mt-4 inline-flex items-center gap-2 rounded-full border border-[#d4af37]/25 bg-[#121216]/90 px-3 py-1.5 text-xs font-mono text-[#fef08a]">
              <span>{copy.kaomoji}</span>
              <span className="text-zinc-500">•</span>
              <span className={state === 'hold' ? 'text-[#fbbf24]' : 'text-[#e5c158]'}>{state.toUpperCase()}</span>
            </div>

            <h1 className="relative z-10 mt-5 max-w-xl font-serif text-2xl leading-tight text-[#f4f4f5] sm:text-3xl">
              {copy.title}
            </h1>
            <p className="relative z-10 mt-3 max-w-xl text-xs leading-relaxed text-zinc-400 sm:text-sm">
              {copy.body}
            </p>

            {!providerVerified && (
              <button
                type="button"
                onClick={onOpenConnectModal}
                className="relative z-10 mt-6 inline-flex items-center gap-2 rounded-xl border border-[#d4af37]/55 bg-[#d4af37]/10 px-4 py-2.5 text-xs font-mono font-semibold text-[#fef08a] transition-colors hover:bg-[#d4af37]/20"
              >
                <Link2 className="h-4 w-4" />
                Verify sovereign paper bridge
              </button>
            )}
          </main>

          <aside className="bg-[#101014] p-4 sm:p-6">
            <div className="space-y-4">
              <div className="rounded-2xl border border-[#27272a] bg-[#09090b] p-4">
                <div className="flex items-center gap-2 text-[10px] font-mono uppercase tracking-[0.14em] text-[#e5c158]">
                  <Radar className="h-4 w-4" />
                  Runtime Context Engine
                </div>
                <div className="mt-4 space-y-2 text-[11px] font-mono">
                  <div className="flex justify-between gap-3 border-b border-[#27272a] pb-2">
                    <span className="text-zinc-500">Provider boundary</span>
                    <span className={providerVerified ? 'text-[#fef08a]' : 'text-zinc-400'}>{observeStatus}</span>
                  </div>
                  <div className="flex justify-between gap-3 border-b border-[#27272a] pb-2">
                    <span className="text-zinc-500">Environment</span>
                    <span className="text-zinc-300">{bridgeStatus?.environment?.toUpperCase() ?? 'UNKNOWN'}</span>
                  </div>
                  <div className="flex justify-between gap-3 border-b border-[#27272a] pb-2">
                    <span className="text-zinc-500">Decision receipt</span>
                    <span className={receipt ? 'text-[#e5c158]' : providerVerified ? 'text-[#fbbf24]' : 'text-zinc-400'}>{ledgerStatus}</span>
                  </div>
                  <div className="flex justify-between gap-3">
                    <span className="text-zinc-500">UI transition</span>
                    <span className={state === 'hold' ? 'text-[#fbbf24]' : 'text-zinc-300'}>{state.toUpperCase()}</span>
                  </div>
                </div>
                <p className="mt-4 text-[10px] leading-relaxed text-zinc-500">
                  Same LEFA. Different evidence conditions. Presentation adapts; financial truth does not.
                </p>
              </div>

              {providerVerified && (
                <div className="rounded-2xl border border-[#27272a] bg-[#121216] p-4">
                  <div className="flex items-center gap-2 text-[10px] font-mono uppercase tracking-[0.14em] text-zinc-400">
                    <ShieldCheck className="h-4 w-4 text-[#e5c158]" />
                    Observation Boundary
                  </div>
                  <div className="mt-3 space-y-2 text-[11px]">
                    <div className="rounded-xl border border-[#27272a] bg-[#09090b] p-3">
                      <div className="text-[10px] font-mono text-zinc-500">Observed at</div>
                      <div className="mt-1 break-words font-mono text-zinc-300">{bridgeStatus?.observed_at}</div>
                    </div>
                    <div className="grid grid-cols-2 gap-2">
                      <div className="rounded-xl border border-[#27272a] bg-[#09090b] p-3">
                        <div className="text-[10px] font-mono text-zinc-500">Provider code</div>
                        <div className="mt-1 font-mono text-zinc-300">{observation?.code ?? 'VERIFIED'}</div>
                      </div>
                      <div className="rounded-xl border border-[#27272a] bg-[#09090b] p-3">
                        <div className="text-[10px] font-mono text-zinc-500">Account state</div>
                        <div className="mt-1 font-mono text-zinc-300">{observation?.account_status ?? 'UNKNOWN'}</div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {providerVerified && !receipt && (
                <div className="rounded-2xl border border-[#d97706]/50 bg-[#14120e] p-4">
                  <div className="flex items-start gap-3">
                    <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0 text-[#fbbf24]" />
                    <div>
                      <div className="text-xs font-semibold text-[#fbbf24]">RECEIPT MISSING → HOLD</div>
                      <p className="mt-2 text-[11px] leading-relaxed text-zinc-400">
                        Provider reachability is not a decision. LEFA waits for a canonical `kopano.alpaca.decision-receipt.v1`.
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {receipt && (
                <div className={`rounded-2xl border p-4 ${receipt.evaluation.decision === 'HOLD' ? 'border-[#d97706]/50 bg-[#14120e]' : 'border-[#d4af37]/40 bg-[#121216]'}`}>
                  <div className="flex items-center justify-between gap-3">
                    <div className="flex items-center gap-2 text-[10px] font-mono uppercase tracking-[0.14em] text-[#e5c158]">
                      <FileCheck2 className="h-4 w-4" />
                      Canonical Receipt
                    </div>
                    <span className={`rounded-lg border px-2 py-1 text-[10px] font-mono font-bold ${receipt.evaluation.decision === 'HOLD' ? 'border-[#d97706]/50 text-[#fbbf24]' : 'border-[#d4af37]/45 text-[#fef08a]'}`}>
                      {receipt.evaluation.decision}
                    </span>
                  </div>
                  <div className="mt-3 rounded-xl border border-[#27272a] bg-[#09090b] p-3 text-[10px] font-mono">
                    <div className="text-zinc-500">Receipt</div>
                    <div className="mt-1 break-all text-zinc-200">{receipt.kc_receipt_id}</div>
                    <div className="mt-3 text-zinc-500">Proof</div>
                    <div className="mt-1 text-zinc-300">{receipt.proof_state}</div>
                  </div>
                  {receipt.evaluation.reasons.length > 0 && (
                    <div className="mt-3 space-y-2">
                      {receipt.evaluation.reasons.slice(0, 3).map((reason, index) => (
                        <div key={`${reason.code}-${index}`} className="rounded-xl border border-[#27272a] bg-[#18181b] p-3 text-[11px]">
                          <div className="font-mono text-[#e5c158]">{reason.code}</div>
                          <p className="mt-1 text-zinc-400">{reason.message}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          </aside>
        </div>

        <div className="grid grid-cols-2 gap-px border-t border-[#27272a] bg-[#27272a] sm:grid-cols-4">
          <div className="bg-[#0c0c0f] p-4">
            <div className="flex items-center gap-2 text-[10px] font-mono text-[#e5c158]"><Radar className="h-3.5 w-3.5" />01 OBSERVE</div>
            <div className="mt-2 text-xs font-semibold text-zinc-200">{observeStatus}</div>
          </div>
          <div className="bg-[#0c0c0f] p-4">
            <div className="flex items-center gap-2 text-[10px] font-mono text-[#e5c158]"><LockKeyhole className="h-3.5 w-3.5" />02 LEDGER</div>
            <div className={`mt-2 text-xs font-semibold ${ledgerStatus === 'HOLD' ? 'text-[#fbbf24]' : 'text-zinc-200'}`}>{ledgerStatus}</div>
          </div>
          <div className="bg-[#0c0c0f] p-4">
            <div className="flex items-center gap-2 text-[10px] font-mono text-zinc-500"><Clock3 className="h-3.5 w-3.5" />03 TIME</div>
            <div className="mt-2 text-xs font-semibold text-zinc-500">WAITING</div>
          </div>
          <div className="bg-[#0c0c0f] p-4">
            <div className="flex items-center gap-2 text-[10px] font-mono text-zinc-500"><ShieldCheck className="h-3.5 w-3.5" />04 REVEAL</div>
            <div className="mt-2 text-xs font-semibold text-zinc-500">NOT CLAIMED</div>
          </div>
        </div>
      </div>
    </section>
  );
};
