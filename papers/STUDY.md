# STUDY — From Lang (2006) to PhD: Verified Benchmark on Live Data

## Research questions
- RQ1: Does Lang's inversion theorem (2.1) hold exactly on live market windows, and does it predict Insertion/Shell cost?
- RQ2: When does Natural-Mergesort's `Θ(n log r)` beat Merge-B on live series (trend `r` small vs chop `r≈n/2`)?
- RQ3: How badly does mid-pivot Quicksort degrade on sorted live data vs Heap/Merge?
- RQ4: Do Horspool/Sunday achieve sublinear `~n/m` on live prose, and when do they collapse?
- RQ5: Does Floyd==Dijkstra hold on live-derived metric graphs (correctness cross-check)?

## Method (2026 synthesis)
Weber-10 + HOW2BENCH-55 + METI loop. Operation counts primary; wall-time secondary
with 5 reps + median. Single command reproduces everything. Live data via Stooq free
CSV + Wikipedia extracts (no key), manifest with sha256. Fallback synthetic clearly flagged.

## Hidden patterns (to turn into PhD chapter)
1. **Disorder dividend:** live trending windows have low runs `r` → Natural-Merge dividend; choppy windows erase it. Plot `inversion_vs_quick.png` shows disorder→cost slope differs per algo (Quick steep, Heap flat).
2. **Skip dividend vs entropy collapse:** Sunday/Horspool skip ∝ rarity of last-char; on `aⁿ`+`aᵐb` collapses to Θ(n·m) — verified worst-case case in suite.
3. **Sorted-data trap:** mid-pivot Quick still Θ(n²)-ish on sorted/reversed 256-arrays; Shell with Sedgewick tail stays near `n log n`.
4. **Metric shortcut:** live symmetrized graphs satisfy triangle inequality → Factor-2 TSP bound relevant (Ch.5.5) as future work.

## Threats & checklists
HOW2BENCH mapping: design (baselines included: naive+JMH-equivalent), construction (live+synthetic worst cases), evaluation (median, Wilcoxon planned, no cherry-pick — full `benchmark_results.json`), release (MIT, Docker, manifest).
Scherer METI: each qualitative claim has an explanation + a test (asserts in `run_benchmarks.py` + `pytest`).

## Next for PhD paper
Add JMH Java numbers in container, Wilcoxon signed-rank + shifted-geomean tables,
perf-counter isolation (freq pin, exclusive), larger live corpus (1M ticks), and AKS/Miller-Rabin timing (Ch.8) as crypto extension.
