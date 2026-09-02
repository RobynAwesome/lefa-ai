/**
 * LEFA AI — Human-facing Sovereign Bridge
 * ========================================
 *
 * The browser does not discover MCP namespaces, inspect credentials, or reason
 * about provider transport. It asks LEFA's backend for one governed projection.
 * Heavy proof stays behind the interface.
 *
 * I_AM_STATELESS_RENTER_NOT_LANDLORD
 */

import type {
  SovereignBridgeStatus,
  SovereignDecision,
  SovereignDecisionReceipt,
  SovereignProofState,
} from './types';

export type SovereignBridgeVerification =
  | {
      ok: true;
      status: SovereignBridgeStatus;
    }
  | {
      ok: false;
      code:
        | 'BRIDGE_UNREACHABLE'
        | 'BRIDGE_HTTP_ERROR'
        | 'BRIDGE_INVALID_RECEIPT'
        | 'BRIDGE_NOT_VERIFIED';
      message: string;
    };

const RECEIPT_SCHEMA = 'kopano.alpaca.decision-receipt.v1';
const BRIDGE_SCHEMA = 'kopano.lefa.sovereign-bridge-status.v1';
const STATUS_URL = '/api/bridge/status';
const VALID_DECISIONS = new Set<SovereignDecision>(['APPROVE', 'HOLD', 'REJECT']);
const VALID_PROOF_STATES = new Set<SovereignProofState>(['LOCAL_RECEIPT', 'EXTERNAL_RECEIPT']);

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isDecisionReceipt(value: unknown): value is SovereignDecisionReceipt {
  if (!isRecord(value)) return false;
  if (value.schema !== RECEIPT_SCHEMA) return false;
  if (typeof value.timestamp !== 'string' || typeof value.cycle_id !== 'string') return false;
  if (typeof value.kc_receipt_id !== 'string' || !value.kc_receipt_id.startsWith('kc:alpaca:')) return false;
  if (typeof value.evidence_sha256 !== 'string' || value.evidence_sha256.length !== 64) return false;
  if (!VALID_PROOF_STATES.has(value.proof_state as SovereignProofState)) return false;

  const evaluation = value.evaluation;
  if (!isRecord(evaluation) || !VALID_DECISIONS.has(evaluation.decision as SovereignDecision)) return false;
  if (!Array.isArray(evaluation.reasons)) return false;
  return true;
}

export function isSovereignBridgeStatus(value: unknown): value is SovereignBridgeStatus {
  if (!isRecord(value)) return false;
  if (value.schema !== BRIDGE_SCHEMA) return false;
  if (value.provider !== 'alpaca') return false;
  if (value.environment !== 'paper') return false;
  if (value.execution_authority !== 'BACKEND_ONLY') return false;
  if (value.bridge_state !== 'VERIFIED' && value.bridge_state !== 'HOLD') return false;
  if (typeof value.observed_at !== 'string') return false;
  if (value.latest_receipt !== null && !isDecisionReceipt(value.latest_receipt)) return false;
  return true;
}

function friendlyHoldMessage(status: SovereignBridgeStatus): string {
  const code = status.provider_observation?.code;

  if (code === 'PAPER_CREDENTIALS_UNAVAILABLE') {
    return 'The secure trading connection still needs setup.';
  }

  if (code === 'SOVEREIGN_BACKEND_UNAVAILABLE') {
    return "LEFA can't reach the trading service right now.";
  }

  return 'The trading connection is not ready yet.';
}

export async function verifySovereignBridge(): Promise<SovereignBridgeVerification> {
  let response: Response;

  try {
    response = await fetch(STATUS_URL, {
      method: 'GET',
      headers: { Accept: 'application/json' },
      cache: 'no-store',
      credentials: 'omit',
    });
  } catch {
    return {
      ok: false,
      code: 'BRIDGE_UNREACHABLE',
      message: "LEFA can't reach the trading service right now.",
    };
  }

  if (!response.ok) {
    return {
      ok: false,
      code: 'BRIDGE_HTTP_ERROR',
      message: "LEFA can't reach the trading service right now.",
    };
  }

  let payload: unknown;
  try {
    payload = await response.json();
  } catch {
    return {
      ok: false,
      code: 'BRIDGE_INVALID_RECEIPT',
      message: 'LEFA could not verify the trading connection.',
    };
  }

  if (!isSovereignBridgeStatus(payload)) {
    return {
      ok: false,
      code: 'BRIDGE_INVALID_RECEIPT',
      message: 'LEFA could not verify the trading connection.',
    };
  }

  if (payload.bridge_state !== 'VERIFIED') {
    return {
      ok: false,
      code: 'BRIDGE_NOT_VERIFIED',
      message: friendlyHoldMessage(payload),
    };
  }

  return { ok: true, status: payload };
}
