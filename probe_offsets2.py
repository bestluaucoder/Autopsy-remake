import requests, re

r = requests.get("https://offsets.imtheo.lol/", timeout=10)
# Look for JS bundle paths or data endpoints in the HTML
scripts = re.findall(r'src="([^"]+\.js[^"]*)"', r.text)
print("Scripts:", scripts[:10])

# Try common JS bundle paths that might contain offset data
for s in scripts[:5]:
    url = "https://offsets.imtheo.lol" + s if s.startswith("/") else s
    try:
        jr = requests.get(url, timeout=8)
        # Search for offset-looking hex values
        hexes = re.findall(r'0x[0-9a-fA-F]{2,4}', jr.text)
        if len(hexes) > 20:
            print(f"\nFound {len(hexes)} hex values in {url[:80]}")
            print("Sample:", hexes[:10])
    except: pass

# Try /assets or /data paths
for p in ["/offsets.json", "/data/offsets.json", "/assets/offsets.json",
          "/api/offsets.json", "/offsets.cpp", "/offsets.h"]:
    try:
        rr = requests.get("https://offsets.imtheo.lol" + p, timeout=5)
        if rr.status_code == 200:
            print(f"\nHIT: {p}")
            print(rr.text[:300])
    except: pass
