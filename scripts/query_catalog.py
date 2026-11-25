#!/usr/bin/env python3
"""Query data/catalog.json from the terminal or from an AI agent.

Examples:
  python3 scripts/query_catalog.py search "react best practices" --limit 5
  python3 scripts/query_catalog.py search pdf --official --json
  python3 scripts/query_catalog.py collection anthropics/skills
  python3 scripts/query_catalog.py install anthropics/skills/pdf
  python3 scripts/query_catalog.py stats
  python3 scripts/query_catalog.py random --category security
"""

from __future__ import annotations
import argparse
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT = ROOT / "data" / "catalog.json"


def load(path: str):
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    return json.loads(p.read_text(encoding="utf-8"))


def tokenize(q: str):
    return [t for t in q.lower().replace("/", " ").replace("-", " ").split() if t]


def search(cat: dict, q: str, *, category=None, official=False, clear=False, limit=10):
    terms = tokenize(q)
    rows = []
    for s in cat["skills"]:
        if category and s["category"] != category:
            continue
        if official and not s["official"]:
            continue
        if clear and s["license"]["status"] not in ("clear",):
            continue
        hay = " ".join([
            s["id"], s["name"], s["title"], s["description"], s["repo"],
            " ".join(s["tags"]), s["category"],
        ]).lower()
        hits = sum(1 for t in terms if t in hay)
        if terms and not hits:
            continue
        rank = hits * 100 + s["score"] + (10 if s["spotlight"] else 0)
        rows.append((rank, s))
    rows.sort(key=lambda x: -x[0])
    return [s for _, s in rows[:limit]]


def brief(s: dict) -> dict:
    return {
        "id": s["id"], "title": s["title"], "shortDescription": s["shortDescription"],
        "repo": s["repo"], "category": s["category"], "license": s["license"]["label"],
        "official": s["official"], "specCompliant": s["specCompliant"],
        "review": s["review"]["requiresReview"], "sourceUrl": s["sourceUrl"],
        "install": s["install"]["direct"],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--catalog", default=str(DEFAULT))
    ap.add_argument("--json", action="store_true", help="emit raw JSON")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("search")
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--category")
    p.add_argument("--official", action="store_true")
    p.add_argument("--clear-license", dest="clear", action="store_true")

    p = sub.add_parser("collection")
    p.add_argument("repo")

    p = sub.add_parser("install")
    p.add_argument("id")
    p.add_argument("--format", choices=["direct", "shorthand", "global", "use", "manual", "collection"], default="direct")

    sub.add_parser("stats")

    p = sub.add_parser("random")
    p.add_argument("--category")
    p.add_argument("--limit", type=int, default=3)

    args = ap.parse_args()
    cat = load(args.catalog)

    if args.cmd == "search":
        items = [brief(s) for s in search(cat, args.query, category=args.category, official=args.official, clear=args.clear, limit=args.limit)]
        out = items
    elif args.cmd == "collection":
        c = next((c for c in cat["collections"] if c["id"] == args.repo or c["repo"] == args.repo), None)
        if not c:
            raise SystemExit(f"collection not found: {args.repo}")
        skills = [brief(s) for s in cat["skills"] if s["collectionId"] == c["id"]]
        out = {**{k: c[k] for k in ("id", "repo", "description", "stars", "skillCount", "license", "tier", "reviewed", "install")}, "indexedSkills": skills}
    elif args.cmd == "install":
        s = next((s for s in cat["skills"] if s["id"] == args.id), None)
        if not s:
            raise SystemExit(f"skill not found: {args.id}")
        out = {"id": s["id"], "sourceUrl": s["sourceUrl"], "command": s["install"][args.format]}
    elif args.cmd == "stats":
        out = cat["meta"]["stats"]
    elif args.cmd == "random":
        pool = [s for s in cat["skills"] if not args.category or s["category"] == args.category]
        out = [brief(s) for s in random.sample(pool, min(args.limit, len(pool)))]
    else:
        raise SystemExit(2)

    if args.cmd == "install" and not args.json:
        print(out["command"])
        print(f"# source: {out['sourceUrl']}", flush=True)
        return
    if args.json or isinstance(out, (dict, list)):
        print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
