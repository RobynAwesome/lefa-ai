from fastapi import HTTPException

from lefa.vercel_app import app, snapshot_payload


def test_vercel_app_exposes_governed_fixture_projection() -> None:
    assert app.title.startswith("LEFA AI")
    payload = snapshot_payload("spy")
    assert payload["market"]["symbol"] == "SPY"
    assert payload["mode"] == "fixture"
    assert payload["execution_authority"] == "zero"
    assert payload["market"]["latest_price"] is None


def test_vercel_app_rejects_invalid_symbol() -> None:
    try:
        snapshot_payload("SPY<script>")
    except HTTPException as exc:
        assert exc.status_code == 400
    else:
        raise AssertionError("invalid symbols must fail closed")
