#!/usr/bin/env python3
"""Fetch the latest Substack posts and write them to _data/substack.json.

Run by .github/workflows/substack.yml on a schedule (and manually). Uses only
the Python standard library, so no dependencies need to be installed.

On any fetch/parse failure it leaves the existing data file untouched, so a
transient Substack outage never wipes the posts already shown on the site.
"""
import json
import os
import sys
import urllib.request
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from xml.etree import ElementTree as ET

FEED_URL = os.environ.get("SUBSTACK_FEED", "https://sherafghanasad.substack.com/feed")
MAX_POSTS = int(os.environ.get("SUBSTACK_MAX", "5"))
OUT_PATH = os.environ.get("SUBSTACK_OUT", "_data/substack.json")
EXCERPT_LEN = 220


class _Stripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)

    def text(self):
        return "".join(self.parts)


def strip_html(html):
    if not html:
        return ""
    stripper = _Stripper()
    try:
        stripper.feed(html)
    except Exception:
        return ""
    return " ".join(stripper.text().split())


def excerpt(text, limit=EXCERPT_LEN):
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + "…"


def fmt_date(raw):
    if not raw:
        return ""
    try:
        return parsedate_to_datetime(raw).strftime("%B %-d, %Y")
    except Exception:
        return raw.strip()


def main():
    req = urllib.request.Request(
        FEED_URL, headers={"User-Agent": "Mozilla/5.0 (newsletter-sync)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read()
    except Exception as exc:
        print(f"::warning::Could not fetch {FEED_URL}: {exc}. Keeping existing data.")
        return 0

    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        print(f"::warning::Could not parse feed: {exc}. Keeping existing data.")
        return 0

    ns = {"content": "http://purl.org/rss/1.0/modules/content/"}
    posts = []
    for item in root.iter("item"):
        desc = strip_html(item.findtext("description") or "")
        if not desc:
            desc = strip_html(item.findtext("content:encoded", default="", namespaces=ns))
        posts.append({
            "title": (item.findtext("title") or "Untitled").strip(),
            "link": (item.findtext("link") or "").strip(),
            "date": fmt_date(item.findtext("pubDate")),
            "excerpt": excerpt(desc),
        })
        if len(posts) >= MAX_POSTS:
            break

    os.makedirs(os.path.dirname(OUT_PATH) or ".", exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(posts, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(f"Wrote {len(posts)} post(s) to {OUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
