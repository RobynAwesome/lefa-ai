from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from lefa import mcp_client
from lefa.ark import ArkLedger
from lefa.config import Settings
from lefa.mcp_client import AlpacaPaperObserver


def _settings(monkeypatch) -> Settings:
    monkeypatch.setenv("ALPACA_API_KEY", "test-paper-key")
    monkeypatch.setenv("ALPACA_SECRET_KEY", "test-paper-secret")
    monkeypatch.setenv("ALPACA_PAPER_TRADE", "true")
    return Settings(_env_file=None)


@pytest.mark.asyncio
async def test_direct_alpaca_observations_are_recorded(monkeypatch):
    with TemporaryDirectory() as tmpdir:
        ledger_path = Path(tmpdir) / "mcp_ledger.jsonl"
        ark = ArkLedger(storage_path=ledger_path)
        settings = _settings(monkeypatch)

        monkeypatch.setattr(
            mcp_client.ReadOnlyAlpaca,
            "get_account",
            lambda self: {
                "id": "account-id",
                "status": "ACTIVE",
                "account_blocked": False,
                "trading_blocked": False,
                "trade_suspended_by_user": False,
                "equity": "100000.00",
            },
        )
        observer = AlpacaPaperObserver(ark_ledger=ark, settings=settings)

        quote = SimpleNamespace(
            bid_price=595.40,
            ask_price=595.60,
            timestamp="2026-09-02T10:00:00Z",
        )
        market_client = MagicMock()
        market_client.get_stock_latest_quote.return_value = {"SPY": quote}
        monkeypatch.setattr(mcp_client, "StockHistoricalDataClient", lambda *args: market_client)

        account_id = await observer.observe_account()
        quote_id = await observer.observe_quote("spy")

        assert account_id
        assert quote_id
        records = [line for line in ledger_path.read_text(encoding="utf-8").splitlines() if line]
        assert len(records) == 2
        assert '"source": "Alpaca"' in records[0]
        assert '"is_fixture": false' in records[0]
        market_client.get_stock_latest_quote.assert_called_once()


@pytest.mark.asyncio
async def test_observer_fails_closed_when_credentials_are_missing(monkeypatch):
    monkeypatch.delenv("ALPACA_API_KEY", raising=False)
    monkeypatch.delenv("ALPACA_SECRET_KEY", raising=False)
    monkeypatch.delenv("ALPACA_API_SECRET", raising=False)
    monkeypatch.delenv("APCA_API_KEY_ID", raising=False)
    monkeypatch.delenv("APCA_API_SECRET_KEY", raising=False)

    observer = AlpacaPaperObserver(
        ark_ledger=MagicMock(),
        settings=Settings(_env_file=None),
    )

    with pytest.raises(RuntimeError, match="ALPACA_CREDENTIALS_UNAVAILABLE"):
        await observer.observe_account()


@pytest.mark.asyncio
async def test_observer_rejects_non_paper_configuration():
    settings = MagicMock()
    settings.alpaca_paper = False
    observer = AlpacaPaperObserver(ark_ledger=MagicMock(), settings=settings)

    with pytest.raises(RuntimeError, match="CRITICAL GOVERNANCE FAILURE"):
        await observer.observe_account()


@pytest.mark.asyncio
async def test_unknown_observation_does_not_claim_execution():
    settings = MagicMock()
    settings.alpaca_paper = True
    settings.alpaca_api_key.get_secret_value.return_value = "test-paper-key"
    settings.alpaca_secret_key.get_secret_value.return_value = "test-paper-secret"
    observer = AlpacaPaperObserver(ark_ledger=MagicMock(), settings=settings)

    with pytest.raises(RuntimeError, match="Unknown read-only Alpaca observation"):
        await observer._execute_mcp_call("place_option_order")
