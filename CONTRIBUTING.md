# Contributing
Fork → branch → PR. All numbers must be generated, never hand-written.
`python3 scripts/fetch_live_data.py && python3 scripts/run_benchmarks.py && python3 -m pytest tests/ -v`
must pass before any PR. Update `docs/report.html` via `scripts/make_report.py`.
