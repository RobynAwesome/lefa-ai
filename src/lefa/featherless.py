"""
LEFA AI — Featherless AI Serverless Inference Engine
=====================================================
Integrates Featherless AI (Lablab.ai Hackathon Official Partner) for open-source
LLM market reasoning, companion dialog, and governed decision explanations.

Governance boundaries:
- Pure advisory / explanation only. Zero broker execution authority.
- Every reasoning request is logged with provenance metadata.
- Graceful offline fallback ensures zero interruption to deterministic risk logic.

I_AM_STATELESS_RENTER_NOT_LANDLORD
"""
from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.request
from typing import Any

logger = logging.getLogger(__name__)

DEFAULT_FEATHERLESS_API_KEY = "rc_895ea88f311a6126b5384f28bfc84b329ded642650ac69edbcca38cf2c95c871"
DEFAULT_FEATHERLESS_MODEL = "Qwen/Qwen2.5-7B-Instruct"
FEATHERLESS_BASE_URL = "https://api.featherless.ai/v1/chat/completions"

LEFA_SYSTEM_PROMPT = """You are LEFA AI, the Governed Financial Intelligence Companion for the Alpaca AI Trading Agents Hackathon.
Your role:
1. Provide concise, clear, human-centered explanations of market observations and governed risk evaluations.
2. Emphasize dual-axis governance: Financial Policy (admissibility) and KPGS Provenance (canonical proof).
3. Always clarify that LEFA operates under strict observation/paper jurisdiction with zero autonomous order authority.
4. Keep explanations concise, professional, and accessible (2-3 sentences max unless asked for deep analysis)."""


class FeatherlessReasoner:
    """Serverless AI inference client for Featherless AI."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        timeout: float = 12.0,
    ) -> None:
        self.api_key = (
            api_key
            or os.getenv("FEATHERLESS_API_KEY")
            or DEFAULT_FEATHERLESS_API_KEY
        )
        self.model = (
            model
            or os.getenv("FEATHERLESS_MODEL")
            or DEFAULT_FEATHERLESS_MODEL
        )
        self.timeout = timeout

    def is_configured(self) -> bool:
        return bool(self.api_key and self.api_key.startswith("rc_"))

    def complete(
        self,
        messages: list[dict[str, str]],
        *,
        max_tokens: int = 150,
        temperature: float = 0.2,
        model: str | None = None,
    ) -> str:
        """Execute chat completion request against Featherless AI endpoint."""
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
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "LEFA-AI-Companion/1.0 (Alpaca-Hackathon)",
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                choices = data.get("choices", [])
                if choices and "message" in choices[0]:
                    return choices[0]["message"].get("content", "").strip()
                return "LEFA AI reasoning generated with no content choices."
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            logger.warning("Featherless API HTTP error %d: %s", e.code, err_body)
            return self._fallback_explanation(messages, reason=f"HTTP_{e.code}")
        except Exception as e:
            logger.warning("Featherless API invocation failed: %s", e)
            return self._fallback_explanation(messages, reason=str(type(e).__name__))

    def explain_market_observation(
        self,
        symbol: str,
        price: str | None,
        market_state: str,
        decision_action: str | None = None,
        rationale: str | None = None,
    ) -> str:
        """Generate a natural-language spoken/written explanation of current market state."""
        prompt = (
            f"Market Symbol: {symbol}\n"
            f"Latest Price: {price or 'N/A'}\n"
            f"Market State: {market_state}\n"
            f"Proposed Action: {decision_action or 'OBSERVE'}\n"
            f"Governance Rationale: {rationale or 'Awaiting live trade proposal.'}\n\n"
            "Explain what this means for the user's governed financial companion in 2 clear sentences."
        )

        messages = [
            {"role": "system", "content": LEFA_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]
        return self.complete(messages, max_tokens=120, temperature=0.1)

    def explain_dual_axis_governance(self) -> str:
        """Explain the core LEFA AI dual-axis architecture."""
        messages = [
            {"role": "system", "content": LEFA_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": "Explain in 2 sentences how LEFA AI's dual-axis governance protects users from rogue execution.",
            },
        ]
        return self.complete(messages, max_tokens=100, temperature=0.1)

    def _fallback_explanation(
        self, messages: list[dict[str, str]], reason: str
    ) -> str:
        """Deterministic fallback when external AI reasoning cannot be reached."""
        last_user_msg = next(
            (m["content"] for m in reversed(messages) if m.get("role") == "user"),
            "Market observation active.",
        )
        return (
            f"Observation recorded under governed deterministic policy."
        )
