from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from lefa.presentation import snapshot_to_ui_view
from lefa.providers import FixtureProvider

PROJECT_ROOT = Path(__file__).resolve().parents[2]
UI_ROOT = PROJECT_ROOT / "ui"
ASSET_ROOT = PROJECT_ROOT / "assets"
PROVIDER = FixtureProvider()

app = FastAPI(
    title="LEFA AI — Governed Financial Intelligence",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)
app.mount("/assets", StaticFiles(directory=ASSET_ROOT), name="assets")


def _validated_symbol(symbol: str) -> str:
    normalized = symbol.strip().upper()
    if not normalized or len(normalized) > 16:
        raise HTTPException(status_code=400, detail="invalid symbol")
    if not all(char.isalnum() or char in ".-" for char in normalized):
        raise HTTPException(status_code=400, detail="invalid symbol")
    return normalized


def snapshot_payload(symbol: str = "SPY") -> dict[str, object]:
    normalized = _validated_symbol(symbol)
    view = snapshot_to_ui_view(PROVIDER.snapshot(normalized))
    return view.model_dump(mode="json")


@app.get("/api/snapshot")
def snapshot(symbol: str = Query(default="SPY", max_length=16)) -> dict[str, object]:
    """Expose only the governed UI projection; no broker credentials or order authority."""

    return snapshot_payload(symbol)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {
        "status": "ok",
        "provider": PROVIDER.name,
        "execution_authority": "zero",
        "runtime": "vercel",
    }


@app.get("/lefa.css", include_in_schema=False)
def stylesheet() -> FileResponse:
    return FileResponse(UI_ROOT / "lefa.css", media_type="text/css")


@app.get("/lefa.js", include_in_schema=False)
def javascript() -> FileResponse:
    return FileResponse(UI_ROOT / "lefa.js", media_type="text/javascript")


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(UI_ROOT / "index.html", media_type="text/html")
