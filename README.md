# LEFA AI

**Sovereign governance before market execution.**

LEFA AI is a Kopano Context-governed paper-trading agent for Alpaca. The first proof of concept is deliberately read-only: it observes an Alpaca paper account, normalizes market state, evaluates proposed defined-risk trades through deterministic policy, and emits inspectable governance receipts.

## Truth lock

- Paper trading only.
- Live trading is prohibited.
- The model may propose; deterministic policy approves or rejects.
- No order route exists in the baseline.
- Every decision produces a machine-readable receipt.

## Baseline flow

`Alpaca paper account -> observation -> proposal -> risk firewall -> receipt`

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
cp .env.example .env
pytest
lefa account
```

Set paper credentials in `.env`. Never commit credentials.

## Initial policy

| Boundary | Value |
|---|---:|
| Environment | Paper only |
| Symbol universe | SPY |
| Maximum risk per proposal | 0.5% equity |
| Maximum aggregate open risk | 2% equity |
| Daily loss stop | 1% equity |
| Execution | Disabled |

See [NOW.md](NOW.md) for current state and the next governed increment.

## Disclaimer

Research and hackathon software only. It is not financial advice and must not be used for live trading.
