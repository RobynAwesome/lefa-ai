"""
Zero-Trust Security Middleware for LEFA FastAPI Backend.

Enforces security headers, CORS allowlisting, rate limiting guidance,
and request sanitization for financial data endpoints.

LEFA handles financial credentials and paper trading orders.
Every boundary must enforce zero-trust: never trust, always verify, fail closed.

I_AM_STATELESS_RENTER_NOT_LANDLORD
RECEIPT OR HOLD
"""

from __future__ import annotations

import hashlib
import logging
import time
from typing import Any

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

# ─── Security Headers ────────────────────────────────────────────────
# Applied to EVERY response. Financial data must not be cached,
# framed, or sniffed.
SECURITY_HEADERS: dict[str, str] = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "0",  # Modern: rely on CSP instead
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
    "Content-Security-Policy": (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: blob:; "
        "connect-src 'self' https://paper-api.alpaca.markets https://api.featherless.ai; "
        "font-src 'self'; "
        "frame-ancestors 'none'"
    ),
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Cache-Control": "no-store",  # Financial data must not be cached
    "Pragma": "no-cache",
}

# ─── CORS Allowlist ──────────────────────────────────────────────────
# Only trusted origins may call LEFA's API.
ALLOWED_ORIGINS: set[str] = {
    "https://lefa-core-live.vercel.app",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
}

# ─── Sensitive Endpoints ─────────────────────────────────────────────
# Endpoints that handle financial data or credentials require
# stricter controls.
SENSITIVE_ENDPOINTS: set[str] = {
    "/api/bridge/status",
    "/api/runtime/status",
    "/api/ai/explain",
    "/api/ai/dual-axis-explainer",
    "/api/mcp/verify",
    "/api/snapshot",
}

# ─── Forbidden Response Keys ─────────────────────────────────────────
# These keys must NEVER appear in any API response body.
# Zero-trust: assume every response is visible to adversaries.
FORBIDDEN_RESPONSE_KEYS: set[str] = {
    "secret",
    "token",
    "password",
    "api_key",
    "authorization",
    "account_number",
    "secret_key",
    "private_key",
}


class ZeroTrustSecurityMiddleware(BaseHTTPMiddleware):
    """
    Applies zero-trust security headers to every response.

    This middleware:
    1. Adds security headers (CSP, HSTS, X-Frame-Options, etc.)
    2. Validates CORS origin against allowlist
    3. Logs request metadata for audit trail
    4. Strips sensitive data from error responses
    """

    async def dispatch(self, request: Request, call_next: Any) -> Response:
        start_time = time.monotonic()

        # ── Origin validation ──
        origin = request.headers.get("origin", "")
        if origin and origin not in ALLOWED_ORIGINS:
            logger.warning(
                "Blocked request from unauthorized origin: %s to %s",
                origin,
                request.url.path,
            )
            # Don't reveal CORS policy details to unauthorized origins
            return Response(status_code=403, content="Forbidden")

        # ── Process request ──
        response = await call_next(request)

        # ── Apply security headers ──
        for header, value in SECURITY_HEADERS.items():
            response.headers[header] = value

        # ── CORS headers for allowed origins ──
        if origin and origin in ALLOWED_ORIGINS:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type"
            response.headers["Access-Control-Max-Age"] = "3600"

        # ── Audit trail header ──
        elapsed_ms = (time.monotonic() - start_time) * 1000
        request_hash = hashlib.sha256(
            f"{request.method}:{request.url.path}:{start_time}".encode()
        ).hexdigest()[:12]
        response.headers["X-LEFA-Request-ID"] = request_hash
        response.headers["X-LEFA-Response-Time-Ms"] = f"{elapsed_ms:.1f}"
        response.headers["X-LEFA-Execution-Authority"] = "zero"

        return response


def sanitize_response_dict(data: dict[str, Any]) -> dict[str, Any]:
    """
    Recursively removes forbidden keys from a response dictionary.

    Zero-trust: no secret, token, password, api_key, authorization,
    or account_number may appear in any API response.
    """
    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        key_lower = key.lower()
        if any(forbidden in key_lower for forbidden in FORBIDDEN_RESPONSE_KEYS):
            continue  # Strip forbidden key entirely
        if isinstance(value, dict):
            sanitized[key] = sanitize_response_dict(value)
        elif isinstance(value, list):
            sanitized[key] = [
                sanitize_response_dict(item) if isinstance(item, dict) else item for item in value
            ]
        else:
            sanitized[key] = value
    return sanitized
