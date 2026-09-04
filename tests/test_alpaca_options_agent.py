from __future__ import annotations

import importlib
from dataclasses import dataclass
from decimal import Decimal
from types import SimpleNamespace

import pytest

from lefa.alpaca import AlpacaPaperBroker
from lefa.featherless import FeatherlessUnavailable
from lefa.governance import calculate_open_risk

runner = importlib.import_module("scripts.run_options_agent")


def test_calculate_open_risk_uses_market_value_for_regular_positions() -> None:
    positions = [
        {"symbol": "SPY", "qty": "10", "market_value": "5000", "side": "long"},
        {"symbol": "QQQ", "qty": "-2", "market_value": "-800", "side": "short"},
    ]

    assert calculate_open_risk(positions) == Decimal(5800)


def test_calculate_open_risk_uses_strike_notional_for_short_options() -> None:
    positions = [
        {
            "symbol": "SPY260116P00400000",
            "qty": "-1",
            "market_value": "-12.50",
            "side": "short",
        }
    ]

    assert calculate_open_risk(positions) == Decimal(40000)


def test_calculate_open_risk_rejects_incomplete_position_data() -> None:
    with pytest.raises(ValueError, match="OPEN_RISK_POSITION_INVALID"):
        calculate_open_risk([{"symbol": "SPY", "qty": "1"}])


def _contracts() -> list[dict[str, str]]:
    return [
        {
            "symbol": "SPY260116P00498000",
            "expiration_date": "2026-01-16",
            "strike_price": "498",
        },
        {
            "symbol": "SPY260116P00495000",
            "expiration_date": "2026-01-16",
            "strike_price": "495",
        },
    ]


class FakeOptionsBroker:
    def __init__(self) -> None:
        self.submitted = False

    def get_option_contracts(
        self, underlying_symbol: str, contract_type: str, limit: int
    ) -> list[dict[str, str]]:
        assert (underlying_symbol, contract_type, limit) == ("SPY", "put", 100)
        return _contracts()

    def get_option_quotes(self, symbols: list[str]) -> dict[str, dict[str, str]]:
        assert symbols == [
            "SPY260116P00498000",
            "SPY260116P00495000",
        ]
        return {
            "SPY260116P00498000": {"bid_price": "2.50", "ask_price": "2.60"},
            "SPY260116P00495000": {"bid_price": "0.90", "ask_price": "1.00"},
        }

    def get_positions(self) -> list[dict[str, str]]:
        return []

    def place_option_order(self, **kwargs: object) -> dict[str, str]:
        self.submitted = True
        assert kwargs["order_class"] == "mleg"
        return {
            "order_id": "order-123",
            "status": "accepted",
            "submitted_at": "2026-01-15T12:00:00+00:00",
        }


def test_option_structure_uses_quoted_same_expiration_contracts() -> None:
    structure = runner._option_structure(FakeOptionsBroker(), "SPY", Decimal(500))

    assert structure["short_symbol"] == "SPY260116P00498000"
    assert structure["long_symbol"] == "SPY260116P00495000"
    assert structure["credit_per_share"] == "1.50"
    assert structure["maximum_loss"] == Decimal("150.00")


def test_option_structure_fails_closed_when_quotes_are_missing() -> None:
    broker = FakeOptionsBroker()
    broker.get_option_quotes = lambda symbols: {}

    with pytest.raises(RuntimeError, match="OPTIONS_QUOTES_UNAVAILABLE"):
        runner._option_structure(broker, "SPY", Decimal(500))


@dataclass
class FakeReasoner:
    configured: bool = True
    explanation: str = "The quoted spread is defined risk and remains subject to policy."

    model: str = "test-model"

    def is_configured(self) -> bool:
        return self.configured

    def complete(self, messages: list[dict[str, str]], **kwargs: object) -> str:
        return self.explanation


