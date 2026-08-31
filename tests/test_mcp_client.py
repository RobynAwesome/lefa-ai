import pytest
import os
from unittest.mock import patch, MagicMock
from pathlib import Path
from tempfile import TemporaryDirectory

from lefa.ark import ArkLedger
from lefa.mcp_client import AlpacaPaperObserver

@pytest.mark.asyncio
async def test_mcp_client_success():
    with TemporaryDirectory() as tmpdir:
        ledger_path = Path(tmpdir) / "mcp_ledger.jsonl"
        ark = ArkLedger(storage_path=ledger_path)
        observer = AlpacaPaperObserver(ark_ledger=ark)
        
        with patch.dict(os.environ, {"ALPACA_PAPER_TRADE": "true"}):
            obs_id = await observer.observe_account()
            assert obs_id is not None
            
            quote_id = await observer.observe_quote("SPY")
            assert quote_id is not None
            
        lines = ledger_path.read_text(encoding="utf-8").strip().split("\n")
        assert len(lines) == 2


@pytest.mark.asyncio
async def test_mcp_client_fails_closed_when_not_paper():
    ark = MagicMock()
    observer = AlpacaPaperObserver(ark_ledger=ark)
    
    with patch.dict(os.environ, {"ALPACA_PAPER_TRADE": "false"}):
        with pytest.raises(RuntimeError, match="CRITICAL GOVERNANCE FAILURE"):
            await observer.observe_account()
