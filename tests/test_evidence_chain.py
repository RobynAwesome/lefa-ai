"""Comprehensive test suite for KPGS 8-Stage Evidence-Backed Chain Architecture."""

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from lefa import bridge_api
from lefa.ark import ArkLedger
from lefa.evidence_chain import KPGS8StageChainRunner


def _app() -> FastAPI:
    app = FastAPI()
    app.include_router(bridge_api.router)
    return app


@pytest.fixture
def tmp_ark_ledger(tmp_path: Path) -> ArkLedger:
    ledger_file = tmp_path / "test_ark_ledger.jsonl"
    return ArkLedger(storage_path=ledger_file)


def test_evidence_chain_full_evidenced_approval(tmp_ark_ledger: ArkLedger):
    runner = KPGS8StageChainRunner(symbol="SPY", ark_ledger=tmp_ark_ledger)
    receipt = runner.run_chain()

    assert receipt.symbol == "SPY"
    assert len(receipt.stages) == 8
    assert receipt.governance_decision == "APPROVE"
    assert receipt.is_fully_evidenced is True
    assert len(receipt.root_hash) == 64
    assert receipt.reasons == ["all_8_stages_fully_evidenced_and_approved"]

    # Verify stage names and order
    expected_stages = [
        "stage_1_witness",
        "stage_2_observation",
        "stage_3_validation",
        "stage_4_attestation",
        "stage_5_canonicalization",
        "stage_6_ledgering",
        "stage_7_time",
        "stage_8_reveal",
    ]
    assert [s.stage_id for s in receipt.stages] == expected_stages
    for stage in receipt.stages:
        assert stage.status == "PASS"
        assert stage.maturity == "EVIDENCED"
        assert len(stage.evidence_hash) == 64


def test_evidence_chain_stale_quote_triggers_hold(tmp_ark_ledger: ArkLedger):
    runner = KPGS8StageChainRunner(symbol="SPY", ark_ledger=tmp_ark_ledger)
    now = datetime.now(UTC)
    stale_time = (now - timedelta(seconds=120)).isoformat()

    stale_witness = {
        "symbol": "SPY",
        "underlying_price": "595.00",
        "quote_timestamp": stale_time,
        "is_live_provider": True,
    }

    receipt = runner.run_chain(witness_data=stale_witness, reference_time=now)
    assert receipt.governance_decision == "HOLD"
    assert receipt.is_fully_evidenced is False

    s1 = next(s for s in receipt.stages if s.stage_id == "stage_1_witness")
    assert s1.status == "HOLD"
    assert "stale" in s1.detail
    assert any("stage_1:quote_stale" in r for r in receipt.reasons)


def test_evidence_chain_missing_timestamp_triggers_hold(tmp_ark_ledger: ArkLedger):
    runner = KPGS8StageChainRunner(symbol="SPY", ark_ledger=tmp_ark_ledger)
    witness = {
        "symbol": "SPY",
        "underlying_price": "595.00",
        "is_live_provider": True,
    }

    receipt = runner.run_chain(witness_data=witness)
    assert receipt.governance_decision == "HOLD"
    assert "stage_1:quote_timestamp_missing" in receipt.reasons


def test_evidence_chain_low_confidence_audio_triggers_hold(tmp_ark_ledger: ArkLedger):
    runner = KPGS8StageChainRunner(symbol="SPY", ark_ledger=tmp_ark_ledger)
    obs = {
        "human_query": "Buy options",
        "channel": "Speechmatics_STT",
        "confidence": 0.45,  # below 0.70 threshold
        "is_complete": True,
    }

    receipt = runner.run_chain(observation_data=obs)
    assert receipt.governance_decision == "HOLD"
    assert "stage_2:unintelligible_or_incomplete_audio" in receipt.reasons


def test_evidence_chain_risk_ceiling_breach_triggers_reject(tmp_ark_ledger: ArkLedger):
    runner = KPGS8StageChainRunner(symbol="SPY", ark_ledger=tmp_ark_ledger)
    breach_validation = {
        "structure": "bull_put_vertical_spread",
        "max_loss": "4500.00",  # 4.5% on 100,000 > 3.0% ceiling
        "portfolio_equity": "100000.00",
        "daily_drawdown_pct": "0.50",
    }

    receipt = runner.run_chain(validation_data=breach_validation)
    assert receipt.governance_decision == "REJECT"

    s3 = next(s for s in receipt.stages if s.stage_id == "stage_3_validation")
    assert s3.status == "REJECT"
    assert "Risk firewall breach" in s3.detail
    assert any("stage_3:risk_ceiling_breach" in r for r in receipt.reasons)


