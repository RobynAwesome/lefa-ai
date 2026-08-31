import React from 'react';
import { AlertTriangle, FileCheck2, Link2, LockKeyhole, ShieldCheck, Unplug } from 'lucide-react';
import type { SovereignBridgeStatus, SovereignDecision } from '../types';

interface RuntimeTruthViewProps {
  bridgeStatus: SovereignBridgeStatus | null;
  onOpenConnectModal: () => void;
}

function decisionClasses(decision: SovereignDecision) {
  if (decision === 'HOLD') return 'border-[#d97706]/60 bg-[#d97706]/10 text-[#fbbf24]';
  if (decision === 'REJECT') return 'border-rose-700/60 bg-rose-950/30 text-rose-300';
  return 'border-[#d4af37]/60 bg-[#d4af37]/10 text-[#fef08a]';
}

export const RuntimeTruthView: React.FC<RuntimeTruthViewProps> = ({
  bridgeStatus,
  onOpenConnectModal,
}) => {
  const receipt = bridgeStatus?.latest_receipt ?? null;

  return (
    <section className="w-full max-w-5xl mx-auto space-y-5" aria-label="LEFA runtime truth">
      <div className="rounded-2xl border border-[#d4af37]/35 bg-[#101014] p-5 sm:p-6 shadow-2xl">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <div className="space-y-1.5">
            <div className="flex items-center gap-2 text-[10px] font-mono uppercase tracking-[0.16em] text-[#e5c158]">
              <ShieldCheck className="h-4 w-4" />
              Runtime Truth
            </div>
            <h1 className="font-serif text-2xl text-[#f4f4f5] sm:text-3xl">LEFA Sovereign Ledger</h1>
            <p className="max-w-2xl text-xs leading-relaxed text-zinc-400 sm:text-sm">
              This surface renders only verified bridge status and canonical Sovereign decision receipts. Synthetic Stitch data is never admitted here.
            </p>
          </div>

          <div className="rounded-xl border border-[#27272a] bg-[#09090b] px-3 py-2 text-[10px] font-mono text-zinc-400">
            <div>Execution authority</div>
            <div className="mt-0.5 font-semibold text-[#fef08a]">BACKEND ONLY</div>
          </div>
        </div>
      </div>

      {!bridgeStatus ? (
        <div className="rounded-2xl border border-[#3f3f46] bg-[#121216] p-6 text-center sm:p-8">
          <div className="mx-auto flex h-11 w-11 items-center justify-center rounded-full border border-[#3f3f46] bg-[#18181b]">
            <Unplug className="h-5 w-5 text-zinc-400" />
          </div>
          <h2 className="mt-4 font-serif text-lg text-zinc-100">Sovereign bridge not verified</h2>
          <p className="mx-auto mt-2 max-w-xl text-xs leading-relaxed text-zinc-400">
            No runtime provider claim is active. LEFA will not populate balances, P&amp;L, strategy decisions, receipts, or market narratives from design-preview data.
          </p>
          <button
            type="button"
            onClick={onOpenConnectModal}
            className="mt-5 inline-flex items-center gap-2 rounded-xl border border-[#d4af37]/60 bg-[#d4af37]/10 px-4 py-2.5 text-xs font-mono font-semibold text-[#fef08a] transition-colors hover:bg-[#d4af37]/20"
          >
            <Link2 className="h-4 w-4" />
            Verify sovereign paper bridge
          </button>
        </div>
      ) : (
        <>
          <div className="grid gap-4 md:grid-cols-2">
            <div className="rounded-2xl border border-[#d4af37]/40 bg-[#121216] p-5">
              <div className="flex items-center gap-2 text-xs font-mono font-semibold text-[#fef08a]">
                <ShieldCheck className="h-4 w-4" />
                Provider boundary verified
              </div>
              <div className="mt-4 space-y-2 text-[11px] font-mono">
                <div className="flex justify-between gap-4 border-b border-[#27272a] pb-2 text-zinc-400">
                  <span>Provider</span>
                  <span className="text-zinc-200">Alpaca</span>
                </div>
                <div className="flex justify-between gap-4 border-b border-[#27272a] pb-2 text-zinc-400">
                  <span>Environment</span>
                  <span className="text-[#e5c158]">PAPER</span>
                </div>
                <div className="flex justify-between gap-4 border-b border-[#27272a] pb-2 text-zinc-400">
                  <span>Observed at</span>
                  <span className="text-right text-zinc-200">{bridgeStatus.observed_at}</span>
                </div>
                <div className="flex justify-between gap-4 text-zinc-400">
                  <span>Provider observation</span>
                  <span className="text-right text-zinc-200">
                    {bridgeStatus.provider_observation?.code ?? 'VERIFIED'}
                  </span>
                </div>
              </div>
            </div>

            <div className="rounded-2xl border border-[#27272a] bg-[#121216] p-5">
              <div className="flex items-center gap-2 text-xs font-mono font-semibold text-zinc-200">
                <LockKeyhole className="h-4 w-4 text-[#e5c158]" />
                Truth boundary
              </div>
              <p className="mt-3 text-[11px] leading-relaxed text-zinc-400">
                {bridgeStatus.truth_boundary ??
                  'Bridge verification proves the governed paper-provider boundary only. It does not prove a strategy decision or an executed order.'}
              </p>
              <div className="mt-4 rounded-xl border border-[#27272a] bg-[#09090b] p-3 text-[10px] font-mono text-zinc-500">
                Provider reachability ≠ risk approval ≠ provider order receipt.
              </div>
            </div>
          </div>

          {!receipt ? (
            <div className="rounded-2xl border border-[#d97706]/50 bg-[#14120e] p-6 sm:p-7">
              <div className="flex items-start gap-3">
                <AlertTriangle className="mt-0.5 h-5 w-5 shrink-0 text-[#fbbf24]" />
                <div>
                  <h2 className="font-serif text-lg text-[#f4f4f5]">No canonical decision receipt published yet</h2>
                  <p className="mt-2 max-w-2xl text-xs leading-relaxed text-zinc-400">
                    The Alpaca paper bridge is observable, but the Sovereign backend has not supplied a persisted `kopano.alpaca.decision-receipt.v1` to LEFA. Runtime remains evidence-light by design.
                  </p>
                  <div className="mt-4 inline-flex rounded-lg border border-[#d97706]/40 bg-[#d97706]/10 px-3 py-1.5 text-[10px] font-mono text-[#fbbf24]">
                    RECEIPT MISSING → HOLD DISPLAY
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <article className="rounded-2xl border border-[#d4af37]/45 bg-[#121216] p-5 sm:p-6">
              <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                <div>
                  <div className="flex items-center gap-2 text-[10px] font-mono uppercase tracking-[0.14em] text-[#e5c158]">
                    <FileCheck2 className="h-4 w-4" />
                    Canonical Decision Receipt
                  </div>
                  <h2 className="mt-2 font-serif text-xl text-zinc-100">{receipt.kc_receipt_id}</h2>
                  <p className="mt-1 text-[10px] font-mono text-zinc-500">Cycle {receipt.cycle_id} • {receipt.timestamp}</p>
                </div>
                <span className={`self-start rounded-lg border px-3 py-1.5 text-xs font-mono font-bold ${decisionClasses(receipt.evaluation.decision)}`}>
                  {receipt.evaluation.decision}
                </span>
              </div>

              <div className="mt-5 grid gap-3 sm:grid-cols-2">
                <div className="rounded-xl border border-[#27272a] bg-[#09090b] p-3 text-[10px] font-mono">
                  <div className="text-zinc-500">Evidence SHA-256</div>
                  <div className="mt-1 break-all text-[#e5c158]">{receipt.evidence_sha256}</div>
                </div>
                <div className="rounded-xl border border-[#27272a] bg-[#09090b] p-3 text-[10px] font-mono">
                  <div className="text-zinc-500">Proof state</div>
                  <div className="mt-1 text-zinc-200">{receipt.proof_state}</div>
                  <div className="mt-2 text-zinc-500">Provider order receipt</div>
                  <div className="mt-1 text-zinc-200">{receipt.provider_receipt_id ?? 'None asserted'}</div>
                </div>
              </div>

              <div className="mt-5">
                <div className="text-[10px] font-mono uppercase tracking-wider text-zinc-500">Deterministic reasons</div>
                {receipt.evaluation.reasons.length === 0 ? (
                  <p className="mt-2 text-xs text-zinc-400">No blocking reasons were recorded in this receipt.</p>
                ) : (
                  <div className="mt-2 space-y-2">
                    {receipt.evaluation.reasons.map((reason, index) => (
                      <div key={`${reason.code}-${index}`} className="rounded-xl border border-[#27272a] bg-[#18181b] p-3 text-[11px]">
                        <div className="flex flex-wrap items-center gap-2 font-mono">
                          <span className="text-[#e5c158]">{reason.code}</span>
                          <span className="text-zinc-500">•</span>
                          <span className="text-zinc-400">{reason.severity}</span>
                        </div>
                        <p className="mt-1.5 text-zinc-300">{reason.message}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="mt-5 rounded-xl border border-[#27272a] bg-[#09090b] p-3 text-[10px] leading-relaxed text-zinc-500">
                A receipt decision never grants browser execution authority. Orders remain a Sovereign backend concern and require their own provider receipt.
              </div>
            </article>
          )}
        </>
      )}
    </section>
  );
};
