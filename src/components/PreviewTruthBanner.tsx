import React from 'react';
import { Beaker, ShieldAlert } from 'lucide-react';

export const PreviewTruthBanner: React.FC = () => (
  <div className="w-full rounded-xl border border-[#d97706]/55 bg-[#d97706]/10 px-4 py-3 font-mono">
    <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex items-center gap-2 text-[11px] font-bold text-[#fbbf24]">
        <Beaker className="h-4 w-4" />
        DESIGN PREVIEW • SYNTHETIC / NON-LIVE
      </div>
      <div className="flex items-center gap-1.5 text-[10px] text-zinc-400">
        <ShieldAlert className="h-3.5 w-3.5 text-[#fbbf24]" />
        Manual state changes here are visual simulations, never trading receipts.
      </div>
    </div>
  </div>
);
