"""Build docs/report.html from verified results/benchmark_results.json (no hand numbers)."""
from __future__ import annotations
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
RES = json.loads((ROOT/"results"/"benchmark_results.json").read_text())
OUT = ROOT/"docs"/"report.html"
OUT.parent.mkdir(exist_ok=True)
rows_sort = []
for k,v in RES["sort"].items():
    rows_sort.append(f"<tr><td>{k}</td><td>{v['n']}</td><td>{v['inversions']}</td><td>{v['runs']}</td><td>{int(v['algos']['quick']['comparisons'])}</td><td>{int(v['algos']['heap']['comparisons'])}</td><td>{int(v['algos']['merge_b']['comparisons'])}</td></tr>")
rows_text = []
for p,v in RES["text"]["cases"].items():
    rows_text.append(f"<tr><td>{p}</td><td>{v['hits']}</td><td>{v['naive_cmp']}</td><td>{v['kmp_cmp']}</td><td>{v['horspool_cmp']}</td><td>{v['sunday_cmp']}</td></tr>")
html = f"""<!doctype html><html><head><meta charset='utf-8'>
<title>Algorithmen-in-Java Benchmark — Live Report</title>
<style>body{{font-family:system-ui,Arial,sans-serif;max-width:960px;margin:32px auto;padding:0 16px}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ccc;padding:6px 8px;font-size:14px}}th{{background:#f5f5f5}}.hero{{background:#0b1020;color:#fff;padding:28px;border-radius:12px}}</style>
</head><body>
<div class='hero'><h1>Algorithmen in Java — Verified Live Benchmark</h1>
<p>Lang (2006) Ch.2/3/5 reproduced end-to-end on live Yahoo Finance + Wikipedia. All numbers generated, never hand-written.</p>
<p>Text: {RES["text"]["text_len"]} chars live &nbsp;|&nbsp; Graph Floyd==Dijkstra: {RES["graph"]["floyd_eq_dijkstra"]} &nbsp;|&nbsp; MST: {RES["graph"]["mst_weight"]}</p></div>
<h2>Sorting on live windows — disorder predicts cost (H1–H3)</h2>
<table><tr><th>window</th><th>n</th><th>inversions</th><th>runs</th><th>quick cmp</th><th>heap cmp</th><th>merge cmp</th></tr>{''.join(rows_sort)}</table>
<h2>Text search on live prose — skip dividend (H4)</h2>
<table><tr><th>pattern</th><th>hits</th><th>naive</th><th>KMP</th><th>Horspool</th><th>Sunday</th></tr>{''.join(rows_text)}</table>
<h2>Figure</h2><img src='../results/figures/inversion_vs_quick.png' style='max-width:100%' alt='inversion vs quick'>
<p><small>Generated from results/benchmark_results.json. Reproduce: python3 scripts/fetch_live_data.py && python3 scripts/run_benchmarks.py && python3 scripts/make_report.py</small></p>
</body></html>"""
OUT.write_text(html)
print(f"WROTE {OUT} ({len(html)} bytes)")
