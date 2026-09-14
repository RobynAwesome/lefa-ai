"""Comprehensive test suite for KPGS 8-Stage Evidence-Backed Chain Architecture."""

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from lefa import bridge_api
from lefa.ark import ArkLedger
from lefa.evidence_chain import (
    BracketManagementNestingProtocol,
    BracketManagementProtocol,
    KPGS8StageChainRunner,
    UltimateBracketManagementNonPlayerProtocol,
    UltimateBracketManagementProtocol,
)


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


def test_bracket_management_protocol_enforcement():
    bmp = BracketManagementProtocol()
    payload = {
        "what": "Bull Put Spread 590/585",
        "who": "Cassey (AI Advisor)",
        "why": "Harvest elevated IV/RV",
    }
    rec = bmp.enforce(payload, context="LEFA_OPTIONS")

    assert rec["schema"] == "bmp_v1.0"
    assert rec["spatial"] == "[LEFA_OPTIONS]"
    assert rec["keynote"] == "{Bull Put Spread 590/585}"
    assert rec["ark"] == "<Cassey (AI Advisor)>"
    assert rec["understand"] == "(Harvest elevated IV/RV)"
    assert len(rec["bmp_hash"]) == 16
    assert rec["cbp_verdict"] == "POC_CLEARED"
    assert rec["foc_purged"] is False

    # Test FOC detection
    foc_payload = {"what": "maybe buy calls", "why": "tbd later"}
    foc_rec = bmp.enforce(foc_payload, context="LEFA_OPTIONS")
    assert foc_rec["cbp_verdict"] == "FOC_SEVERED"
    assert foc_rec["foc_purged"] is True
    assert "maybe" in foc_rec["foc_markers"]
    assert "later" in foc_rec["foc_markers"]


def test_bracket_management_nesting_protocol_domains():
    bmp = BracketManagementProtocol()
    bmnp = BracketManagementNestingProtocol()

    rec = bmp.enforce({"what": "test"}, context="LEFA_OPTIONS")
    nested = bmnp.nest(rec, domain="LEFA", agent="CASSEY")

    assert nested["schema"] == "bmnp_v1"
    assert nested["domain"] == "LEFA"
    assert nested["agent"] == "CASSEY"
    assert nested["nesting"] == f"[GSMB[LEFA[CASSEY[{rec['bmp_hash']}]]]]"

    # Test unknown domain fallback to GSMB
    fallback = bmnp.nest(rec, domain="UNKNOWN_DOMAIN", agent="AGENT_X")
    assert fallback["domain"] == "GSMB"
    assert fallback["nesting"] == f"[GSMB[GSMB[AGENT_X[{rec['bmp_hash']}]]]]"


def test_ultimate_bracket_management_protocol_rtc_seal():
    ubmp = UltimateBracketManagementProtocol()
    res = ubmp.produce_ubmp(
        chain_id="A1B2C3D4E5F6",
        ikp_code="CLEAN",
        dso="HDSO",
        dso_label="###!!!",
        rtc_hash="fdeb30981a5398d8",
        clean=True,
        four_ws_valid=True,
        bmp_hash="47378521fcdf2984",
        cbp_verdict="POC_CLEARED",
        bmnp_nesting="[GSMB[LEFA[CASSEY[47378521fcdf2984]]]]",
        pp_status="FAST_TRACK",
    )

    assert res["schema"] == "ubmp_output_v1"
    assert res["chain_id"] == "A1B2C3D4E5F6"
    assert res["ikp_code"] == "CLEAN"
    assert res["dso"] == "HDSO"
    assert res["dso_label"] == "###!!!"
    assert res["constraint"] == "I_AM_STATELESS_RENTER_NOT_LANDLORD"
    assert res["clean"] is True


