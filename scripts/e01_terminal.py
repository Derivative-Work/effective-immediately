"""E01's terminal: real nvidia-smi output caught during a heavy stage, then scripts/effective-immediately run for real.

- nvidia-smi: assets/captures/nvidia_smi/postfilter/ holds 58 captures taken every 0.4 s while the music-deslop
  postfilter re-ran on the locked master (production log 18; its output matched the master's postfilter byte for byte).
  The one shown is the first at the run's peak power. It is typeset as captured, trailing spaces trimmed.
- The script is run here and its output checked, so the terminal shows what it really prints.
Writes remotion/public/gen/captures/terminal.json.
Usage: .venv/bin/python -I scripts/e01_terminal.py
"""
import json
import re
import subprocess
from pathlib import Path

CAPS = sorted(Path("assets/captures/nvidia_smi/postfilter").glob("nvidia-smi_*.txt"))
SCRIPT = "scripts/effective-immediately"


def reading(path):
    t = path.read_text()
    util = int(re.search(r"(\d+)%\s+Default", t).group(1))
    watts = int(re.search(r"(\d+)W /\s+\d+W", t).group(1))
    return util, watts


def main():
    best = max(CAPS, key=lambda p: (reading(p), -CAPS.index(p)))
    util, watts = reading(best)
    lines = [ln.rstrip() for ln in best.read_text().splitlines()]
    out = subprocess.run([SCRIPT], capture_output=True, text=True, check=True).stdout.splitlines()
    assert out == ["Effective Immediately", "AI-generated satire", "Not investment advice", "generating..."], out
    Path("remotion/public/gen/captures").mkdir(parents=True, exist_ok=True)
    Path("remotion/public/gen/captures/terminal.json").write_text(json.dumps(
        {"smi": lines, "smi_source": str(best), "script": SCRIPT, "script_out": out}, indent=1) + "\n")
    print(f"{best.name}: {util}% at {watts} W, {len(lines)} lines; script prints {out}")


if __name__ == "__main__":
    main()
