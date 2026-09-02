import json
import os
import urllib.error
import urllib.request

api_key = os.environ.get("FEATHERLESS_API_KEY", "").strip()
if not api_key:
    raise SystemExit("FEATHERLESS_API_KEY is required")

url = "https://api.featherless.ai/v1/models"
req = urllib.request.Request(
    url,
    headers={
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "User-Agent": "LEFA-AI/0.1.0",
    },
)

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        print("STATUS:", resp.status)
        res = json.loads(resp.read().decode("utf-8"))
        print("MODELS COUNT:", len(res.get("data", [])))
        if res.get("data"):
            print("FIRST 5 MODELS:", [m["id"] for m in res["data"][:5]])
except urllib.error.HTTPError as exc:
    raise SystemExit(f"Featherless HTTP {exc.code}") from exc
except urllib.error.URLError as exc:
    raise SystemExit("Featherless unavailable") from exc