def test_ultimate_bracket_management_non_player_pkap_math():
    ubmnp = UltimateBracketManagementNonPlayerProtocol()

    # Baseline nominal: matches sap_spawn_log.jsonl line 1
    eval_pass = ubmnp.evaluate_pkap(
        bmnp_depth=6.0,
        bmp_score=0.95,
        ubmp_score=1.0,
        ubmnp_base=3.35,
        kpgs_power=3,
        dso_weight=3.0,
        rtc_factor=1.0,
        four_ws_complete=True,
        is_clean=True,
    )
    assert eval_pass["verdict"] == "POC_AUTHORIZED"
    assert eval_pass["autonomous_authorized"] is True
    assert eval_pass["pkap_score"] == pytest.approx(9.1508, rel=1e-3)
    assert eval_pass["pkap_result"]["steps"]["B_brackets"] == 5.7
    assert eval_pass["pkap_result"]["steps"]["O_orders"] == 9.05
    assert eval_pass["pkap_result"]["steps"]["D_denominator"] == 81.0

    # Incomplete 4Ws or FOC: matches sap_spawn_log.jsonl line 4
    eval_foc = ubmnp.evaluate_pkap(
        four_ws_complete=False,
        is_clean=False,
    )
    assert eval_foc["verdict"] == "FOC_DECLINED"
    assert eval_foc["autonomous_authorized"] is False
    assert eval_foc["pkap_score"] == pytest.approx(0.0015, rel=1e-2)


def test_evidence_chain_receipt_includes_bmp_bmnp_ubmp_ubmnp(tmp_ark_ledger: ArkLedger):
    runner = KPGS8StageChainRunner(symbol="SPY", ark_ledger=tmp_ark_ledger)
    receipt = runner.run_chain()

    assert receipt.governance_decision == "APPROVE"
    assert receipt.bmp["schema"] == "bmp_v1.0"
    assert receipt.bmnp["schema"] == "bmnp_v1"
    assert receipt.ubmp["schema"] == "ubmp_output_v1"
    assert receipt.ubmnp["schema"] == "ubmnp_non_player_v1"
    assert receipt.ubmnp["autonomous_authorized"] is True
    assert receipt.ubmp["constraint"] == "I_AM_STATELESS_RENTER_NOT_LANDLORD"


def test_kpgs_three_turn_feedback_loop(tmp_ark_ledger: ArkLedger):
    runner = KPGS8StageChainRunner(symbol="SPY", ark_ledger=tmp_ark_ledger)
    res = runner.run_feedback_loop(turns=3, perturbation_turn=2)

    assert res["schema"] == "kpgs_feedback_loop_v1"
    assert res["turns_requested"] == 3
    assert res["whole_system_verdict"] == "POC_VALIDATED_CONVERGED"
    assert res["integrity_score"] == 1.0
    assert res["all_turns_honest"] is True
    assert res["constraint"] == "I_AM_STATELESS_RENTER_NOT_LANDLORD"

    turns = res["turns"]
    assert len(turns) == 3

    # Turn 1: Nominal baseline execution -> PASS
    assert turns[0]["turn"] == 1
    assert turns[0]["decision"] == "APPROVE"
    assert turns[0]["is_fully_evidenced"] is True
    assert turns[0]["ubmnp_authorized"] is True
    assert turns[0]["pkap_score"] > 5.0

    # Turn 2: Controlled perturbation -> HOLD fail-closed
    assert turns[1]["turn"] == 2
    assert turns[1]["decision"] == "HOLD"
    assert turns[1]["is_fully_evidenced"] is False
    assert turns[1]["ubmnp_authorized"] is False
    assert any("stage_1:quote_stale" in r for r in turns[1]["reasons"])

    # Turn 3: Recovery and convergence -> PASS
    assert turns[2]["turn"] == 3
    assert turns[2]["decision"] == "APPROVE"
    assert turns[2]["is_fully_evidenced"] is True
    assert turns[2]["ubmnp_authorized"] is True
    assert turns[2]["pkap_score"] > 5.0
