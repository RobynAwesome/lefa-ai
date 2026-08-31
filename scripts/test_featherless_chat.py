import json
import urllib.request
import urllib.error

api_key = "rc_895ea88f311a6126b5384f28bfc84b329ded642650ac69edbcca38cf2c95c871"
url = "https://api.featherless.ai/v1/chat/completions"

models_to_test = [
    "meta-llama/Llama-3.3-70B-Instruct",
    "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "mistralai/Mistral-7B-Instruct-v0.2",
    "Qwen/Qwen2.5-7B-Instruct"
]

for model in models_to_test:
    req_data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are LEFA AI, the Governed Financial Intelligence Companion for the Alpaca AI Trading Agents Hackathon."},
            {"role": "user", "content": "Explain what dual-axis governance means in LEFA AI in 1 concise sentence."}
        ],
        "max_tokens": 100,
        "temperature": 0.2
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(req_data).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "LEFA-AI-Companion/1.0"
        }
    )

    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            print(f"SUCCESS [{model}]:")
            print(res["choices"][0]["message"]["content"])
            break
    except urllib.error.HTTPError as e:
        print(f"HTTP ERROR [{model}] {e.code}: {e.read().decode('utf-8', errors='ignore')}")
    except Exception as e:
        print(f"ERROR [{model}]: {e}")
