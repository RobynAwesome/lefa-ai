import React from 'react';
import { motion } from 'motion/react';
import { SystemState } from '../types';

interface CompanionAvatarProps {
  state: SystemState;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  showKaomojiBadge?: boolean;
  customKaomoji?: string;
  onClick?: () => void;
  reducedMotion?: boolean;
}

export const CompanionAvatar: React.FC<CompanionAvatarProps> = ({
  state,
  size = 'lg',
  showKaomojiBadge = true,
  customKaomoji,
  onClick,
  reducedMotion = false,
}) => {
  const sizeClasses = {
    sm: 'w-16 h-16',
    md: 'w-28 h-28',
    lg: 'w-44 h-44 sm:w-52 sm:h-52',
    xl: 'w-60 h-60 sm:w-72 sm:h-72',
  };

  const getKaomojiForState = () => {
    if (customKaomoji) return customKaomoji;
    switch (state) {
      case 'disconnected':
        return 'ᓚᘏᗢ';
      case 'observing':
        return 'Observing… +_+';
      case 'ledgered':
        return 'Preserved. (●\'◡\'●)';
      case 'hold':
        return 'Holding. U_U';
      case 'reveal':
        return 'Truth. (❁´◡`❁)';
      default:
        return 'ᓚᘏᗢ';
    }
  };

  const getStateColor = () => {
    switch (state) {
      case 'observing':
        return {
          stroke: '#10b981',
          glow: 'rgba(16, 185, 129, 0.35)',
          bg: 'from-emerald-500/10 to-emerald-950/30',
        };
      case 'ledgered':
        return {
          stroke: '#d4af37',
          glow: 'rgba(212, 175, 55, 0.4)',
          bg: 'from-[#d4af37]/15 to-amber-950/30',
        };
      case 'hold':
        return {
          stroke: '#f59e0b',
          glow: 'rgba(245, 158, 11, 0.35)',
          bg: 'from-amber-500/10 to-orange-950/30',
        };
      case 'reveal':
        return {
          stroke: '#38bdf8',
          glow: 'rgba(56, 189, 248, 0.4)',
          bg: 'from-cyan-500/15 to-blue-950/30',
        };
      case 'disconnected':
      default:
        return {
          stroke: '#71717a',
          glow: 'rgba(113, 113, 122, 0.2)',
          bg: 'from-zinc-800/20 to-zinc-950/30',
        };
    }
  };

  const colors = getStateColor();

  return (
    <div
      className="relative flex flex-col items-center justify-center select-none group cursor-pointer"
      onClick={onClick}
      id="lefa-companion-anchor"
    >
      {/* Outer Glow & Geometric Linework */}
      <div className={`relative ${sizeClasses[size]} flex items-center justify-center p-2`}>
        {/* Background Atmospheric Radial */}
        <div
          className="absolute inset-0 rounded-full blur-xl opacity-40 transition-all duration-700 pointer-events-none"
          style={{ background: colors.glow }}
        />

        {/* SVG Orbital Geometric Linework */}
        <svg
          className="absolute inset-0 w-full h-full pointer-events-none overflow-visible"
          viewBox="0 0 200 200"
        >
          {/* Static outer dashed alignment ring */}
          <circle
            cx="100"
            cy="100"
            r="94"
            fill="none"
            stroke={colors.stroke}
            strokeWidth="1.2"
            strokeDasharray="4 8"
            opacity="0.6"
          />

          {/* Animated counter-rotating middle ring */}
          <motion.circle
            cx="100"
            cy="100"
            r="86"
            fill="none"
            stroke={colors.stroke}
            strokeWidth="1"
            strokeDasharray="12 16"
            animate={reducedMotion ? {} : { rotate: 360 }}
            transition={{ repeat: Infinity, duration: 18, ease: 'linear' }}
            style={{ transformOrigin: '100px 100px' }}
            opacity="0.75"
          />

          {/* Inner ring */}
          <circle
            cx="100"
            cy="100"
            r="78"
            fill="none"
            stroke={colors.stroke}
            strokeWidth="1.5"
            opacity="0.9"
          />
        </svg>

        {/* Core Canonical Emblem (Vector Geometric Avatar) */}
        <div
          className={`relative w-[78%] h-[78%] rounded-full overflow-hidden border-2 flex items-center justify-center bg-gradient-to-br ${colors.bg} transition-all duration-700 z-10 shadow-2xl`}
          style={{ borderColor: colors.stroke }}
        >
          {/* High-res Canonical Vector Avatar */}
          <img
            src="/lefa-companion-root.svg"
            alt="LEFA"
            className="w-[85%] h-[85%] object-contain drop-shadow-[0_0_12px_rgba(212,175,55,0.4)] transition-transform duration-700 group-hover:scale-105"
            onError={(e) => {
              // Fallback to inline vector geometry if image request is blocked
              (e.currentTarget as HTMLElement).style.display = 'none';
            }}
          />

          {/* Fallback Inner Geometry in case image is disabled */}
          <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none p-2 text-center">
            <span className="text-[10px] font-mono tracking-widest text-[#fef08a] uppercase opacity-80">
              LEFA
            </span>
          </div>
        </div>

        {/* Active Node Ping */}
        {state === 'observing' && (
          <div className="absolute top-1 right-3 z-20">
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
              <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500" />
            </span>
          </div>
        )}
      </div>

      {/* Kaomoji Mood Pill Badge */}
      {showKaomojiBadge && (
        <div className="mt-2 px-3 py-1 rounded-full bg-[#121216]/95 border border-zinc-700/60 shadow-lg text-[11px] font-mono text-[#fef08a] backdrop-blur-md flex items-center gap-1.5 transition-all">
          <span className="w-1.5 h-1.5 rounded-full" style={{ background: colors.stroke }} />
          <span>{getKaomojiForState()}</span>
        </div>
      )}
    </div>
  );
};
