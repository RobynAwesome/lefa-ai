import os
import urllib.error
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from lefa.featherless import FeatherlessReasoner, FeatherlessUnavailable
from lefa.web_api import app

client = TestClient(app)


def test_featherless_reasoner_requires_explicit_configuration():
    with patch.dict(os.environ, {}, clear=True):
        reasoner = FeatherlessReasoner()
        assert reasoner.is_configured() is False
        with pytest.raises(FeatherlessUnavailable, match="NOT_CONFIGURED"):
            reasoner.complete([{"role": "user", "content": "Hello"}])


def test_featherless_reasoner_explicit_key_is_configured():
    reasoner = FeatherlessReasoner(api_key="test-only-key", model="Qwen/Qwen2.5-7B-Instruct")
    assert reasoner.is_configured() is True
    assert reasoner.model == "Qwen/Qwen2.5-7B-Instruct"


def test_featherless_reasoner_provider_error_is_not_fake_success():
    reasoner = FeatherlessReasoner(api_key="test-only-key")
    error = urllib.error.HTTPError("url", 403, "Forbidden", {}, None)
    with (
        patch("urllib.request.urlopen", side_effect=error),
        pytest.raises(FeatherlessUnavailable, match="HTTP_403"),
    ):
        reasoner.complete([{"role": "user", "content": "Hello"}])


def test_featherless_explain_market_observation_mocked():
    reasoner = FeatherlessReasoner(api_key="test-only-key")
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"choices": [{"message": {"content": "Market evidence remains under governed observation."}}]}'
    mock_response.__enter__.return_value = mock_response

    with patch("urllib.request.urlopen", return_value=mock_response):
        explanation = reasoner.explain_market_observation(
            "SPY", None, "unknown", "OBSERVE", "No live market price admitted."
        )
        assert "governed observation" in explanation


def test_web_api_explain_endpoint_reports_unavailable_when_unconfigured():
    with patch.dict(os.environ, {}, clear=True):
        response = client.post(
            "/api/ai/explain",
            json={
                "symbol": "SPY",
                "price": None,
                "market_state": "unknown",
                "decision_action": "OBSERVE",
                "rationale": "No live market observation admitted",
            },
        )

    assert response.status_code == 503
    data = response.json()
    assert data["detail"]["state"] == "UNAVAILABLE"


def test_web_api_explain_endpoint_success_with_server_configuration():
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"choices": [{"message": {"content": "Live provider explanation."}}]}'
    mock_response.__enter__.return_value = mock_response

    with (
        patch.dict(os.environ, {"FEATHERLESS_API_KEY": "test-only-key"}, clear=True),
        patch("urllib.request.urlopen", return_value=mock_response),
    ):
        response = client.post(
            "/api/ai/explain",
            json={
                "symbol": "SPY",
                "price": None,
                "market_state": "unknown",
                "decision_action": "OBSERVE",
                "rationale": "No invented facts",
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert data["explanation"] == "Live provider explanation."
    assert data["provider"] == "Featherless AI"


def test_web_api_dual_axis_explainer_reports_unavailable_when_unconfigured():
    with patch.dict(os.environ, {}, clear=True):
        response = client.get("/api/ai/dual-axis-explainer")

    assert response.status_code == 503
    assert response.json()["detail"]["state"] == "UNAVAILABLE"
