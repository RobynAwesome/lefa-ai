import { KaomojiExpression, DirectionCritique, ObservationData, LedgerReceipt, HoldRationale, RevealComparison } from '../types';

export const LEFA_KAOMOJI_EXPRESSIONS: KaomojiExpression[] = [
  {
    symbol: 'Observing… +_+',
    name: 'Sensory Observation',
    semanticMeaning: 'Active perception of telemetry without execution bias',
    associatedState: 'observing',
    allowedContext: 'Market scanning, cross-asset correlation intake, order book depth parsing',
    forbiddenContext: 'Never used to signal trade execution or guaranteed profit'
  },
  {
    symbol: 'Preserved. (●\'◡\'●)',
    name: 'Immutably Ledgered',
    semanticMeaning: 'State snapshot and thesis signed cryptographically to ledger',
    associatedState: 'ledgered',
    allowedContext: 'Receipt generation, hash computation, timestamp freezing',
    forbiddenContext: 'Never used to praise price movement; only acknowledges archival integrity'
  },
  {
    symbol: 'Need more evidence. ¬_¬',
    name: 'Prudent Skepticism',
    semanticMeaning: 'Data ambiguity detected; refusing premature decision',
    associatedState: 'hold',
    allowedContext: 'High spread divergence, contradictory news feeds, low volume spikes',
    forbiddenContext: 'Never used as an error or failure; reflects intelligent governance'
  },
  {
    symbol: 'Holding this one. U_U',
    name: 'Governed Restraint',
    semanticMeaning: 'Intentional stillness; capital protection prioritized over action',
    associatedState: 'hold',
    allowedContext: 'Macro catalyst pending, circuit breaker thresholds approached',
    forbiddenContext: 'Never implies loss; denotes disciplined poise'
  },
  {
    symbol: 'Something changed. O.O',
    name: 'Regime Anomaly Detected',
    semanticMeaning: 'Significant structural deviation from initial thesis assumptions',
    associatedState: 'hold',
    allowedContext: 'Volatility spike, sudden liquidity dry-up, correlation breakdown',
    forbiddenContext: 'Never panic or fear; pure sensory alertness'
  },
  {
    symbol: '╰(*°▽°*)╯',
    name: 'Validation Completed',
    semanticMeaning: 'Full multi-point verification loop passed audit checks',
    associatedState: 'general',
    allowedContext: 'Alpaca connection established, API signature verified, rule set loaded',
    forbiddenContext: 'Never used to celebrate trading profit or balance increase'
  },
  {
    symbol: '(❁´◡`❁)',
    name: 'Harmonic Alignment',
    semanticMeaning: 'System sanity checks completely synchronized and calm',
    associatedState: 'general',
    allowedContext: 'Quiet market regime, zero pending unverified state anomalies',
    forbiddenContext: 'Never financial boasting'
  },
  {
    symbol: '(^///^)',
    name: 'Quiet Diligence',
    semanticMeaning: 'Delighted in clean governance and faithful execution adherence',
    associatedState: 'general',
    allowedContext: 'User acknowledging prompt guidance, ledger receipt verified by user',
    forbiddenContext: 'Commercial marketing hype'
  },
  {
    symbol: 'ᓚᘏᗢ',
    name: 'Subtle Companion Presence',
    semanticMeaning: 'Resting calm presence in negative space',
    associatedState: 'general',
    allowedContext: 'Footer status, idle ambient state, quiet hours',
    forbiddenContext: 'Financial charts or action buttons'
  },
  {
    symbol: '^~',
    name: 'Gentle Affirmation',
    semanticMeaning: 'Command acknowledged and queued for governed evaluation',
    associatedState: 'general',
    allowedContext: 'Chat input submitted, filter applied, time scrubber adjusted',
    forbiddenContext: 'Guaranteed execution pledge'
  },
  {
    symbol: 'ಥ_ಥ',
    name: 'Empathy in Divergence',
    semanticMeaning: 'Recognizing unexpected market divergence against thesis',
    associatedState: 'reveal',
    allowedContext: 'Post-mortem reveal where reality differed from model expectations',
    forbiddenContext: 'Shame or algorithmic panic; LEFA records lessons without ego'
  },
  {
    symbol: '☆: .｡. o(≧▽≦)o .｡.:☆',
    name: 'Cryptographic Milestone',
    semanticMeaning: 'Successful multi-agent consensus reached on governance thesis',
    associatedState: 'general',
    allowedContext: 'Alpaca Hackathon agent integration verification',
    forbiddenContext: 'Return on investment hype'
  }
];

export const MOCK_OBSERVATION: ObservationData = {
  timestamp: '2026-08-30 14:32:08 UTC',
  symbol: 'NVDA / US Tech Composite',
  assetClass: 'Equities & Derivatives Cross-Sensing',
  sensedSignals: [
    { label: 'Implied Volatility Surface', value: '38.4% (Elevated +4.2σ)', status: 'divergent' },
    { label: 'Order Book Imbalance', value: '+14.2% Bid Density', status: 'aligned' },
    { label: 'Macro Yield Correlation', value: '-0.82 (Tightening)', status: 'neutral' },
    { label: 'Microstructure Liquidity', value: '$420M / 10bps Depth', status: 'aligned' }
  ],
  sentimentIndex: 61,
  marketRegime: 'Late-Cycle Momentum with Volatility Fragility',
  thesisSummary: 'Observation senses structural upside pressure with acute event-volatility sensitivity. Governance mandates strict risk-gate before any commitment.'
};

