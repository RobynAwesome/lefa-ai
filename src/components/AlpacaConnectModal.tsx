import React, { useEffect, useState } from 'react';
import { motion } from 'motion/react';
import {
  AlertCircle,
  CheckCircle2,
  LoaderCircle,
  ShieldCheck,
  X,
} from 'lucide-react';
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
  onDisconnect,
}) => {
  const [isVerifying, setIsVerifying] = useState(false);
  const [verificationMessage, setVerificationMessage] = useState<string | null>(null);

  const handleVerify = async () => {
    setIsVerifying(true);
    setVerificationMessage(null);

    const result = await verifySovereignBridge();
    setIsVerifying(false);

    if (!result.ok) {
      setVerificationMessage(result.message);
      return;
    }

    onConnectSuccess(result.status);
  };

  useEffect(() => {
    if (!isOpen || isConnected) return;
    void handleVerify();
    // Connection truth is checked once when the experience opens.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isOpen, isConnected]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
      <motion.div
        initial={{ opacity: 0, y: 12, scale: 0.98 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        exit={{ opacity: 0, y: 8, scale: 0.98 }}
        className="relative w-full max-w-sm overflow-hidden rounded-[28px] border border-[#d4af37]/30 bg-[#0d0d11] shadow-2xl"
      >
        <button
          onClick={onClose}
          className="absolute right-4 top-4 z-10 rounded-full border border-white/10 bg-white/5 p-2 text-zinc-400 transition hover:text-white"
          aria-label="Close"
        >
          <X className="h-4 w-4" />
        </button>

        <div className="px-6 pb-7 pt-8 text-center">
          {isConnected ? (
            <>
              <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-full border border-emerald-400/30 bg-emerald-400/10">
                <CheckCircle2 className="h-7 w-7 text-emerald-300" />
              </div>
              <p className="mb-1 text-[11px] font-medium uppercase tracking-[0.24em] text-emerald-300/80">
                Connected
              </p>
              <h3 className="font-serif text-2xl text-zinc-50">Alpaca is ready</h3>
              <p className="mx-auto mt-3 max-w-[280px] text-sm leading-6 text-zinc-400">
                Paper trading is connected. LEFA keeps the sensitive work protected in the background.
              </p>

              <button
                onClick={onClose}
                className="mt-7 w-full rounded-2xl bg-gradient-to-r from-[#d4af37] via-[#e5c158] to-[#c5a059] px-4 py-3.5 text-sm font-semibold text-black transition hover:brightness-110 active:scale-[0.99]"
              >
                Continue
              </button>
              <button
                onClick={() => {
                  onDisconnect();
                  onClose();
                }}
                className="mt-3 text-xs text-zinc-500 transition hover:text-zinc-300"
              >
                Disconnect
              </button>
            </>
          ) : isVerifying ? (
            <>
              <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-full border border-[#d4af37]/25 bg-[#d4af37]/10">
                <LoaderCircle className="h-7 w-7 animate-spin text-[#e5c158]" />
              </div>
              <p className="mb-1 text-[11px] font-medium uppercase tracking-[0.24em] text-[#e5c158]/80">
                Connecting
              </p>
              <h3 className="font-serif text-2xl text-zinc-50">Checking Alpaca</h3>
              <p className="mx-auto mt-3 max-w-[280px] text-sm leading-6 text-zinc-400">
                LEFA is securely checking your paper-trading connection.
              </p>
            </>
          ) : (
            <>
              <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-full border border-amber-400/25 bg-amber-400/10">
                <AlertCircle className="h-7 w-7 text-amber-300" />
              </div>
              <p className="mb-1 text-[11px] font-medium uppercase tracking-[0.24em] text-amber-300/80">
                Not ready yet
              </p>
              <h3 className="font-serif text-2xl text-zinc-50">Connection needs setup</h3>
              <p className="mx-auto mt-3 max-w-[280px] text-sm leading-6 text-zinc-400">
                {verificationMessage ?? 'LEFA is keeping this connection safe until setup is complete.'}
              </p>

              <button
                type="button"
                onClick={() => void handleVerify()}
                className="mt-7 w-full rounded-2xl bg-gradient-to-r from-[#d4af37] via-[#e5c158] to-[#c5a059] px-4 py-3.5 text-sm font-semibold text-black transition hover:brightness-110 active:scale-[0.99]"
              >
                Try again
              </button>
              <button
                onClick={onClose}
                className="mt-3 text-xs text-zinc-500 transition hover:text-zinc-300"
              >
                Continue for now
              </button>
            </>
          )}
        </div>

        <div className="flex items-center justify-center gap-2 border-t border-white/5 bg-white/[0.02] px-4 py-3 text-[10px] text-zinc-600">
          <ShieldCheck className="h-3.5 w-3.5" />
          <span>Paper trading only • protected by LEFA</span>
        </div>
      </motion.div>
    </div>
  );
};
