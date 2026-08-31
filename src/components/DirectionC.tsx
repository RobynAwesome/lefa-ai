import React, { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { MessageSquare, Send, Sparkles, Mic, ShieldAlert, FileCode2, ArrowRight, CornerDownLeft, Lock, Key } from 'lucide-react';
import { SystemState, ViewportMode } from '../types';
import { CompanionAvatar } from './CompanionAvatar';
import { MOCK_OBSERVATION, MOCK_LEDGER_RECEIPT, MOCK_HOLD_RATIONALE, MOCK_REVEAL_DATA } from '../data/expressionGrammar';

interface DirectionCProps {
  state: SystemState;
  onStateChange: (state: SystemState) => void;
  viewportMode: ViewportMode;
  onOpenConnectModal: () => void;
  isAlpacaConnected: boolean;
  reducedMotion: boolean;
}

export const DirectionC: React.FC<DirectionCProps> = ({
  state,
  onStateChange,
  viewportMode,
  onOpenConnectModal,
  isAlpacaConnected,
  reducedMotion
}) => {
  const [inputQuery, setInputQuery] = useState('');
  const [activeTab, setActiveTab] = useState<'dialogue' | 'evidence'>('dialogue');

  const samplePrompts = [
    { label: 'Sense current market regime', targetState: 'observing' as SystemState, query: 'What signals are you observing across our universe right now?' },
    { label: 'Audit preserved thesis receipt', targetState: 'ledgered' as SystemState, query: 'Show me the immutable ledger receipt for our current thesis.' },
    { label: 'Why are we in a HOLD state?', targetState: 'hold' as SystemState, query: 'Explain the governance rationale behind our current HOLD status.' },
    { label: 'Reveal Then-vs-Now truth', targetState: 'reveal' as SystemState, query: 'Compare our original thesis with realized market outcome today.' },
  ];

  const handlePromptClick = (p: typeof samplePrompts[0]) => {
    setInputQuery(p.query);
    onStateChange(p.targetState);
  };

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputQuery.trim()) return;
    // Simple state mapping from user query keywords if custom
    const lower = inputQuery.toLowerCase();
    if (lower.includes('hold') || lower.includes('wait') || lower.includes('risk')) {
      onStateChange('hold');
    } else if (lower.includes('receipt') || lower.includes('ledger') || lower.includes('preserve')) {
      onStateChange('ledgered');
    } else if (lower.includes('reveal') || lower.includes('outcome') || lower.includes('truth') || lower.includes('then')) {
      onStateChange('reveal');
    } else {
      onStateChange('observing');
    }
  };

  return (
    <div 
      className={`relative w-full min-h-[680px] bg-[#0b0b0e] text-[#f4f4f5] font-sans flex flex-col justify-between overflow-hidden rounded-2xl border border-[#27272a] shadow-2xl ${
        viewportMode === 'mobile' ? 'max-w-[390px] mx-auto' : 'w-full'
      }`}
      id="direction-c-surface"
    >
      {/* Top Header */}
      <header className="relative z-10 px-6 pt-5 pb-3 flex items-center justify-between border-b border-[#27272a]/60 bg-[#0b0b0e]/90 backdrop-blur-md">
        <div className="flex items-center gap-2.5">
          <div className="w-6 h-6 rounded-full border border-[#d4af37]/60 flex items-center justify-center bg-[#121216]">
            <MessageSquare className="w-3.5 h-3.5 text-[#e5c158]" />
          </div>
          <div>
            <span className="text-xs font-semibold tracking-wider font-mono text-[#e5c158] uppercase">LEFA AI</span>
            <span className="text-[10px] text-zinc-500 block leading-tight">Conversational Control Room</span>
          </div>
        </div>

        <button 
          onClick={onOpenConnectModal}
          className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-[#18181b] border border-[#27272a] hover:border-[#d4af37]/50 transition-colors text-[11px] font-mono text-zinc-300 cursor-pointer"
        >
          <span className={`w-1.5 h-1.5 rounded-full ${isAlpacaConnected ? 'bg-[#e5c158]' : 'bg-zinc-500'}`} />
          <span>{isAlpacaConnected ? 'Voice/API Live' : 'Connect Alpaca'}</span>
        </button>
      </header>

      {/* Main Conversation Stream with Companion Presence */}
      <main className="relative z-10 flex-1 flex flex-col px-6 py-4 overflow-y-auto">
        
        {/* Compact Companion Anchor in Top Bar */}
        <div className="flex items-center justify-between p-3 rounded-xl bg-[#121216]/80 border border-[#27272a] mb-4">
          <div className="flex items-center gap-3">
            <CompanionAvatar 
              state={state} 
              size="sm" 
              showKaomojiBadge={false} 
              reducedMotion={reducedMotion}
            />
            <div>
              <span className="text-xs font-serif font-medium text-zinc-200">LEFA</span>
              <span className="text-[10px] font-mono text-zinc-400 block">
                {state === 'disconnected' && 'Awaiting authentication (●\'◡\'●)'}
                {state === 'observing' && 'Observing stream… +_+'}
                {state === 'ledgered' && 'Preserved & signed (●\'◡\'●)'}
                {state === 'hold' && 'Holding this one. U_U'}
                {state === 'reveal' && 'Truth revealed. (❁´◡`❁)'}
              </span>
            </div>
          </div>

          <div className="text-right">
            <span className="text-[10px] font-mono text-[#d4af37] bg-[#d4af37]/10 px-2 py-0.5 rounded border border-[#d4af37]/20">
              Governed Agent
            </span>
          </div>
        </div>

        {/* Dialogue Stream */}
        <div className="space-y-4 flex-1">
          
          {/* System Greeting or First-use */}
          {state === 'disconnected' ? (
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-3"
            >
              <div className="p-4 rounded-2xl bg-[#18181b] border border-[#27272a] text-xs space-y-2 text-zinc-300">
                <p className="font-serif text-sm text-[#f4f4f5]">
                  "Greetings. I am LEFA, your companion for governed financial intelligence."
                </p>
                <p className="text-zinc-400 text-[11px] leading-relaxed">
                  I operate strictly under the law of <strong>Observe → Ledger → Reveal</strong>. Connect your Alpaca Paper Trading account to begin governed telemetry intake.
                </p>
              </div>

              <div className="p-3 rounded-xl bg-[#121216] border border-[#27272a] flex items-center justify-between">
                <span className="text-[11px] font-mono text-zinc-400">Authentication Required</span>
                <button
                  onClick={onOpenConnectModal}
                  className="px-3 py-1.5 rounded-lg bg-[#e5c158] text-black font-mono text-xs font-semibold flex items-center gap-1.5 cursor-pointer hover:bg-[#fef08a]"
                >
                  <Key className="w-3.5 h-3.5" />
                  <span>Connect Alpaca</span>
                </button>
              </div>
            </motion.div>
          ) : (
            <div className="space-y-3">
              
              {/* User Mock Message */}
              <div className="flex justify-end">
                <div className="max-w-[85%] p-3 rounded-2xl rounded-tr-none bg-[#27272a] text-xs text-zinc-100 font-sans">
                  {inputQuery || (
                    state === 'observing' ? 'What signals are you observing across our universe right now?' :
                    state === 'ledgered' ? 'Show me the immutable ledger receipt for our current thesis.' :
                    state === 'hold' ? 'Explain the governance rationale behind our current HOLD status.' :
                    'Compare our original thesis with realized market outcome today.'
                  )}
                </div>
              </div>

              {/* LEFA Response with Inline Governed Evidence Card */}
              <div className="flex justify-start">
                <div className="max-w-[95%] space-y-2">
                  
                  {/* Speech Bubble */}
                  <div className="p-3.5 rounded-2xl rounded-tl-none bg-[#141418] border border-[#27272a] text-xs text-zinc-300 space-y-1.5">
                    <div className="flex items-center gap-2 font-mono text-[10px] text-[#e5c158]">
                      <span>LEFA COMPANION</span>
                      <span>•</span>
                      <span>
                        {state === 'observing' && 'Observing… +_+'}
                        {state === 'ledgered' && 'Preserved. (●\'◡\'●)'}
                        {state === 'hold' && 'Need more evidence. ¬_¬'}
                        {state === 'reveal' && 'Revealed truthfully. (❁´◡`❁)'}
                      </span>
                    </div>

                    <p className="leading-relaxed text-zinc-200">
                      {state === 'observing' && "I am actively sensing cross-asset volatility and order-book depth for NVDA. Here is the sensory surface—zero execution authority is being asserted:"}
                      {state === 'ledgered' && "I have committed the current thesis to an immutable cryptographic block. Here is your permanent receipt artifact:"}
                      {state === 'hold' && "I have enforced a governed HOLD on all execution. Action without clarity is gambling. Here is the risk gate telemetry:"}
                      {state === 'reveal' && "Time has elapsed. Comparing what we preserved at T₀ with realized price action reveals that our HOLD averted a 3.2% flash drawdown:"}
                    </p>
                  </div>

                  {/* Inline Governed Evidence Surface */}
                  <div className="p-3 rounded-xl bg-[#09090b] border border-[#d4af37]/30 space-y-2">
                    
                    {state === 'observing' && (
                      <div className="space-y-1.5 text-xs font-mono">
                        <div className="flex justify-between text-zinc-400 border-b border-[#27272a] pb-1 text-[10px]">
                          <span>SIGNAL SURFACE</span>
                          <span className="text-[#e5c158]">{MOCK_OBSERVATION.symbol}</span>
                        </div>
                        {MOCK_OBSERVATION.sensedSignals.map((s, i) => (
                          <div key={i} className="flex justify-between text-[11px]">
                            <span className="text-zinc-500">{s.label}:</span>
                            <span className="text-zinc-300">{s.value}</span>
                          </div>
                        ))}
                      </div>
                    )}

                    {state === 'ledgered' && (
                      <div className="space-y-1 text-xs font-mono">
                        <div className="flex items-center justify-between text-[10px] text-[#e5c158] border-b border-[#27272a] pb-1">
                          <span className="flex items-center gap-1"><Lock className="w-3 h-3" /> RECEIPT BLOCK</span>
                          <span>{MOCK_LEDGER_RECEIPT.receiptId}</span>
                        </div>
                        <p className="text-[11px] text-zinc-300 italic pt-1 font-serif">"{MOCK_LEDGER_RECEIPT.observedThesis}"</p>
                        <div className="text-[10px] text-zinc-500 pt-1">
                          SHA256: <span className="text-[#e5c158]">{MOCK_LEDGER_RECEIPT.hash}</span>
                        </div>
                      </div>
                    )}

                    {state === 'hold' && (
                      <div className="space-y-1.5 text-xs font-mono">
                        <div className="flex items-center justify-between text-[10px] text-[#fbbf24] border-b border-[#27272a] pb-1">
                          <span>RISK GATE ACTIVE (HOLD)</span>
                          <span>Score: {MOCK_HOLD_RATIONALE.uncertaintyScore}/100</span>
                        </div>
                        <p className="text-[11px] text-zinc-300">{MOCK_HOLD_RATIONALE.reason}</p>
                        <div className="p-1.5 rounded bg-[#18181b] text-[10px] text-amber-200/90">
                          {MOCK_HOLD_RATIONALE.companionThought}
                        </div>
                      </div>
                    )}

                    {state === 'reveal' && (
                      <div className="space-y-1.5 text-xs font-mono">
                        <div className="flex items-center justify-between text-[10px] text-[#fef08a] border-b border-[#27272a] pb-1">
                          <span>TRUTH COMPARISON</span>
                          <span>THEN vs NOW</span>
                        </div>
                        <div className="text-[11px] text-zinc-300">
                          <span className="text-zinc-500">Realized Path: </span>
                          {MOCK_REVEAL_DATA.realizedMarketTrajectory}
                        </div>
                        <div className="text-[10px] text-[#e5c158] italic pt-1">
                          "{MOCK_REVEAL_DATA.companionReflection}"
                        </div>
                      </div>
                    )}

                  </div>

                </div>
              </div>

            </div>
          )}

        </div>

        {/* Quick Suggested Prompts */}
        <div className="mt-3 pt-2 border-t border-[#27272a]/50">
          <div className="text-[10px] font-mono text-zinc-500 mb-1.5">Contextual Governed Prompts:</div>
          <div className="flex flex-wrap gap-1.5">
            {samplePrompts.map((p, idx) => (
              <button
                key={idx}
                onClick={() => handlePromptClick(p)}
                className="text-[10px] font-mono px-2.5 py-1 rounded-lg bg-[#18181b] border border-[#27272a] hover:border-[#d4af37]/60 text-zinc-300 hover:text-[#fef08a] transition-colors cursor-pointer truncate max-w-full"
              >
                {p.label}
              </button>
            ))}
          </div>
        </div>

      </main>

      {/* Bottom Input Area */}
      <footer className="relative z-10 p-4 border-t border-[#27272a]/60 bg-[#0b0b0e]/95">
        <form onSubmit={handleSend} className="relative flex items-center">
          <input
            type="text"
            value={inputQuery}
            onChange={(e) => setInputQuery(e.target.value)}
            placeholder="Ask LEFA (e.g. 'Why are we holding?', 'Show ledger receipt')..."
            className="w-full py-2.5 pl-3.5 pr-20 rounded-xl bg-[#121216] border border-[#27272a] focus:border-[#d4af37] focus:outline-none text-xs text-zinc-200 placeholder-zinc-500 font-sans"
          />
          <div className="absolute right-1.5 flex items-center gap-1">
            <button
              type="button"
              className="p-1.5 text-zinc-400 hover:text-zinc-200 cursor-pointer"
              title="Voice Prompt Simulation"
            >
              <Mic className="w-3.5 h-3.5" />
            </button>
            <button
              type="submit"
              className="p-1.5 rounded-lg bg-[#d4af37] text-black hover:bg-[#e5c158] cursor-pointer transition-colors"
            >
              <Send className="w-3.5 h-3.5" />
            </button>
          </div>
        </form>
      </footer>
    </div>
  );
};
