import React, { useState } from 'react';
import { getMCPStatus } from '../api/lefa';
import { motion } from 'motion/react';
import { ArrowRight, CheckCircle2, Key, Shield, X } from 'lucide-react';

interface AlpacaConnectModalProps {
  isOpen: boolean;
  onClose: () => void;
  isConnected: boolean;
  onConnectSuccess: () => void;
  onDisconnect: () => void;
}

export const AlpacaConnectModal: React.FC<AlpacaConnectModalProps> = ({
  isOpen,
  onClose,
  isConnected,
  onConnectSuccess,
  onDisconnect,
}) => {
  const [isVerifying, setIsVerifying] = useState(false);
  const [verifyError, setVerifyError] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleConnect = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsVerifying(true);
    setVerifyError(null);

    try {
      const proof = await getMCPStatus();
      if (proof.status !== 'ready') {
        const details = proof.failures.length
          ? proof.failures.join(', ')
          : 'runtime_evidence_unavailable';
        setVerifyError(
          `Alpaca paper runtime proof is not ready: ${details}. Configure credentials locally and run governed MCP discovery first.`,
        );
        return;
      }

      onConnectSuccess();
      onClose();
    } catch (error) {
      setVerifyError(
        error instanceof Error
          ? error.message
          : 'Unable to verify the Alpaca paper runtime proof.',
      );
    } finally {
      setIsVerifying(false);
    }
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
              <Key className="w-3.5 h-3.5 text-[#e5c158]" />
            </div>
            <div>
              <h3 className="text-base font-serif text-zinc-100">Alpaca Observation Bridge</h3>
              <p className="text-[10px] font-mono text-zinc-400">Governed paper-runtime proof gate</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-xl bg-[#18181b] text-zinc-400 hover:text-white border border-[#27272a] cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="p-5 space-y-4 text-xs">
          {isConnected ? (
            <div className="space-y-4">
              <div className="p-4 rounded-2xl bg-emerald-950/30 border border-emerald-500/40 text-emerald-200 space-y-2">
                <div className="flex items-center gap-2 font-mono font-semibold">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  <span>Alpaca Paper Runtime Proof Ready</span>
                </div>
                <p className="text-[11px] text-zinc-300">
                  LEFA may enter governed read-only observation mode. This UI does not possess order or execution authority.
                </p>
              </div>

              <button
                onClick={handleDisconnect}
                className="w-full py-2.5 rounded-xl bg-rose-950/40 border border-rose-600/40 text-rose-300 font-mono text-xs hover:bg-rose-900/40 transition-colors cursor-pointer"
              >
                Leave Observation Mode
              </button>
            </div>
          ) : (
            <form onSubmit={handleConnect} className="space-y-4">
              <div className="p-4 rounded-2xl bg-[#121216] border border-[#27272a] space-y-3">
                <div className="flex items-center gap-2 text-[#e5c158] font-mono font-semibold">
                  <Shield className="w-4 h-4" />
                  <span>Credentials stay local</span>
                </div>
                <p className="text-[11px] leading-relaxed text-zinc-300">
                  LEFA never asks the browser to hold your Alpaca API key or secret. Configure paper credentials in the local runtime, run MCP discovery, then return here to check the sanitized proof.
                </p>
                <div className="rounded-xl border border-[#d4af37]/20 bg-black/20 p-3 font-mono text-[10px] text-zinc-400">
                  Issue #2 remains HOLD until namespace, paper mode, readable tools, network, auth and schema evidence are witnessed by the backend.
                </div>
              </div>

              {verifyError && (
                <div className="p-3 rounded-xl bg-amber-950/30 border border-amber-600/40 text-amber-200 font-mono text-[11px] leading-relaxed">
                  {verifyError}
                </div>
              )}

              <button
                type="submit"
                disabled={isVerifying}
                className="w-full py-3 rounded-xl bg-gradient-to-r from-[#d4af37] via-[#e5c158] to-[#c5a059] text-black font-semibold text-xs font-mono hover:brightness-110 active:scale-[0.98] transition-all cursor-pointer flex items-center justify-center gap-2 shadow-lg shadow-[#d4af37]/20 disabled:opacity-60 disabled:cursor-wait"
              >
                {isVerifying ? (
                  <span>Checking Governed Runtime Proof...</span>
                ) : (
                  <>
                    <span>Check Paper Runtime Proof</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </form>
          )}
        </div>

        <div className="p-3.5 border-t border-[#27272a] bg-[#121216] text-[10px] font-mono text-zinc-500 text-center">
          Alpaca AI Trading Agents Hackathon • Built in South Africa
        </div>
      </motion.div>
    </div>
  );
};
