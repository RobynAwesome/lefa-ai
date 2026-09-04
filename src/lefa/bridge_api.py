"""LEFA's server-side Alpaca paper bridge and runtime projections.

The bridge owns the provider call. It never delegates account truth to another
application and it never exposes credentials or execution authority to the
browser.

REALITY_STATE > INDEX_STATE
RECEIPT OR HOLD
"""
from __future__ import annotations

import os
from datetime import UTC, datetime, timedelta
from decimal import Decimal, InvalidOperation
from typing import Any

from alpaca.common.exceptions import APIError
from fastapi import APIRouter

from lefa.alpaca import ReadOnlyAlpaca
from lefa.config import Settings

router = APIRouter()

BRIDGE_SCHEMA = "kopano.lefa.sovereign-bridge-status.v1"
RUNTIME_SCHEMA = "kopano.lefa.runtime-status.v1"

_UNAVAILABLE_CODES = {
    "PAPER_PROVIDER_ERROR",
    "PAPER_PROVIDER_UNREACHABLE",
}
_REQUIRED_ACCOUNT_FIELDS = {
    "status",
    "account_blocked",
    "trading_blocked",
    "trade_suspended_by_user",
}
_RUNTIME_SYMBOL = "SPY"
_MAX_QUOTE_AGE = timedelta(minutes=5)
_MAX_QUOTE_FUTURE_SKEW = timedelta(seconds=30)


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _hold_payload(code: str, *, detail: str) -> dict[str, Any]:
    unavailable = code in _UNAVAILABLE_CODES or code.startswith("PAPER_PROVIDER_HTTP_")
    return {
        "schema": BRIDGE_SCHEMA,
        "provider": "alpaca",
        "environment": "paper",
        "bridge_state": "HOLD",
        "execution_authority": "BACKEND_ONLY",
        "observed_at": _now_iso(),
        "latest_receipt": None,
        "provider_observation": {
            "code": code,
            "account_status": "UNKNOWN",
            "account_blocked": None,
            "trading_blocked": None,
            "trade_suspended_by_user": None,
        },
        "experience": {
            "state": "UNAVAILABLE" if unavailable else "SETUP_NEEDED",
            "headline": "Trading connection unavailable"
            if unavailable
            else "Trading connection needs setup",
            "detail": detail,
        },
        "truth_boundary": "LEFA owns the provider call; browser execution authority remains zero.",
    }


def _account_status_payload(account: dict[str, Any]) -> dict[str, Any]:
    account_status = account["status"].upper()
    account_blocked = account["account_blocked"]
    trading_blocked = account["trading_blocked"]
    trade_suspended = account["trade_suspended_by_user"]
    is_verified = (
        account_status == "ACTIVE"
        and not account_blocked
        and not trading_blocked
        and not trade_suspended
    )

    if is_verified:
        code = "PAPER_ACCOUNT_OBSERVED"
        experience = {
            "state": "READY",
            "headline": "Alpaca is ready",
            "detail": "Paper trading is connected directly through LEFA's governed backend.",
        }
    else:
        code = f"ACCOUNT_{account_status}"
        experience = {
            "state": "SETUP_NEEDED",
            "headline": "Trading connection on hold",
            "detail": f"Alpaca reported account status: {account_status}.",
        }

    return {
        "schema": BRIDGE_SCHEMA,
        "provider": "alpaca",
        "environment": "paper",
        "bridge_state": "VERIFIED" if is_verified else "HOLD",
        "execution_authority": "BACKEND_ONLY",
        "observed_at": _now_iso(),
        "latest_receipt": None,
        "provider_observation": {
            "code": code,
            "account_status": account_status,
            "account_blocked": account_blocked,
            "trading_blocked": trading_blocked,
            "trade_suspended_by_user": trade_suspended,
        },
        "experience": experience,
        "truth_boundary": "LEFA owns the provider call; browser execution authority remains zero.",
    }


def _validate_account(account: Any) -> dict[str, Any]:
    if not isinstance(account, dict) or not _REQUIRED_ACCOUNT_FIELDS.issubset(account):
        raise ValueError("Alpaca returned an incomplete account response")

    status = account["status"]
    flags = [
        account["account_blocked"],
        account["trading_blocked"],
        account["trade_suspended_by_user"],
    ]
    if not isinstance(status, str) or not status.strip() or not all(
        isinstance(flag, bool) for flag in flags
    ):
        raise ValueError("Alpaca returned an invalid account response")

    return {
        "status": status.strip(),
        "account_blocked": account["account_blocked"],
        "trading_blocked": account["trading_blocked"],
        "trade_suspended_by_user": account["trade_suspended_by_user"],
    }


def _check_direct_alpaca_status() -> dict[str, Any]:
    """Read and sanitize Alpaca paper account truth using LEFA's native adapter."""
    try:
        settings = Settings()
    except ValueError:
        return _hold_payload(
            "PAPER_CONFIGURATION_INVALID",
            detail="LEFA requires a paper-only Alpaca configuration.",
        )

    api_key = settings.alpaca_api_key.get_secret_value().strip()
    secret_key = settings.alpaca_secret_key.get_secret_value().strip()
    if not api_key or not secret_key or "your_" in api_key.lower() or "your_" in secret_key.lower():
        return _hold_payload(
            "PAPER_CREDENTIALS_UNAVAILABLE",
            detail="The secure Alpaca paper connection is still being configured.",
        )

    try:
        account = ReadOnlyAlpaca(settings).get_account()
        return _account_status_payload(_validate_account(account))
    except APIError as exc:
        status_code = getattr(exc, "status_code", None)
        code = (
            f"PAPER_PROVIDER_HTTP_{status_code}"
            if isinstance(status_code, int)
            else "PAPER_PROVIDER_ERROR"
        )
        return _hold_payload(
            code,
            detail="Alpaca paper trading service returned an error.",
        )
    except (ConnectionError, TimeoutError, OSError):
        return _hold_payload(
            "PAPER_PROVIDER_UNREACHABLE",
            detail="Could not connect to Alpaca paper trading.",
        )
    except (TypeError, ValueError, KeyError):
        return _hold_payload(
            "PAPER_PROVIDER_RESPONSE_INVALID",
            detail="LEFA could not verify the Alpaca paper account response.",
        )


