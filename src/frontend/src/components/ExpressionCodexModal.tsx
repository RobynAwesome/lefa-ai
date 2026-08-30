import React, { useState } from 'react';
import { motion } from 'motion/react';
import { X, Sparkles, AlertCircle, CheckCircle2, ShieldCheck, Heart } from 'lucide-react';
import { LEFA_KAOMOJI_EXPRESSIONS } from '../data/expressionGrammar';
import { CompanionAvatar } from './CompanionAvatar';
import { SystemState } from '../types';

interface ExpressionCodexModalProps {
  isOpen: boolean;
  onClose: () => void;
  currentState: SystemState;
  onPreviewKaomoji: (k: string) => void;
}

export const ExpressionCodexModal: React.FC<ExpressionCodexModalProps> = ({
  isOpen,
  onClose,
  currentState,
  onPreviewKaomoji
}) => {
  const [selectedKaomoji, setSelectedKaomoji] = useState(LEFA_KAOMOJI_EXPRESSIONS[0]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md overflow-y-auto">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.95 }}
        className="relative w-full max-w-4xl bg-[#0e0e12] border border-[#d4af37]/40 rounded-3xl shadow-2xl overflow-hidden my-8"
      >
        {/* Header */}
        <div className="p-6 border-b border-[#27272a] flex items-center justify-between bg-[#121216]">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full border border-[#d4af37] flex items-center justify-center bg-[#18181b]">
              <Sparkles className="w-4 h-4 text-[#e5c158]" />
            </div>
            <div>
              <h2 className="text-xl font-serif text-[#f4f4f5]">
                Candidate LEFA Expression Grammar
              </h2>
              <p className="text-xs text-zinc-400 font-mono">
                Micro-interaction state signatures & truthful emotional telemetry
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 rounded-xl bg-[#18181b] text-zinc-400 hover:text-white border border-[#27272a] cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 space-y-6 max-h-[75vh] overflow-y-auto font-sans">
          
          {/* Strict Non-Profit Guardrail Directive Banner */}
          <div className="p-4 rounded-2xl bg-[#18181b] border-l-4 border-[#d4af37] space-y-1.5 text-xs">
            <div className="flex items-center gap-2 font-mono text-[#fef08a] font-semibold">
              <ShieldCheck className="w-4 h-4 text-[#d4af37]" />
              <span>THE TRUTH GUARDRAIL (NON-NEGOTIABLE):</span>
            </div>
            <p className="text-zinc-300 leading-relaxed">
              An expression may <strong>never</strong> imply investment performance unless actual backend evidence supports that outcome. A delighted LEFA represents <em>"connection successful," "receipt preserved,"</em> or <em>"validation completed"</em>—never artificial financial hype.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            {/* Left Column: Kaomoji Selector List */}
            <div className="space-y-2 md:col-span-1 border-r border-[#27272a]/80 pr-4">
              <span className="text-[11px] font-mono text-zinc-500 uppercase tracking-wider block mb-2">
                Candidate Symbols:
              </span>
              <div className="space-y-1.5 max-h-[380px] overflow-y-auto pr-1">
                {LEFA_KAOMOJI_EXPRESSIONS.map((expr) => {
                  const isSelected = selectedKaomoji.symbol === expr.symbol;
                  return (
                    <button
                      key={expr.symbol}
                      onClick={() => {
                        setSelectedKaomoji(expr);
                        onPreviewKaomoji(expr.symbol);
                      }}
                      className={`w-full p-2.5 rounded-xl border text-left flex items-center justify-between font-mono text-xs transition-all cursor-pointer ${
                        isSelected 
                          ? 'bg-[#d4af37]/20 border-[#d4af37] text-[#fef08a] font-bold shadow-sm'
                          : 'bg-[#121216] border-[#27272a] text-zinc-300 hover:border-zinc-500'
                      }`}
                    >
                      <span className="truncate">{expr.symbol}</span>
                      <span className="text-[10px] text-zinc-500 font-sans">{expr.name.split(' ')[0]}</span>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Right Columns: Live Avatar & Semantic Breakdown */}
            <div className="md:col-span-2 space-y-4">
              
              {/* Interactive Live Avatar Preview */}
              <div className="p-4 rounded-2xl bg-[#121216] border border-[#27272a] flex flex-col sm:flex-row items-center gap-6">
                <div className="shrink-0">
                  <CompanionAvatar 
                    state={currentState} 
                    size="md" 
                    customKaomoji={selectedKaomoji.symbol} 
                  />
                </div>
                <div className="space-y-1.5 text-center sm:text-left">
                  <span className="text-[10px] font-mono text-[#d4af37] uppercase">Current Active Preview</span>
                  <h4 className="text-lg font-serif text-zinc-100 font-medium">
                    {selectedKaomoji.name}
                  </h4>
                  <div className="inline-block px-3 py-1 rounded-lg bg-[#18181b] border border-[#d4af37]/40 font-mono text-sm text-[#fef08a] font-bold">
                    {selectedKaomoji.symbol}
                  </div>
                </div>
              </div>

              {/* Semantic Analysis Details */}
              <div className="p-4 rounded-2xl bg-[#14120e] border border-[#27272a] space-y-3 text-xs">
                <div>
                  <span className="text-[10px] font-mono text-zinc-500 uppercase block mb-1">Semantic Meaning:</span>
                  <p className="text-zinc-200 leading-relaxed font-serif">
                    {selectedKaomoji.semanticMeaning}
                  </p>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2 border-t border-[#27272a]">
                  <div className="p-2.5 rounded-xl bg-[#18181b] border border-[#27272a] space-y-1">
                    <span className="text-[10px] font-mono text-emerald-400 block font-semibold">
                      ✓ ALLOWED USAGE:
                    </span>
                    <p className="text-zinc-300 text-[11px] leading-relaxed">
                      {selectedKaomoji.allowedContext}
                    </p>
                  </div>

                  <div className="p-2.5 rounded-xl bg-[#18181b] border border-[#27272a] space-y-1">
                    <span className="text-[10px] font-mono text-rose-400 block font-semibold">
                      ✕ FORBIDDEN USAGE:
                    </span>
                    <p className="text-zinc-300 text-[11px] leading-relaxed">
                      {selectedKaomoji.forbiddenContext}
                    </p>
                  </div>
                </div>
              </div>

            </div>

          </div>

        </div>

        {/* Footer */}
        <div className="p-4 border-t border-[#27272a] bg-[#121216] flex items-center justify-between text-xs font-mono">
          <span className="text-zinc-500">Emotional telemetry grounded in backend reality</span>
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-[#d4af37] text-black font-semibold hover:bg-[#e5c158] cursor-pointer"
          >
            Done Exploring
          </button>
        </div>

      </motion.div>
    </div>
  );
};
