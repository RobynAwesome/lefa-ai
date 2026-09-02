"""LEFA server-to-server Sovereign bridge and runtime projections.

Heavy provider/KPGS evidence remains behind the backend boundary. The primary
runtime endpoint exposes only the smallest truthful human state.

REALITY_STATE > INDEX_STATE
RECEIPT OR HOLD
"""
from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from fastapi import APIRouter

router = APIRouter()

BRIDGE_SCHEMA = "kopano.lefa.sovereign-bridge-status.v1"
RUNTIME_SCHEMA = "kopano.lefa.runtime-status.v1"
DEFAULT_SOVEREIGN_STATUS_URL = (
    "https://kopano-sovereign-hub-o8zt.vercel.app/api/lefa/alpaca-status"
)

_ALLOWED_PROVIDER_FIELDS = {
    "code",
    "account_status",
    "account_blocked",
    "trading_blocked",
    "trade_suspended_by_user",
}


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _upstream_url() -> str:
    return os.getenv("LEFA_SOVEREIGN_STATUS_URL", DEFAULT_SOVEREIGN_STATUS_URL).strip()


def _hold_payload(code: str, *, detail: str) -> dict[str, Any]:
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
            "state": "UNAVAILABLE" if code == "SOVEREIGN_BACKEND_UNAVAILABLE" else "SETUP_NEEDED",
            "headline": "Trading connection unavailable"
            if code == "SOVEREIGN_BACKEND_UNAVAILABLE"
            else "Trading connection needs setup",
            "detail": detail,
        },
        "truth_boundary": "LEFA projects governed provider state; browser execution authority remains zero.",
    }


def _sanitize_status(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return _hold_payload(
            "SOVEREIGN_CONTRACT_INVALID",
            detail="LEFA could not verify the trading service response.",
        )

    if (
        payload.get("schema") != BRIDGE_SCHEMA
        or payload.get("provider") != "alpaca"
        or payload.get("environment") != "paper"
        or payload.get("execution_authority") != "BACKEND_ONLY"
        or payload.get("bridge_state") not in {"VERIFIED", "HOLD"}
    ):
        return _hold_payload(
            "SOVEREIGN_CONTRACT_INVALID",
            detail="LEFA could not verify the trading service response.",
        )

    provider_raw = payload.get("provider_observation")
    provider_observation: dict[str, Any] | None = None
    if isinstance(provider_raw, dict):
        provider_observation = {
            key: provider_raw.get(key)
            for key in _ALLOWED_PROVIDER_FIELDS
            if key in provider_raw
        }

    bridge_state = str(payload["bridge_state"])
    provider_code = (
        str(provider_observation.get("code"))
        if provider_observation and provider_observation.get("code") is not None
        else "UNKNOWN"
    )

    if bridge_state == "VERIFIED":
        experience = {
            "state": "READY",
            "headline": "Alpaca is ready",
            "detail": "Paper trading is connected through LEFA's governed backend.",
        }
    elif provider_code == "PAPER_CREDENTIALS_UNAVAILABLE":
        experience = {
            "state": "SETUP_NEEDED",
            "headline": "Trading connection needs setup",
            "detail": "The secure trading service is still being configured.",
        }
    else:
        experience = {
            "state": "SETUP_NEEDED",
            "headline": "Trading connection isn't ready yet",
            "detail": "LEFA is keeping this connection on hold until the backend is ready.",
        }

    latest_receipt = payload.get("latest_receipt")
    if latest_receipt is not None and not isinstance(latest_receipt, dict):
        latest_receipt = None

    return {
        "schema": BRIDGE_SCHEMA,
        "provider": "alpaca",
        "environment": "paper",
        "bridge_state": bridge_state,
        "execution_authority": "BACKEND_ONLY",
        "observed_at": payload.get("observed_at")
        if isinstance(payload.get("observed_at"), str)
        else _now_iso(),
        "latest_receipt": latest_receipt,
        "provider_observation": provider_observation,
        "experience": experience,
        "truth_boundary": "LEFA projects governed provider state; browser execution authority remains zero.",
    }


def _read_upstream_status() -> Any:
    request = Request(
        _upstream_url(),
        headers={
            "Accept": "application/json",
            "User-Agent": "LEFA-AI/sovereign-bridge",
        },
        method="GET",
    )

    try:
        with urlopen(request, timeout=4) as response:
            body = response.read().decode("utf-8")
    except HTTPError as exc:
        # Sovereign Hub intentionally uses HTTP 503 for governed HOLD state.
        body = exc.read().decode("utf-8")
    except (URLError, TimeoutError, OSError) as exc:
        raise RuntimeError("sovereign backend unavailable") from exc

    return json.loads(body)


def _current_bridge_status() -> dict[str, Any]:
    try:
        upstream = _read_upstream_status()
    except (RuntimeError, json.JSONDecodeError, UnicodeDecodeError):
        return _hold_payload(
            "SOVEREIGN_BACKEND_UNAVAILABLE",
            detail="LEFA can't reach the secure trading service right now.",
        )

    return _sanitize_status(upstream)


def _runtime_projection(bridge: dict[str, Any]) -> dict[str, Any]:
    """Project backend truth into the primary non-technical runtime contract.

    No market/account number is emitted until a separate non-fixture observation
    contract exists. A verified account bridge therefore becomes WAITING_FOR_MARKET,
    not synthetic live telemetry.
    """

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
            "state": "WAITING_FOR_EVIDENCE",
            "symbol": None,
            "latest_price": None,
            "market_state": "unknown",
            "observed_at": None,
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
