import json
import os
import urllib.error
import urllib.request

api_key = os.environ.get("FEATHERLESS_API_KEY", "").strip()
if not api_key:
    raise SystemExit("FEATHERLESS_API_KEY is required")

url = "https://api.featherless.ai/v1/chat/completions"
models_to_test = [
    "meta-llama/Llama-3.3-70B-Instruct",
    "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "mistralai/Mistral-7B-Instruct-v0.2",
    "Qwen/Qwen2.5-7B-Instruct",
]

for model in models_to_test:
    req_data = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are LEFA AI, the Governed Financial Intelligence Companion.",
            },
            {
                "role": "user",
                "content": "Explain dual-axis governance in LEFA AI in one concise sentence.",
            },
        ],
        "max_tokens": 100,
        "temperature": 0.2,
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
            print(f"SUCCESS [{model}]:")
            print(res["choices"][0]["message"]["content"])
            break
    except urllib.error.HTTPError as exc:
        print(f"HTTP ERROR [{model}] {exc.code}")
    except urllib.error.URLError:
        print(f"NETWORK ERROR [{model}]")
