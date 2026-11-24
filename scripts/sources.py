"""docs/sources.md: every factual claim on screen, with links to check it against (human, 2026-11-24).

The fact card and disclosure come from config/cards.json, so this list matches what renders. Everything else on screen
that states a fact (chart figures, signs, tags, phone stamps, counters, closing cards) is listed below with its source.
Usage: .venv/bin/python -I scripts/sources.py
"""
import json
from pathlib import Path

C = json.load(open("config/cards.json"))
SAGA = json.load(open("config/saga.json"))
SEC_8K_NOV11 = "https://www.sec.gov/Archives/edgar/data/1045810/000104581026000082/0001045810-26-000082-index.html"
SEC_8K_NOV23 = "https://www.sec.gov/Archives/edgar/data/1045810/000104581026000090/0001045810-26-000090-index.html"
REL_NOV12 = "https://nvidianews.nvidia.com/news/nvidia-announces-ceo-transition"
REL_NOV23 = "https://nvidianews.nvidia.com/news/nvidia-board-reinstates-jensen-huang-as-president-ceo-and-board-director"
Q3 = "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Third-Quarter-Fiscal-2027/default.aspx"
CNBC_NOV20 = "https://www.cnbc.com/2026/11/20/nvidias-7-week-losing-streak-is-longest-since-2008-financial-crisis.html"
AP_NOV23 = "https://www.bostonglobe.com/2026/11/23/business/nvidia-reinstates-jensen-huang/"
CNBC_NOV12 = "https://www.cnbc.com/2026/11/12/nvidia-jensen-huang-ceo-live-updates.html"

# Everything on screen outside the cards that states a fact: (where, what it says, sources, note).
ON_SCREEN = [
    ("E01, real screenshot", "Nvidia's \"NVIDIA Announces CEO Transition\" release, November 12, 2026", [REL_NOV12], "The human's capture, cropped (decisions 30)."),
    ("E01t, terminal", "nvidia-smi: RTX 5090 at 100%, 572 W / 575 W, during the postfilter run", [], "Real capture, assets/captures/nvidia_smi/postfilter/nvidia-smi_022618_55.txt (decisions 30)."),
    ("E03, phone", f"\"{SAGA['phone']['filingStamp']}\", FORM 8-K, Item 5.02, \"effective immediately\"", [SEC_8K_NOV11, REL_NOV12], "The 8-K was accepted 2026-11-12 08:52:41; Item 5.02 covers officer departures."),
    ("E11, E11 close, boardroom screens", "Candles: NVDA, Nov 11 14:00 to Nov 12 close; \"−14.3% at the low\", \"−4.3% at the close\"", [CNBC_NOV12, "https://databento.com/datasets/EQUS.MINI"],
     "Shapes from Databento US Equities Mini; figures from official closes (config/official_closes.json): low 148.80 and close 166.19 against 173.73."),
    ("E13, scoreboard", f"\"{SAGA['q3Revenue']}\" and \"▲{SAGA['q3Growth']}\" (Q3 FY2027 revenue, $bn)", [Q3], ""),
    ("E15i, calendar", f"\"{SAGA['quarterEnded']}\" circled: the quarter's last day", [Q3, "https://xenospectrum.com/en/nvidia-fy2027-q3-data-center-growth/"], ""),
    ("E18p, phone", f"\"{SAGA['phone']['nightDate']}\", \"…would be {SAGA['statementWord']}…\"", ["https://www.nbcnews.com/business/corporations/jensen-huang-agrees-house-interview-nvidias-chip-smuggling-rcna609803"],
     "He said he would be \"honored\" to return (Nov 17). The 11:48 clock is set dressing."),
    ("E20, E21, desk phone", "\"SENIOR LEVELS\"", [REL_NOV23], "The release: \"input from senior levels of the United States government\"."),
    ("E21, tags", f"\"{SAGA['officialsTag']}\"", [REL_NOV23], ""),
    ("E21, tags", "\"Investigation: continuing (Nvidia, Nov 23)\"", [REL_NOV23], ""),
    ("E21, tags", "\"House interviews: Dec 1–2\"", ["https://axios.com/2026/11/17/nvidia-jensen-huang-congress-testify-dates"], ""),
    ("E21, tags", "\"The White House took credit on TV the same day (see fact card)\"", ["https://www.nbcnews.com/politics/trump-administration/trump-nvidia-board-reinstates-jensen-huang-rcna610882"], ""),
    ("E22s and later boardroom screens", "Daily candles Nov 11–23; \"−14.0% on Nov 20\", \"+31.5% on Nov 23\"", [CNBC_NOV20, AP_NOV23, "https://databento.com/datasets/EQUS.MINI"],
     "Official closes 145.98 → 125.53 → 165.05. CNBC says 14%, AP 165.05 and \"more than 31%\". The 125.53 and 145.98 closes appear only in smaller outlets (Trefis, NewsBytes); a major outlet or Nasdaq's own record would be better."),
    ("E23, signs", " / ".join(SAGA["governanceSigns"]), ["https://finviz.com/news/423751/nvidia-board-of-directors-establishes-national-security-and-export-control-oversight-committee", REL_NOV23],
     "Committee created Nov 17; the compliance officer search announced Nov 23."),
    ("E24, counters", f"\"YOU: {SAGA['dayCount']} DAYS\", \"PLAQUE: 2 DAYS\"", [REL_NOV12, REL_NOV23, "https://sfist.com/2026/11/14/san-jose-dennys-reverses-course-reinstalls-plaque-honoring-former-nvidia-ceo/"],
     "Nov 12 to Nov 23 is 11 days; the plaque went back within two days."),
    ("E25, real screenshot", "Nvidia's \"NVIDIA Board Reinstates Jensen Huang as President, CEO and Board Director\" release, November 23, 2026", [REL_NOV23], "The human's capture, cropped."),
    ("Closing cards", " · ".join(C["closing"]), [REL_NOV23, "https://axios.com/2026/11/17/nvidia-jensen-huang-congress-testify-dates"], ""),
    ("Timing claims used in checks", "Resignation release 8:48 am Nov 12; 8-K accepted 8:52 am; reinstatement release 8:55 am Nov 23",
     ["https://finviz.com/news/421754/nvidia-announces-ceo-transition", SEC_8K_NOV11, "https://www.stocktitan.net/news/NVDA/nvidia-board-reinstates-jensen-huang-as-president-ceo-and-board-0p954rb1hzde.html", SEC_8K_NOV23],
     "Not on screen as text, except the E03 stamp; they settle the card's Nov 12 date (decisions 27)."),
]

