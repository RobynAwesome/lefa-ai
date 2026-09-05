from types import SimpleNamespace

import pytest
from alpaca.trading.enums import OrderClass

from lefa.alpaca import AlpacaPaperBroker


class FakeTradingClient:
    def __init__(self) -> None:
        self.submitted = None

    def submit_order(self, *, order_data):
        self.submitted = order_data
        return SimpleNamespace(
            id="provider-order-123",
            client_order_id=order_data.client_order_id,
            symbol=None,
            status="new",
            submitted_at="2026-09-05T16:00:00Z",
            order_class=OrderClass.MLEG,
        )

    def get_order_by_id(self, order_id: str):
        return SimpleNamespace(
            id=order_id,
            client_order_id="lefa-demo",
            symbol=None,
            status="new",
            submitted_at="2026-09-05T16:00:00Z",
            order_class=OrderClass.MLEG,
        )


def _broker() -> tuple[AlpacaPaperBroker, FakeTradingClient]:
    client = FakeTradingClient()
    broker = object.__new__(AlpacaPaperBroker)
    broker._client = client
    return broker, client


def _legs() -> list[dict[str, str]]:
    return [
        {"symbol": "SPY260918P00095000", "ratio_qty": "1", "side": "sell"},
        {"symbol": "SPY260918P00090000", "ratio_qty": "1", "side": "buy"},
    ]


def test_credit_spread_rejects_positive_limit_price() -> None:
    broker, _ = _broker()
    with pytest.raises(ValueError, match="negative Alpaca mleg limit price"):
        broker.place_option_order(
            symbol="SPY",
            limit_price="0.90",
            legs=_legs(),
            client_order_id="lefa-demo",
        )


def test_credit_spread_uses_public_submit_order_and_provider_id() -> None:
    broker, client = _broker()
    result = broker.place_option_order(
        symbol="SPY",
        limit_price="-0.90",
        legs=_legs(),
        client_order_id="lefa-demo",
    )

    assert client.submitted is not None
    assert client.submitted.order_class == OrderClass.MLEG
    assert client.submitted.limit_price == -0.90
    assert client.submitted.symbol is None
    assert len(client.submitted.legs) == 2
    assert result["order_id"] == "provider-order-123"
    assert result["signed_limit_price"] == "-0.90"


def test_provider_confirmation_is_separate_read() -> None:
    broker, _ = _broker()
    confirmed = broker.get_order("provider-order-123")
    assert confirmed["order_id"] == "provider-order-123"
    assert confirmed["status"] == "new"
