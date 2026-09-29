"""Fetch LIVE public data (no API key): Stooq market quotes + Wikipedia text.

Writes data/live_market.csv, data/live_text.txt, data/MANIFEST.json with sha256.
Fallbacks to synthetic deterministic data if offline (marked clearly).
"""
from __future__ import annotations
import csv, hashlib, json, time, urllib.request, pathlib, random

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

SYMBOLS = ["AAPL", "MSFT", "NVDA", "SPY"]
YAHOO_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d&range=3mo"
WIKI_URL = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&format=json&titles=Algorithm"


def sha256_file(p):
    h = hashlib.sha256()
    h.update(pathlib.Path(p).read_bytes())
    return h.hexdigest()


def fetch_market():
    rows = []
    try:
        for sym in SYMBOLS:
            url = YAHOO_URL.format(sym=sym)
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (algo-bench/1.0)"})
            with urllib.request.urlopen(req, timeout=15) as r:
                j = json.loads(r.read().decode("utf-8"))
            res = j["chart"]["result"][0]
            closes = res["indicators"]["quote"][0]["close"]
            ts = res["timestamp"]
            for t_, c in zip(ts, closes):
                if c is None:
                    continue
                rows.append({"Symbol": sym, "Date": t_, "Close": f"{c:.2f}", "Volume": "0"})
        if not rows:
            raise RuntimeError("empty yahoo response")
        live = True
    except Exception as e:
        print(f"[fetch] market live failed ({e}), using synthetic fallback")
        rnd = random.Random(42)
        base = 100.0
        for s in SYMBOLS:
            for k in range(60):
                base += rnd.uniform(-2, 2)
                rows.append({"Symbol": s, "Close": f"{base:.2f}", "Volume": "1000000"})
        live = False
    out = DATA / "live_market.csv"
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    return out, live, len(rows)


def fetch_text():
    try:
        req = urllib.request.Request(WIKI_URL, headers={"User-Agent": "algo-bench/1.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            j = json.loads(r.read().decode("utf-8"))
        pages = j["query"]["pages"]
        txt = next(iter(pages.values()))["extract"]
        live = True
    except Exception as e:
        print(f"[fetch] text live failed ({e}), synthetic fallback")
        txt = ("quicksort heapsort mergesort " * 500) + "algorithm benchmark live verification "
        live = False
    out = DATA / "live_text.txt"
    out.write_text(txt, encoding="utf-8")
    return out, live, len(txt)


def main():
    t0 = time.time()
    mkt, mkt_live, mkt_n = fetch_market()
    txt, txt_live, txt_n = fetch_text()
    manifest = {
        "fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "market_file": str(mkt.name), "market_live": mkt_live, "market_rows": mkt_n,
        "market_sha256": sha256_file(mkt),
        "text_file": str(txt.name), "text_live": txt_live, "text_chars": txt_n,
        "text_sha256": sha256_file(txt),
        "elapsed_s": round(time.time() - t0, 2),
    }
    (DATA / "MANIFEST.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
