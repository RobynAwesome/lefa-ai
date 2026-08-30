/**
 * LEFA AI Frontend API Client
 * ============================
 * Bridges the React frontend to the governed Python backend.
 *
 * Governance boundaries:
 * - Credentials (API keys, secrets) NEVER pass through this client.
 *   They are used locally by the Alpaca SDK; only sanitized non-secret
 *   evidence (namespace, paper_trade flag, tool names, status flags)
 *   is forwarded to /api/mcp/verify.
 * - The snapshot endpoint returns explicit fixture state when not connected.
 *   No believable fake financial values are invented.
 *
 * I_AM_STATELESS_RENTER_NOT_LANDLORD
 */

export interface MCPVerifyRequest {
  namespace: string | null;
  server_identity: string | null;
  server_version: string | null;
  paper_trade: boolean | null;
  tool_names: string[];
  account_status: string | null;
  account_blocked: boolean | null;
  trading_blocked: boolean | null;
  auth_ok: boolean;
  network_ok: boolean;
  schema_ok: boolean;
}

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
 * Submit sanitized MCP runtime evidence to the governed proof gate.
 * Credentials must never appear in the evidence object.
 */
export async function verifyMCPEvidence(
  evidence: MCPVerifyRequest
): Promise<MCPVerifyResponse> {
  const res = await fetch(`${BASE}/mcp/verify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(evidence),
  });
  if (!res.ok) {
    throw new Error(`MCP verify failed: ${res.status} ${res.statusText}`);
  }
  return res.json() as Promise<MCPVerifyResponse>;
}

/**
 * Fetch the current LEFA snapshot.
 * Returns explicit fixture state (no fake balances) when not connected.
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
