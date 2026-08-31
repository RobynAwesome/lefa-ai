import json
import urllib.request
import urllib.error

api_key = "rc_895ea88f311a6126b5384f28bfc84b329ded642650ac69edbcca38cf2c95c871"
url = "https://api.featherless.ai/v1/models"

req = urllib.request.Request(
    url,
    headers={
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
)

try:
    with urllib.request.urlopen(req) as resp:
        print("STATUS:", resp.status)
        res = json.loads(resp.read().decode("utf-8"))
        print("MODELS COUNT:", len(res.get("data", [])))
        if res.get("data"):
            print("FIRST 5 MODELS:", [m["id"] for m in res["data"][:5]])
except urllib.error.HTTPError as e:
    print(f"HTTP ERROR {e.code}: {e.reason}")
    print("BODY:", e.read().decode("utf-8", errors="ignore"))
except Exception as e:
    print(f"ERROR: {e}")
