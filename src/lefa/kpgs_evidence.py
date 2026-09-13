"""
LEFA AI — KPGS Cryptographic 8-Stage Evidence Engine
=====================================================
Transforms procedural proof stages into cryptographically verifiable,
evidence-backed stages under the Kopano Provenance Governance System (KPGS).

The 8 Canonical Stages:
  1. stage_1_witness        (T0): Live provider market evidence (quotes, Greeks, IV/RV)
  2. stage_2_observation    (T0): Human intention (Speechmatics audio / text prompt)
  3. stage_3_validation     (T1): Deterministic risk firewall policy verification
  4. stage_4_attestation    (T1): Advisory AI reasoning rationale (Featherless/Cassey)
  5. stage_5_canonicalization(T2): Dual-axis bridge consensus
  6. stage_6_ledgering      (T2): Immutable Ark append-only commit digest
  7. stage_7_time           (T3): Freshness window & DTE expiry horizon
  8. stage_8_reveal         (T3): Provider execution receipt or governed hold outcome

Invariants:
  - REALITY_STATE > INDEX_STATE
  - RECEIPT OR HOLD
  - I_AM_STATELESS_RENTER_NOT_LANDLORD
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from lefa.governance import ProofStage, ProofStageMaturity


def _hash_payload(data: Any) -> str:
    """Compute a deterministic SHA-256 digest of arbitrary structured data."""
    if isinstance(data, (dict, list)):
        serialized = json.dumps(data, sort_keys=True, default=str)
    else:
        serialized = str(data)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class KPGSEvidenceBundle:
    """Carries real provider artifacts for each stage of the KPGS lifecycle."""

    witness_data: dict[str, Any] | None = None
    observation_data: dict[str, Any] | None = None
    validation_data: dict[str, Any] | None = None
    attestation_data: dict[str, Any] | None = None
    canonical_data: dict[str, Any] | None = None
    ledger_data: dict[str, Any] | None = None
    time_data: dict[str, Any] | None = None
    reveal_data: dict[str, Any] | None = None


class KPGSEvidenceEngine:
    """Evaluates and constructs cryptographic proof chains for KPGS governance."""

    STAGE_NAMES = (
        "stage_1_witness",
        "stage_2_observation",
        "stage_3_validation",
        "stage_4_attestation",
        "stage_5_canonicalization",
        "stage_6_ledgering",
        "stage_7_time",
        "stage_8_reveal",
    )

    @classmethod
    def build_proof_depth(cls, bundle: KPGSEvidenceBundle | None = None) -> tuple[ProofStage, ...]:
        """Construct the 8-stage proof depth tuple.

        If evidence is supplied for a stage, it is marked EVIDENCED with a SHA-256
        reference. Stages lacking evidence default to PROCEDURAL (fail closed).
        """
        if bundle is None:
            return tuple(
                ProofStage(
                    stage=name,
                    maturity=ProofStageMaturity.PROCEDURAL,
                    evidence_ref=None,
                )
                for name in cls.STAGE_NAMES
            )

        stages_evidence = [
            ("stage_1_witness", bundle.witness_data),
            ("stage_2_observation", bundle.observation_data),
            ("stage_3_validation", bundle.validation_data),
            ("stage_4_attestation", bundle.attestation_data),
            ("stage_5_canonicalization", bundle.canonical_data),
            ("stage_6_ledgering", bundle.ledger_data),
            ("stage_7_time", bundle.time_data),
            ("stage_8_reveal", bundle.reveal_data),
        ]

        result: list[ProofStage] = []
        for stage_name, evidence in stages_evidence:
            if evidence is not None and bool(evidence):
                evidence_digest = _hash_payload(evidence)
                result.append(
                    ProofStage(
                        stage=stage_name,
                        maturity=ProofStageMaturity.EVIDENCED,
                        evidence_ref=f"sha256:{evidence_digest}",
                    )
                )
            else:
                result.append(
                    ProofStage(
                        stage=stage_name,
                        maturity=ProofStageMaturity.PROCEDURAL,
                        evidence_ref=None,
                    )
                )

        return tuple(result)

    @classmethod
    def compute_composite_chain_hash(
        cls, proof_depth: tuple[ProofStage, ...], timestamp: datetime | None = None
    ) -> str:
        """Computes the root SHA-256 hash connecting all stages in an immutable chain."""
        ts = (timestamp or datetime.now(UTC)).isoformat()
        chain_tokens: list[str] = [ts]

        for stage in proof_depth:
            ref = stage.evidence_ref or "procedural_stub"
            chain_tokens.append(f"{stage.stage}:{stage.maturity.value}:{ref}")

        combined = "|".join(chain_tokens)
        return hashlib.sha256(combined.encode("utf-8")).hexdigest()

    @classmethod
    def is_fully_evidenced(cls, proof_depth: tuple[ProofStage, ...]) -> bool:
        """Returns True only if all 8 stages are backed by verified evidence."""
        if len(proof_depth) != 8:
            return False
        return all(
            stage.maturity
            in (
                ProofStageMaturity.EVIDENCED,
                ProofStageMaturity.INDEPENDENTLY_VALIDATED,
            )
            and stage.evidence_ref is not None
            for stage in proof_depth
        )
