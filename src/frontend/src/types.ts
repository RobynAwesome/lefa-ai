export type SystemState = 'disconnected' | 'observing' | 'ledgered' | 'hold' | 'reveal';

export type DesignDirection = 'direction-a' | 'direction-b' | 'direction-c' | 'canvas-matrix';

export type ViewportMode = 'mobile' | 'desktop' | 'dual';

export interface KaomojiExpression {
  symbol: string;
  name: string;
  semanticMeaning: string;
  associatedState: SystemState | 'general';
  allowedContext: string;
  forbiddenContext: string;
}

export interface ObservationData {
  timestamp: string;
  symbol: string;
  assetClass: string;
  sensedSignals: {
    label: string;
    value: string;
    status: 'neutral' | 'divergent' | 'aligned' | 'unknown';
  }[];
  sentimentIndex: number; // 0-100
  marketRegime: string;
  thesisSummary: string;
}

export interface LedgerReceipt {
  receiptId: string;
  blockTimestamp: string;
  hash: string;
  observedThesis: string;
  governanceStatus: 'IMMUTABLE_LOCKED' | 'PENDING' | 'INVALIDATED';
  riskParameters: {
    maxDrawdownCap: string;
    volatilityGate: string;
    liquidityBuffer: string;
  };
}

export interface HoldRationale {
  reason: string;
  triggers: string[];
  uncertaintyScore: number; // 0-100
  kaomoji: string;
  companionThought: string;
  actionRequired: string;
}

export interface RevealComparison {
  initialThesisTimestamp: string;
  revealTimestamp: string;
  projectedTrajectory: string;
  realizedMarketTrajectory: string;
  accuracyAssessment: 'THESIS_CONFIRMED' | 'REGIME_SHIFT_DETECTED' | 'DISSONANCE_OBSERVED';
  companionReflection: string;
  lessonsPreserved: string[];
}

export interface DirectionCritique {
  directionId: 'direction-a' | 'direction-b' | 'direction-c';
  title: string;
  subtitle: string;
  philosophy: string;
  strongestIdea: string;
  biggestWeakness: string;
  companionRole: string;
  scoreCard: {
    humanWarmth: number;
    governanceClarity: number;
    mobileEfficiency: number;
    temporalContinuity: number;
    truthTransparency: number;
  };
  recommendation: string;
}
