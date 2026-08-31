import json
import urllib.request
import urllib.error

api_key = "rc_895ea88f311a6126b5384f28bfc84b329ded642650ac69edbcca38cf2c95c871"
url = "https://api.featherless.ai/v1/chat/completions"

models = [
    "mistralai/Mistral-7B-Instruct-v0.3",
    "Qwen/Qwen2.5-7B-Instruct",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-8B",
    "mistralai/Mistral-7B-Instruct-v0.2"
]

for model in models:
    req_data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are LEFA AI, the Governed Financial Intelligence Companion for the Alpaca Hackathon. You explain market observations and governed risk evaluations."},
            {"role": "user", "content": "SPY is at 598.50. Risk policy allows max 2% allocation. Should we buy, hold, or observe? Explain in 2 sentences."}
        ],
        "max_tokens": 120,
        "temperature": 0.1
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
            print(f"=== MODEL: {model} ===")
            print(res["choices"][0]["message"]["content"])
    except urllib.error.HTTPError as e:
        print(f"FAILED [{model}]: {e.read().decode('utf-8', errors='ignore')}")
    except Exception as e:
        print(f"ERROR [{model}]: {e}")
