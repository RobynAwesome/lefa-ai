# Alpaca MCP read-only proof lane

**Status:** POC-0 Issue #2 pre-seed
**Authority:** read-only observation only
**Execution:** no order, cancellation, liquidation, replacement, or exercise route may enter LEFA

This document defines the repository-side proof gate for connecting LEFA to an Alpaca paper MCP session.

The gate does not store secrets, raw MCP config, account numbers, or full payload dumps. It accepts only sanitized runtime evidence that can prove:

- the Alpaca MCP namespace was discovered at runtime;
- server identity/version were recorded without secrets;
- `ALPACA_PAPER_TRADE` was proven `true`;
- authentication and network access succeeded;
- schemas matched the expected read-only proof surface;
- the account was active and not blocked;
- account/market observations were read-only;
- no order-like tool was reachable from the LEFA observation path.

## Runtime evidence contract

Use `lefa.mcp_observation.MCPRuntimeEvidence` for the sanitized proof facts:

- `namespace`
- `server_identity`
- `server_version`
- `paper_trade`
- `tool_names`
- `account_status`
- `account_blocked`
- `trading_blocked`
- `auth_ok`
- `network_ok`
- `schema_ok`
- `observed_at`

Then call `evaluate_read_only_mcp_evidence(...)`.

The result is a `ReadOnlyMCPProof` with either:

- `READY` and no failures; or
- `BLOCKED` plus explicit fail-closed reasons.

## Required fail-closed cases

The proof lane blocks when any of these are true:

- namespace is missing;
- auth failed;
- network failed;
- schema drift is detected;
- paper mode is false or unproven;
- account/trading is blocked;
- any reachable tool name contains order/cancel/replace/liquidate/exercise semantics.

## Governance hold

Passing this gate only proves LEFA may ingest read-only paper observations. It does not authorize order placement, recommendations, autonomous scheduling, account funding, live trading, or changes to Alpaca account settings.