# The disclosure card's claims, with sources (scripts/sources.py is re-run when they change).
DISCLOSURE = json.loads(Path("config/disclosure_sources.json").read_text()) if Path("config/disclosure_sources.json").exists() else []


def main():
    out = ["# Sources to fact-check against", "",
           "Generated by `scripts/sources.py` from `config/cards.json` and the list in that script. Every factual claim on screen, "
           "with the pages to check it against. Open each page; don't rely on search snippets (brief, audit plan).", "",
           "## Fact card", ""]
    for i, (fact, srcs) in enumerate(zip(C["facts"], C["fact_sources"]), 1):
        out.append(f"{i}. {fact}")
        for s in srcs:
            out.append(f"   - {s['name']}: <{s['url']}>")
        if not srcs:
            out.append("   - (no source: a statement about the video)")
        out.append("")
    out += ["## Disclosure card", "", C["disclosure"], ""]
    for d in DISCLOSURE:
        out.append(f"- **{d['claim']}**")
        for u in d["urls"]:
            out.append(f"  - <{u}>")
    if not DISCLOSURE:
        out.append("- (sources being gathered)")
    out += ["", "## Everything else on screen", "", "| Where | What it says | Sources | Note |", "| --- | --- | --- | --- |"]
    for where, what, urls, note in ON_SCREEN:
        out.append(f"| {where} | {what} | {'<br>'.join(f'<{u}>' for u in urls) or '—'} | {note} |")
    out += ["", "## Not claims", "",
            "Set dressing with no factual weight: E19's callers (Employees, Investors, Partners, Customers; the brief calls them the groups his statement named, unsourced, but the screen claims nothing about a statement), the clocks on the night phone (11:48) and the desk phones (9:14), \"The Company\", "
            "the generic diner and its plaque text (from the lyric, not the real plaque), and the purchase order."]
    Path("docs/sources.md").write_text("\n".join(out) + "\n")
    print(f"docs/sources.md: {len(C['facts'])} fact lines, {len(DISCLOSURE)} disclosure claims, {len(ON_SCREEN)} other items")


if __name__ == "__main__":
    main()
