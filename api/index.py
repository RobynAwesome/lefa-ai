import sys
from pathlib import Path

# Add src to sys.path so lefa modules can be resolved
SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from lefa.web_api import app

# Export as handler for Vercel Serverless Function
handler = app
