/**
 * LEFA AI Frontend API Client
 * ============================
 * Bridges the React frontend to the governed Python backend.
 *
 * Governance boundaries:
 * - Credentials (API keys, secrets) NEVER pass through this client.
 * - The browser does not self-assert Alpaca runtime evidence.
 * - MCP readiness comes from backend-owned sanitized runtime proof state.
 * - The snapshot endpoint returns explicit fixture state until live proof exists.
 *
 * I_AM_STATELESS_RENTER_NOT_LANDLORD
 */

export interface MCPVerifyResponse {
  status: 'ready' | 'blocked';
  failures: string[];
  namespace: string | null;
  server_identity: string | null;
  paper_trade: boolean | null;
  readable_tool_names: string[];
  observed_at: string;
}

export interface SnapshotResponse {
  connection_state: 'disconnected' | 'fixture' | 'connected' | 'error';
  account_status: string | null;
  cash: string | null;
  buying_power: string | null;
  portfolio_equity: string | null;
  provenance_source: string;
  provenance_is_fixture: boolean;
  market_symbol: string;
  market_state: 'open' | 'closed' | 'unknown';
  latest_price: string | null;
  decision: {
    decision_id: string;
    proposed_action: string;
    instrument: string;
    rationale_summary: string;
    state: string;
  } | null;
  validation_status: string | null;
  activity_count: number;
}

const BASE = '/api';

/**
 * Ask the backend whether a real sanitized Alpaca paper-runtime proof is ready.
 * The browser cannot manufacture or submit proof material for this decision.
 */
export async function getMCPStatus(): Promise<MCPVerifyResponse> {
  const res = await fetch(`${BASE}/mcp/status`);
  if (!res.ok) {
    throw new Error(`MCP status failed: ${res.status} ${res.statusText}`);
  }
  return res.json() as Promise<MCPVerifyResponse>;
}

/**
 * Fetch the current LEFA snapshot.
 * Returns explicit fixture state until live Alpaca observation is proven.
 */
export async function getSnapshot(connected: boolean): Promise<SnapshotResponse> {
  const res = await fetch(`${BASE}/snapshot?connected=${connected}`);
  if (!res.ok) {
    throw new Error(`Snapshot fetch failed: ${res.status} ${res.statusText}`);
  }
  return res.json() as Promise<SnapshotResponse>;
}

/**
 * Health check — confirms backend is reachable.
 */
export async function healthCheck(): Promise<{ status: string }> {
  const res = await fetch(`${BASE}/health`);
  if (!res.ok) throw new Error('Backend unreachable');
  return res.json();
}