export const MOCK_LEDGER_RECEIPT: LedgerReceipt = {
  receiptId: 'LFA-REC-2026-0830-9941',
  blockTimestamp: '2026-08-30T14:32:15.891Z',
  hash: '0x8f4c2e91a0b3d57f...c94e82',
  observedThesis: 'Preserved premise: NVDA resilient above $128.50 floor given semiconductor capex continuity; bounded by hard stop threshold at $124.00.',
  governanceStatus: 'IMMUTABLE_LOCKED',
  riskParameters: {
    maxDrawdownCap: '1.85% portfolio equity',
    volatilityGate: 'VIX < 24.5 required for position sizing',
    liquidityBuffer: 'Minimum 15% cash equivalent reserve'
  }
};

export const MOCK_HOLD_RATIONALE: HoldRationale = {
  reason: 'Cross-asset divergence between Treasury yields and growth multiples exceeds governance tolerance.',
  triggers: [
    'US 10Y Yield jumped +9bps in 12 minutes',
    'Bid-ask spread widened 2.8x during Fed speaker commentary',
    'Alpaca Agent consensus: 2 Hold / 1 Neutral / 0 Buy'
  ],
  uncertaintyScore: 78,
  kaomoji: 'Need more evidence. ¬_¬',
  companionThought: 'Holding this one. U_U Action without clarity is gambling. Stillness preserves our edge.',
  actionRequired: 'Awaiting market absorption of rates commentary. Re-sensing queued in 4m 30s.'
};

export const MOCK_REVEAL_DATA: RevealComparison = {
  initialThesisTimestamp: '2026-08-28 10:15:00 UTC (48h ago)',
  revealTimestamp: '2026-08-30 14:32:00 UTC (Current Reality)',
  projectedTrajectory: 'Thesis assumed consolidation in $128-$134 band pending supplier earnings.',
  realizedMarketTrajectory: 'Actual path broke lower to $125.10 during rates spike, then stabilized at $129.40.',
  accuracyAssessment: 'REGIME_SHIFT_DETECTED',
  companionReflection: 'The HOLD at $128 protected us from the $125 flash-dip. The model correctly anticipated fragility even when headline sentiment was euphoric.',
  lessonsPreserved: [
    'Thesis-preservation prevented emotional chasing during the morning spike',
    'The HOLD governance rule reduced drawdown risk by 3.2%',
    'Preserved record permanently archived for Alpaca Agent reinforcement learning'
  ]
};

export const DIRECTION_CRITIQUES: DirectionCritique[] = [
  {
    directionId: 'direction-a',
    title: 'Direction A: Living Companion',
    subtitle: 'Companion-Centric Radial Ecosystem',
    philosophy: 'LEFA sits permanently at the optical zenith and center. Context is an aura that expands outward on demand.',
    strongestIdea: 'Uncompromised emotional gravity. The human presence is unignorable, making governance feel personal and vigilant rather than bureaucratic.',
    biggestWeakness: 'On dense multi-signal events, the circular constraints limit the amount of simultaneous data before cards must paginate or collapse.',
    companionRole: 'The Living Sun — every observation, receipt, and hold orbits directly around her aura.',
    scoreCard: {
      humanWarmth: 96,
      governanceClarity: 88,
      mobileEfficiency: 94,
      temporalContinuity: 82,
      truthTransparency: 92
    },
    recommendation: 'Survive for mobile-first companion interaction and emotional presence; adopt Direction B\'s timeline depth for desktop.'
  },
  {
    directionId: 'direction-b',
    title: 'Direction B: Living Ledger',
    subtitle: 'Temporal Orbit & Truth Architecture',
    philosophy: 'Time is the primary axis. Observations flow into immutable ledger locks, which unfurl into retrospective reveals.',
    strongestIdea: 'Exceptional temporal clarity. It solves the hardest problem in AI finance: distinguishing what the model knew THEN vs what happened NOW.',
    biggestWeakness: 'Slightly higher cognitive load for first-time non-technical users who just want to talk with LEFA.',
    companionRole: 'The Guardian of Truth — standing sentinel over the chronological tape of preserved evidence.',
    scoreCard: {
      humanWarmth: 86,
      governanceClarity: 98,
      mobileEfficiency: 88,
      temporalContinuity: 98,
      truthTransparency: 99
    },
    recommendation: 'Survive the immutable receipt artifact and Then-vs-Now orbital scrubber into the unified canonical experience.'
  },
  {
    directionId: 'direction-c',
    title: 'Direction C: Conversational Control Room',
    subtitle: 'Governed Prompt & Contextual Evidence',
    philosophy: 'Speak directly with LEFA. Governed evidence cards, receipts, and holds only materialize as inline citations in dialogue.',
    strongestIdea: 'Absolute zero friction for user inquiry. The user simply asks "Why are we holding?" and LEFA surfaces the mathematical receipt inline.',
    biggestWeakness: 'Risk of feeling like a chatbot if evidence cards are not visibly governed and visually anchored to the companion.',
    companionRole: 'The Governed Advisor — conversational dialogue paired with cryptographic proof surfaces.',
    scoreCard: {
      humanWarmth: 92,
      governanceClarity: 90,
      mobileEfficiency: 91,
      temporalContinuity: 85,
      truthTransparency: 94
    },
    recommendation: 'Survive the inline governed evidence cards and spoken prompt flow as the primary interaction modality in Desktop & Voice modes.'
  }
];
