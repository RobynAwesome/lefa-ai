"""LEFA-owned Alpaca paper connection and human-facing runtime projections.

The hackathon runtime is self-contained inside ``lefa-ai``. Provider credentials,
account observation and paper execution remain server-side; the browser receives
only a small truthful state.

REALITY_STATE > INDEX_STATE
RECEIPT OR HOLD
"""
from __future__ import annotations

import os
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter

from lefa.alpaca import AlpacaPaperBroker
from lefa.config import Settings

router = APIRouter()

# Retained for frontend compatibility during the submission window. This schema
# is produced locally by LEFA and no longer implies a Sovereign Hub runtime hop.
BRIDGE_SCHEMA = "kopano.lefa.sovereign-bridge-status.v1"
RUNTIME_SCHEMA = "kopano.lefa.runtime-status.v1"


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _hold_payload(
    code: str,
    *,
    detail: str,
    unavailable: bool = False,
) -> dict[str, Any]:
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
        "truth_boundary": (
            "LEFA directly observes its configured Alpaca paper account server-side; "
            "browser execution authority remains zero."
        ),
    }


def _observe_alpaca_account() -> dict[str, Any]:
    """Observe the configured Alpaca paper account directly from LEFA."""

    settings = Settings()
    api_key = settings.alpaca_api_key.get_secret_value().strip()
    secret_key = settings.alpaca_secret_key.get_secret_value().strip()

    if not api_key:
        return _hold_payload(
            "PAPER_API_KEY_UNAVAILABLE",
            detail="LEFA's Alpaca paper connection still needs setup.",
        )
    if not secret_key:
        return _hold_payload(
            "PAPER_SECRET_KEY_UNAVAILABLE",
            detail="LEFA's Alpaca paper connection still needs setup.",
        )

    try:
        account = AlpacaPaperBroker(settings).get_account()
    except Exception:  # noqa: BLE001 - provider boundary must fail closed without leaking SDK details
        return _hold_payload(
            "ALPACA_ACCOUNT_UNAVAILABLE",
            detail="LEFA can't verify Alpaca right now.",
            unavailable=True,
        )

    status = str(account.get("status", "UNKNOWN"))
    account_blocked = bool(account.get("account_blocked", False))
    trading_blocked = bool(account.get("trading_blocked", False))
    trade_suspended = bool(account.get("trade_suspended_by_user", False))
    active = "ACTIVE" in status.upper()
    verified = active and not account_blocked and not trading_blocked and not trade_suspended
    observed_at = _now_iso()

    if verified:
        experience = {
            "state": "READY",
            "headline": "Alpaca is ready",
            "detail": "Your paper-trading connection is ready.",
        }
        code = "PAPER_ACCOUNT_OBSERVED"
    else:
        experience = {
            "state": "SETUP_NEEDED",
            "headline": "Trading connection isn't ready yet",
            "detail": "LEFA is keeping trading on hold until the paper account is ready.",
        }
        code = "PAPER_ACCOUNT_RESTRICTED"

    return {
        "schema": BRIDGE_SCHEMA,
        "provider": "alpaca",
        "environment": "paper",
        "bridge_state": "VERIFIED" if verified else "HOLD",
        "execution_authority": "BACKEND_ONLY",
        "observed_at": observed_at,
        "latest_receipt": {
            "kind": "alpaca.paper.account-observation",
            "observed_at": observed_at,
            "account_id": str(account.get("id", "")),
        },
        "provider_observation": {
            "code": code,
            "account_status": status,
            "account_blocked": account_blocked,
            "trading_blocked": trading_blocked,
            "trade_suspended_by_user": trade_suspended,
        },
        "experience": experience,
        "truth_boundary": (
            "LEFA directly observes its configured Alpaca paper account server-side; "
            "this status does not itself prove an options order or P&L result."
        ),
    }


def _current_bridge_status() -> dict[str, Any]:
    return _observe_alpaca_account()


def _runtime_projection(bridge: dict[str, Any]) -> dict[str, Any]:
    """Project backend truth into the primary non-technical runtime contract."""

    experience = bridge.get("experience") if isinstance(bridge.get("experience"), dict) else {}
    bridge_ready = bridge.get("bridge_state") == "VERIFIED"
    experience_state = str(experience.get("state", "UNAVAILABLE"))

    if bridge_ready:
        state = "WAITING_FOR_MARKET"
        headline = "Connected and ready to observe"
        detail = "LEFA will show market facts when fresh backend evidence arrives."
    elif experience_state == "SETUP_NEEDED":
        state = "SETUP_NEEDED"
        headline = str(experience.get("headline", "Trading connection needs setup"))
        detail = str(experience.get("detail", "The secure trading service is still being configured."))
    else:
        state = "UNAVAILABLE"
        headline = "Trading service unavailable"
        detail = "LEFA can't verify Alpaca right now."

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
            "state": "WAITING_FOR_EVIDENCE",
            "symbol": None,
            "latest_price": None,
            "market_state": "unknown",
            "observed_at": None,
        },
        "decision": {"state": "NO_DECISION"},
        "ai": {
            "state": ai_state,
            "label": "AI explanation",
        },
    }


@router.get("/api/bridge/status")
def get_bridge_status() -> dict[str, Any]:
    """Return LEFA-owned, sanitized Alpaca paper-account truth."""

    return _current_bridge_status()


@router.get("/api/runtime/status")
def get_runtime_status() -> dict[str, Any]:
    """Return the small human-facing runtime state used by the primary UI."""

    return _runtime_projection(_current_bridge_status())
