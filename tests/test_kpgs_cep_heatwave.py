"""
Tests for KPGS Group-By Data Science, CEP 8-Stage Stream Engine & Heat Wave Matrix
"""

from __future__ import annotations

import time

from lefa.kpgs_cep_heatwave import (
    STAGE_EPOCHS,
    STAGE_NAMES,
    AnomalyType,
    CEPStreamProcessor,
    GroupByDataScienceEngine,
    HeatWaveMatrix,
    KPGSProofEvent,
    StageMaturity,
    ThermalZone,
)


def _make_event(
    dns_zone: str,
    stage_id: int,
    trace_id: str = "trace-001",
    latency_ms: float = 12.0,
    maturity: StageMaturity = StageMaturity.EVIDENCED,
    risk_ratio: float = 0.25,
) -> KPGSProofEvent:
    return KPGSProofEvent(
        event_id=f"ev-{stage_id}-{int(time.time() * 1000)}",
        trace_id=trace_id,
        dns_zone=dns_zone,
        stage_id=stage_id,
        stage_name=STAGE_NAMES[stage_id],
        epoch=STAGE_EPOCHS[stage_id],
        timestamp=time.time(),
        latency_ms=latency_ms,
        maturity=maturity,
        risk_ratio=risk_ratio,
        hash_digest=f"sha256:mock_{stage_id}",
    )


def test_cep_nominal_causality_flow():
    cep = CEPStreamProcessor(latency_threshold_ms=100.0)
    trace_id = "trace-pristine"

    # Ingest full 8-stage sequence in correct temporal order
    for stage in range(1, 9):
        anomalies = cep.ingest(_make_event("kasilink.com", stage, trace_id, latency_ms=15.0))
        assert len(anomalies) == 0

    completeness_anomalies = cep.verify_trace_completeness(trace_id)
    assert len(completeness_anomalies) == 0
    assert len(cep.anomalies) == 0


def test_cep_causal_inversion_detected():
    cep = CEPStreamProcessor()
    trace_id = "trace-inverted"

    # Ingest Stage 4 before Stage 3
    cep.ingest(_make_event("lefa-ai.internal", 4, trace_id))
    anomalies = cep.ingest(_make_event("lefa-ai.internal", 3, trace_id))

    assert len(anomalies) > 0
    assert any(a.anomaly_type == AnomalyType.CAUSAL_INVERSION for a in anomalies)


def test_cep_skipped_stage_detected():
    cep = CEPStreamProcessor()
    trace_id = "trace-skipped"

    # Ingest stages 1, 2, 3, 5, 6, 7, 8 (stage 4 is omitted)
    for stage in [1, 2, 3, 5, 6, 7, 8]:
        cep.ingest(_make_event("kasilink.com", stage, trace_id))

    missing = cep.verify_trace_completeness(trace_id)
    assert len(missing) == 1
    assert missing[0].stage_id == 4
    assert missing[0].anomaly_type == AnomalyType.STAGE_SKIPPED


def test_cep_evidence_void_and_tamper_detected():
    cep = CEPStreamProcessor()

    anom1 = cep.ingest(
        _make_event(
            "kopano-labs.com",
            1,
            "t-void",
            maturity=StageMaturity.PROCEDURAL,
        )
    )
    assert any(a.anomaly_type == AnomalyType.EVIDENCE_VOID for a in anom1)

    anom2 = cep.ingest(
        _make_event(
            "kopano-labs.com",
            2,
            "t-tamper",
            maturity=StageMaturity.TAMPERED,
        )
    )
    assert any(a.anomaly_type == AnomalyType.TAMPER_DETECTED for a in anom2)


def test_groupby_data_science_aggregations():
    events: list[KPGSProofEvent] = []

    # DNS 1: kasilink.com (100% evidenced, low latency)
    for _ in range(10):
        events.append(
            _make_event(
                "kasilink.com",
                1,
                latency_ms=10.0,
                maturity=StageMaturity.EVIDENCED,
            )
        )

    # DNS 2: lefa-ai.internal (50% procedural, high latency)
    for i in range(10):
        mat = StageMaturity.EVIDENCED if i < 5 else StageMaturity.PROCEDURAL
        events.append(
            _make_event(
                "lefa-ai.internal",
                1,
                latency_ms=80.0,
                maturity=mat,
            )
        )

    metrics = GroupByDataScienceEngine.aggregate(events)
    assert len(metrics) == 2

    kasi_m = next(m for m in metrics if m.dns_zone == "kasilink.com")
    lefa_m = next(m for m in metrics if m.dns_zone == "lefa-ai.internal")

    assert kasi_m.count == 10
    assert kasi_m.mean_latency_ms == 10.0
    assert kasi_m.evidence_ratio == 1.0
    assert kasi_m.temperature < 0.25  # Pristine FROST

    assert lefa_m.count == 10
    assert lefa_m.mean_latency_ms == 80.0
    assert lefa_m.evidence_ratio == 0.50
    assert lefa_m.temperature > kasi_m.temperature


def test_heatwave_matrix_and_accountability_lock():
    events: list[KPGSProofEvent] = []
    cep = CEPStreamProcessor()

    # Generate full 8-stage matrix for kasilink.com (Pristine)
    for s in range(1, 9):
        ev = _make_event("kasilink.com", s, latency_ms=8.0, maturity=StageMaturity.EVIDENCED)
        events.append(ev)
        cep.ingest(ev)

    # Generate failing stage for rogue-domain.xyz (Severe Anomaly)
    rogue_ev = _make_event(
        "rogue-domain.xyz",
        3,
        latency_ms=350.0,
        maturity=StageMaturity.TAMPERED,
        risk_ratio=1.5,
    )
    events.append(rogue_ev)
    cep.ingest(rogue_ev)

    metrics = GroupByDataScienceEngine.aggregate(events, anomalies=cep.anomalies)
    matrix = HeatWaveMatrix(metrics)

    # kasilink.com should have Frost/Temperate temperatures
    assert matrix.classify_zone(matrix.get_temperature("kasilink.com", 1)) == ThermalZone.FROST

    # rogue-domain.xyz should trip Heat Wave and lock
    rogue_temp = matrix.get_temperature("rogue-domain.xyz", 3)
    assert rogue_temp >= 0.75
    assert matrix.classify_zone(rogue_temp) == ThermalZone.HEAT_WAVE

    locks = matrix.check_accountability_lock(threshold=0.75)
    assert len(locks) >= 1
    assert locks[0]["dns_zone"] == "rogue-domain.xyz"
    assert locks[0]["action"] == "TRIGGER_FAIL_CLOSED_HOLD"

    # Verify ASCII render output
    ascii_out = matrix.render_ascii()
    assert "HEAT WAVE ACCOUNTABILITY MATRIX" in ascii_out
    assert "rogue-domain.xyz" in ascii_out
    assert "ACTIVE ACCOUNTABILITY LOCKOUTS" in ascii_out
