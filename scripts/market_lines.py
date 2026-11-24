"""The boardroom screen's two charts, as candlesticks from real NVDA bars.

Source: Databento's US Equities Mini 1-minute bars (assets/market/nvda_databento.json, scripts/fetch_databento.py). Its
terms require "Data provided by Databento" wherever this is published (decisions 28). Alpaca's bars
(nvda_bars.json) are no longer used: its terms forbid public display. US Equities Mini doesn't carry the closing auction,
so the numbers printed on screen and the dashed line use the official closes in config/official_closes.json, which the
news reports. The candles' own closes are the last regular-session trades, within $0.40 of those.

- drop (E11): 30-minute candles from Nov 11 14:00 to the Nov 12 close, extended hours included, because the fall began
  after hours on Nov 11. Extended-hours candles are flagged so the chart can shade them.
- recover (E22): daily candles, Nov 11 to Nov 23. Both big moves happened outside the session (the Nov 12 open came after
  the Nov 11 after-hours fall; the Nov 23 jump came pre-market), so a daily candle shows them as gaps, not bodies. Gaps over
  5% are drawn as shaded bands from the previous close to the open, a standard chart annotation, so the jumps read.
Candles are coloured by their close against the previous close (a down day is red even if it rose from its open), which is
how a viewer reads "the day". x is trading time (overnight gaps close up). The y axis doesn't start at zero, so the Nov 11
close is drawn as a dashed line and the moves are labelled in percent. Market value is taken to move with the share price.
Bad prints, in extended hours only, are left out as charting services filter them: a wick more than 3% beyond its
minute's open and close (Alpaca's feed had one, Nov 12 08:22), and an open more than 3% from both the minute before and
its own close (Databento's Nov 12 04:00 opened at 172.12, against 160.43 the evening before and a 161.50 close).
Writes only the normalised shapes and tags to remotion/public/gen/timing/market.json.
Usage: .venv/bin/python -I scripts/market_lines.py
"""
import datetime as dt
import json
from pathlib import Path
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
D = json.load(open("assets/market/nvda_databento.json"))
OFFICIAL = json.load(open("config/official_closes.json"))
CLOSE = {d: v["price"] for d, v in OFFICIAL["closes"].items()}
when = lambda b: dt.datetime.fromisoformat(b["t"].replace("Z", "+00:00")).astimezone(ET)
RAW = [(when(b), b) for b in D["minute"]]
BAD_PRINT = 0.03   # a wick more than 3% beyond the minute's open and close, in extended hours only


def regular(t):
    return t.weekday() < 5 and dt.time(9, 30) <= t.time() < dt.time(16, 0)


def clean(t, b, before):
    o, h, l = b["o"], b["h"], b["l"]
    if not regular(t):
        if before is not None and abs(o / before - 1) > BAD_PRINT and abs(o / b["c"] - 1) > BAD_PRINT:
            print(f"bad print left out: {t:%b %d %H:%M} open {o} (minute before closed {before}, this one {b['c']})")
            o = b["c"]   # its high, set by the same print, is then caught by the wick rule below
        top, bot = max(o, b["c"]), min(o, b["c"])
        if h > top * (1 + BAD_PRINT):
            print(f"bad print left out: {t:%b %d %H:%M} high {h} (open {b['o']}, close {b['c']})")
            h = top
        if l < bot * (1 - BAD_PRINT):
            print(f"bad print left out: {t:%b %d %H:%M} low {l} (open {b['o']}, close {b['c']})")
            l = bot
    return {**b, "o": o, "h": h, "l": l}


MINUTE = [(t, clean(t, b, RAW[i - 1][1]["c"] if i else None)) for i, (t, b) in enumerate(RAW)]


