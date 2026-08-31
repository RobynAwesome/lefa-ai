import pytest
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from lefa.ark import ArkLedger
from lefa.voice import VoiceObserver, VoiceProjector

@pytest.mark.asyncio
async def test_voice_rtc_loop():
    with TemporaryDirectory() as tmpdir:
        ledger_path = Path(tmpdir) / "voice_ledger.jsonl"
        ark = ArkLedger(storage_path=ledger_path)
        
        # Test STT (The Eye -> The Voice)
        stt = VoiceObserver(ark_ledger=ark)
        obs_id = await stt.recognize_speech(audio_source="mic_1", mock_transcript="Buy 10 shares of AAPL")
        assert obs_id is not None
        
        # Test TTS (The Voice -> The Face/Ears)
        tts = VoiceProjector(ark_ledger=ark)
        rev_id = await tts.speak_reveal(context_id=obs_id, spoken_text="Trade executed successfully.")
        assert rev_id is not None
        
        # Verify RTC Persistence
        lines = ledger_path.read_text(encoding="utf-8").strip().split("\n")
        assert len(lines) == 2
        
        obs_record = json.loads(lines[0])
        assert obs_record["type"] == "OBSERVATION"
        assert obs_record["data"]["temporal_state"] == "T0"
        assert obs_record["data"]["observation"]["transcript"] == "Buy 10 shares of AAPL"
        
        rev_record = json.loads(lines[1])
        assert rev_record["type"] == "REVEAL"
        assert rev_record["data"]["temporal_state"] == "T3"
        assert rev_record["data"]["outcome"]["spoken"] == "Trade executed successfully."
        assert rev_record["data"]["context_id"] == obs_id
