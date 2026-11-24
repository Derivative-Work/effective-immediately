"""Fetch NVDA's bars from Databento's US Equities Mini dataset (EQUS.MINI) for the boardroom screen (decisions 28).

Databento's user agreement (s1.6) requires crediting it wherever the data is published ("Data provided by Databento").
The key is read at run time from the file the human named, sent only to hist.databento.com, and never written, logged
or printed.
- `probe` (free): the dataset's schemas, its available range, and Databento's cost estimate for each planned request.
- `fetch`: the same estimate, then the download, only if the total is under MAX_COST. Raw bars go to assets/market/
  (git-ignored) in the same shape as nvda_bars.json, so scripts/market_lines.py can read either.
Usage: .venv/bin/python -I scripts/fetch_databento.py probe|fetch [path/to/databento.env]
"""
import base64
import datetime as dt
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://hist.databento.com/v0/"
DATASET = "EQUS.MINI"
SYMBOL = "NVDA"
START, END = "2026-11-10T00:00:00Z", "2026-11-24T01:00:00Z"   # the same window as the Alpaca pull
MAX_COST = 1.00   # USD, the human's cap for this pull
OUT = Path("assets/market/nvda_databento.json")
SCHEMAS = ["ohlcv-1m", "ohlcv-1d"]


def key(path):
    for line in Path(path).expanduser().read_text().splitlines():
        line = line.strip().removeprefix("export ")
        if line.startswith("DATABENTO_API_KEY="):
            return line.split("=", 1)[1].strip().strip("'\"")
    raise SystemExit("DATABENTO_API_KEY not found in the key file")


def call(k, endpoint, params, raw=False):
    """Metadata endpoints take GET; the data endpoint takes POST."""
    auth = base64.b64encode(f"{k}:".encode()).decode()
    q = urllib.parse.urlencode(params)
    post = endpoint.startswith("timeseries.")
    req = urllib.request.Request(API + endpoint + ("" if post else f"?{q}"), data=q.encode() if post else None,
                                 headers={"Authorization": f"Basic {auth}", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            body = r.read().decode()
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:400]
        raise SystemExit(f"{endpoint}: HTTP {e.code} {detail}")
    return body if raw else json.loads(body)


def ends(k, schemas):
    """Each schema's end: the window's end, or the last data the dataset has for it (daily bars lag by a day)."""
    rng = call(k, "metadata.get_dataset_range", {"dataset": DATASET})["schema"]
    iso = lambda x: dt.datetime.fromisoformat(x[:19]).replace(tzinfo=dt.timezone.utc)
    return {s: min(iso(END), iso(rng[s]["end"])).strftime("%Y-%m-%dT%H:%M:%SZ") for s in schemas}


def costs(k, ends):
    return {s: float(call(k, "metadata.get_cost", {"dataset": DATASET, "symbols": SYMBOL, "schema": s, "start": START, "end": e,
                                                     "stype_in": "raw_symbol", "mode": "historical-streaming"})) for s, e in ends.items()}


def bars(k, schema, end):
    text = call(k, "timeseries.get_range", {"dataset": DATASET, "symbols": SYMBOL, "schema": schema, "start": START, "end": end,
                                            "stype_in": "raw_symbol", "encoding": "json", "pretty_px": "true"}, raw=True)
    rows = []
    for line in text.splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        ns = int(r["hd"]["ts_event"])
        t = dt.datetime.fromtimestamp(ns // 1_000_000_000, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        rows.append({"t": t, **{c: float(r[f]) for c, f in (("o", "open"), ("h", "high"), ("l", "low"), ("c", "close"))}, "v": int(r["volume"])})
    return rows


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "probe"
    k = key(sys.argv[2] if len(sys.argv) > 2 else "~/Documents/databento.env")
    schemas = call(k, "metadata.list_schemas", {"dataset": DATASET})
    e = ends(k, [s for s in SCHEMAS if s in schemas])
    est = costs(k, e)
    total = sum(est.values())
    print(f"{DATASET} schemas: {schemas}")
    print(f"requests: {e}")
    print(f"cost estimate: {est}, total ${total:.4f} (cap ${MAX_COST:.2f})")
    if mode != "fetch":
        return
    if total >= MAX_COST:
        raise SystemExit(f"estimate ${total:.4f} is not under the ${MAX_COST:.2f} cap: nothing downloaded")
    got = {s: bars(k, s, e[s]) for s in est}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"symbol": SYMBOL, "source": "Databento", "dataset": DATASET, "start": START, "ends": e,
                               "fetched": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "cost_estimate_usd": round(total, 4),
                               "day_utc": got.get("ohlcv-1d", []), "minute": got["ohlcv-1m"]}) + "\n")
    print(f"wrote {OUT}: {len(got['ohlcv-1m'])} minute bars, {len(got.get('ohlcv-1d', []))} daily bars")


if __name__ == "__main__":
    main()