def _patch_runner(monkeypatch: pytest.MonkeyPatch, broker: FakeOptionsBroker) -> None:
    monkeypatch.setattr(
        runner,
        "get_alpaca_account",
        lambda: {
            "account_id": "acct-123",
            "account_number": "PA123",
            "status": "ACTIVE",
            "equity": Decimal(100000),
            "last_equity": Decimal(100000),
            "buying_power": Decimal(100000),
            "cash": Decimal(100000),
            "options_level": 2,
        },
    )
    monkeypatch.setattr(
        runner,
        "get_alpaca_quote",
        lambda symbol: {
            "symbol": symbol,
            "bid_price": "499",
            "ask_price": "501",
            "timestamp": "2026-01-15T12:00:00+00:00",
        },
    )
    monkeypatch.setattr(runner, "AlpacaPaperBroker", lambda: broker)
    monkeypatch.setattr(runner, "FeatherlessReasoner", FakeReasoner)


def test_run_agent_cycle_submits_only_after_risk_approval(monkeypatch: pytest.MonkeyPatch) -> None:
    broker = FakeOptionsBroker()
    _patch_runner(monkeypatch, broker)

    result = runner.run_agent_cycle("SPY")

    assert result["decision"] == "approve"
    assert result["execution_state"] == "ORDER_SUBMITTED"
    assert result["alpaca_order_id"] == "order-123"
    assert broker.submitted is True


def test_run_agent_cycle_holds_when_open_risk_is_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    broker = FakeOptionsBroker()
    broker.get_positions = lambda: [{"symbol": "SPY", "qty": "1"}]
    _patch_runner(monkeypatch, broker)

    result = runner.run_agent_cycle("SPY")

    assert result == {
        "decision": "hold",
        "execution_state": "HOLD",
        "provider_code": "ALPACA_OPEN_RISK_UNAVAILABLE",
    }
    assert broker.submitted is False


def test_run_agent_cycle_holds_when_featherless_is_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    broker = FakeOptionsBroker()

    class UnavailableReasoner(FakeReasoner):
        def complete(self, messages: list[dict[str, str]], **kwargs: object) -> str:
            raise FeatherlessUnavailable("NETWORK_UNAVAILABLE")

    _patch_runner(monkeypatch, broker)
    monkeypatch.setattr(runner, "FeatherlessReasoner", UnavailableReasoner)

    result = runner.run_agent_cycle("SPY")

    assert result["provider_code"] == "FEATHERLESS_NETWORK_UNAVAILABLE"
    assert result["execution_state"] == "HOLD"
    assert broker.submitted is False


def test_place_option_order_builds_native_two_leg_request() -> None:
    submitted: list[object] = []

    class FakeClient:
        def submit_order(self, request: object) -> SimpleNamespace:
            submitted.append(request)
            return SimpleNamespace(
                id="order-456",
                status="accepted",
                submitted_at="2026-01-15T12:00:00+00:00",
            )

    broker = AlpacaPaperBroker.__new__(AlpacaPaperBroker)
    broker._client = FakeClient()
    result = broker.place_option_order(
        order_class="mleg",
        order_type="limit",
        time_in_force="day",
        limit_price=Decimal("1.50"),
        legs=[
            {
                "action": "sell_to_open",
                "symbol": "SPY260116P00498000",
                "side": "sell",
                "ratio_qty": "1",
            },
            {
                "action": "buy_to_open",
                "symbol": "SPY260116P00495000",
                "side": "buy",
                "ratio_qty": "1",
            },
        ],
        qty=1,
        client_order_id="client-456",
    )

    assert result["order_id"] == "order-456"
    assert len(submitted) == 1
    request = submitted[0]
    assert request.order_class.value == "mleg"
    assert request.symbol is None
    assert len(request.legs) == 2
    assert request.legs[0].position_intent.value == "sell_to_open"
    assert request.legs[1].position_intent.value == "buy_to_open"


@pytest.mark.parametrize(
    ("kwargs", "error"),
    [
        ({"order_class": "simple"}, "ALPACA_OPTION_ORDER_PARAMETERS_UNSUPPORTED"),
        ({"order_type": "market"}, "ALPACA_OPTION_ORDER_PARAMETERS_UNSUPPORTED"),
        ({"legs": [{"action": "sell_to_open", "symbol": "SPY260116P00498000"}]}, "ALPACA_MLEG_LEGS_INVALID"),
    ],
)
def test_place_option_order_rejects_unsupported_native_shapes(
    kwargs: dict[str, object], error: str
) -> None:
    broker = AlpacaPaperBroker.__new__(AlpacaPaperBroker)

    with pytest.raises(ValueError, match=error):
        broker.place_option_order(**kwargs)
