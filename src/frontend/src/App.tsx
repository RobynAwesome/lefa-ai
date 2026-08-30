/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * LEFA AI — App Root
 * ==================
 * Governed financial intelligence companion.
 * OBSERVE → LEDGER → TIME → REVEAL
 *
 * Changes from Stitch export:
 * 1. AlpacaConnectModal now calls /api/mcp/verify (governed proof gate).
 * 2. SnapshotBanner fetches /api/snapshot — no fake financial state.
 * 3. @google/genai dependency removed (not needed for this POC stage).
 * 4. Credential defaults removed from AlpacaConnectModal (empty strings).
 *
 * I_AM_STATELESS_RENTER_NOT_LANDLORD
 */

import React, { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { SystemState, DesignDirection, ViewportMode } from './types';
import { StateSimulatorBar } from './components/StateSimulatorBar';
import { DirectionA } from './components/DirectionA';
import { DirectionB } from './components/DirectionB';
import { DirectionC } from './components/DirectionC';
import { CanvasMatrix } from './components/CanvasMatrix';
import { CritiqueModal } from './components/CritiqueModal';
import { ExpressionCodexModal } from './components/ExpressionCodexModal';
import { DesignSystemSpec } from './components/DesignSystemSpec';
import { AlpacaConnectModal } from './components/AlpacaConnectModal';
import { SnapshotBanner } from './components/SnapshotBanner';
import { getSnapshot } from './api/lefa';
import type { SnapshotResponse } from './api/lefa';

export default function App() {
  const [currentState, setCurrentState] = useState<SystemState>('disconnected');
  const [activeDirection, setActiveDirection] = useState<DesignDirection>('canvas-matrix');
  const [viewportMode, setViewportMode] = useState<ViewportMode>('desktop');
  const [reducedMotion, setReducedMotion] = useState(false);
  const [soundEnabled, setSoundEnabled] = useState(false);
  const [isAlpacaConnected, setIsAlpacaConnected] = useState(false);

  // Governed snapshot state — bound to backend, never invented
  const [snapshot, setSnapshot] = useState<SnapshotResponse | null>(null);
  const [snapshotLoading, setSnapshotLoading] = useState(false);

  // Modals
  const [isCritiqueOpen, setIsCritiqueOpen] = useState(false);
  const [isCodexOpen, setIsCodexOpen] = useState(false);
  const [isDesignDocOpen, setIsDesignDocOpen] = useState(false);
  const [isConnectModalOpen, setIsConnectModalOpen] = useState(false);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  // Fetch snapshot when connection state changes
  useEffect(() => {
    let cancelled = false;
    setSnapshotLoading(true);
    getSnapshot(isAlpacaConnected)
      .then((data) => { if (!cancelled) setSnapshot(data); })
      .catch(() => { if (!cancelled) setSnapshot(null); })
      .finally(() => { if (!cancelled) setSnapshotLoading(false); });
    return () => { cancelled = true; };
  }, [isAlpacaConnected]);

  // Optional subtle harmonic tone synthesized via Web Audio API on state transition
  const playStateChime = useCallback((state: SystemState) => {
    if (!soundEnabled || typeof window === 'undefined') return;
    try {
      const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
      const ctx = new AudioCtx();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      const freqs: Record<SystemState, number> = {
        disconnected: 220,
        observing: 392,
        ledgered: 523.25,
        hold: 329.63,
        reveal: 659.25,
      };
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freqs[state] || 440, ctx.currentTime);
      gain.gain.setValueAtTime(0.04, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.6);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + 0.6);
    } catch {
      // Audio context may be restricted before user gesture; gracefully ignore
    }
  }, [soundEnabled]);

  const handleStateChange = (newState: SystemState) => {
    setCurrentState(newState);
    playStateChime(newState);
  };

  const handleConnectSuccess = () => {
    setIsAlpacaConnected(true);
    setCurrentState('observing');
    setToastMessage("Alpaca Paper Sandbox Verified (●'◡'●)");
    setTimeout(() => setToastMessage(null), 3000);
  };

  const handleDisconnect = () => {
    setIsAlpacaConnected(false);
    setCurrentState('disconnected');
    setToastMessage('Alpaca Disconnected. Returning to unpopulated truth state.');
    setTimeout(() => setToastMessage(null), 3000);
  };

  const handlePreviewKaomoji = (kaomoji: string) => {
    setToastMessage(`Expression Preview: ${kaomoji}`);
    setTimeout(() => setToastMessage(null), 2500);
  };

  return (
    <div className="min-h-screen bg-[#09090b] text-[#f4f4f5] font-sans flex flex-col selection:bg-[#d4af37]/30 selection:text-[#fef08a] antialiased">
      {/* Top Global State & Direction Navigation Bar */}
      <StateSimulatorBar
        currentState={currentState}
        onStateChange={handleStateChange}
        activeDirection={activeDirection}
        onDirectionChange={setActiveDirection}
        viewportMode={viewportMode}
        onViewportChange={setViewportMode}
        reducedMotion={reducedMotion}
        onToggleReducedMotion={() => setReducedMotion(!reducedMotion)}
        soundEnabled={soundEnabled}
        onToggleSound={() => setSoundEnabled(!soundEnabled)}
        onOpenCritique={() => setIsCritiqueOpen(true)}
        onOpenCodex={() => setIsCodexOpen(true)}
        onOpenDesignDoc={() => setIsDesignDocOpen(true)}
      />

      {/* Governed Snapshot Banner — bound to backend, no fake state */}
      <div className="w-full px-4 pt-3 pb-1">
        <SnapshotBanner snapshot={snapshot} isLoading={snapshotLoading} />
      </div>

      {/* Main Viewport Workspace */}
      <main className="flex-1 flex flex-col items-center justify-center p-4 sm:p-6 lg:p-8">
        <div className="w-full max-w-7xl mx-auto flex flex-col items-center justify-center">

          {activeDirection === 'canvas-matrix' && (
            <CanvasMatrix
              state={currentState}
              onStateChange={handleStateChange}
              onSelectDirection={(dir) => {
                setActiveDirection(dir);
                setViewportMode('desktop');
              }}
              onOpenConnectModal={() => setIsConnectModalOpen(true)}
              isAlpacaConnected={isAlpacaConnected}
              reducedMotion={reducedMotion}
              onOpenCritiqueModal={() => setIsCritiqueOpen(true)}
            />
          )}

          {activeDirection === 'direction-a' && (
            <div className={`w-full transition-all duration-300 ${viewportMode === 'mobile' ? 'max-w-[420px]' : 'max-w-4xl'}`}>
              <div className="mb-3 flex items-center justify-between text-xs font-mono text-zinc-400">
                <span className="text-[#e5c158]">Focus: Direction A — Living Companion</span>
                <span>Viewport: {viewportMode === 'mobile' ? '~390px Mobile Native' : 'Responsive Desktop'}</span>
              </div>
              <DirectionA
                state={currentState}
                onStateChange={handleStateChange}
                viewportMode={viewportMode}
                onOpenConnectModal={() => setIsConnectModalOpen(true)}
                isAlpacaConnected={isAlpacaConnected}
                reducedMotion={reducedMotion}
              />
            </div>
          )}

          {activeDirection === 'direction-b' && (
            <div className={`w-full transition-all duration-300 ${viewportMode === 'mobile' ? 'max-w-[420px]' : 'max-w-4xl'}`}>
              <div className="mb-3 flex items-center justify-between text-xs font-mono text-zinc-400">
                <span className="text-[#e5c158]">Focus: Direction B — Living Ledger</span>
                <span>Viewport: {viewportMode === 'mobile' ? '~390px Mobile Native' : 'Responsive Desktop'}</span>
              </div>
              <DirectionB
                state={currentState}
                onStateChange={handleStateChange}
                viewportMode={viewportMode}
                onOpenConnectModal={() => setIsConnectModalOpen(true)}
                isAlpacaConnected={isAlpacaConnected}
                reducedMotion={reducedMotion}
              />
            </div>
          )}

          {activeDirection === 'direction-c' && (
            <div className={`w-full transition-all duration-300 ${viewportMode === 'mobile' ? 'max-w-[420px]' : 'max-w-4xl'}`}>
              <div className="mb-3 flex items-center justify-between text-xs font-mono text-zinc-400">
                <span className="text-[#e5c158]">Focus: Direction C — Conversational Control Room</span>
                <span>Viewport: {viewportMode === 'mobile' ? '~390px Mobile Native' : 'Responsive Desktop'}</span>
              </div>
              <DirectionC
                state={currentState}
                onStateChange={handleStateChange}
                viewportMode={viewportMode}
                onOpenConnectModal={() => setIsConnectModalOpen(true)}
                isAlpacaConnected={isAlpacaConnected}
                reducedMotion={reducedMotion}
              />
            </div>
          )}

        </div>
      </main>

      {/* Floating Micro-Toast */}
      <AnimatePresence>
        {toastMessage && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            className="fixed bottom-6 right-6 z-50 px-4 py-2.5 rounded-2xl bg-[#121216]/95 border border-[#d4af37]/60 text-xs font-mono text-[#fef08a] shadow-2xl backdrop-blur-md flex items-center gap-2"
          >
            <span className="w-2 h-2 rounded-full bg-[#d4af37] animate-ping" />
            <span>{toastMessage}</span>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Modals */}
      <CritiqueModal
        isOpen={isCritiqueOpen}
        onClose={() => setIsCritiqueOpen(false)}
        onSelectDirection={(dir) => {
          setActiveDirection(dir);
          setViewportMode('desktop');
        }}
      />
      <ExpressionCodexModal
        isOpen={isCodexOpen}
        onClose={() => setIsCodexOpen(false)}
        currentState={currentState}
        onPreviewKaomoji={handlePreviewKaomoji}
      />
      <DesignSystemSpec
        isOpen={isDesignDocOpen}
        onClose={() => setIsDesignDocOpen(false)}
      />
      <AlpacaConnectModal
        isOpen={isConnectModalOpen}
        onClose={() => setIsConnectModalOpen(false)}
        isConnected={isAlpacaConnected}
        onConnectSuccess={handleConnectSuccess}
        onDisconnect={handleDisconnect}
      />
    </div>
  );
}
