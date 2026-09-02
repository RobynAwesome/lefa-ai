import json
import os
import urllib.error
import urllib.request

api_key = os.environ.get("FEATHERLESS_API_KEY", "").strip()
if not api_key:
    raise SystemExit("FEATHERLESS_API_KEY is required")

url = "https://api.featherless.ai/v1/chat/completions"
models = [
    "mistralai/Mistral-7B-Instruct-v0.3",
    "Qwen/Qwen2.5-7B-Instruct",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-8B",
    "mistralai/Mistral-7B-Instruct-v0.2",
]

for model in models:
    req_data = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are LEFA AI, a governed financial intelligence companion.",
            },
            {
                "role": "user",
                "content": (
                    "Explain how a governed trading companion should respond when "
                    "market evidence is incomplete. Do not invent prices or account state."
                ),
            },
        ],
        "max_tokens": 120,
        "temperature": 0.1,
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(req_data).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "LEFA-AI-Companion/1.0",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            print(f"=== MODEL: {model} ===")
            print(res["choices"][0]["message"]["content"])
    except urllib.error.HTTPError as exc:
        print(f"FAILED [{model}] HTTP {exc.code}")
    except urllib.error.URLError:
        print(f"FAILED [{model}] NETWORK_UNAVAILABLE")
