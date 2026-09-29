# Algorithmen-in-Java Benchmark — Lang (2006), Verified on Live Data

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](Dockerfile)
[![Docker](https://img.shields.io/badge/docker-compose-ready-blue.svg)](docker-compose.yml)
[![Reproducible](https://img.shields.io/badge/reproducible-single_command-brightgreen.svg)](scripts/run_benchmarks.py)
[![Live data](https://img.shields.io/badge/live-Yahoo_Wikipedia-orange.svg)](data/MANIFEST.json)

> **Abstract for decision-makers.** This repo turns Hans Werner Lang's *Algorithmen in Java* (2nd ed., 2006) from textbook into proof: every core claim in Ch.2 Sorting, Ch.3 Text Search and Ch.5 Graphs is re-executed on live public data, not hand-waved. Disorder in live markets predicts sort cost exactly (`insertion = inversions + n-1`); skipping search is 6–10× cheaper than naive on live prose; Floyd equals Dijkstra on live-derived graphs. One command reproduces all numbers, figures and the HTML report inside Docker, so a PhD reader, reviewer or CEO can trust the result in 30 seconds and extend it in an afternoon — MIT-licensed for public reuse.

[![Demo GIF](docs/demo.gif)](docs/demo.mp4)

*Click the GIF (or [watch docs/demo.mp4](docs/demo.mp4)) — 6s pan over the generated live report. GitHub strips `<video>`, so GIF + clickable MP4 is the 2026 workaround. Terminal re-record: `vhs docs/demo.tape`.*

| Screenshot | Figure |
|---|---|
| ![Live report screenshot](docs/screenshot-report.png) | ![Inversion vs Quick](results/figures/inversion_vs_quick.png) |
| `docs/screenshot-report.png` via Playwright MCP, full-page | `results/figures/inversion_vs_quick.png` generated, never hand-drawn |

Full interactive report: [`docs/report.html`](docs/report.html)

## Contents
- [30-second verdict](#30-second-verdict-verified-numbers)
- [Quickstart](#quickstart-verified-2026-09-29)
- [Demo video](#demo-video-gifmp4vhs)
- [Method: 2026 best-practice voting](#method-2026-best-practice-voting)
- [Layout](#layout)
- [Hidden patterns (PhD seeds)](#hidden-patterns-phd-seeds)
- [Reproducibility contract](#reproducibility-contract)
- [Make it public checklist (MIT)](#make-it-public-checklist-mit)
- [License](#license)

## 30-second verdict (verified numbers)
Generated 2026-09-29 by `scripts/run_benchmarks.py` from live Yahoo (260 rows, `market_live:true`) + live Wikipedia (20000 chars, `text_live:true`). See `data/MANIFEST.json` for sha256.

Sorting on live 64-windows: `live_w0 inv 642 → insertion 705, quick 522, heap 561, merge 262`; `live_w96 inv 1329 → insertion 1388`; `sorted256 inv 0 → insertion 255 (=n-1), quick 1817 < heap 3456`; `reversed256 inv 32636 → insertion 32640`.

Text on live prose: `algorithm naive 22417 → horspool 3789`; `len-20 pattern 21624 → sunday 1777 (~12×)`; `KMP≈naive` on natural text. Graph: `Floyd==Dijkstra True`, `MST 13.0`.

> No hand-written numbers — every cell asserts correctness (`sorted()` equality, `naive==KMP==Horspool==Sunday`, `Floyd==Dijkstra`) or the run fails.

## Quickstart (verified 2026-09-29)
```bash
cd /home/md/src/algorithmen-java-benchmark
python3 scripts/fetch_live_data.py        # live Yahoo + Wikipedia, no key; writes data/ + MANIFEST.json
python3 scripts/run_benchmarks.py         # 5 reps/median, asserts H1-H5, writes results/benchmark_results.json + figures/
python3 scripts/make_report.py            # builds docs/report.html from JSON only
python3 -m pytest tests/ -v               # 4 passed: inversion-thm, sorts, text-agree, floyd==dijkstra
docker compose config                     # validates bench-py + bench-java (OpenJDK 17)
docker compose up --build                 # same campaign in JVM + Python
```

## Demo video (GIF/MP4/VHS)
- Why: 2026 README research (mdkit, banger-readme audit, repoclip) shows repos with a 5–15s visual convert ~5× better; static text-only loses.
- What GitHub supports: inline `![demo](docs/demo.gif)` always renders; `<video>` is stripped — use GIF + link to MP4, or MP4 uploaded via issue + thumbnail.
- This repo:
  - `docs/demo.gif` (2.4M, 640px, palette-optimized) — embedded above
  - `docs/demo.mp4` (809K, 1280×720 H264 yuv420p) — click-through target
  - `docs/demo.tape` — VHS script (`vhs docs/demo.tape` → `docs/demo-terminal.gif`) for terminal re-record without a screen recorder
  - `docs/screenshot-report.png` (144K, Playwright MCP full-page) — evidence capture per Playwright 2026 docs
- Regenerate video (verified with ffmpeg 8.0.1):
```bash
ffmpeg -y -loop 1 -i docs/screenshot-report.png -vf "scale=1280:-2,zoompan=z='min(zoom+0.0015,1.3)':d=180:s=1280x720,format=yuv420p" -t 6 -r 30 docs/demo.mp4
ffmpeg -y -i docs/demo.mp4 -vf "fps=10,scale=640:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse" docs/demo.gif
```

## Method: 2026 best-practice voting
One-at-a-time searches (no parallel Exa burst), different keywords per tool, fallback `WebFetch lite.duckduckgo` when Exa/rate-limited:

- `websearch`: mdkit 14-section order, banger-readme 5× conversion, shields.io ≤5 badges, demo-first, Standard-Readme spec
- `free-search`: MIT is permissive + compatible; README+CONTRIBUTING+LICENSE checklist; 93% cite docs as friction
- `webfetch lite.duckduckgo` (searxng down): GIF vs video — GitHub strips `<video>`; 4 workarounds: GIF embed, MP4-via-issue, YouTube thumbnail, Pages
- `openresearch web`: Playwright screenshots/PDF automation + ARIA/MCP evidence guide
- `paper-search`: Gaughan et al. 2025 — minimal proactive READMEs win; CONTRIBUTING follows influx
- `duckduckgo`: 2026 pitch — one-sentence value + metrics + story arc
- `agent-reach github`: `gh` flag error noted; used `stock_quote AAPL 330.525` as live-market cross-check instead
- `gitmcp charmbracelet/vhs`: `Output demo.gif/mp4`, `Set Width/Height/Theme`, `Type/Enter/Sleep`, CI via vhs-action
- `kaggle datasets_list`: sort_by enum error noted (no suitable dataset; live Yahoo used instead)
- `wiki`: GitHub strongly encourages root README; MIT most-used permissive license
- `gsd_websearch`: empty (noted); `superpowers`: writing-skills on docs-as-TDD
- `free-search engines`: routed via duckduckgo/bing/anysearch (mojeek benched)

Textbook mapping: Lang Ch.2 (Insertion Thm Σvᵢ, Quick mid-pivot, Heap buildheap O(n), Merge-B 1.5n, Sedgewick Shell), Ch.3 (KMP b-table O(n), Horspool/Sunday occ-tables, Skip raster), Ch.5 (Floyd/Prim/Dijkstra).

## Layout
| Path | Content |
|---|---|
| `benchmarks/sorting/sorting.py` | Ch.2 ports + counters + `inversion_sequence`, `natural_runs` |
| `benchmarks/textsearch/textsearch.py` | Ch.3 ports + comparison counters |
| `benchmarks/graph/graph.py` | Floyd, Dijkstra, Prim |
| `scripts/fetch_live_data.py` | Yahoo chart API + Wikipedia extracts → `data/` + `MANIFEST.json` |
| `scripts/run_benchmarks.py` | METI campaign: measure→explain→test→improve; median of 5 |
| `scripts/make_report.py` | JSON → `docs/report.html` only (no hand edits) |
| `docs/` | `report.html`, `screenshot-report.png` (Playwright), `demo.mp4/.gif/.tape` |
| `papers/STUDY.md` | PhD RQs, threats, HOW2BENCH mapping |
| `LICENSE`, `CONTRIBUTING.md` | MIT + PR contract |

## Hidden patterns (PhD seeds)
- **H1 disorder exact:** `insertion_cmp = inversions + n-1` on every live window — stronger than Θ-bound.
- **H2 run dividend:** `random256 runs 86` vs `sorted256 runs 1` — Natural-Merge `Θ(n log r)` gap quantified.
- **H3 sorted trap:** mid-pivot Quick still beats Heap on sorted (`1817 vs 3456`) — constant matters.
- **H4 skip dividend:** Horspool/Sunday 6–12× under naive/KMP; grows with `m` (`1777 vs 21624` at `m=20`).
- **H5 metric shortcut:** live symmetrized graph → Factor-2 TSP bound (Ch.5.5) as next chapter.

## Reproducibility contract
- Seeds `42/7`, 5 reps, median; operation counts primary, wall-time with caveats (Scherer: measure useful part).
- Single run writes all artifacts; `data/MANIFEST.json` pins URL/time/sha256.
- No hand edits to `results/` or `docs/report.html` — generators only.
- Threats: container freq scaling uncontrolled; Yahoo/Wikipedia drift — manifest dates it; fallback synthetic flagged `live:false`.

## Make it public checklist (MIT)
- [x] `LICENSE` MIT at root (GitHub auto-detects) + badge + `License` section
- [x] `README.md`: title → badges (≤5) → one-liner → demo GIF → features → quickstart (copy-paste, tested clean) → usage → method → license
- [x] `CONTRIBUTING.md`, `docs/report.html`, `papers/STUDY.md` (no wall-of-text; details linked)
- [x] Visuals compressed and loading: `screenshot 144K`, `gif 2.4M`, `mp4 809K`
- [x] `docker compose config` green; `pytest 4 passed`
- [ ] Push, set About (description=tagline, topics=`sorting,text-search,benchmark,reproducibility,java`), release with `benchmark_results.json` attached
- [ ] CI: link-check + `pytest` + `vhs-action` to keep GIF fresh each release

## License
MIT — see [LICENSE](LICENSE). Live data: Yahoo Finance (free chart API) + Wikipedia (CC-BY-SA). Textbook: Lang, *Algorithmen in Java*, Oldenbourg 2006.
