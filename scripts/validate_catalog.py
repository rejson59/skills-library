#!/usr/bin/env python3
"""Consistency checks for the generated catalog. Used in CI."""

from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
errors: list[str] = []
warnings: list[str] = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def read(path):
    p = ROOT / path
    if not p.exists():
        err(f"missing file: {path}")
        return None
    return p.read_text(encoding="utf-8")


cat_text = read("data/catalog.json")
if not cat_text:
    sys.exit(1)
cat = json.loads(cat_text)
sources = json.loads((DATA / "sources.json").read_text(encoding="utf-8"))

# catalog.js must contain the exact same object
js = read("data/catalog.js") or ""
prefix = "window.__SKILLS_LIBRARY__ = "
if not js.startswith(prefix) or not js.rstrip().endswith(";"):
    err("catalog.js has an unexpected wrapper")
else:
    try:
        js_obj = json.loads(js[len(prefix):].rstrip().rstrip(";"))
    except Exception as e:
        err(f"catalog.js is not valid JSON: {e}")
    else:
        if js_obj != cat:
            err("catalog.js differs from catalog.json — run build_catalog.py")

# Required top-level structure
for key in ("meta", "categories", "agents", "packs", "spotlight", "collections", "skills"):
    if key not in cat:
        err(f"missing top-level key: {key}")
if cat.get("meta", {}).get("version") != 1:
    err("meta.version must be 1")

# IDs and references
skill_ids = [s["id"] for s in cat["skills"]]
if len(skill_ids) != len(set(skill_ids)):
    err("duplicate skill ids")
by_id = {s["id"]: s for s in cat["skills"]}
collection_ids = [c["id"] for c in cat["collections"]]
if len(collection_ids) != len(set(collection_ids)):
    err("duplicate collection ids")
by_col = {c["id"]: c for c in cat["collections"]}
category_ids = {c["id"] for c in cat["categories"]}
valid_license = {"clear", "check", "per-skill", "unknown"}
valid_tiers = {"essential", "curated", "discovered"}
valid_source_types = {"directory", "single", "collection"}
valid_safe_use = {"security", "chinese"}

for s in cat["skills"]:
    if s.get("collectionId") not in by_col:
        err(f"skill {s['id']} points at missing collection {s.get('collectionId')}")
    if s.get("category") not in category_ids:
        err(f"skill {s['id']} has unknown category {s.get('category')}")
    if s.get("license", {}).get("status") not in valid_license:
        err(f"skill {s['id']} has unknown license status")
    if s.get("tier") not in valid_tiers:
        err(f"skill {s['id']} has unknown tier")
    if not s.get("sourceUrl", "").startswith("https://github.com/"):
        err(f"skill {s['id']} has a bad sourceUrl")
    inst = s.get("install", {})
    if not inst.get("direct", "").startswith("npx skills add "):
        err(f"skill {s['id']} has a bad direct install command")
    if not s.get("description"):
        err(f"skill {s['id']} has no description")
    if not s.get("verified"):
        err(f"skill {s['id']} is not marked verified")
    for note in s.get("safeUse", []):
        if note.get("code") not in valid_safe_use or not note.get("en") or not note.get("pl"):
            err(f"skill {s['id']} has a malformed safe-use note")

for c in cat["collections"]:
    if c.get("sourceType") not in valid_source_types:
        err(f"collection {c['id']} has unknown sourceType {c.get('sourceType')}")
    if c.get("category") not in category_ids:
        err(f"collection {c['id']} has unknown category")
    if c.get("license", {}).get("status") not in valid_license:
        err(f"collection {c['id']} has unknown license status")
    if c.get("tier") not in valid_tiers:
        err(f"collection {c['id']} has unknown tier")
    if c["skillCount"] > c["skillFileCount"]:
        err(f"collection {c['id']}: unique skills exceed file count")
    install = c.get("install", "")
    if c.get("sourceType") == "directory" or c["skillCount"] == 0:
        if not install.startswith("git clone "):
            err(f"directory {c['id']} has a bad install hint")
    elif not install.startswith("npx skills add "):
        err(f"collection {c['id']} has a bad install command")

for sid in cat["spotlight"]:
    if sid not in by_id:
        err(f"spotlight references missing skill {sid}")
for pack in cat["packs"]:
    for sid in pack["skills"]:
        if sid not in by_id:
            err(f"pack {pack['id']} references missing skill {sid}")
    if not pack.get("script"):
        err(f"pack {pack['id']} has no install script")

# Every curated source should be present (GitHub redirects are canonicalized at build time)
curated = {c["repo"] for c in cat["collections"] if c["reviewed"]}
for src in sources["sources"]:
    if src["repo"] not in curated:
        warn(f"curated source not present in catalog: {src['repo']} (404 or redirect?)")

# Generated companions
for path in ("data/discovered.json", "data/schema.json", "CATALOG.md", "llms.txt", "README.md", "README.pl.md", "index.html", "assets/app.js", "assets/styles.css"):
    if not (ROOT / path).exists():
        err(f"missing generated/companion file: {path}")
stats = cat["meta"].get("stats", {})
expected_stats = (
    f"| {stats.get('reposScanned', 0)} | {stats.get('skillFilesFound', 0):,} | "
    f"{stats.get('uniqueSkillFoldersFound', 0):,} | {stats.get('curatedCollections', 0)} | "
    f"{stats.get('indexedSkills', 0)} | {cat['meta'].get('generatedDate', '')} |"
)
for path in ("README.md", "README.pl.md"):
    text = read(path) or ""
    if "<!-- STATS:START -->" not in text or "<!-- STATS:END -->" not in text:
        err(f"{path} is missing stats markers")
    if "| 0 | 0 | 0 | 0 | 0 | — |" in text:
        warn(f"{path} still has placeholder stats")
    if expected_stats not in text:
        err(f"{path} stats do not match catalog metadata; expected: {expected_stats}")

# No accidental browser-facing localhost references
js_app = read("assets/app.js") or ""
if re.search(r"https?://(localhost|127\.0\.0\.1)", js_app):
    err("app.js contains a localhost URL")

disc = json.loads((DATA / "discovered.json").read_text(encoding="utf-8")) if (DATA / "discovered.json").exists() else {}
auto_count = sum(1 for c in cat["collections"] if not c["reviewed"])
if disc.get("count") != auto_count:
    err("discovered.json count does not match catalog")

stats = cat["meta"]["stats"]
if stats["indexedSkills"] != len(cat["skills"]):
    err("meta.stats.indexedSkills does not match skills[]")
if stats["collections"] != len(cat["collections"]):
    err("meta.stats.collections does not match collections[]")

for w in warnings:
    print("WARN:", w)
for e in errors:
    print("ERROR:", e)
print(f"\n{len(cat['skills'])} skills · {len(cat['collections'])} collections · "
      f"{len(cat['packs'])} packs · {len(errors)} errors · {len(warnings)} warnings")
sys.exit(1 if errors else 0)
