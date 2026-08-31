/**
 * SnapshotBanner
 * ==============
 * Displays governed account/market state from the LEFA Python backend.
 *
 * Truthfulness mandate (Issue #3 / DESIGN.md):
 * - All values come through the LEFADataProvider snapshot boundary.
 * - When fixture mode: shows "Not Connected" / "—" — never invents numbers.
 * - When connected: shows only what the backend has actually observed.
 * - No believable fake financial state is ever rendered.
 */
import React from 'react';
import type { SnapshotResponse } from '../api/lefa';

interface SnapshotBannerProps {
  snapshot: SnapshotResponse | null;
  isLoading: boolean;
}

export const SnapshotBanner: React.FC<SnapshotBannerProps> = ({
  snapshot,
  isLoading,
}) => {
  if (isLoading) {
    return (
      <div className="w-full max-w-2xl mx-auto px-4 py-2 rounded-xl bg-[#121216] border border-[#27272a] font-mono text-[11px] text-zinc-500 text-center animate-pulse">
        Loading governed state…
      </div>
    );
  }

  const isFixture = !snapshot || snapshot.provenance_is_fixture;

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div className="px-4 py-2.5 rounded-xl bg-[#121216]/80 border border-[#27272a] font-mono text-[11px] flex flex-wrap gap-x-6 gap-y-1 items-center justify-between">
        <div className="flex items-center gap-1.5">
          <span
            className={`w-1.5 h-1.5 rounded-full ${
              isFixture ? 'bg-zinc-600' : 'bg-[#d4af37]'
            }`}
          />
          <span className="text-zinc-400">
            {isFixture ? 'Fixture Mode' : 'Alpaca Connected'}
          </span>
        </div>

        <div className="flex items-center gap-1 text-zinc-500">
          <span>Portfolio Equity:</span>
          <span className="text-zinc-200">
            {snapshot?.portfolio_equity != null ? `$${snapshot.portfolio_equity}` : '—'}
          </span>
        </div>

        <div className="flex items-center gap-1 text-zinc-500">
          <span>Buying Power:</span>
          <span className="text-zinc-200">
            {snapshot?.buying_power != null ? `$${snapshot.buying_power}` : '—'}
          </span>
        </div>

        <div className="flex items-center gap-1 text-zinc-500">
          <span>Market:</span>
          <span className="text-zinc-200">
            {snapshot?.market_symbol && snapshot.market_symbol !== '—'
              ? snapshot.market_symbol
              : '—'}
          </span>
        </div>

        {isFixture && (
          <span className="text-[10px] text-zinc-600 italic">
            * No real account data — fixture only
          </span>
        )}
      </div>
    </div>
  );
};
