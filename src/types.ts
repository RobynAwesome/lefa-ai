export type SystemState = 'disconnected' | 'observing' | 'ledgered' | 'hold' | 'reveal';

export type DesignDirection = 'direction-a' | 'direction-b' | 'direction-c' | 'canvas-matrix';

export type ViewportMode = 'mobile' | 'desktop' | 'dual';

export type ExperienceMode = 'design-preview' | 'runtime';

export type SovereignDecision = 'APPROVE' | 'HOLD' | 'REJECT';
export type SovereignProofState = 'LOCAL_RECEIPT' | 'EXTERNAL_RECEIPT';

export interface SovereignDecisionReason {
  severity: SovereignDecision;
  code: string;
  message: string;
}

export interface SovereignDecisionReceipt {
  schema: 'kopano.alpaca.decision-receipt.v1';
  timestamp: string;
  cycle_id: string;
  observation: unknown;
  proposal: unknown;
  evaluation: {
    decision: SovereignDecision;
    reasons: SovereignDecisionReason[];
    metrics?: Record<string, unknown>;
  };
  tool_intent: unknown | null;
  provider_result: unknown | null;
  kc_receipt_id: string;
  evidence_sha256: string;
  provider_receipt_id: string | null;
  proof_state: SovereignProofState;
}

export interface SovereignProviderObservation {
  code: string;
  account_status: string;
  account_blocked: boolean | null;
  trading_blocked: boolean | null;
  trade_suspended_by_user: boolean | null;
}

export interface SovereignBridgeStatus {
  schema: 'kopano.lefa.sovereign-bridge-status.v1';
  provider: 'alpaca';
  environment: 'paper';
  bridge_state: 'VERIFIED' | 'HOLD';
  execution_authority: 'BACKEND_ONLY';
  observed_at: string;
  latest_receipt: SovereignDecisionReceipt | null;
  provider_observation?: SovereignProviderObservation;
  truth_boundary?: string;
}

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
