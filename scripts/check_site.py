#!/usr/bin/env python3
"""
Site checks for The Yellow.
Run locally with:  python3 scripts/check_site.py
The GitHub Action runs this on every push; a non-zero exit fails the build.

Checks performed on every .html page:
  1. Internal links (the-yellow-*.html / index.html) resolve to a real file.
  2. Required SEO tags are present: <title>, description, canonical,
     Open Graph, Twitter Card, and at least one JSON-LD block.
  3. Every JSON-LD block is valid JSON.
  4. robots.txt and sitemap.xml exist.
"""
import os
import re
import json
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = []
warnings = []

html_files = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))

if not html_files:
    print("No HTML files found.")
    sys.exit(1)

for fname in html_files:
    path = os.path.join(ROOT, fname)
    with open(path, encoding="utf-8") as fh:
        s = fh.read()

    # skip redirect stubs left at old URLs (they forward to the clean URL)
    if 'http-equiv="refresh"' in s:
        continue

    # --- 1. internal links resolve (clean, extensionless URLs) ---
    for link in re.findall(r'href="/([a-z0-9-]*)(?:#[^"]*)?"', s):
        target = "index.html" if link == "" else f"{link}.html"
        if not os.path.isfile(os.path.join(ROOT, target)):
            errors.append(f"{fname}: broken internal link -> /{link}")

    # --- 2. required SEO tags ---
    checks = {
        "<title>": "<title>" in s,
        "meta description": 'name="description"' in s,
        "canonical": 'rel="canonical"' in s,
        "Open Graph": 'property="og:title"' in s,
        "Twitter Card": 'name="twitter:card"' in s,
        "JSON-LD": "application/ld+json" in s,
    }
    for label, ok in checks.items():
        if not ok:
            errors.append(f"{fname}: missing {label}")

    # --- 3. JSON-LD validity ---
    for i, block in enumerate(re.findall(
            r'<script type="application/ld\+json">(.*?)</script>', s, re.S)):
        try:
            json.loads(block)
        except json.JSONDecodeError as exc:
            errors.append(f"{fname}: invalid JSON-LD block {i} ({exc})")

    # --- soft check: alt attributes on images ---
    imgs = re.findall(r'<img\b[^>]*>', s)
    for img in imgs:
        if "alt=" not in img:
            warnings.append(f"{fname}: <img> without alt attribute")

# --- 4. required support files ---
for required in ("robots.txt", "sitemap.xml"):
    if not os.path.isfile(os.path.join(ROOT, required)):
        errors.append(f"missing required file: {required}")

# --- report ---
print(f"Checked {len(html_files)} HTML pages.\n")

if warnings:
    print(f"{len(warnings)} warning(s):")
    for w in warnings:
        print(f"  ! {w}")
    print()

if errors:
    print(f"{len(errors)} error(s):")
    for e in errors:
        print(f"  X {e}")
    print("\nFAILED")
    sys.exit(1)

print("All checks passed.")
sys.exit(0)
