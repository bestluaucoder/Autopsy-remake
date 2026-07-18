import requests

base = "https://offsets.imtheo.lol"
paths = [
    "/api/offsets", "/api/latest", "/api/version", "/api/raw",
    "/offsets", "/latest", "/version",
    "/api/offsets/latest", "/api/offsets/raw",
    "/api/v1/offsets", "/api/v1/latest",
]
for p in paths:
    try:
        r = requests.get(base + p, timeout=5)
        print(f"{p:30s}  {r.status_code}  {r.text[:120]}")
    except Exception as e:
        print(f"{p:30s}  ERR  {e}")
