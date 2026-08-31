import json
import urllib.request

api_key = "rc_895ea88f311a6126b5384f28bfc84b329ded642650ac69edbcca38cf2c95c871"
url = "https://api.featherless.ai/v1/models"

req = urllib.request.Request(
    url,
    headers={
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }
)

with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode("utf-8"))
    models = [m["id"] for m in res.get("data", [])]

qwen_models = [m for m in models if "qwen2.5" in m.lower() and "instruct" in m.lower()][:10]
mistral_models = [m for m in models if "mistral" in m.lower() and "instruct" in m.lower()][:10]
deepseek_models = [m for m in models if "deepseek" in m.lower()][:10]

print("QWEN MODELS:", qwen_models)
print("MISTRAL MODELS:", mistral_models)
print("DEEPSEEK MODELS:", deepseek_models)
