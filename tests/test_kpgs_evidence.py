"""
Unit tests for KPGSEvidenceEngine (KPGS 8-Stage Cryptographic Evidence Engine).
Validates:
  1. Default bundle produces 8 procedural stages.
  2. Populated bundle produces 8 evidenced stages with SHA-256 digests.
  3. Fully evidenced verification check.
  4. Composite chain hash determinism and tamper sensitivity.
  5. Integration with CanonicalTradingOrchestrator._proof_depth.
"""

from datetime import UTC, datetime
from decimal import Decimal

from lefa.governance import ProofStageMaturity
from lefa.kpgs_evidence import KPGSEvidenceBundle, KPGSEvidenceEngine
from lefa.orchestration import _proof_depth


def test_default_bundle_is_procedural():
    depth = KPGSEvidenceEngine.build_proof_depth(None)
    assert len(depth) == 8
    assert all(stage.maturity == ProofStageMaturity.PROCEDURAL for stage in depth)
    assert all(stage.evidence_ref is None for stage in depth)
    assert not KPGSEvidenceEngine.is_fully_evidenced(depth)


def test_fully_evidenced_bundle():
    bundle = KPGSEvidenceBundle(
        witness_data={"symbol": "SPY", "price": "595.20", "iv_rv_ratio": 1.28},
        observation_data={"intent": "observe_options_chain", "source": "voice_rtc"},
        validation_data={"max_loss": "1750.00", "risk_pct": "1.75", "policy_limit": "3.00"},
        attestation_data={
            "rationale": "High IV/RV provides rich premium opportunity",
            "model": "qwen2.5",
        },
        canonical_data={"agreement": "dual_axis_pass", "jurisdiction": "paper"},
        ledger_data={"ledger_path": "ark_ledger.jsonl", "offset": 42},
        time_data={"expiry": "2026-09-25", "dte": 14, "observed_at": datetime.now(UTC).isoformat()},
        reveal_data={"order_id": "alpaca-paper-order-001", "status": "accepted"},
    )
    depth = KPGSEvidenceEngine.build_proof_depth(bundle)
    assert len(depth) == 8
    assert all(stage.maturity == ProofStageMaturity.EVIDENCED for stage in depth)
    assert all(
        stage.evidence_ref is not None and stage.evidence_ref.startswith("sha256:")
        for stage in depth
    )
    assert KPGSEvidenceEngine.is_fully_evidenced(depth)


def test_partial_evidence_fails_closed_to_not_fully_evidenced():
    bundle = KPGSEvidenceBundle(
        witness_data={"symbol": "SPY", "price": "595.20"},
        observation_data={"intent": "observe_options_chain"},
        # missing remaining 6 stages
    )
    depth = KPGSEvidenceEngine.build_proof_depth(bundle)
    assert len(depth) == 8
    assert depth[0].maturity == ProofStageMaturity.EVIDENCED
    assert depth[1].maturity == ProofStageMaturity.EVIDENCED
    assert depth[2].maturity == ProofStageMaturity.PROCEDURAL
    assert not KPGSEvidenceEngine.is_fully_evidenced(depth)


def test_composite_chain_hash_tamper_detection():
    bundle_a = KPGSEvidenceBundle(witness_data={"symbol": "SPY", "price": "595.20"})
    bundle_b = KPGSEvidenceBundle(
        witness_data={"symbol": "SPY", "price": "595.21"}
    )  # 1 cent difference

    depth_a = KPGSEvidenceEngine.build_proof_depth(bundle_a)
    depth_b = KPGSEvidenceEngine.build_proof_depth(bundle_b)

    fixed_time = datetime(2026, 9, 13, 15, 0, 0, tzinfo=UTC)
    hash_a = KPGSEvidenceEngine.compute_composite_chain_hash(depth_a, timestamp=fixed_time)
    hash_b = KPGSEvidenceEngine.compute_composite_chain_hash(depth_b, timestamp=fixed_time)

    assert hash_a != hash_b, "1-cent price change in witness data must produce different root hash"


def test_orchestration_proof_depth_integration():
    bundle = KPGSEvidenceBundle(
        witness_data={"symbol": "QQQ", "price": "490.00"},
        validation_data={"trade_risk": Decimal("0.02")},
    )
    result = {"status": "success", "evidence_bundle": bundle}
    depth = _proof_depth(result)
    assert len(depth) == 8
    assert depth[0].maturity == ProofStageMaturity.EVIDENCED
    assert depth[2].maturity == ProofStageMaturity.EVIDENCED
    assert depth[1].maturity == ProofStageMaturity.PROCEDURAL
