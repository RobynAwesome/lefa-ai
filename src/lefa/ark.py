import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict
from uuid import UUID, uuid4

logger = logging.getLogger(__name__)

class ArkLedger:
    """
    The Ark: LEFA's Ledger & Temporal Engine.
    Reality-to-Cloud (RTC) component preserving observations (T0), decisions (T1), and outcomes (T3+).
    Law: Future knowledge must not rewrite what the system knew in the past.
    """
    
    def __init__(self, storage_path: Path = Path("receipts/ark_ledger.jsonl")):
        self.storage_path = storage_path
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
    def _append_to_ledger(self, record_type: str, data: Dict[str, Any]) -> str:
        record = {
            "record_id": str(uuid4()),
            "timestamp": datetime.now(UTC).isoformat(),
            "type": record_type,
            "data": data
        }
        
        # Append-only immutability simulation
        with open(self.storage_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
            
        logger.info(f"Ark Ledger appended: {record_type} [{record['record_id']}]")
        return record["record_id"]
        
    def record_observation(self, source: str, observation_data: Dict[str, Any]) -> str:
        """T0: Record an observation from The Eye."""
        data = {
            "temporal_state": "T0",
            "source": source,
            "observation": observation_data
        }
        return self._append_to_ledger("OBSERVATION", data)

    def record_decision(self, receipt_dict: Dict[str, Any], context_id: str) -> str:
        """T1: Record a decision from The Brain/Hand based on T0."""
        data = {
            "temporal_state": "T1",
            "context_id": context_id, # Link back to observation
            "receipt": receipt_dict
        }
        return self._append_to_ledger("DECISION", data)
        
    def reveal_outcome(self, context_id: str, outcome_data: Dict[str, Any]) -> str:
        """T3+: Record the reality outcome matching a past decision."""
        data = {
            "temporal_state": "T3",
            "context_id": context_id,
            "outcome": outcome_data
        }
        return self._append_to_ledger("REVEAL", data)
