"""
LEFA AI — Featherless AI Serverless Inference Engine
=====================================================
Open-source LLM explanation support for LEFA.

Governance boundaries:
- Pure advisory / explanation only. Zero broker execution authority.
- Credentials are environment-only and never have a source-code fallback.
- Provider failure is explicit; it is never converted into synthetic "live" reasoning.

I_AM_STATELESS_RENTER_NOT_LANDLORD
"""
from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.request

logger = logging.getLogger(__name__)

DEFAULT_FEATHERLESS_MODEL = "Qwen/Qwen2.5-7B-Instruct"
FEATHERLESS_BASE_URL = "https://api.featherless.ai/v1/chat/completions"

LEFA_SYSTEM_PROMPT = """You are LEFA AI, the Governed Financial Intelligence Companion for the Alpaca AI Trading Agents Hackathon.
Your role:
1. Provide concise, clear, human-centered explanations of market observations and governed risk evaluations.
2. Emphasize dual-axis governance: Financial Policy (admissibility) and KPGS Provenance (canonical proof).
3. Always clarify that LEFA operates under strict observation/paper jurisdiction with zero autonomous order authority.
4. Keep explanations concise, professional, and accessible (2-3 sentences max unless asked for deep analysis)."""


class FeatherlessUnavailable(RuntimeError):
    """Raised when live Featherless inference cannot be truthfully produced."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


class FeatherlessReasoner:
    """Server-side advisory inference client for Featherless AI."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        timeout: float = 12.0,
    ) -> None:
        self.api_key = api_key or os.getenv("FEATHERLESS_API_KEY", "").strip()
        self.model = model or os.getenv("FEATHERLESS_MODEL") or DEFAULT_FEATHERLESS_MODEL
        self.timeout = timeout

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def complete(
        self,
        messages: list[dict[str, str]],
        *,
        max_tokens: int = 150,
        temperature: float = 0.2,
        model: str | None = None,
    ) -> str:
        """Execute one live completion or fail explicitly without synthetic success."""
        if not self.is_configured():
            raise FeatherlessUnavailable("NOT_CONFIGURED")

        target_model = model or self.model
        payload = {
            "model": target_model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        req = urllib.request.Request(
            FEATHERLESS_BASE_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": "Bearer" + " " + self.api_key,
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "LEFA-AI-Companion/1.0 (Alpaca-Hackathon)",
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            logger.warning("Featherless inference HTTP status %d", exc.code)
            raise FeatherlessUnavailable(f"HTTP_{exc.code}") from exc
        except urllib.error.URLError as exc:
            logger.warning("Featherless inference network unavailable")
            raise FeatherlessUnavailable("NETWORK_UNAVAILABLE") from exc
        except (TimeoutError, OSError) as exc:
            logger.warning("Featherless inference transport unavailable")
            raise FeatherlessUnavailable("TRANSPORT_UNAVAILABLE") from exc
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            logger.warning("Featherless inference returned invalid JSON")
            raise FeatherlessUnavailable("INVALID_RESPONSE") from exc

        choices = data.get("choices") if isinstance(data, dict) else None
        if not isinstance(choices, list) or not choices:
            raise FeatherlessUnavailable("EMPTY_RESPONSE")

        first = choices[0]
        if not isinstance(first, dict):
            raise FeatherlessUnavailable("INVALID_RESPONSE")
        message = first.get("message")
        if not isinstance(message, dict):
            raise FeatherlessUnavailable("INVALID_RESPONSE")
        content = message.get("content")
        if not isinstance(content, str) or not content.strip():
            raise FeatherlessUnavailable("EMPTY_RESPONSE")
        return content.strip()

    def explain_market_observation(
        self,
        symbol: str,
        price: str | None,
        market_state: str,
        decision_action: str | None = None,
        rationale: str | None = None,
    ) -> str:
        """Explain backend-supplied market evidence; never invent the evidence itself."""
        prompt = (
            f"Market Symbol: {symbol}\n"
            f"Latest Price: {price or 'N/A'}\n"
            f"Market State: {market_state}\n"
            f"Proposed Action: {decision_action or 'OBSERVE'}\n"
            f"Governance Rationale: {rationale or 'No governed proposal is available.'}\n\n"
            "Explain what this means for the user in 2 clear sentences. Do not invent missing facts."
        )

        messages = [
            {"role": "system", "content": LEFA_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]
        return self.complete(messages, max_tokens=120, temperature=0.1)

    def explain_dual_axis_governance(self) -> str:
        """Explain the core LEFA dual-axis architecture."""
        messages = [
            {"role": "system", "content": LEFA_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": "Explain in 2 sentences how LEFA AI's dual-axis governance protects users from rogue execution.",
            },
        ]
        return self.complete(messages, max_tokens=100, temperature=0.1)