def intraday(start, end, minutes):
    out = {}
    for t, b in MINUTE:
        if start <= t < end:
            k = t.replace(minute=t.minute // minutes * minutes, second=0)
            c = out.setdefault(k, {"t": k, "o": b["o"], "h": b["h"], "l": b["l"], "c": b["c"], "ext": not regular(k)})
            c["h"], c["l"], c["c"] = max(c["h"], b["h"]), min(c["l"], b["l"]), b["c"]
    return list(out.values())


def session_days():
    """Daily candles from the regular session's minutes (Databento's own daily bars run midnight to midnight UTC)."""
    days = {}
    for t, b in MINUTE:
        if regular(t):
            d = days.setdefault(str(t.date()), {"t": str(t.date()), "o": b["o"], "h": b["h"], "l": b["l"], "c": b["c"], "ext": False})
            d["h"], d["l"], d["c"] = max(d["h"], b["h"]), min(d["l"], b["l"]), b["c"]
    return days


DAY = session_days()


def daily(first, last):
    return [DAY[d] for d in sorted(DAY) if first <= d <= last]


GAP = 0.05


def chart(candles, prev_close, base, label, start, tags, mark_gaps=False):
    lo = min([c["l"] for c in candles] + [base])
    hi = max([c["h"] for c in candles] + [base])
    pad = (hi - lo) * 0.1
    y = lambda v: round(1 - (v - lo + pad) / (hi - lo + 2 * pad), 4)
    rows, before = [], prev_close
    for c in candles:
        rows.append({"o": y(c["o"]), "h": y(c["h"]), "l": y(c["l"]), "c": y(c["c"]), "up": c["c"] >= before, "ext": c["ext"]})
        before = c["c"]
    gaps = [i for i in range(1, len(candles)) if isinstance(candles[i]["t"], dt.datetime)
            and candles[i]["t"].date() != candles[i - 1]["t"].date()]
    jumps = [{"at": i, "from": y(candles[i - 1]["c"]), "to": y(candles[i]["o"]), "up": candles[i]["o"] > candles[i - 1]["c"]}
             for i in range(1, len(candles)) if mark_gaps and abs(candles[i]["o"] / candles[i - 1]["c"] - 1) > GAP]
    return {"label": label, "base": y(base), "candles": rows, "start": start, "gaps": gaps, "jumps": jumps, "tags": tags}


def pct(a, b):
    return f"{100 * (a / b - 1):+.1f}%".replace("-", "−")


def main():
    tz = lambda *a: dt.datetime(*a, tzinfo=ET)
    p11, c12, p19, p20, c23 = (CLOSE[d] for d in ("2026-11-11", "2026-11-12", "2026-11-19", "2026-11-20", "2026-11-23"))
    low12 = OFFICIAL["intraday_low"]["2026-11-12"]["price"]
    for d, c in CLOSE.items():   # the candles' last trades should sit close to the official closes
        assert abs(DAY[d]["c"] - c) < 0.5, (d, DAY[d]["c"], c)

    drop = intraday(tz(2026, 11, 11, 14, 0), tz(2026, 11, 12, 16, 0), 30)
    low = min(range(len(drop)), key=lambda i: drop[i]["l"])
    assert abs(drop[low]["l"] - low12) < 0.01, "the intraday low should be the day's low"
    first_fall = next(i for i, c in enumerate(drop) if c["t"] >= tz(2026, 11, 11, 16, 30))
    out = {"drop": chart(drop, drop[0]["o"], p11, "market value, intraday · Nov 11–12", first_fall,
                         [{"at": low, "text": f"{pct(low12, p11)} at the low", "where": "low"},
                          {"at": len(drop) - 1, "text": f"{pct(c12, p11)} at the close", "where": "corner"}])}

    days = daily("2026-11-11", "2026-11-23")
    i20 = next(i for i, c in enumerate(days) if c["t"] == "2026-11-20")
    out["recover"] = chart(days, DAY["2026-11-10"]["c"], p11, "market value · Nov 11–23", i20,
                           [{"at": i20, "text": f"{pct(p20, p19)} on Nov 20", "where": "low"},
                            {"at": len(days) - 1, "text": f"{pct(c23, p20)} on Nov 23", "where": "corner"}], mark_gaps=True)
    out["source"] = {"credit": "Data provided by Databento", "dataset": D["dataset"], "fetched": D["fetched"],
                     "printed_figures": "official closes, config/official_closes.json", "symbol_not_shown": True}
    Path("remotion/public/gen/timing/market.json").write_text(json.dumps(out, ensure_ascii=False) + "\n")
    for k in ("drop", "recover"):
        m = out[k]
        print(k, len(m["candles"]), "candles, reveal from", m["start"], "overnight", m["gaps"], "jumps", [j["at"] for j in m["jumps"]], [t["text"] for t in m["tags"]], "|", m["label"])


if __name__ == "__main__":
    main()
