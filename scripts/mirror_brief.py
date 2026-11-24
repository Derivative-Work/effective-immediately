"""Write a plain-text mirror of one tab of the brief (docs/brief.md) from a docs-tool read of it.

The read is `read(ref=node <tab body>, engine=prose, container=project 9bf617ca-b4cf-4f42-ad49-18eb6ffad325, payload={"kind":"view"})`,
the tab body being 087a99f9-3ba0 (one tab); its
result (JSON, optionally followed by a notice) is saved to a file and passed here. The doc stays the source of truth.
Usage: python3 -I scripts/mirror_brief.py <saved read result> [out=docs/brief.md] [tab label]
"""
import html
import json
import re
import sys

src = open(sys.argv[1]).read()
out_path = sys.argv[2] if len(sys.argv) > 2 else "docs/brief.md"
tab = sys.argv[3] if len(sys.argv) > 3 else "main tab"
d, _ = json.JSONDecoder().raw_decode(src)
x, rev = d["data"]["xml"], d["data"]["rev"]

cdata = {}
def keep(m):
    k = f"\x00{len(cdata)}\x00"
    cdata[k] = m.group(1)
    return k

x = re.sub(r"<!\[CDATA\[(.*?)\]\]>", keep, x, flags=re.S)
x = re.sub(r"<paragraph[^>]*heading='(\d)'[^>]*>", lambda m: "\n\n" + "#" * int(m.group(1)) + " ", x)
x = re.sub(r"<table[^>]*>", "\n", x).replace("</table>", "\n")
x = re.sub(r"<listItem[^>]*>\s*<paragraph[^>]*>", "\n- ", x)
x = re.sub(r"<row[^>]*>", "\n|", x)
x = re.sub(r"<cell[^>]*>\s*(<paragraph[^>]*>)?", " ", x).replace("</cell>", " |")
x = re.sub(r"<codeBlock[^>]*>", "\n\n```\n", x).replace("</codeBlock>", "\n```\n")
x = re.sub(r"<blockquote[^>]*>", "\n\n> ", x)
x = re.sub(r"<paragraph[^>]*>", "\n\n", x)
x = re.sub(r"</?bold>", "**", x)
x = re.sub(r"</?code>", "`", x)
x = re.sub(r"<date[^>]*value='([^']*)'[^>]*/>", r"\1", x)
x = re.sub(r"<mention[^>]*name='([^']*)'[^>]*/>", r"\1", x)
x = re.sub(r"<mention[^>]*ref='file/[^']*'[^>]*label='([^']*)'[^>]*/>", r"\1 (docs/cut_list.md)", x)  # a tab chip
x = re.sub(r"<link[^>]*href='([^']*)'[^>]*>(.*?)</link>",
           lambda m: f"[{re.sub('<[^>]+>', '', m.group(2))}]({m.group(1)})", x, flags=re.S)
x = html.unescape(re.sub(r"<[^>]+>", "", x))
for k, v in cdata.items():
    x = x.replace(k, v)
x = x.replace("> \n\n", "> ")
x = re.sub(r"\n{3,}", "\n\n", x).strip()

lines, out = x.split("\n"), []
for i, line in enumerate(lines):
    out.append(line)
    if line.startswith("|") and (i == 0 or not lines[i - 1].startswith("|")):
        out.append("|" + " --- |" * (line.count("|") - 1))
hdr = (f"<!-- Plain-text mirror of the Claude Doc https://claude.ai/artifact/MctWPu388YjJNuZmGg27Xz ({tab}, rev {rev}), "
       f"read with the docs tools. The doc is the source of truth. Regenerate: scripts/mirror_brief.py. -->\n\n")
open(out_path, "w").write(hdr + "\n".join(out) + "\n")
print(f"rev {rev} -> {out_path}")
