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
  reducedMotion = false
}) => {
  // Use the canonical generated portrait asset
  const imageSrc = '/src/assets/images/lefa_companion_portrait_1788115028929.jpg';

  const sizeClasses = {
    sm: 'w-20 h-20',
    md: 'w-36 h-36',
    lg: 'w-52 h-52 sm:w-60 sm:h-60',
    xl: 'w-72 h-72 sm:w-84 sm:h-84'
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
        return 'Holding this one. U_U';
      case 'reveal':
        return 'Truth revealed. (❁´◡`❁)';
      default:
        return 'ᓚᘏᗢ';
    }
  };

  const getStateAura = () => {
    switch (state) {
      case 'observing':
        return 'border-[#c5a059] shadow-[0_0_35px_rgba(212,175,55,0.28)]';
      case 'ledgered':
        return 'border-[#e5c158] shadow-[0_0_30px_rgba(229,193,88,0.35)]';
      case 'hold':
        return 'border-[#d97706] shadow-[0_0_25px_rgba(217,119,6,0.22)]';
      case 'reveal':
        return 'border-[#fef08a] shadow-[0_0_40px_rgba(254,240,138,0.30)]';
      case 'disconnected':
      default:
        return 'border-[#c5a059]/40 shadow-[0_0_15px_rgba(212,175,55,0.1)]';
    }
  };

  return (
    <div 
      className="relative flex flex-col items-center justify-center select-none group cursor-pointer"
      onClick={onClick}
      id="lefa-companion-anchor"
    >
      {/* Outer Geometric Gold Linework & Ring System */}
      <div className={`relative ${sizeClasses[size]} flex items-center justify-center p-3`}>
        
        {/* Subtle Background Glow Radial */}
        <div 
          className={`absolute inset-0 rounded-full transition-opacity duration-700 pointer-events-none ${
            state === 'observing' ? 'opacity-70 bg-gradient-to-r from-[#d4af37]/15 via-transparent to-[#c5a059]/15' :
            state === 'ledgered' ? 'opacity-90 bg-gradient-to-tr from-[#e5c158]/20 via-transparent to-[#d4af37]/20' :
            state === 'hold' ? 'opacity-60 bg-gradient-to-br from-[#d97706]/20 via-transparent to-[#b45309]/15' :
            state === 'reveal' ? 'opacity-85 bg-gradient-to-t from-[#fef08a]/20 via-[#d4af37]/15 to-transparent' :
            'opacity-30 bg-[#d4af37]/5'
          }`} 
        />

        {/* SVG Orbital Geometric Linework */}
        <svg 
          className="absolute inset-0 w-full h-full pointer-events-none overflow-visible"
          viewBox="0 0 200 200"
        >
          <defs>
            <linearGradient id="goldGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#fef08a" stopOpacity="0.9" />
              <stop offset="50%" stopColor="#d4af37" stopOpacity="0.7" />
              <stop offset="100%" stopColor="#854d0e" stopOpacity="0.4" />
            </linearGradient>
            <linearGradient id="holdGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#fbbf24" stopOpacity="0.8" />
              <stop offset="100%" stopColor="#b45309" stopOpacity="0.3" />
            </linearGradient>
          </defs>

          {/* Outer Thin Celestial Orbit */}
          <circle
            cx="100"
            cy="100"
            r="94"
            fill="none"
            stroke="url(#goldGradient)"
            strokeWidth="0.8"
            strokeDasharray={state === 'observing' ? '4 8' : state === 'ledgered' ? '0' : '2 6'}
            className={!reducedMotion && state === 'observing' ? 'animate-[spin_40s_linear_infinite]' : ''}
          />

          {/* Middle Precision Dial Ring */}
          <circle
            cx="100"
            cy="100"
            r="86"
            fill="none"
            stroke="url(#goldGradient)"
            strokeWidth={state === 'ledgered' ? '1.5' : '0.6'}
            strokeDasharray={state === 'hold' ? '16 6' : '1 5'}
            className={!reducedMotion && state === 'hold' ? 'animate-[spin_60s_linear_infinite_reverse]' : ''}
          />

          {/* Cardinal Geometric Tick Marks (4 Governed Poles) */}
          <line x1="100" y1="2" x2="100" y2="10" stroke="#d4af37" strokeWidth="1.2" strokeOpacity="0.8" />
          <line x1="100" y1="190" x2="100" y2="198" stroke="#d4af37" strokeWidth="1.2" strokeOpacity="0.8" />
          <line x1="2" y1="100" x2="10" y2="100" stroke="#d4af37" strokeWidth="1.2" strokeOpacity="0.8" />
          <line x1="190" y1="100" x2="198" y2="100" stroke="#d4af37" strokeWidth="1.2" strokeOpacity="0.8" />

          {/* Diagonal Sensor Nodes */}
          <circle cx="32" cy="32" r="1.5" fill="#d4af37" fillOpacity="0.7" />
          <circle cx="168" cy="32" r="1.5" fill="#d4af37" fillOpacity="0.7" />
          <circle cx="32" cy="168" r="1.5" fill="#d4af37" fillOpacity="0.7" />
          <circle cx="168" cy="168" r="1.5" fill="#d4af37" fillOpacity="0.7" />

          {/* State Specific Geometric Highlights */}
          {state === 'observing' && (
            <motion.circle
              cx="100"
              cy="100"
              r="90"
              fill="none"
              stroke="#e5c158"
              strokeWidth="1.8"
              strokeDasharray="40 160"
              initial={{ rotate: 0 }}
              animate={reducedMotion ? {} : { rotate: 360 }}
              transition={{ repeat: Infinity, duration: 4, ease: "linear" }}
            />
          )}

          {state === 'ledgered' && (
            <>
              {/* Immutable Locking Brackets */}
              <path d="M 88,6 A 94,94 0 0,1 112,6" fill="none" stroke="#fef08a" strokeWidth="2.5" />
              <path d="M 88,194 A 94,94 0 0,0 112,194" fill="none" stroke="#fef08a" strokeWidth="2.5" />
              <circle cx="100" cy="100" r="82" fill="none" stroke="#d4af37" strokeWidth="1" />
            </>
          )}

          {state === 'hold' && (
            <>
              {/* Dual Restraint Notches */}
              <rect x="96" y="2" width="8" height="3" fill="#fbbf24" />
              <rect x="96" y="195" width="8" height="3" fill="#fbbf24" />
              <rect x="2" y="96" width="3" height="8" fill="#fbbf24" />
              <rect x="195" y="96" width="3" height="8" fill="#fbbf24" />
            </>
          )}
        </svg>

        {/* Circular Frame Containing Canonical LEFA Portrait */}
        <div 
          className={`relative w-full h-full rounded-full overflow-hidden border-2 transition-all duration-700 z-10 ${getStateAura()}`}
        >
          <img
            src={imageSrc}
            alt="LEFA — Canonical Financial Intelligence Companion"
            referrerPolicy="no-referrer"
            className="w-full h-full object-cover object-center scale-[1.03] transition-transform duration-700 group-hover:scale-105"
          />

          {/* Restrained Vignette & Metallic Tint Overlay */}
          <div className="absolute inset-0 bg-gradient-to-b from-transparent via-black/10 to-black/50 pointer-events-none" />
          
          {/* Subtle State-based Inner Border Lighting */}
          {state === 'observing' && (
            <div className="absolute inset-0 rounded-full border border-[#d4af37]/30 animate-pulse pointer-events-none" />
          )}
        </div>

        {/* Satellite Node Indicator */}
        <div className="absolute -top-1 right-2 z-20">
          <span className="relative flex h-3.5 w-3.5">
            {state === 'observing' && (
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#d4af37] opacity-75" />
            )}
            <span 
              className={`relative inline-flex rounded-full h-3.5 w-3.5 border border-black/80 ${
                state === 'observing' ? 'bg-[#d4af37]' :
                state === 'ledgered' ? 'bg-[#e5c158]' :
                state === 'hold' ? 'bg-[#f59e0b]' :
                state === 'reveal' ? 'bg-[#fef08a]' :
                'bg-zinc-600'
              }`} 
            />
          </span>
        </div>
      </div>

      {/* Kaomoji Expression Pill / State Micro-Signature */}
      {showKaomojiBadge && (
        <motion.div 
          key={getKaomojiForState()}
          initial={{ opacity: 0, y: 4 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="mt-3.5 z-20"
        >
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#121216]/90 border border-[#d4af37]/30 backdrop-blur-md shadow-lg text-xs font-mono text-[#f4f4f5] hover:border-[#d4af37] transition-colors">
            <span className="text-[#e5c158] font-bold">
              {getKaomojiForState()}
            </span>
          </div>
        </motion.div>
      )}
    </div>
  );
};
