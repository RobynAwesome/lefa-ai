# NOW - LEFA AI

## Pre-seed

- Repository began with an MIT license only.
- Goal: establish the smallest inspectable KC x Alpaca vertical slice.
- Authority boundary: read-only Alpaca paper telemetry; no order execution.

## Current state

- Python package baseline defined.
- Environment configuration fails closed unless Alpaca paper mode is explicit.
- Account observation adapter is read-only.
- Deterministic risk firewall returns structured governance receipts.
- Unit tests and GitHub Actions validate the firewall without credentials.

## Next proof

1. Confirm paper-account connectivity with `lefa account`.
2. Add SPY quote and option-chain observation.
3. Normalize one vertical-credit-spread proposal.
4. Test approval and rejection receipts against recorded fixtures.
5. Add paper execution only in a separate reviewed pull request.

## Holds

- Live trading: prohibited.
- Autonomous scheduling: prohibited until observation and recovery tests pass.
- Multi-leg MCP execution: held pending adapter validation.

## Post-seed receipt

Baseline is successful when CI passes and a maintainer can retrieve paper-account telemetry without any available order path.
