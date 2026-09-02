from unittest.mock import MagicMock, patch
import urllib.error

from lefa.featherless import FeatherlessReasoner
from lefa.web_api import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_featherless_reasoner_init():
    reasoner = FeatherlessReasoner(api_key="rc_test_key_123", model="Qwen/Qwen2.5-7B-Instruct")
    assert reasoner.is_configured() is True
    assert reasoner.model == "Qwen/Qwen2.5-7B-Instruct"


def test_featherless_reasoner_fallback_on_error():
    reasoner = FeatherlessReasoner(api_key="rc_invalid")
    with patch("urllib.request.urlopen", side_effect=urllib.error.HTTPError("url", 403, "Forbidden", {}, None)):
        result = reasoner.complete([{"role": "user", "content": "Hello"}])
        assert "Observation recorded under governed deterministic policy." in result
        assert "HTTP_403" not in result


def test_featherless_explain_market_observation_mocked():
    reasoner = FeatherlessReasoner()
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"choices": [{"message": {"content": "SPY is stable at 598.50 under governed observation."}}]}'
    mock_response.__enter__.return_value = mock_response

    with patch("urllib.request.urlopen", return_value=mock_response):
        explanation = reasoner.explain_market_observation("SPY", "598.50", "open", "OBSERVE", "Within 2% risk limit.")
        assert "SPY is stable" in explanation


def test_web_api_explain_endpoint():
    response = client.post(
        "/api/ai/explain",
        json={
            "symbol": "SPY",
            "price": "598.50",
            "market_state": "open",
            "decision_action": "OBSERVE",
            "rationale": "Governed test rationale"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "explanation" in data
    assert data["provider"] == "Featherless AI"


def test_web_api_dual_axis_explainer_endpoint():
    response = client.get("/api/ai/dual-axis-explainer")
    assert response.status_code == 200
    data = response.json()
    assert "explanation" in data
    assert data["provider"] == "Featherless AI"
