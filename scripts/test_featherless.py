import json
import urllib.request
import os

api_key = os.environ.get("FEATHERLESS_API_KEY", "rc_895ea88f311a6126b5384f28bfc84b329ded642650ac69edbcca38cf2c95c871")
url = "https://api.featherless.ai/v1/chat/completions"

req_data = {
    "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "messages": [
        {"role": "system", "content": "You are LEFA AI, the Governed Financial Intelligence Companion for the Alpaca Hackathon."},
        {"role": "user", "content": "Explain in one clear sentence what dual-axis governance means in LEFA AI."}
    ],
    "max_tokens": 150,
    "temperature": 0.3
}

req = urllib.request.Request(
    url,
    data=json.dumps(req_data).encode("utf-8"),
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "LEFA-AI/0.1.0"
    }
)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        content = res["choices"][0]["message"]["content"]
        print("FEATHERLESS_SUCCESS:")
        print(content)
except Exception as e:
    print(f"FEATHERLESS_ERROR: {e}")
