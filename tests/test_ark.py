import json
from pathlib import Path
from tempfile import TemporaryDirectory

from lefa.ark import ArkLedger

def test_ark_ledger_temporal_sequence():
    with TemporaryDirectory() as tmpdir:
        ledger_path = Path(tmpdir) / "test_ledger.jsonl"
        ark = ArkLedger(storage_path=ledger_path)
        
        # T0 Observation
        obs_id = ark.record_observation("AlpacaMCP", {"status": "ACTIVE", "equity": 10000})
        assert obs_id is not None
        
        # T1 Decision
        dec_id = ark.record_decision({"decision": "APPROVE"}, context_id=obs_id)
        assert dec_id is not None
        
        # T3 Reveal
        rev_id = ark.reveal_outcome(context_id=dec_id, outcome_data={"profit": 50})
        assert rev_id is not None
        
        # Verify persistence and immutability (append-only)
        lines = ledger_path.read_text(encoding="utf-8").strip().split("\n")
        assert len(lines) == 3
        
        obs_record = json.loads(lines[0])
        assert obs_record["type"] == "OBSERVATION"
        assert obs_record["data"]["temporal_state"] == "T0"
        
        dec_record = json.loads(lines[1])
        assert dec_record["type"] == "DECISION"
        assert dec_record["data"]["temporal_state"] == "T1"
        assert dec_record["data"]["context_id"] == obs_id
        
        rev_record = json.loads(lines[2])
        assert rev_record["type"] == "REVEAL"
        assert rev_record["data"]["temporal_state"] == "T3"
        assert rev_record["data"]["context_id"] == dec_id
