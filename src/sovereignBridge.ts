/**
 * LEFA AI — Sovereign Bridge
 * ==========================
 * Verifies the Alpaca paper runtime proof by calling the governed Python backend.
 *
 * On lefa-core-live.vercel.app this calls /api/mcp/status (same origin).
 * Locally, Vite proxies /api → http://localhost:8000.
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
        | 'BRIDGE_UNCONFIGURED'
        | 'BRIDGE_UNREACHABLE'
        | 'BRIDGE_HTTP_ERROR'
        | 'BRIDGE_INVALID_RECEIPT'
        | 'BRIDGE_NOT_VERIFIED';
      message: string;
    };

const RECEIPT_SCHEMA = 'kopano.alpaca.decision-receipt.v1';
const BRIDGE_SCHEMA = 'kopano.lefa.sovereign-bridge-status.v1';
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

/**
 * Adapter: converts the Python backend MCPVerifyResponse to the canonical
 * SovereignBridgeStatus contract expected by the UI.
 *
 * Python /api/mcp/status returns:
 *   { status: 'ready'|'blocked', failures: string[], namespace: string|null,
 *     server_identity: string|null, paper_trade: bool|null,
 *     readable_tool_names: string[], observed_at: string }
 */
function adaptPythonMcpResponse(payload: Record<string, unknown>): SovereignBridgeStatus {
  const isReady = payload.status === 'ready';
  return {
    schema: 'kopano.lefa.sovereign-bridge-status.v1',
    provider: 'alpaca',
    environment: 'paper',
    bridge_state: isReady ? 'VERIFIED' : 'HOLD',
    execution_authority: 'BACKEND_ONLY',
    observed_at: typeof payload.observed_at === 'string' ? payload.observed_at : new Date().toISOString(),
    latest_receipt: null,
    truth_boundary: isReady
      ? 'Alpaca paper runtime verified — OBSERVE only, no execution authority.'
      : `Bridge hold: ${Array.isArray(payload.failures) ? (payload.failures as string[]).join(', ') : 'runtime evidence unavailable'}`,
  };
}

function configuredStatusUrl(): string {
  const meta = import.meta as ImportMeta & {
    env?: Record<string, string | undefined>;
  };
  const raw = meta.env?.VITE_LEFA_SOVEREIGN_STATUS_URL?.trim();
  // Default to same-origin Python backend. Works on lefa-core-live.vercel.app
  // and in local dev when the Vite proxy forwards /api → :8000.
  return raw || '/api/mcp/status';
}

export async function verifySovereignBridge(): Promise<SovereignBridgeVerification> {
  const url = configuredStatusUrl();

  let response: Response;
  try {
    response = await fetch(url, {
      method: 'GET',
      headers: { Accept: 'application/json' },
      cache: 'no-store',
      credentials: 'omit',
    });
  } catch {
    return {
      ok: false,
      code: 'BRIDGE_UNREACHABLE',
      message: 'The sovereign status endpoint is unreachable. Receipt or HOLD.',
    };
  }

  if (!response.ok) {
    return {
      ok: false,
      code: 'BRIDGE_HTTP_ERROR',
      message: `The sovereign status endpoint returned HTTP ${response.status}. LEFA remains disconnected.`,
    };
  }

  let payload: unknown;
  try {
    payload = await response.json();
  } catch {
    return {
      ok: false,
      code: 'BRIDGE_INVALID_RECEIPT',
      message: 'The sovereign status endpoint did not return valid JSON.',
    };
  }

  if (!isRecord(payload)) {
    return {
      ok: false,
      code: 'BRIDGE_INVALID_RECEIPT',
      message: 'The response was not a JSON object.',
    };
  }

  // Accept the canonical BRIDGE_SCHEMA directly (future backend upgrade)
  if (isSovereignBridgeStatus(payload)) {
    if (payload.bridge_state !== 'VERIFIED') {
      return {
        ok: false,
        code: 'BRIDGE_NOT_VERIFIED',
        message: 'The sovereign bridge reported HOLD. LEFA will not promote the provider to connected.',
      };
    }
    return { ok: true, status: payload };
  }

  // Adapt Python MCPVerifyResponse → SovereignBridgeStatus
  if (typeof payload.status === 'string') {
    const adapted = adaptPythonMcpResponse(payload);
    if (adapted.bridge_state !== 'VERIFIED') {
      return {
        ok: false,
        code: 'BRIDGE_NOT_VERIFIED',
        message: adapted.truth_boundary ?? 'Alpaca paper runtime proof is not ready.',
      };
    }
    return { ok: true, status: adapted };
  }

  return {
    ok: false,
    code: 'BRIDGE_INVALID_RECEIPT',
    message: 'The response failed the LEFA sovereign bridge contract. No connected state was granted.',
  };
}
