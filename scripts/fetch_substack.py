#!/usr/bin/env python3
"""Fetch the latest Substack posts and write them to _data/substack.json.

Run by .github/workflows/substack.yml on a schedule (and manually). Uses only
the Python standard library, so no dependencies need to be installed.

Strategy:
  1. Fetch the publication's RSS feed directly (browser-like headers).
  2. If that's blocked -- Substack/Cloudflare commonly 403s cloud/CI IPs --
     fall back to the rss2json gateway, whose servers aren't blocked.
On total failure it leaves the existing data file untouched, so a transient
outage never wipes the posts already shown on the site.
"""
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from xml.etree import ElementTree as ET

FEED_URL = os.environ.get("SUBSTACK_FEED", "https://sherafghanasad.substack.com/feed")
MAX_POSTS = int(os.environ.get("SUBSTACK_MAX", "5"))
OUT_PATH = os.environ.get("SUBSTACK_OUT", "_data/substack.json")
EXCERPT_LEN = 220

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/rss+xml, application/xml, text/xml;q=0.9, */*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


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
    raw = raw.strip()
    try:  # RFC 822, the standard RSS pubDate format
        return parsedate_to_datetime(raw).strftime("%B %-d, %Y")
    except Exception:
        pass
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):  # rss2json style
        try:
            return datetime.strptime(raw[:19], fmt).strftime("%B %-d, %Y")
        except Exception:
            pass
    return raw


def _get(url, timeout=30):
    req = urllib.request.Request(url, headers=BROWSER_HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def from_rss(raw):
    root = ET.fromstring(raw)
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
    return posts


def from_rss2json(feed_url):
    api = "https://api.rss2json.com/v1/api.json?" + urllib.parse.urlencode({"rss_url": feed_url})
    data = json.loads(_get(api))
    if data.get("status") != "ok":
        raise RuntimeError("rss2json status %s: %s" % (data.get("status"), data.get("message")))
    posts = []
    for item in (data.get("items") or [])[:MAX_POSTS]:
        desc = strip_html(item.get("description") or "") or strip_html(item.get("content") or "")
        posts.append({
            "title": (item.get("title") or "Untitled").strip(),
            "link": (item.get("link") or "").strip(),
            "date": fmt_date(item.get("pubDate")),
            "excerpt": excerpt(desc),
        })
    return posts


def from_feed2json(feed_url):
    # feed2json fetches fresh server-side (unlike rss2json, which caches hard)
    api = "https://feed2json.org/convert?" + urllib.parse.urlencode({"url": feed_url})
    data = json.loads(_get(api))
    posts = []
    for item in (data.get("items") or [])[:MAX_POSTS]:
        desc = (strip_html(item.get("summary") or "")
                or strip_html(item.get("content_html") or "")
                or (item.get("content_text") or "").strip())
        posts.append({
            "title": (item.get("title") or "Untitled").strip(),
            "link": (item.get("url") or "").strip(),
            "date": fmt_date(item.get("date_published")),
            "excerpt": excerpt(desc),
        })
    return posts


def main():
    # Try in order; the GitHub runner's IP is blocked by Substack (403), so the
    # direct fetch usually fails on CI and a gateway is used. Prefer the first
    # method that returns posts; feed2json fetches fresh, rss2json can be stale.
    methods = [
        ("direct feed", lambda: from_rss(_get(FEED_URL))),
        ("feed2json gateway", lambda: from_feed2json(FEED_URL)),
        ("rss2json gateway", lambda: from_rss2json(FEED_URL)),
    ]
    posts = None
    any_success = False
    for name, fetch in methods:
        try:
            result = fetch()
        except Exception as exc:
            print(f"::warning::{name} failed: {exc}")
            continue
        any_success = True
        if result:
            posts = result
            print(f"Fetched {len(result)} post(s) via {name}")
            break
        print(f"{name} returned 0 posts")

    if posts is None:
        if not any_success:
            print("::warning::All fetch methods failed. Keeping existing data.")
            return 0
        posts = []  # every method agreed the feed is empty

    os.makedirs(os.path.dirname(OUT_PATH) or ".", exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(posts, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(f"Wrote {len(posts)} post(s) to {OUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
