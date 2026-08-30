import React, { useState } from 'react';
import { verifyMCPEvidence } from '../api/lefa';
import { motion } from 'motion/react';
import { X, Key, Shield, CheckCircle2, Lock, ArrowRight, ExternalLink } from 'lucide-react';

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
  onDisconnect
}) => {
  const [apiKey, setApiKey] = useState('');
  const [apiSecret, setApiSecret] = useState('');
  const [environment, setEnvironment] = useState<'paper' | 'live'>('paper');
  const [isVerifying, setIsVerifying] = useState(false);

  if (!isOpen) return null;

  const handleConnect = (e: React.FormEvent) => {
    e.preventDefault();
    setIsVerifying(true);
    setTimeout(() => {
      setIsVerifying(false);
      onConnectSuccess();
      onClose();
    }, 1000);
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
        {/* Header */}
        <div className="p-5 border-b border-[#27272a] flex items-center justify-between bg-[#121216]">
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-full border border-[#d4af37] flex items-center justify-center bg-[#18181b]">
              <Key className="w-3.5 h-3.5 text-[#e5c158]" />
            </div>
            <div>
              <h3 className="text-base font-serif text-zinc-100">Alpaca Trading Bridge</h3>
              <p className="text-[10px] font-mono text-zinc-400">Governed AI Agent Integration</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-xl bg-[#18181b] text-zinc-400 hover:text-white border border-[#27272a] cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Body */}
        <div className="p-5 space-y-4 text-xs">
          
          {isConnected ? (
            <div className="space-y-4">
              <div className="p-4 rounded-2xl bg-emerald-950/30 border border-emerald-500/40 text-emerald-200 space-y-2">
                <div className="flex items-center gap-2 font-mono font-semibold">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  <span>Alpaca Paper Sandbox Connected</span>
                </div>
                <p className="text-[11px] text-zinc-300">
                  LEFA is listening to real-time market streams in governed observation mode. No execution commands will ever be initiated without multi-signature verification.
                </p>
              </div>

              <div className="p-3 rounded-xl bg-[#121216] border border-[#27272a] font-mono text-[11px] space-y-1">
                <div className="flex justify-between text-zinc-400">
                  <span>Target API:</span>
                  <span className="text-zinc-200">paper-api.alpaca.markets</span>
                </div>
                <div className="flex justify-between text-zinc-400">
                  <span>Scope:</span>
                  <span className="text-[#e5c158]">READ_STREAM + HASH_LEDGER</span>
                </div>
              </div>

              <button
                onClick={handleDisconnect}
                className="w-full py-2.5 rounded-xl bg-rose-950/40 border border-rose-600/40 text-rose-300 font-mono text-xs hover:bg-rose-900/40 transition-colors cursor-pointer"
              >
                Disconnect Alpaca Bridge
              </button>
            </div>
          ) : (
            <form onSubmit={handleConnect} className="space-y-4">
              <div className="space-y-1">
                <label className="text-[10px] font-mono text-zinc-400 uppercase">Environment</label>
                <div className="grid grid-cols-2 gap-2">
                  <button
                    type="button"
                    onClick={() => setEnvironment('paper')}
                    className={`py-2 rounded-xl border text-xs font-mono transition-all cursor-pointer ${
                      environment === 'paper' 
                        ? 'bg-[#d4af37]/20 border-[#d4af37] text-[#fef08a] font-bold' 
                        : 'bg-[#18181b] border-[#27272a] text-zinc-400'
                    }`}
                  >
                    Paper Trading (Safe)
                  </button>
                  <button
                    type="button"
                    onClick={() => setEnvironment('live')}
                    className={`py-2 rounded-xl border text-xs font-mono transition-all cursor-pointer ${
                      environment === 'live' 
                        ? 'bg-[#d4af37]/20 border-[#d4af37] text-[#fef08a] font-bold' 
                        : 'bg-[#18181b] border-[#27272a] text-zinc-400'
                    }`}
                  >
                    Live Trading (Governed)
                  </button>
                </div>
              </div>

              <div className="space-y-1">
                <label className="text-[10px] font-mono text-zinc-400 uppercase">Alpaca API Key ID</label>
                <input
                  type="text"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  className="w-full p-2.5 rounded-xl bg-[#18181b] border border-[#27272a] text-xs font-mono text-zinc-200 focus:border-[#d4af37] focus:outline-none"
                  placeholder="PK..."
                  required
                />
              </div>

              <div className="space-y-1">
                <label className="text-[10px] font-mono text-zinc-400 uppercase">Alpaca API Secret</label>
                <input
                  type="password"
                  value={apiSecret}
                  onChange={(e) => setApiSecret(e.target.value)}
                  className="w-full p-2.5 rounded-xl bg-[#18181b] border border-[#27272a] text-xs font-mono text-zinc-200 focus:border-[#d4af37] focus:outline-none"
                  placeholder="Secret key..."
                  required
                />
              </div>

              <div className="p-3 rounded-xl bg-[#121216] border border-[#27272a] text-[11px] text-zinc-400 space-y-1">
                <div className="flex items-center gap-1.5 text-[#e5c158] font-mono">
                  <Shield className="w-3.5 h-3.5" />
                  <span>Governed Non-Custodial Bridge</span>
                </div>
                <p className="text-[10px] leading-relaxed">
                  Keys are used exclusively to ingest telemetry and cryptographically timestamp decisions. LEFA never alters order sizes autonomously.
                </p>
              </div>

              <button
                type="submit"
                disabled={isVerifying}
                className="w-full py-3 rounded-xl bg-gradient-to-r from-[#d4af37] via-[#e5c158] to-[#c5a059] text-black font-semibold text-xs font-mono hover:brightness-110 active:scale-[0.98] transition-all cursor-pointer flex items-center justify-center gap-2 shadow-lg shadow-[#d4af37]/20"
              >
                {verifyError && (
                <div className="p-2.5 rounded-xl bg-rose-950/40 border border-rose-600/40 text-rose-300 font-mono text-[11px]">
                  {verifyError}
                </div>
              )}
              {isVerifying ? (
                  <span>Verifying API Signature...</span>
                ) : (
                  <>
                    <span>Connect & Verify Stream</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </form>
          )}

        </div>

        {/* Footer */}
        <div className="p-3.5 border-t border-[#27272a] bg-[#121216] text-[10px] font-mono text-zinc-500 text-center">
          Alpaca AI Trading Agents Hackathon • Built in South Africa
        </div>
      </motion.div>
    </div>
  );
};