def _current_bridge_status() -> dict[str, Any]:
    return _check_direct_alpaca_status()


def _validate_quote(
    quote: Any,
    *,
    symbol: str,
    now: datetime | None = None,
) -> dict[str, Any]:
    if not isinstance(quote, dict) or quote.get("symbol") != symbol:
        raise ValueError("Alpaca returned an invalid quote symbol")

    raw_timestamp = quote.get("timestamp")
    if not isinstance(raw_timestamp, str) or not raw_timestamp.strip():
        raise ValueError("Alpaca returned a quote without a timestamp")
    try:
        timestamp = datetime.fromisoformat(raw_timestamp)
    except ValueError as exc:
        raise ValueError("Alpaca returned an invalid quote timestamp") from exc
    if timestamp.tzinfo is None:
        raise ValueError("Alpaca returned a timezone-naive quote timestamp")
    timestamp = timestamp.astimezone(UTC)

    current_time = now or datetime.now(UTC)
    if current_time.tzinfo is None:
        current_time = current_time.replace(tzinfo=UTC)
    else:
        current_time = current_time.astimezone(UTC)
    quote_age = current_time - timestamp
    if quote_age > _MAX_QUOTE_AGE or quote_age < -_MAX_QUOTE_FUTURE_SKEW:
        raise ValueError("Alpaca quote is outside the freshness window")

    try:
        bid_price = Decimal(str(quote["bid_price"]))
        ask_price = Decimal(str(quote["ask_price"]))
    except (KeyError, InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError("Alpaca returned malformed quote prices") from exc
    if (
        not bid_price.is_finite()
        or not ask_price.is_finite()
        or bid_price <= 0
        or ask_price <= 0
        or bid_price > ask_price
    ):
        raise ValueError("Alpaca returned invalid quote prices")

    return {
        "state": "OBSERVED",
        "symbol": symbol,
        "latest_price": str((bid_price + ask_price) / Decimal(2)),
        "market_state": "unknown",
        "observed_at": timestamp.isoformat(),
    }


def _read_market_observation() -> dict[str, Any] | None:
    """Read one fresh quote or return no evidence when the provider is not truthful."""
    try:
        settings = Settings()
        quote = ReadOnlyAlpaca(settings).get_latest_quote(_RUNTIME_SYMBOL)
        return _validate_quote(quote, symbol=_RUNTIME_SYMBOL)
    except APIError:
        return None
    except (
        AttributeError,
        ConnectionError,
        KeyError,
        OSError,
        RuntimeError,
        TimeoutError,
        TypeError,
        ValueError,
    ):
        return None


def _runtime_projection(bridge: dict[str, Any]) -> dict[str, Any]:
    """Project backend truth into the primary non-technical runtime contract.

    A verified account bridge becomes WAITING_FOR_MARKET until a fresh,
    independently validated Alpaca quote is available.
    """

    experience = bridge.get("experience") if isinstance(bridge.get("experience"), dict) else {}
    bridge_ready = bridge.get("bridge_state") == "VERIFIED"
    experience_state = str(experience.get("state", "UNAVAILABLE"))
    market_observation = _read_market_observation() if bridge_ready else None

    if bridge_ready:
        state = "WAITING_FOR_MARKET"
        headline = "Connected and ready to observe"
        detail = (
            "Fresh Alpaca market evidence is available."
            if market_observation
            else "LEFA will show market facts when fresh backend evidence arrives."
        )
    elif experience_state == "SETUP_NEEDED":
        state = "SETUP_NEEDED"
        headline = str(experience.get("headline", "Trading connection needs setup"))
        detail = str(experience.get("detail", "The secure trading service is still being configured."))
    else:
        state = "UNAVAILABLE"
        headline = "Trading service unavailable"
        detail = "LEFA can't reach the secure trading service right now."

    ai_state = "AVAILABLE" if os.getenv("FEATHERLESS_API_KEY", "").strip() else "UNAVAILABLE"

    return {
        "schema": RUNTIME_SCHEMA,
        "state": state,
        "headline": headline,
        "detail": detail,
        "observed_at": bridge.get("observed_at")
        if isinstance(bridge.get("observed_at"), str)
        else _now_iso(),
        "connection": {
            "state": "READY" if bridge_ready else experience_state,
            "label": "Alpaca paper trading",
        },
        "market": {
            **(
                market_observation
                or {
                    "state": "WAITING_FOR_EVIDENCE",
                    "symbol": None,
                    "latest_price": None,
                    "market_state": "unknown",
                    "observed_at": None,
                }
            )
        },
        "decision": {
            "state": "NO_DECISION",
        },
        "ai": {
            "state": ai_state,
            "label": "AI explanation",
        },
    }


@router.get("/api/bridge/status")
def get_bridge_status() -> dict[str, Any]:
    """Return advanced/sanitized governed Alpaca paper truth."""

    return _current_bridge_status()


@router.get("/api/runtime/status")
def get_runtime_status() -> dict[str, Any]:
    """Return the small human-facing runtime state used by the primary UI."""

    return _runtime_projection(_current_bridge_status())
