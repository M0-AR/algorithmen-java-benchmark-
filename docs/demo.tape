# VHS terminal demo — regenerate GIF without screen recorder (2026 best practice)
# Requires: vhs + ttyd + ffmpeg. Run: vhs docs/demo.tape  (outputs docs/demo-terminal.gif)
Output docs/demo-terminal.gif
Set Width 1100
Set Height 620
Set FontSize 18
Set Theme "Catppuccin Frappe"
Type "cd /home/md/src/algorithmen-java-benchmark && python3 scripts/run_benchmarks.py"
Enter
Sleep 3s
Type "python3 -m pytest tests/ -v"
Enter
Sleep 3s
