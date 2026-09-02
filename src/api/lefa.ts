/**
 * LEFA AI Frontend API Client
 * ============================
 * Browser clients consume small backend projections. Credentials, provider
 * transport and proof machinery never belong in this layer.
 *
 * I_AM_STATELESS_RENTER_NOT_LANDLORD
 */

export interface RuntimeStatusResponse {
  schema: 'kopano.lefa.runtime-status.v1';
  state: 'SETUP_NEEDED' | 'WAITING_FOR_MARKET' | 'UNAVAILABLE';
  headline: string;
  detail: string;
  observed_at: string;
  connection: {
    state: 'READY' | 'SETUP_NEEDED' | 'UNAVAILABLE';
    label: string;
  };
  market: {
    state: 'WAITING_FOR_EVIDENCE';
    symbol: string | null;
    latest_price: string | null;
    market_state: 'open' | 'closed' | 'unknown';
    observed_at: string | null;
  };
  decision: {
    state: 'NO_DECISION';
  };
  ai: {
    state: 'AVAILABLE' | 'UNAVAILABLE';
    label: string;
  };
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
 * Fetch the only runtime status contract the primary human UI should consume.
 * A healthy Alpaca account does not imply market evidence; absent evidence stays null.
 */
export async function getRuntimeStatus(): Promise<RuntimeStatusResponse> {
  const res = await fetch(`${BASE}/runtime/status`, {
    method: 'GET',
    headers: { Accept: 'application/json' },
    cache: 'no-store',
    credentials: 'omit',
  });
  if (!res.ok) {
    throw new Error(`Runtime status failed: ${res.status}`);
  }
  return res.json() as Promise<RuntimeStatusResponse>;
}

/** Engineering continuity only. Primary runtime must not consume this route. */
export async function getMCPStatus(): Promise<MCPVerifyResponse> {
  const res = await fetch(`${BASE}/mcp/status`);
  if (!res.ok) {
    throw new Error(`MCP status failed: ${res.status} ${res.statusText}`);
  }
  return res.json() as Promise<MCPVerifyResponse>;
}

/**
 * Legacy fixture-aware reference surface. Primary runtime must not use the browser
 * `connected` flag as evidence of a real account or market observation.
 */
export async function getSnapshot(connected: boolean): Promise<SnapshotResponse> {
  const res = await fetch(`${BASE}/snapshot?connected=${connected}`);
  if (!res.ok) {
    throw new Error(`Snapshot fetch failed: ${res.status} ${res.statusText}`);
  }
  return res.json() as Promise<SnapshotResponse>;
}

export async function healthCheck(): Promise<{
  status: string;
  ai_inference_configured?: boolean;
}> {
  const res = await fetch(`${BASE}/health`);
  if (!res.ok) throw new Error('Backend unreachable');
  return res.json();
}

export interface AIExplainResponse {
  explanation: string;
  model: string;
  provider: string;
}

/**
 * Request advisory language for evidence already supplied by the backend/UI caller.
 * This route is not a market-data source.
 */
export async function getAIExplanation(params: {
  symbol: string;
  price?: string | null;
  market_state?: string;
  decision_action?: string | null;
  rationale?: string | null;
  custom_prompt?: string | null;
}): Promise<AIExplainResponse> {
  const res = await fetch(`${BASE}/ai/explain`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params),
  });
  if (!res.ok) {
    throw new Error(`AI explanation unavailable: ${res.status}`);
  }
  return res.json() as Promise<AIExplainResponse>;
}

/** Explain the governance concept; this does not require live market evidence. */
export async function getDualAxisExplanation(): Promise<AIExplainResponse> {
  const res = await fetch(`${BASE}/ai/dual-axis-explainer`);
  if (!res.ok) {
    throw new Error(`AI explanation unavailable: ${res.status}`);
  }
  return res.json() as Promise<AIExplainResponse>;
}
