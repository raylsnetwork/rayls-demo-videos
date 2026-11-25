#!/usr/bin/env python3
"""Build one ReadMe "Demos" page body per product section from demos.json.

Usage: python3 tools/build_pages.py <public base URL of this repo's files>
Writes pages/<slug>.mdx (newest demo first).
"""
import json
import pathlib
import sys
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = sys.argv[1].rstrip("/")

TIMELINE = """export const Demo = ({ date, title, by, children }) => (
  <div style={{ position: 'relative', marginLeft: 7, paddingLeft: 28, paddingBottom: 40, borderLeft: '2px solid rgba(123, 92, 250, 0.35)' }}>
    <span style={{ position: 'absolute', left: -8, top: 3, width: 14, height: 14, borderRadius: '50%', background: '#7B5CFA' }} />
    <div style={{ fontSize: 13, fontWeight: 600, letterSpacing: '0.04em', textTransform: 'uppercase', color: '#7B5CFA' }}>{date}</div>
    <div style={{ fontSize: 20, fontWeight: 600, lineHeight: 1.3, margin: '4px 0 2px' }}>{title}</div>
    <div style={{ fontSize: 14, opacity: 0.7, marginBottom: 12 }}>{by}</div>
    {children}
  </div>
)
"""


def nice(d):
    return date.fromisoformat(d).strftime("%-d %B %Y")


def player(d):
    if "file" in d:
        w = "540px" if d.get("ratio") == "1/1" else "100%"
        return (
            f'<video controls preload="metadata" playsInline poster="{BASE}/posters/{d["file"]}.jpg" '
            f"style={{{{ display: 'block', width: '100%', maxWidth: '{w}', aspectRatio: '{d['ratio']}', borderRadius: 8, background: '#000' }}}}>"
            f'<source src="{BASE}/videos/{d["file"]}.mp4" type="video/mp4" /></video>'
        )
    if "loom" in d:
        return (
            f'<iframe src="https://www.loom.com/embed/{d["loom"]}?hide_owner=true&hide_share=true&hide_title=true" '
            f'title="{d["title"]}" allowFullScreen '
            f"style={{{{ display: 'block', width: '100%', aspectRatio: '{d['ratio']}', border: 0, borderRadius: 8 }}}} />"
        )
    if "x" in d:
        return (
            f'<iframe src="https://platform.twitter.com/embed/Tweet.html?id={d["x"]}&dnt=true" '
            f'title="{d["title"]}" scrolling="no" '
            "style={{ display: 'block', width: '100%', maxWidth: 550, height: 640, border: 0 }} />"
        )
    raise ValueError(d)


def page(section, demos):
    out = [TIMELINE]
    if not demos:
        out.append(f"Recorded demos of {section['name']} will appear here, newest first.")
        return "\n".join(out) + "\n"
    out.append(f"Recorded demos of {section['name']}, newest first.\n")
    for d in demos:
        out.append(f'<Demo date="{nice(d["date"])}" title={{{json.dumps(d["title"])}}} by="{d["by"]}">')
        out.append("")
        out.append(d["text"])
        out.append("")
        if "parts" in d:
            # Long cuts are split to stay under jsDelivr's 20 MB per file.
            for i, f in enumerate(d["parts"], 1):
                out.append(f"**Part {i} of {len(d['parts'])}**\n")
                out.append(player({**d, "file": f}))
                out.append("")
        else:
            out.append(player(d))
        if "full" in d:
            out.append("")
            out.append(f"Cut from the [full recording on X]({d['full']}), screen share only.")
            out.append("")
        out.append("</Demo>\n")
    return "\n".join(out)


data = json.loads((ROOT / "demos.json").read_text())
(ROOT / "pages").mkdir(exist_ok=True)
for s in data["sections"]:
    demos = sorted((d for d in data["demos"] if d["section"] == s["category"]), key=lambda d: d["date"], reverse=True)
    (ROOT / "pages" / f"{s['slug']}.mdx").write_text(page(s, demos))
    print(s["slug"], len(demos))
