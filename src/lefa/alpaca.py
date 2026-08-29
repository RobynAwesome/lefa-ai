from decimal import Decimal

from alpaca.trading.client import TradingClient

from lefa.config import Settings
from lefa.governance import AccountState


class ReadOnlyAlpaca:
    """Paper telemetry adapter. Intentionally exposes no order methods."""

    def __init__(self, settings: Settings) -> None:
        self._client = TradingClient(
            settings.alpaca_api_key.get_secret_value(),
            settings.alpaca_secret_key.get_secret_value(),
            paper=True,
        )

    def account_state(self) -> AccountState:
        account = self._client.get_account()
        equity = Decimal(str(account.equity))
        last_equity = Decimal(str(account.last_equity))
        return AccountState(
            equity=equity,
            open_risk=Decimal(0),
            daily_pnl=equity - last_equity,
        )
