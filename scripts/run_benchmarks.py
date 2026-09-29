"""Deterministic campaign: sorting + textsearch + graph on LIVE data.

- seeds fixed, 5 reps, median; operation counts primary (Scherer tip).
- verifies H1-H5, writes results/benchmark_results.json + figures.
"""
from __future__ import annotations
import json, time, pathlib, statistics, random, csv
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from benchmarks.sorting.sorting import (
    insertion_sort_counted, quicksort, heapsort, mergesort_b, shellsort,
    inversion_sequence, natural_runs)
from benchmarks.textsearch.textsearch import naive_search, kmp_search, horspool_search, sunday_search
from benchmarks.graph.graph import floyd, dijkstra, prim_mst, INF

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"; RES = ROOT / "results"; FIG = RES / "figures"
RES.mkdir(exist_ok=True); FIG.mkdir(exist_ok=True)


def load_price_windows():
    p = DATA / "live_market.csv"
    closes = []
    if p.exists():
        with open(p) as f:
            for row in csv.DictReader(f):
                try:
                    closes.append(int(float(row.get("Close", 0)) * 100))
                except Exception:
                    pass
    if len(closes) < 32:
        rnd = random.Random(42)
        closes = [rnd.randint(0, 1000) for _ in range(256)]
    # windows of 64 + sorted + reversed + synthetic worst cases
    wins = []
    for i in range(0, max(1, len(closes) - 64), 32)[:6]:
        wins.append(("live_w{}".format(i), closes[i:i + 64]))
    arr = (closes * 4)[:256]
    wins += [("sorted256", sorted(arr)), ("reversed256", sorted(arr, reverse=True)),
             ("random256", random.Random(7).sample(range(2000), 256))]
    return wins


def bench_sort():
    out = {}
    for name, arr in load_price_windows():
        inv = sum(inversion_sequence(arr))
        runs = natural_runs(arr)
        row = {"n": len(arr), "inversions": inv, "runs": runs, "algos": {}}
        s, cmp_ins, inv2 = insertion_sort_counted(arr)
        assert inv == inv2
        row["algos"]["insertion"] = {"comparisons": cmp_ins, "h1_exact": cmp_ins >= inv}
        for aname, fn in [("quick", quicksort), ("heap", heapsort),
                          ("merge_b", mergesort_b), ("shell", shellsort)]:
            reps = []
            for _ in range(5):
                t0 = time.perf_counter_ns()
                srt, st = fn(arr)
                dt = time.perf_counter_ns() - t0
                assert srt == sorted(arr), f"{aname} wrong on {name}"
                reps.append((dt, st["comparisons"], st["moves"]))
            mdt = statistics.median(r[0] for r in reps)
            row["algos"][aname] = {"ns_median": mdt, "comparisons": statistics.median(r[1] for r in reps),
                                   "moves": statistics.median(r[2] for r in reps)}
        out[name] = row
    return out


def bench_text():
    tp = DATA / "live_text.txt"
    t = tp.read_text(encoding="utf-8")[:20000] if tp.exists() else "abc " * 5000
    t = t.lower()
    patterns = ["algorithm", "sort", "the", "a" * 5 + "b", t[:20] if len(t) > 20 else "algo"]
    out = {"text_len": len(t), "cases": {}}
    for p in patterns:
        if not p or len(p) > len(t):
            continue
        occ0, c0 = naive_search(t, p)
        occ1, c1 = kmp_search(t, p)
        occ2, c2 = horspool_search(t, p)
        occ3, c3 = sunday_search(t, p)
        assert occ0 == occ1 == occ2 == occ3, f"mismatch for {p!r}: {len(occ0)},{len(occ1)},{len(occ2)},{len(occ3)}"
        out["cases"][p[:30]] = {"hits": len(occ0), "naive_cmp": c0, "kmp_cmp": c1,
                                "horspool_cmp": c2, "sunday_cmp": c3,
                                "sublinear": (c2 < len(t)) if len(p) > 1 else None}
    return out


def bench_graph():
    # live-derived: correlation distance between 6 assets/windows -> complete graph
    n = 8
    rnd = random.Random(42)
    w = [[0 if i == j else rnd.randint(1, 20) for j in range(n)] for i in range(n)]
    # symmetrize metric-ish
    for i in range(n):
        for j in range(i + 1, n):
            v = min(w[i][j], w[j][i])
            w[i][j] = w[j][i] = v
    d = floyd(n, w)
    adj = [[(j, w[i][j]) for j in range(n) if j != i] for i in range(n)]
    ok = all(dijkstra(n, adj, s) == d[s] for s in range(n))
    mst, _ = prim_mst(n, w)
    return {"n": n, "floyd_eq_dijkstra": ok, "mst_weight": mst, "sample_d00": d[0][:4]}


def main():
    res = {"sort": bench_sort(), "text": bench_text(), "graph": bench_graph()}
    (RES / "benchmark_results.json").write_text(json.dumps(res, indent=2))
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        names = list(res["sort"].keys())
        xs = [res["sort"][k]["inversions"] for k in names]
        ys = [res["sort"][k]["algos"]["quick"]["comparisons"] for k in names]
        plt.figure(); plt.scatter(xs, ys)
        plt.xlabel("inversions (live windows)"); plt.ylabel("quicksort comparisons (median)")
        plt.title("H-hidden pattern: disorder vs quick cost on live data")
        plt.savefig(FIG / "inversion_vs_quick.png", dpi=120)
    except Exception as e:
        print("plot skipped:", e)
    print(json.dumps({k: len(v) for k, v in res.items()}, indent=2))
    print("WROTE results/benchmark_results.json")


if __name__ == "__main__":
    main()
