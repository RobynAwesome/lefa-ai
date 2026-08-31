import React, { useState } from 'react';
import { motion } from 'motion/react';
import { X, Shield, CheckCircle2, Lock, ArrowRight, AlertTriangle } from 'lucide-react';
import { verifySovereignBridge } from '../sovereignBridge';
import type { SovereignBridgeStatus } from '../types';

interface AlpacaConnectModalProps {
  isOpen: boolean;
  onClose: () => void;
  isConnected: boolean;
  onConnectSuccess: (status: SovereignBridgeStatus) => void;
  onDisconnect: () => void;
}

export const AlpacaConnectModal: React.FC<AlpacaConnectModalProps> = ({
  isOpen,
  onClose,
  isConnected,
  onConnectSuccess,
  onDisconnect
}) => {
  const [isVerifying, setIsVerifying] = useState(false);
  const [verificationMessage, setVerificationMessage] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleVerify = async () => {
    setIsVerifying(true);
    setVerificationMessage(null);

    const result = await verifySovereignBridge();
    setIsVerifying(false);

    if ('message' in result) {
      setVerificationMessage(result.message);
      return;
    }

    onConnectSuccess(result.status);
    onClose();
  };

  const handleDisconnect = () => {
    onDisconnect();
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.95 }}
        className="relative w-full max-w-md bg-[#0e0e12] border border-[#d4af37]/40 rounded-3xl shadow-2xl overflow-hidden font-sans"
      >
        <div className="p-5 border-b border-[#27272a] flex items-center justify-between bg-[#121216]">
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-full border border-[#d4af37] flex items-center justify-center bg-[#18181b]">
              <Shield className="w-3.5 h-3.5 text-[#e5c158]" />
            </div>
            <div>
              <h3 className="text-base font-serif text-zinc-100">Sovereign Alpaca Bridge</h3>
              <p className="text-[10px] font-mono text-zinc-400">Receipt-bound • Paper-only • Backend-gated</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-xl bg-[#18181b] text-zinc-400 hover:text-white border border-[#27272a] cursor-pointer"
            aria-label="Close bridge dialog"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="p-5 space-y-4 text-xs">
          {isConnected ? (
            <div className="space-y-4">
              <div className="p-4 rounded-2xl bg-[#d4af37]/10 border border-[#d4af37]/45 text-[#fef08a] space-y-2">
                <div className="flex items-center gap-2 font-mono font-semibold">
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Sovereign paper bridge verified</span>
                </div>
                <p className="text-[11px] text-zinc-300 leading-relaxed">
                  LEFA has accepted a valid backend bridge-status contract. This does not mean a trade is approved and it does not grant browser execution authority.
                </p>
              </div>

              <div className="p-3 rounded-xl bg-[#121216] border border-[#27272a] font-mono text-[11px] space-y-1.5">
                <div className="flex justify-between gap-4 text-zinc-400">
                  <span>Provider:</span>
                  <span className="text-zinc-200">Alpaca</span>
                </div>
                <div className="flex justify-between gap-4 text-zinc-400">
                  <span>Environment:</span>
                  <span className="text-[#e5c158]">PAPER ONLY</span>
                </div>
                <div className="flex justify-between gap-4 text-zinc-400">
                  <span>Execution authority:</span>
                  <span className="text-zinc-200">BACKEND ONLY</span>
                </div>
                <div className="flex justify-between gap-4 text-zinc-400">
                  <span>Decision truth:</span>
                  <span className="text-zinc-200">KC receipt</span>
                </div>
              </div>

              <button
                onClick={handleDisconnect}
                className="w-full py-2.5 rounded-xl bg-[#18181b] border border-[#3f3f46] text-zinc-300 font-mono text-xs hover:border-[#d4af37]/60 transition-colors cursor-pointer"
              >
                Disconnect LEFA View
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="p-4 rounded-2xl bg-[#121216] border border-[#27272a] space-y-3">
                <div className="flex items-start gap-2.5">
                  <Lock className="w-4 h-4 mt-0.5 text-[#e5c158] shrink-0" />
                  <div>
                    <div className="font-mono text-[#fef08a] text-[11px]">No Alpaca credentials belong in this browser.</div>
                    <p className="mt-1 text-[10px] leading-relaxed text-zinc-400">
                      LEFA verifies a governed backend status receipt only. Alpaca credentials, account telemetry, risk evaluation and order routing remain behind the sovereign execution boundary.
                    </p>
                  </div>
                </div>
              </div>

              <div className="p-3 rounded-xl bg-[#121216] border border-[#27272a] font-mono text-[10px] space-y-1.5 text-zinc-400">
                <div className="flex justify-between gap-4">
                  <span>Required schema:</span>
                  <span className="text-zinc-200 text-right">kopano.lefa.sovereign-bridge-status.v1</span>
                </div>
                <div className="flex justify-between gap-4">
                  <span>Provider:</span>
                  <span className="text-zinc-200">alpaca</span>
                </div>
                <div className="flex justify-between gap-4">
                  <span>Environment:</span>
                  <span className="text-[#e5c158]">paper</span>
                </div>
                <div className="flex justify-between gap-4">
                  <span>Execution:</span>
                  <span className="text-zinc-200">BACKEND_ONLY</span>
                </div>
              </div>

              {verificationMessage && (
                <div className="p-3 rounded-xl bg-[#d97706]/10 border border-[#d97706]/50 text-[10px] text-[#fbbf24] font-mono flex items-start gap-2">
                  <AlertTriangle className="w-3.5 h-3.5 mt-0.5 shrink-0" />
                  <span>{verificationMessage}</span>
                </div>
              )}

              <button
                type="button"
                onClick={handleVerify}
                disabled={isVerifying}
                className="w-full py-3 rounded-xl bg-gradient-to-r from-[#d4af37] via-[#e5c158] to-[#c5a059] disabled:opacity-50 text-black font-semibold text-xs font-mono hover:brightness-110 active:scale-[0.98] transition-all cursor-pointer flex items-center justify-center gap-2 shadow-lg shadow-[#d4af37]/20"
              >
                {isVerifying ? (
                  <span>Verifying sovereign receipt boundary…</span>
                ) : (
                  <>
                    <span>Verify Paper Bridge</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>

              <p className="text-center text-[9px] font-mono text-zinc-500 leading-relaxed">
                No configured endpoint or invalid receipt = disconnected. There is no simulated success path.
              </p>
            </div>
          )}
        </div>

        <div className="p-3.5 border-t border-[#27272a] bg-[#121216] text-[10px] font-mono text-zinc-500 text-center">
          Alpaca AI Trading Agents Hackathon • Built in South Africa • Receipt or HOLD
        </div>
      </motion.div>
    </div>
  );
};