def test_evidence_chain_drawdown_ceiling_breach_triggers_reject(tmp_ark_ledger: ArkLedger):
    runner = KPGS8StageChainRunner(symbol="SPY", ark_ledger=tmp_ark_ledger)
    drawdown_breach = {
        "structure": "bull_put_vertical_spread",
        "max_loss": "1000.00",
        "portfolio_equity": "100000.00",
        "daily_drawdown_pct": "5.80",  # > 5.0% ceiling
    }

    receipt = runner.run_chain(validation_data=drawdown_breach)
    assert receipt.governance_decision == "REJECT"
    assert any("stage_3:drawdown_ceiling_breach" in r for r in receipt.reasons)


def test_evidence_chain_advisory_outage_triggers_hold(tmp_ark_ledger: ArkLedger):
    runner = KPGS8StageChainRunner(symbol="SPY", ark_ledger=tmp_ark_ledger)
    attestation = {
        "advisory_model": "Featherless AI",
        "provider_status": "OFFLINE",
        "rationale": "None",
    }

    receipt = runner.run_chain(attestation_data=attestation)
    assert receipt.governance_decision == "HOLD"
    assert "stage_4:advisory_provider_outage" in receipt.reasons


def test_evidence_chain_consensus_divergence_triggers_hold(tmp_ark_ledger: ArkLedger):
    runner = KPGS8StageChainRunner(symbol="SPY", ark_ledger=tmp_ark_ledger)
    divergent = {
        "dual_axis_consensus": "DIVERGENCE",
        "financial_axis": "APPROVE",
        "sovereign_axis": "HOLD",
    }

    receipt = runner.run_chain(canonical_data=divergent)
    assert receipt.governance_decision == "HOLD"
    assert "stage_5:consensus_divergence" in receipt.reasons


def test_evidence_chain_dte_boundary_triggers_hold(tmp_ark_ledger: ArkLedger):
    runner = KPGS8StageChainRunner(symbol="SPY", ark_ledger=tmp_ark_ledger)
    # Outside 7-21 days (e.g. 4 days)
    too_short = {"dte": 4}
    receipt = runner.run_chain(time_data=too_short)
    assert receipt.governance_decision == "HOLD"
    assert "stage_7:dte_out_of_bounds_4" in receipt.reasons

    # Too long (e.g. 45 days)
    too_long = {"dte": 45}
    receipt2 = runner.run_chain(time_data=too_long)
    assert receipt2.governance_decision == "HOLD"
    assert "stage_7:dte_out_of_bounds_45" in receipt2.reasons


def test_evidence_chain_missing_order_id_triggers_hold(tmp_ark_ledger: ArkLedger):
    runner = KPGS8StageChainRunner(symbol="SPY", ark_ledger=tmp_ark_ledger)
    reveal = {"alpaca_order_id": "", "is_verified": False}

    receipt = runner.run_chain(reveal_data=reveal)
    assert receipt.governance_decision == "HOLD"
    assert "stage_8:missing_alpaca_order_id" in receipt.reasons


def test_evidence_chain_ark_ledger_commit(tmp_ark_ledger: ArkLedger):
    runner = KPGS8StageChainRunner(symbol="SPY", ark_ledger=tmp_ark_ledger)
    receipt = runner.run_chain()

    assert receipt.governance_decision == "APPROVE"
    assert tmp_ark_ledger.storage_path.exists()
    content = tmp_ark_ledger.storage_path.read_text(encoding="utf-8")
    assert receipt.receipt_id in content


def test_bridge_api_chain_verify_get_endpoint():
    app = _app()
    client = TestClient(app)

    response = client.get("/api/bridge/chain/verify?symbol=SPY")
    assert response.status_code == 200
    data = response.json()

    assert data["symbol"] == "SPY"
    assert len(data["stages"]) == 8
    assert data["governance_decision"] == "APPROVE"
    assert data["is_fully_evidenced"] is True
    assert "root_hash" in data


def test_bridge_api_chain_verify_post_endpoint():
    app = _app()
    client = TestClient(app)

    # Post with risk breach
    payload = {
        "symbol": "QQQ",
        "validation_data": {
            "structure": "bull_put_vertical_spread",
            "max_loss": "5000.00",
            "portfolio_equity": "100000.00",
            "daily_drawdown_pct": "1.00",
        },
    }
    response = client.post("/api/bridge/chain/verify", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["symbol"] == "QQQ"
    assert data["governance_decision"] == "REJECT"
    assert any("stage_3:risk_ceiling_breach" in r for r in data["reasons"])
