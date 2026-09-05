"""LEFA AI — truthful autonomous options demo runner.

The camera-safe invariant is simple: real provider evidence or HOLD.
No simulated account, hard-coded market price, fabricated AI rationale, contract
fallback, or local claim of broker success is permitted in this runner.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from alpaca.common.exceptions import APIError
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
load_dotenv()

from lefa.alpaca import AlpacaPaperBroker  # noqa: E402
from lefa.config import Settings  # noqa: E402
from lefa.featherless import FeatherlessReasoner, FeatherlessUnavailable  # noqa: E402
from lefa.governance import AccountState, Decision, RiskPolicy, TradeProposal  # noqa: E402
from lefa.options_market import AlpacaOptionsMarket, CreditSpreadCandidate  # noqa: E402

ALLOWED_SYMBOLS = ("SPY", "QQQ", "AAPL", "NVDA")
COMPETITION_BASELINE_EQUITY = Decimal("100000.00")
MAX_DRAWDOWN_FRACTION = Decimal("0.05")


def _money(value: Decimal) -> str:
    return f"${value:,.2f}"


def _account_ref(account_id: str) -> str:
    clean = account_id.strip()
    return f"…{clean[-8:]}" if len(clean) > 8 else clean


def _level(value: Any) -> int | None:
    raw = getattr(value, "value", value)
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None


def _hold(code: str, detail: str, *, evidence: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = {
        "state": "HOLD",
        "code": code,
        "detail": detail,
        "observed_at": datetime.now(UTC).isoformat(),
        "evidence": evidence or {},
    }
    print(f"\n[HOLD] {code}")
    print(f"  {detail}")
    return payload


def _scan_market(
    market: AlpacaOptionsMarket,
    symbols: tuple[str, ...],
) -> tuple[CreditSpreadCandidate | None, dict[str, str]]:
    errors: dict[str, str] = {}
    for symbol in symbols:
        print(f"  Scanning {symbol} against live Alpaca stock/options evidence…")
        try:
            candidate = market.candidate(symbol, quantity=1)
        except (APIError, OSError, RuntimeError, ValueError) as exc:
            errors[symbol] = f"{type(exc).__name__}: {exc}"
            print(f"    HOLD {symbol}: provider evidence unavailable")
            continue
        if candidate is not None:
            print(f"    PASS {symbol}: admissible defined-risk candidate found")
            return candidate, errors
        print(f"    HOLD {symbol}: strategy gates not satisfied by provider evidence")
    return None, errors


def _reason_about_candidate(
    reasoner: FeatherlessReasoner,
    candidate: CreditSpreadCandidate,
) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You are LEFA AI, an options-market reasoning renter. You may explain only the "
                "provider facts supplied by the user. Do not invent prices, Greeks, fills, P&L, "
                "or broker state. You have zero execution authority. Return at most 90 words."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Underlying {candidate.underlying}; spot {candidate.spot}; "
                f"20-session annualized RV {candidate.realized_volatility:.4f}; "
                f"ATM IV {candidate.atm_implied_volatility:.4f}; "
                f"IV/RV {candidate.iv_rv_ratio:.3f}; DTE {candidate.dte}; "
                f"short put {candidate.short_leg.symbol} strike {candidate.short_leg.strike} "
                f"delta {candidate.short_leg.delta:.3f} bid {candidate.short_leg.bid} "
                f"ask {candidate.short_leg.ask}; long put {candidate.long_leg.symbol} "
                f"strike {candidate.long_leg.strike} bid {candidate.long_leg.bid} "
                f"ask {candidate.long_leg.ask}; conservative net credit "
                f"{candidate.net_credit}; maximum loss {candidate.maximum_loss}. "
                "Explain why this candidate either fits or remains bounded by the declared "
                "defined-risk volatility-premium strategy."
            ),
        },
    ]
    return reasoner.complete(messages, max_tokens=140, temperature=0.1)


def run_agent_cycle(symbol: str = "AUTO", *, execute: bool = False) -> dict[str, Any]:
    print("=" * 78)
    print("  LEFA AI — GOVERNED AUTONOMOUS OPTIONS ALPHA AGENT")
    print("  TRUTH MODE: REAL PROVIDER EVIDENCE OR HOLD")
    print("=" * 78)
    print(f"Run timestamp: {datetime.now(UTC).isoformat()}")

    print("\n[1/6] ALPACA PAPER ACCOUNT REHYDRATION")
    try:
        settings = Settings()
        broker = AlpacaPaperBroker(settings)
        account = broker.get_account()
        positions = broker.get_positions()
        open_orders = broker.get_orders("open")
    except (APIError, OSError, RuntimeError, ValueError) as exc:
        return _hold(
            "ALPACA_ACCOUNT_UNAVAILABLE",
            f"LEFA could not verify the configured Alpaca paper account: {type(exc).__name__}",
        )

    account_status = str(account["status"]).upper()
    options_level = _level(account["options_trading_level"] or account["options_approved_level"])
    print(f"  Account:              {_account_ref(str(account['id']))}")
    print(f"  Status:               {account_status}")
    print(f"  Equity:               {_money(account['equity'])}")
    print(f"  Cash:                 {_money(account['cash'])}")
    print(f"  Buying power:         {_money(account['buying_power'])}")
    print(f"  Options level:        {options_level if options_level is not None else 'UNKNOWN'}")
    print(f"  Existing positions:   {len(positions)}")
    print(f"  Existing open orders: {len(open_orders)}")

    if "ACTIVE" not in account_status:
        return _hold("ACCOUNT_NOT_ACTIVE", "Alpaca paper account is not ACTIVE.")
    if account["account_blocked"] or account["trading_blocked"] or account["trade_suspended_by_user"]:
        return _hold("ACCOUNT_RESTRICTED", "Alpaca reports a trading restriction on the paper account.")
    if options_level is None or options_level < 3:
        return _hold("OPTIONS_LEVEL_INSUFFICIENT", "Level 3 options permission is not verified.")
    if positions:
        return _hold(
            "OPEN_POSITIONS_REQUIRE_RISK_REHYDRATION",
            "Existing positions are present; LEFA refuses to assume their defined risk is zero.",
            evidence={"position_count": len(positions)},
        )
    if open_orders:
        return _hold(
            "OPEN_ORDERS_PRESENT",
            "Existing broker orders are present; LEFA will not stack a new demo order over them.",
            evidence={"open_order_count": len(open_orders)},
        )

    baseline = Decimal(os.getenv("LEFA_COMPETITION_BASELINE_EQUITY", str(COMPETITION_BASELINE_EQUITY)))
    drawdown = max(Decimal("0"), baseline - account["equity"])
    drawdown_fraction = drawdown / baseline
    print(f"  Competition baseline: {_money(baseline)}")
    print(f"  Baseline drawdown:    {drawdown_fraction * 100:.2f}%")
    if drawdown_fraction >= MAX_DRAWDOWN_FRACTION:
        return _hold(
            "MAX_DRAWDOWN_CIRCUIT_BREAKER",
            "Verified equity is at or beyond the 5% competition drawdown ceiling.",
            evidence={"drawdown_fraction": str(drawdown_fraction)},
        )

    print("\n[2/6] LIVE ALPACA MARKET + OPTIONS EVIDENCE")
    requested = symbol.upper()
    if requested == "AUTO":
        scan_symbols = ALLOWED_SYMBOLS
    elif requested in ALLOWED_SYMBOLS:
        scan_symbols = (requested,)
    else:
        return _hold(
            "SYMBOL_NOT_ALLOWED",
            f"{requested} is outside LEFA's governed universe: {', '.join(ALLOWED_SYMBOLS)}.",
        )

    try:
        market = AlpacaOptionsMarket(settings)
    except ValueError as exc:
        return _hold("MARKET_CLIENT_UNAVAILABLE", str(exc))

    candidate, scan_errors = _scan_market(market, scan_symbols)
    if candidate is None:
        return _hold(
            "NO_ADMISSIBLE_MARKET_CANDIDATE",
            "No symbol satisfied the live 7–21 DTE, delta, liquidity, IV/RV, and credit gates.",
            evidence={"provider_errors": scan_errors},
        )

    print(f"  Selected underlying:  {candidate.underlying}")
    print(f"  Retrieved spot:       {_money(candidate.spot)}")
    print(f"  20-session RV:        {candidate.realized_volatility * 100:.2f}%")
    print(f"  ATM IV:               {candidate.atm_implied_volatility * 100:.2f}%")
    print(f"  IV/RV ratio:          {candidate.iv_rv_ratio:.3f} (gate ≥ 1.150)")
    print(f"  Expiration horizon:   {candidate.dte} DTE")
    print(
        f"  Short put:            {candidate.short_leg.symbol} | "
        f"Δ {candidate.short_leg.delta:.3f} | {candidate.short_leg.bid}/{candidate.short_leg.ask}"
    )
    print(
        f"  Protective put:       {candidate.long_leg.symbol} | "
        f"Δ {candidate.long_leg.delta:.3f} | {candidate.long_leg.bid}/{candidate.long_leg.ask}"
    )
    print(f"  Conservative credit:  {_money(candidate.net_credit * 100)} per spread")
    print(f"  Maximum defined loss: {_money(candidate.maximum_loss)}")

    print("\n[3/6] FEATHERLESS AI REASONING")
    reasoner = FeatherlessReasoner()
    if not reasoner.is_configured():
        return _hold(
            "FEATHERLESS_NOT_CONFIGURED",
            "The AI reasoning provider is not configured; LEFA will not substitute canned rationale.",
        )
    try:
        rationale = _reason_about_candidate(reasoner, candidate)
    except FeatherlessUnavailable as exc:
        return _hold(
            "FEATHERLESS_UNAVAILABLE",
            f"Live Featherless inference failed with provider code {exc.code}; no fallback was invented.",
        )
    print(f"  Model:                {reasoner.model}")
    print(f"  Rationale:            {rationale}")

    print("\n[4/6] DETERMINISTIC RISK FIREWALL")
    account_state = AccountState(
        equity=account["equity"],
        open_risk=Decimal("0.00"),
        daily_pnl=account["equity"] - account["last_equity"],
    )
    proposal = TradeProposal(
        symbol=candidate.underlying,
        structure="vertical_credit_spread",
        maximum_loss=candidate.maximum_loss,
    )
    policy = RiskPolicy(
        allowed_symbols=frozenset(ALLOWED_SYMBOLS),
        allowed_structures=frozenset({"vertical_credit_spread"}),
        max_trade_risk_fraction=Decimal("0.03"),
        max_open_risk_fraction=Decimal("0.12"),
        daily_loss_stop_fraction=Decimal("0.05"),
    )
    receipt = policy.evaluate(account_state, proposal)
    print(f"  Decision:             {receipt.decision.value.upper()}")
    print(f"  Reasons:              {', '.join(receipt.reasons)}")
    print(
        f"  Trade max-loss ratio: {(proposal.maximum_loss / account_state.equity) * 100:.3f}% "
        "(gate ≤ 3.000%)"
    )
    if receipt.decision is not Decision.APPROVE:
        return _hold(
            "DETERMINISTIC_RISK_REJECT",
            "The proposal failed LEFA's zero-override financial policy.",
            evidence={"reasons": receipt.reasons},
        )

    print("\n[5/6] CONTENT-HASHED EXECUTION INTENT")
    receipt_data: dict[str, Any] = {
        "schema": "kopano.lefa.options-demo-receipt.v2",
        "receipt_id": str(receipt.receipt_id),
        "created_at": receipt.created_at.isoformat(),
        "paper_account_ref": _account_ref(str(account["id"])),
        "paper_mode": True,
        "symbol": candidate.underlying,
        "structure": proposal.structure,
        "market_evidence": {
            "retrieved_at": candidate.observed_at,
            "spot": str(candidate.spot),
            "realized_volatility": candidate.realized_volatility,
            "atm_implied_volatility": candidate.atm_implied_volatility,
            "iv_rv_ratio": candidate.iv_rv_ratio,
            "dte": candidate.dte,
            "short_leg": {
                "symbol": candidate.short_leg.symbol,
                "strike": str(candidate.short_leg.strike),
                "delta": candidate.short_leg.delta,
                "bid": str(candidate.short_leg.bid),
                "ask": str(candidate.short_leg.ask),
            },
            "long_leg": {
                "symbol": candidate.long_leg.symbol,
                "strike": str(candidate.long_leg.strike),
                "delta": candidate.long_leg.delta,
                "bid": str(candidate.long_leg.bid),
                "ask": str(candidate.long_leg.ask),
            },
            "net_credit": str(candidate.net_credit),
            "signed_alpaca_limit_price": str(candidate.signed_alpaca_limit_price),
            "maximum_loss": str(candidate.maximum_loss),
        },
        "ai": {"provider": "Featherless", "model": reasoner.model, "rationale": rationale},
        "risk": {"decision": receipt.decision.value, "reasons": receipt.reasons},
        "execution_requested": execute,
    }
    intent_json = json.dumps(receipt_data, sort_keys=True, separators=(",", ":"))
    intent_hash = hashlib.sha256(intent_json.encode()).hexdigest()
    receipt_data["intent_sha256"] = intent_hash
    print(f"  Receipt ID:           {receipt.receipt_id}")
    print(f"  Intent SHA-256:       {intent_hash}")
    print(f"  Alpaca limit sign:    {candidate.signed_alpaca_limit_price} (negative = credit)")

    print("\n[6/6] ALPACA PAPER EXECUTION")
    if not execute:
        receipt_data["execution"] = {
            "state": "NOT_REQUESTED",
            "detail": "Run again with --execute to request the governed paper order.",
        }
        print("  Execution state:      NOT_REQUESTED")
        print("  No broker write occurred. Use --execute only when you want the paper order submitted.")
    else:
        try:
            submitted = broker.place_option_order(
                symbol=candidate.underlying,
                order_class="mleg",
                order_type="limit",
                time_in_force="day",
                limit_price=candidate.signed_alpaca_limit_price,
                legs=candidate.legs_payload,
                qty=1,
                client_order_id=f"lefa-{str(receipt.receipt_id)[:12]}",
            )
            order_id = str(submitted["order_id"])
            confirmed = broker.get_order(order_id)
        except (APIError, OSError, RuntimeError, ValueError) as exc:
            receipt_data["execution"] = {
                "state": "HOLD",
                "code": "ALPACA_ORDER_NOT_CONFIRMED",
                "provider_error_type": type(exc).__name__,
            }
            print("  Execution state:      HOLD")
            print(f"  Alpaca order was not confirmed: {type(exc).__name__}")
        else:
            status = str(confirmed.get("status") or "UNKNOWN")
            confirmed_id = str(confirmed.get("order_id") or "")
            if confirmed_id != order_id:
                receipt_data["execution"] = {
                    "state": "HOLD",
                    "code": "PROVIDER_ORDER_ID_MISMATCH",
                    "submitted_order_id": order_id,
                    "confirmed_order_id": confirmed_id,
                }
                print("  Execution state:      HOLD — provider confirmation ID mismatch")
            else:
                receipt_data["execution"] = {
                    "state": "PROVIDER_RECEIPT_CONFIRMED",
                    "order_id": order_id,
                    "client_order_id": submitted.get("client_order_id"),
                    "status": status,
                    "submitted_at": confirmed.get("submitted_at"),
                    "order_class": confirmed.get("order_class"),
                    "signed_limit_price": str(candidate.signed_alpaca_limit_price),
                }
                print("  Execution truth:      PROVIDER_RECEIPT_CONFIRMED")
                print(f"  Alpaca order ID:      {order_id}")
                print(f"  Provider status:      {status}")
                print("  Fill state:           not claimed unless Alpaca status itself reports a fill")

    final_json = json.dumps(receipt_data, sort_keys=True, separators=(",", ":"))
    final_hash = hashlib.sha256(final_json.encode()).hexdigest()
    receipt_data["final_sha256"] = final_hash

    print("\n" + "=" * 78)
    print("  JUDGE RECEIPT")
    print(f"  Symbol:               {candidate.underlying}")
    print(f"  Risk decision:        {receipt.decision.value.upper()}")
    print(f"  Execution state:      {receipt_data['execution']['state']}")
    print(f"  Final SHA-256:        {final_hash}")
    print("  Claim boundary:       no simulation, no synthetic provider success, paper only")
    print("=" * 78)
    return receipt_data


def main() -> None:
    parser = argparse.ArgumentParser(description="Run LEFA's camera-safe options agent cycle")
    parser.add_argument(
        "--symbol",
        default="AUTO",
        help="SPY, QQQ, AAPL, NVDA, or AUTO to scan the governed universe",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Submit the approved candidate to Alpaca Paper and verify the provider order receipt",
    )
    args = parser.parse_args()
    run_agent_cycle(args.symbol, execute=args.execute)


if __name__ == "__main__":
    main()
