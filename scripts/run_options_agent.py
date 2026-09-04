"""
LEFA AI - Alpaca paper options agent runner.

Every account, market, contract, rationale, and order result in this runner is
provider-backed. Missing or invalid evidence stops the cycle; it is never
replaced with a simulated account, hard-coded quote, fake contract, or queued
execution claim.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import os
import sys
from collections import defaultdict
from datetime import UTC, datetime
from decimal import ROUND_DOWN, Decimal, InvalidOperation
from typing import Any

from alpaca.common.exceptions import APIError

# Ensure src is on the Python path when the script is run directly.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from lefa.alpaca import AlpacaPaperBroker, ReadOnlyAlpaca
from lefa.config import Settings
from lefa.featherless import FeatherlessReasoner, FeatherlessUnavailable
from lefa.governance import (
    AccountState,
    Decision,
    RiskPolicy,
    TradeProposal,
    calculate_open_risk,
)

_PROVIDER_ERRORS = (
    APIError,
    ConnectionError,
    TimeoutError,
    OSError,
    RuntimeError,
    TypeError,
    ValueError,
    InvalidOperation,
)


def _settings() -> Settings:
    try:
        return Settings()
    except ValueError as exc:
        raise RuntimeError("PAPER_CONFIGURATION_INVALID") from exc


def get_alpaca_account() -> dict[str, Any]:
    """Read and validate the configured Alpaca paper account."""
    account = ReadOnlyAlpaca(_settings()).get_account()
    status = str(account["status"]).upper()
    if (
        status != "ACTIVE"
        or account["account_blocked"]
        or account["trading_blocked"]
        or account["trade_suspended_by_user"]
    ):
        raise RuntimeError("ALPACA_ACCOUNT_NOT_TRADABLE")

    return {
        "account_id": account["id"],
        "account_number": account["account_number"],
        "status": status,
        "equity": Decimal(account["equity"]),
        "last_equity": Decimal(account["last_equity"]),
        "buying_power": Decimal(account["buying_power"]),
        "cash": Decimal(account["cash"]),
        "options_level": account["options_level"],
    }


def get_alpaca_quote(symbol: str) -> dict[str, str]:
    """Read one current underlying quote from Alpaca."""
    return ReadOnlyAlpaca(_settings()).get_latest_quote(symbol)


def _option_structure(
    broker: AlpacaPaperBroker,
    symbol: str,
    underlying_mid: Decimal,
    *,
    quantity: int = 1,
) -> dict[str, Any]:
    """Choose a quoted, same-expiration bull put spread from active contracts."""
    if quantity < 1 or underlying_mid <= 0:
        raise ValueError("OPTIONS_PARAMETERS_INVALID")
    contracts = broker.get_option_contracts(symbol, "put", limit=100)
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for contract in contracts:
        contract_symbol_raw = contract.get("symbol")
        expiration_raw = contract.get("expiration_date")
        strike_raw = contract.get("strike_price")
        contract_type = str(contract.get("type", "put")).strip().lower()
        contract_status = str(contract.get("status", "active")).strip().lower()
        if (
            not contract_symbol_raw
            or expiration_raw is None
            or not str(expiration_raw).strip()
            or contract_type != "put"
            or contract_status != "active"
            or strike_raw is None
        ):
            continue
        contract_symbol = str(contract_symbol_raw).strip().upper()
        expiration = str(expiration_raw).strip()
        try:
            strike = Decimal(str(strike_raw))
        except (InvalidOperation, ValueError, TypeError):
            continue
        if strike > 0 and strike < underlying_mid:
            normalized = dict(contract)
            normalized["symbol"] = contract_symbol
            normalized["expiration_date"] = expiration
            normalized["strike"] = strike
            grouped[expiration].append(normalized)

    candidates: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for expiration in sorted(grouped):
        by_strike: dict[Decimal, dict[str, Any]] = {}
        for contract in sorted(grouped[expiration], key=lambda item: item["strike"], reverse=True):
            by_strike.setdefault(contract["strike"], contract)
        ordered = list(by_strike.values())
        candidates.extend(itertools.pairwise(ordered))
        if candidates:
            break

    if not candidates:
        raise RuntimeError("OPTIONS_CONTRACTS_UNAVAILABLE")

    quote_symbols = [
        symbol_name
        for pair in candidates[:12]
        for symbol_name in (pair[0]["symbol"], pair[1]["symbol"])
    ]
    quotes = broker.get_option_quotes(quote_symbols)
    for short_contract, long_contract in candidates[:12]:
        short_quote = quotes.get(short_contract["symbol"])
        long_quote = quotes.get(long_contract["symbol"])
        if not short_quote or not long_quote:
            continue
        try:
            short_bid = Decimal(short_quote["bid_price"])
            long_ask = Decimal(long_quote["ask_price"])
            short_ask = Decimal(short_quote["ask_price"])
            long_bid = Decimal(long_quote["bid_price"])
        except (InvalidOperation, KeyError, ValueError, TypeError):
            continue
        if (
            short_bid <= 0
            or short_ask <= 0
            or long_bid <= 0
            or long_ask <= 0
            or short_bid > short_ask
            or long_bid > long_ask
        ):
            continue
        credit = (short_bid - long_ask).quantize(Decimal("0.01"), rounding=ROUND_DOWN)
        width = short_contract["strike"] - long_contract["strike"]
        if credit <= 0 or width <= credit:
            continue

        maximum_loss = (width - credit) * Decimal(100) * quantity
        return {
            "expiration_date": str(short_contract["expiration_date"]),
            "short_symbol": str(short_contract["symbol"]),
            "long_symbol": str(long_contract["symbol"]),
            "short_strike": str(short_contract["strike"]),
            "long_strike": str(long_contract["strike"]),
            "width": str(width),
            "credit_per_share": str(credit),
            "maximum_loss": maximum_loss,
            "short_quote": short_quote,
            "long_quote": long_quote,
        }

    raise RuntimeError("OPTIONS_QUOTES_UNAVAILABLE")


def _hold_result(code: str, detail: str) -> dict[str, str]:
    print(f"  Execution State:       HOLD ({code})")
    print(f"  Detail:                {detail}")
    return {
        "decision": Decision.HOLD.value,
        "execution_state": "HOLD",
        "provider_code": code,
    }


def run_agent_cycle(symbol: str = "SPY") -> dict[str, Any]:
    print("=" * 70)
    print("  LEFA AI - AUTONOMOUS OPTIONS ALPHA AGENT")
    print("  Alpaca AI Trading Agents Hackathon (Options Alpha Track)")
    print("  Official Partner: Featherless AI (Qwen/Qwen2.5-7B-Instruct)")
    print("=" * 70)
    print(f"Timestamp: {datetime.now(UTC).isoformat()}")

    normalized_symbol = symbol.strip().upper()
    if not normalized_symbol:
        return _hold_result("ALPACA_SYMBOL_INVALID", "An underlying symbol is required.")

    print("\n[STEP 1: READING ALPACA PAPER ACCOUNT]")
    try:
        account = get_alpaca_account()
    except _PROVIDER_ERRORS:
        return _hold_result(
            "ALPACA_ACCOUNT_UNAVAILABLE",
            "LEFA could not verify an active, unblocked Alpaca paper account.",
        )
    print(f"  Account ID:            {account['account_id']}")
    print(f"  Account Status:        {account['status']}")
    print(f"  Current Equity:        ${account['equity']:,.2f}")
    print(f"  Cash Balance:          ${account['cash']:,.2f}")
    print(f"  Buying Power:          ${account['buying_power']:,.2f}")
    print(f"  Options Level:         {account['options_level'] or 'N/A'}")
    print("  Broker Mode:           Direct Alpaca Paper API")

    print(f"\n[STEP 2: READING ALPACA MARKET DATA - {normalized_symbol}]")
    try:
        underlying_quote = get_alpaca_quote(normalized_symbol)
        underlying_mid = (
            Decimal(underlying_quote["bid_price"]) + Decimal(underlying_quote["ask_price"])
        ) / Decimal(2)
        if underlying_mid <= 0:
            raise ValueError("ALPACA_UNDERLYING_QUOTE_INVALID")
    except _PROVIDER_ERRORS:
        return _hold_result(
            "ALPACA_UNDERLYING_QUOTE_UNAVAILABLE",
            "LEFA could not obtain a valid current quote for the underlying.",
        )
    print(
        f"  Bid / Ask:             ${underlying_quote['bid_price']} / "
        f"${underlying_quote['ask_price']}"
    )
    print(f"  Midpoint:               ${underlying_mid:.2f}")
    print(f"  Quote Timestamp:        {underlying_quote['timestamp']}")

    print("\n[STEP 3: READING ALPACA OPTION CONTRACTS AND QUOTES]")
    try:
        broker = AlpacaPaperBroker()
        structure = _option_structure(broker, normalized_symbol, underlying_mid)
    except _PROVIDER_ERRORS:
        return _hold_result(
            "ALPACA_OPTIONS_MARKET_DATA_UNAVAILABLE",
            "LEFA could not obtain two active, quoted same-expiration option contracts.",
        )
    print(f"  Expiration:             {structure['expiration_date']}")
    print(f"  Short Put:              {structure['short_symbol']}")
    print(f"  Long Put:               {structure['long_symbol']}")
    print(f"  Width:                  ${structure['width']}")
    print(f"  Conservative Credit:    ${structure['credit_per_share']} / share")

    print("\n[STEP 4: FEATHERLESS AI SERVERLESS REASONING]")
    try:
        reasoner = FeatherlessReasoner()
        configured = reasoner.is_configured()
    except _PROVIDER_ERRORS:
        reasoner = None
        configured = False
    if not configured or reasoner is None:
        return _hold_result(
            "FEATHERLESS_NOT_CONFIGURED",
            "No live Featherless rationale is available for this cycle.",
        )
    print(f"  Featherless Status:     ONLINE (Model: {reasoner.model})")
    market_prompt = (
        f"Underlying: {normalized_symbol}; bid {underlying_quote['bid_price']}; "
        f"ask {underlying_quote['ask_price']}; midpoint {underlying_mid:.2f}. "
        f"Proposed bull put spread: sell {structure['short_symbol']} at "
        f"{structure['short_strike']} and buy {structure['long_symbol']} at "
        f"{structure['long_strike']}; conservative quoted credit "
        f"{structure['credit_per_share']} per share; maximum loss "
        f"{structure['maximum_loss']}. Explain the market evidence and risk boundaries "
        "without inventing volatility, delta, or missing facts."
    )
    try:
        explanation = reasoner.complete(
            [
                {
                    "role": "system",
                    "content": (
                        "You are LEFA AI, an institutional options alpha reasoning engine. "
                        "Provide a concise market regime evaluation using only supplied facts."
                    ),
                },
                {"role": "user", "content": market_prompt},
            ],
            max_tokens=150,
        )
    except FeatherlessUnavailable as exc:
        return _hold_result(
            f"FEATHERLESS_{exc.code}",
            "LEFA could not produce a live rationale from Featherless AI.",
        )
    print(f'\n  Featherless AI Rationale:\n  "{explanation}"')

    print("\n[STEP 5: DETERMINISTIC RISK FIREWALL EVALUATION]")
    try:
        account_state = AccountState(
            equity=account["equity"],
            open_risk=calculate_open_risk(broker.get_positions()),
            daily_pnl=account["equity"] - account["last_equity"],
        )
    except _PROVIDER_ERRORS:
        return _hold_result(
            "ALPACA_OPEN_RISK_UNAVAILABLE",
            "LEFA could not calculate existing portfolio exposure from Alpaca positions.",
        )
    proposal = TradeProposal(
        symbol=normalized_symbol,
        structure="vertical_credit_spread",
        maximum_loss=structure["maximum_loss"],
    )
    policy = RiskPolicy(
        allowed_symbols=frozenset({"SPY", "QQQ", "AAPL", "NVDA"}),
        allowed_structures=frozenset({"vertical_credit_spread"}),
    )
    receipt = policy.evaluate(account_state, proposal)
    status_icon = "[PASS] APPROVE" if receipt.decision == Decision.APPROVE else "[FAIL] REJECT"
    print(f"  Risk Decision:         {status_icon}")
    print(f"  Evaluated Reasons:     {', '.join(receipt.reasons)}")
    print(f"  Calculated Max Loss:   ${proposal.maximum_loss:,.2f}")

    legs = [
        {
            "action": "sell_to_open",
            "symbol": structure["short_symbol"],
            "strike": structure["short_strike"],
            "type": "put",
            "ratio_qty": "1",
            "side": "sell",
        },
        {
            "action": "buy_to_open",
            "symbol": structure["long_symbol"],
            "strike": structure["long_strike"],
            "type": "put",
            "ratio_qty": "1",
            "side": "buy",
        },
    ]
    receipt_data: dict[str, Any] = {
        "receipt_id": str(receipt.receipt_id),
        "timestamp": receipt.created_at.isoformat(),
        "account_id": account["account_id"],
        "symbol": proposal.symbol,
        "structure": proposal.structure,
        "max_loss_usd": str(proposal.maximum_loss),
        "decision": receipt.decision.value,
        "reasons": receipt.reasons,
        "ai_explanation": explanation,
        "alpaca_tool": "AlpacaPaperBroker.place_option_order",
        "alpaca_order_class": "mleg",
        "legs": legs,
        "execution_state": "RISK_REJECTED"
        if receipt.decision != Decision.APPROVE
        else "NOT_SUBMITTED",
    }

    print("\n[STEP 6: GOVERNED ALPACA PAPER ORDER]")
    if receipt.decision != Decision.APPROVE:
        print("  Execution State:       RISK_REJECTED (no order submitted)")
    else:
        try:
            order_res = broker.place_option_order(
                order_class="mleg",
                time_in_force="day",
                limit_price=Decimal(structure["credit_per_share"]),
                legs=legs,
                qty=1,
                client_order_id=f"lefa-{str(receipt.receipt_id)[:12]}",
            )
            order_id = order_res.get("order_id")
            order_status = order_res.get("status")
            submitted_at = order_res.get("submitted_at")
            if not order_id or not order_status:
                raise ValueError("ALPACA_ORDER_RESPONSE_INVALID")
            receipt_data.update(
                {
                    "alpaca_order_id": order_id,
                    "alpaca_order_status": order_status,
                    "alpaca_submitted_at": submitted_at,
                    "execution_state": "ORDER_SUBMITTED",
                }
            )
            print(f"  Alpaca Order ID:       {order_id}")
            print(f"  Alpaca Order Status:   {order_status}")
            print("  Execution State:       ORDER_SUBMITTED (paper API confirmed receipt)")
        except _PROVIDER_ERRORS:
            receipt_data["execution_state"] = "HOLD"
            receipt_data["provider_code"] = "ALPACA_ORDER_SUBMISSION_FAILED"
            print("  Execution State:       HOLD (Alpaca did not confirm order submission)")

    raw_json = json.dumps(receipt_data, sort_keys=True)
    receipt_hash = hashlib.sha256(raw_json.encode()).hexdigest()
    receipt_data["receipt_sha256"] = receipt_hash
    print(f"  Receipt ID:            {receipt.receipt_id}")
    print(f"  SHA-256 Hash:          {receipt_hash}")
    print("=" * 70)
    return receipt_data


if __name__ == "__main__":
    sym = sys.argv[1] if len(sys.argv) > 1 else "SPY"
    run_agent_cycle(sym)
