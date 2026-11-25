#!/usr/bin/env python3
"""Friendly installer helper for Skills Library.

By default this script only PRINTS commands. Nothing is executed unless you pass
--yes. Always review the upstream SKILL.md before installing (see SECURITY.md).

  python3 scripts/install.py search pdf
  python3 scripts/install.py show anthropics/skills/pdf
  python3 scripts/install.py install anthropics/skills/pdf
  python3 scripts/install.py install anthropics/skills/pdf --yes --global
  python3 scripts/install.py pack starter
  python3 scripts/install.py pack starter --yes
"""

from __future__ import annotations
import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT = ROOT / "data" / "catalog.json"
WARNING = "⚠️  Skills are third-party code/instructions. Read the source before installing."


def load(path: str):
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    return json.loads(p.read_text(encoding="utf-8"))


def search(cat, query, limit=10):
    terms = [t for t in query.lower().replace("/", " ").replace("-", " ").split() if t]
    rows = []
    for s in cat["skills"]:
        hay = " ".join([s["id"], s["title"], s["description"], " ".join(s["tags"]), s["repo"]]).lower()
        hits = sum(1 for t in terms if t in hay)
        if hits:
            rows.append((hits * 100 + s["score"], s))
    rows.sort(key=lambda x: -x[0])
    return [s for _, s in rows[:limit]]


def show(s):
    print(f"\n{s['title']}  ({s['id']})")
    print(f"  {s['shortDescription']}")
    print(f"  source   : {s['sourceUrl']}")
    print(f"  license  : {s['license']['label']} [{s['license']['status']}]")
    print(f"  repo     : {s['repo']}  ★{s['stars']:,}  {s['category']}")
    print(f"  tier     : {s['tier']}  reviewed={s['reviewed']}  official={s['official']}")
    if s["license"]["note"]:
        print(f"  note     : {s['license']['note']}")
    if s["review"]["requiresReview"]:
        print("  review   : scripts/allowed-tools/shell signals found — inspect the folder")
    print(f"  install  : {s['install']['direct']}")


def run(cmd: str):
    print(f"$ {cmd}", flush=True)
    try:
        return subprocess.run(shlex.split(cmd), check=False).returncode
    except FileNotFoundError:
        print("npx not found. Install Node.js 22.20+ or use the manual command instead.", file=sys.stderr)
        return 127


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--catalog", default=str(DEFAULT))
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("search")
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=10)

    p = sub.add_parser("show")
    p.add_argument("id")

    p = sub.add_parser("install")
    p.add_argument("id")
    p.add_argument("--yes", action="store_true", help="actually execute the command")
    p.add_argument("--global", dest="global_", action="store_true")
    p.add_argument("--format", choices=["direct", "shorthand", "global", "use", "manual", "collection"], default=None)

    p = sub.add_parser("pack")
    p.add_argument("id")
    p.add_argument("--yes", action="store_true", help="actually execute every command")

    args = ap.parse_args()
    cat = load(args.catalog)
    by_id = {s["id"]: s for s in cat["skills"]}

    if args.cmd == "search":
        rows = search(cat, args.query, args.limit)
        for s in rows:
            flag = " ⚠︎" if s["review"]["requiresReview"] else ""
            print(f"{s['id']:<62} {s['license']['label']:<22}{flag}  {s['shortDescription'][:70]}")
        if not rows:
            print("No matches. Try `npx skills find <query>` for skills outside this catalog.")

    elif args.cmd == "show":
        s = by_id.get(args.id)
        if not s:
            raise SystemExit(f"skill not found: {args.id}")
        show(s)

    elif args.cmd == "install":
        s = by_id.get(args.id)
        if not s:
            raise SystemExit(f"skill not found: {args.id}")
        fmt = args.format or ("global" if args.global_ else "direct")
        cmd = s["install"][fmt]
        show(s)
        print(f"\n{WARNING}\n")
        if args.yes:
            raise SystemExit(run(cmd))
        print("Dry run — re-run with --yes to execute:\n  " + cmd)

    elif args.cmd == "pack":
        pack = next((p for p in cat["packs"] if p["id"] == args.id), None)
        if not pack:
            raise SystemExit("packs: " + ", ".join(p["id"] for p in cat["packs"]))
        title = pack["title"]["en"]
        print(f"\n{pack['icon']} {title}\n{pack['description']['en']}\n")
        cmds = pack["commands"]
        for c in cmds:
            print("  " + c)
        print(f"\n{WARNING}\n")
        if args.yes:
            for c in cmds:
                code = run(c)
                if code:
                    print(f"command exited {code}; stopping", file=sys.stderr)
                    raise SystemExit(code)
        else:
            print(f"Dry run — {len(cmds)} commands. Re-run with --yes to execute them.")


if __name__ == "__main__":
    main()
