#!/usr/bin/env python3
"""Create or update the Demos pages on a ReadMe branch from pages/*.mdx.

Usage: README_API_KEY=... python3 tools/upload_pages.py <branch, e.g. 1_demos>
"""
import json
import os
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
BRANCH = sys.argv[1]
KEY = os.environ["README_API_KEY"]
API = "https://api.readme.com/v2"


def call(method, path, body=None):
    req = urllib.request.Request(
        API + path,
        method=method,
        data=None if body is None else json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json", "Accept": "application/json", "User-Agent": "curl/8.7.1"},
    )
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")


data = json.loads((ROOT / "demos.json").read_text())
for s in data["sections"]:
    body = (ROOT / "pages" / f"{s['slug']}.mdx").read_text()
    cat = urllib.parse.quote(s["category"])
    page = {
        "title": "Demos",
        "content": {"body": body},
        "privacy": {"view": "public"},
        "metadata": {
            "title": f"{s['category'].replace('Rayls ', '')} demos – Rayls Docs",
            "description": f"Recorded demos of {s['name']}, newest first.",
        },
    }
    code, _ = call("GET", f"/branches/{BRANCH}/guides/{s['slug']}")
    if code == 200:
        code, res = call("PATCH", f"/branches/{BRANCH}/guides/{s['slug']}", page)
    else:
        page |= {"slug": s["slug"], "category": {"uri": f"/branches/{BRANCH}/categories/guides/{cat}"}}
        code, res = call("POST", f"/branches/{BRANCH}/guides", page)
    print(s["slug"], code, "" if code < 300 else json.dumps(res)[:400])
