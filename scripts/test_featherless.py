import json
import os
import urllib.error
import urllib.request

api_key = os.environ.get("FEATHERLESS_API_KEY", "").strip()
if not api_key:
    raise SystemExit("FEATHERLESS_API_KEY is required")

url = "https://api.featherless.ai/v1/chat/completions"
req_data = {
    "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "messages": [
        {
            "role": "system",
            "content": "You are LEFA AI, the Governed Financial Intelligence Companion.",
        },
        {
            "role": "user",
            "content": "Explain in one clear sentence what dual-axis governance means in LEFA AI.",
        },
    ],
    "max_tokens": 150,
    "temperature": 0.3,
}

req = urllib.request.Request(
    url,
    data=json.dumps(req_data).encode("utf-8"),
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "LEFA-AI/0.1.0",
    },
)

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        content = res["choices"][0]["message"]["content"]
        print("FEATHERLESS_SUCCESS:")
        print(content)
except urllib.error.HTTPError as exc:
    raise SystemExit(f"Featherless HTTP {exc.code}") from exc
except urllib.error.URLError as exc:
    raise SystemExit("Featherless unavailable") from exc
