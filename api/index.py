import sys
from pathlib import Path

# Add src to sys.path so lefa modules can be resolved
SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from lefa.bridge_api import router as bridge_router
from lefa.web_api import app

# Keep the engineering MCP proof routes in lefa.web_api while exposing a separate
# human-facing bridge projection for the browser.
app.include_router(bridge_router)

# Export as handler for Vercel Serverless Function
handler = app
