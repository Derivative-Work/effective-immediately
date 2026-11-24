"""Fetch NVDA's real bars from Alpaca's market-data API for the boardroom screen's line (read-only: no orders).

No longer used for the video: Alpaca's terms forbid displaying its data publicly. scripts/fetch_databento.py replaced it
(decisions 28).

The key is read at run time from the file the human named and is never written, logged or printed. Raw bars go to
assets/market/ (git-ignored); scripts/market_lines.py derives the on-screen shapes from them.
Usage: .venv/bin/python -I scripts/fetch_market.py [path/to/price-title.env]
"""
import datetime as dt
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

URL = "https://data.alpaca.markets/v2/stocks/bars"
OUT = Path("assets/market")
START, END = "2026-11-10T00:00:00Z", "2026-11-24T01:00:00Z"


def load_env(path):
    env = {}
    for line in Path(path).expanduser().read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.removeprefix("export ").strip()] = v.strip().strip("'\"")
    return env


def get(env, timeframe, feed):
    bars, token = [], None
    end = min(dt.datetime.fromisoformat(END.replace("Z", "+00:00")), dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=16))
    while True:
        q = {"symbols": "NVDA", "timeframe": timeframe, "start": START, "end": end.strftime("%Y-%m-%dT%H:%M:%SZ"), "adjustment": "split", "feed": feed, "limit": 10000, "sort": "asc"}
        if token:
            q["page_token"] = token
        req = urllib.request.Request(f"{URL}?{urllib.parse.urlencode(q)}", headers={"APCA-API-KEY-ID": env["ALPACA_KEY_ID"], "APCA-API-SECRET-KEY": env["ALPACA_SECRET_KEY"], "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=40) as r:
            d = json.load(r)
        bars += (d.get("bars") or {}).get("NVDA", [])
        token = d.get("next_page_token")
        if not token:
            return bars


def main():
    env = load_env(sys.argv[1] if len(sys.argv) > 1 else "~/Documents/price-title.env")
    OUT.mkdir(parents=True, exist_ok=True)
    feeds = ["sip", env.get("ALPACA_FEED", "iex")]
    for feed in dict.fromkeys(feeds):
        try:
            minute, day = get(env, "1Min", feed), get(env, "1Day", feed)
        except urllib.error.HTTPError as e:
            print(f"feed {feed}: HTTP {e.code}")
            continue
        (OUT / "nvda_bars.json").write_text(json.dumps({"symbol": "NVDA", "feed": feed, "adjustment": "split", "start": START, "fetched": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "day": day, "minute": minute}) + "\n")
        print(f"feed {feed}: {len(minute)} minute bars, {len(day)} daily bars")
        return
    raise SystemExit("no feed returned data")


if __name__ == "__main__":
    main()
