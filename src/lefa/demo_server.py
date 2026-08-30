from __future__ import annotations

import argparse
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from lefa.presentation import snapshot_to_ui_view
from lefa.providers import FixtureProvider

PROJECT_ROOT = Path(__file__).resolve().parents[2]
UI_ROOT = PROJECT_ROOT / "ui"
ASSET_ROOT = PROJECT_ROOT / "assets"


class LEFADemoHandler(BaseHTTPRequestHandler):
    provider = FixtureProvider()

    def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        parsed = urlparse(self.path)
        if parsed.path == "/api/snapshot":
            self._serve_snapshot(parsed.query)
            return

        if parsed.path == "/":
            self._serve_file(UI_ROOT / "index.html", "text/html; charset=utf-8")
            return

        ui_files = {
            "/lefa.css": (UI_ROOT / "lefa.css", "text/css; charset=utf-8"),
            "/lefa.js": (UI_ROOT / "lefa.js", "text/javascript; charset=utf-8"),
        }
        if parsed.path in ui_files:
            path, content_type = ui_files[parsed.path]
            self._serve_file(path, content_type)
            return

        companion_path = "/assets/companion/lefa-companion-root.svg"
        if parsed.path == companion_path:
            self._serve_file(
                ASSET_ROOT / "companion" / "lefa-companion-root.svg",
                "image/svg+xml; charset=utf-8",
            )
            return

        self.send_error(HTTPStatus.NOT_FOUND)

    def _serve_snapshot(self, query: str) -> None:
        symbol = parse_qs(query).get("symbol", ["SPY"])[0].strip().upper()
        if not symbol or len(symbol) > 16 or not all(char.isalnum() or char in ".-" for char in symbol):
            self.send_error(HTTPStatus.BAD_REQUEST, "invalid symbol")
            return

        view = snapshot_to_ui_view(self.provider.snapshot(symbol))
        payload = json.dumps(view.model_dump(mode="json"), separators=(",", ":")).encode()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _serve_file(self, path: Path, content_type: str) -> None:
        try:
            payload = path.read_bytes()
        except FileNotFoundError:
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the governed LEFA interface POC")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), LEFADemoHandler)
    print(f"LEFA governed interface: http://{args.host}:{args.port}")
    print("Provider: FixtureProvider (non-live). Execution authority: ZERO.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
