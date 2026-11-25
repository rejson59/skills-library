#!/usr/bin/env python3
"""Build the Skills Library catalog from live GitHub data.

What this script does (no third-party Python packages required):

1. Runs the GitHub search API over the queries in ``data/sources.json``.
2. Fetches metadata and recursive git trees for every candidate repository.
3. Counts real ``SKILL.md`` files (and unique skill folder names — many repos
   publish the same skill into .claude/, .cursor/, .agents/ etc.).
4. Fetches the actual ``SKILL.md`` frontmatter for the editorially selected
   skills, extracts name/description/license/allowed-tools and computes simple
   review heuristics.
5. Writes machine-readable and human-readable outputs:
   ``data/catalog.json``, ``data/catalog.js``, ``data/discovered.json``,
   ``CATALOG.md``, ``llms.txt`` and refreshes the stats blocks in the READMEs.

Authentication is optional for small runs but strongly recommended:
    export GITHUB_TOKEN=...   # or GH_TOKEN; falls back to `gh auth token`

Usage:
    python3 scripts/build_catalog.py
    python3 scripts/build_catalog.py --no-discover      # curated sources only
    python3 scripts/build_catalog.py --max-repos 250    # faster local run

The script never copies upstream skill bodies into the repository: we index
metadata and link to the original files, so upstream licenses stay intact.
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import json
import math
import os
import posixpath
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
API = "https://api.github.com"
NOW = dt.datetime.now(dt.timezone.utc)
TODAY = NOW.date().isoformat()

PERMISSIVE = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "CC0-1.0", "Unlicense", "MPL-2.0"}
COPYLEFT = {"AGPL-3.0", "GPL-2.0", "GPL-3.0", "LGPL-2.1", "LGPL-3.0", "EPL-2.0", "CC-BY-SA-4.0", "CC-BY-4.0"}
OFFICIAL_ORGS = {
    "anthropics", "openai", "google", "googleworkspace", "google-labs-code", "github",
    "vercel-labs", "vercel", "cloudflare", "duckdb", "obsidianmd", "android",
    "huggingface", "greensock", "microsoft", "nvidia", "alibaba", "minimax-ai",
    "janestreet", "gsap", "prisma", "openzeppelin", "trailofbits", "genspark-ai",
}
EXCLUDE_SEGMENTS = {
    "evals", "eval", "tests", "test", "examples", "example", "templates", "template",
    "docs", "doc", "benchmarks", "benchmark", "fixtures", "fixture", "node_modules",
    ".changeset", "PULL_REQUEST_TEMPLATE", "ISSUE_TEMPLATE", "__pycache__",
}
SCRIPT_EXTS = (".py", ".sh", ".bash", ".zsh", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".rb", ".go", ".rs", ".ps1", ".bat", ".php", ".pl", ".lua")
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]")
SAFE_USE = {
    "security": {
        "en": "Security-oriented skill. Use only on systems you own or are explicitly authorized to test, and inspect bundled scripts, network calls, and tool permissions first.",
        "pl": "Skill o profilu bezpieczeństwa. Używaj wyłącznie w systemach, które posiadasz lub masz wyraźną autoryzację do testów; najpierw sprawdź skrypty, połączenia sieciowe i uprawnienia narzędzi.",
    },
    "chinese": {
        "en": "The upstream description is primarily in Chinese. Review and translate the source before using it in an English or Polish workflow.",
        "pl": "Opis źródłowy jest głównie w języku chińskim. Przejrzyj i przetłumacz źródło przed użyciem w angielskim lub polskim procesie pracy.",
    },
}
KEYWORDS = {
    "pdf": r"\bpdf\b", "docx": r"\bdocx\b|\bword\b", "slides": r"\bpptx\b|powerpoint|slides?",
    "excel": r"\bxlsx\b|spreadsheet|excel", "markdown": r"markdown|obsidian",
    "react": r"react|next\.?js", "frontend": r"frontend|front-end|ui\b|css|tailwind",
    "design": r"design|art.direction|visual", "animation": r"animat|gsap|motion",
    "security": r"security|vulnerab|pentest|audit|exploit|owasp|threat",
    "testing": r"test|tdd|playwright|e2e|qa", "debugging": r"debug|bug|trace",
    "review": r"code.review|review|pull.request|\bpr\b", "git": r"\bgit\b|worktree|commit",
    "api": r"\bapi\b|openapi|graphql|rest", "database": r"sql|database|duckdb|postgres",
    "data": r"data|dataset|analytics|science|research", "ml": r"\bml\b|llm|model|huggingface|training",
    "cloud": r"cloud|deploy|vercel|aws|azure|gcp|kubernetes|docker",
    "automation": r"automat|workflow|n8n|zapier|scrape|crawl|browser",
    "marketing": r"marketing|seo|copywriting|cro|ads?|growth|linkedin",
    "product": r"product|\bprd\b|okr|roadmap|founder|startup",
    "writing": r"writing|edit|humaniz|prose|blog|content",
    "planning": r"plan|spec|brainstorm|architect|strategy",
    "mobile": r"android|ios|swiftui|react.native|mobile",
    "web3": r"solidity|smart.contract|solana|jupiter|blockchain",
    "meta": r"skill.creator|skill.author|meta.skill|find.skills|improve.skills",
    "accessibility": r"accessib|a11y|wcag", "performance": r"performance|optimiz|profil",
    "memory": r"memory|context.window|persistent", "agents": r"agent|subagent|multi.agent|orchestr",
}
SKILL_CATEGORY_HINTS = [
    ("security", r"security|vulnerab|pentest|exploit|owasp|threat|malware|reverse|ctf|red.?team|audit"),
    ("documents", r"\bpdf\b|\bdocx\b|\bpptx\b|\bxlsx\b|document|spreadsheet|slides|office|obsidian"),
    ("data", r"\bdata\b|sql|database|duckdb|paper|research|academic|science|huggingface|dataset|analytics"),
    ("meta", r"skill.creator|skill.author|find.skills|meta.skill|skill.opt|generator"),
    ("writing", r"writing|humaniz|prose|edit|blog|content|copywriting"),
    ("design", r"design|\bui\b|\bux\b|frontend|css|tailwind|animation|gsap|visual|brand|diagram|icon|svg|art.direction"),
    ("business", r"marketing|seo|product|\bprd\b|okr|roadmap|founder|startup|growth|sales|finance|linkedin|\bcro\b"),
    ("engineering", r"code|review|\btdd\b|debug|\bapi\b|typescript|react|nextjs|\bgit\b|test|playwright"),
    ("devops", r"deploy|docker|kubernetes|aws|azure|gcp|cloud"),
    ("workflow", r"workflow|planning|memory|orchestr|agent|context"),
]
SECURITY_SKILL_RE = re.compile(SKILL_CATEGORY_HINTS[0][1], re.I)
CATEGORY_HINTS = [
    ("security", r"security|vulnerab|pentest|audit|ctf|offensive|red.team|hack"),
    ("design", r"design|ui|ux|frontend|animation|css|gsap|art.direction|diagram"),
    ("documents", r"document|pdf|docx|pptx|xlsx|office|obsidian|slides|workspace"),
    ("business", r"marketing|seo|product|founder|startup|growth|sales|finance|linkedin"),
    ("data", r"science|research|data|duckdb|huggingface|llm|academic|paper|database"),
    ("devops", r"cloud|deploy|devops|kubernetes|docker|vercel|gcp|aws|azure"),
    ("meta", r"skill.creator|authoring|best.practices|meta.skill|skill.opt|generator"),
    ("writing", r"writing|humaniz|editing|prose|readme|copywriting"),
    ("workflow", r"workflow|planning|memory|orchestr|agent|context"),
    ("engineering", r"engineer|code|review|tdd|debug|api|typescript|react"),
]


def log(*args):
    print(*args, file=sys.stderr)


def get_token() -> str | None:
    for key in ("GITHUB_TOKEN", "GH_TOKEN", "GITHUB_API_TOKEN"):
        if os.environ.get(key):
            return os.environ[key].strip()
    try:
        return subprocess.check_output(["gh", "auth", "token"], text=True, timeout=10).strip()
    except Exception:
        return None


TOKEN = get_token()


class GitHub:
    def __init__(self, token: str | None):
        self.token = token

    def get(self, path: str, params: dict | None = None, raw: bool = False, tries: int = 4):
        url = API + path
        if params:
            sep = "&" if "?" in url else "?"
            url += sep + urllib.parse.urlencode(params)
        headers = {
            "Accept": "application/vnd.github.raw" if raw else "application/vnd.github+json",
            "User-Agent": "skills-library-catalog-builder",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = "Bearer " + self.token
        for attempt in range(tries):
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=45) as resp:
                    body = resp.read().decode("utf-8", errors="replace")
                return body if raw else json.loads(body) if body.strip() else None
            except urllib.error.HTTPError as e:
                if e.code in (403, 429):
                    reset = e.headers.get("X-RateLimit-Reset")
                    wait = 5 + attempt * 5
                    if reset and reset.isdigit():
                        wait = max(wait, min(60, int(reset) - int(time.time()) + 2))
                    log(f"rate limited on {path}; sleeping {wait}s")
                    time.sleep(wait)
                    continue
                if e.code == 404:
                    return None
                if e.code >= 500:
                    time.sleep(2 + attempt * 2)
                    continue
                log(f"HTTP {e.code} for {path}: {e.reason}")
                return None
            except Exception as e:
                if attempt == tries - 1:
                    log(f"request failed for {path}: {e}")
                    return None
                time.sleep(1 + attempt)
        return None


GH = GitHub(TOKEN)


def spdx(meta: dict) -> str | None:
    lic = meta.get("license")
    if isinstance(lic, dict):
        return lic.get("spdx_id")
    return lic or None


def license_info(meta: dict, license_files: list[str], override: str | None = None) -> dict:
    value = spdx(meta)
    if value and value != "NOASSERTION":
        status = "clear" if value in PERMISSIVE or value in COPYLEFT else "check"
        label = value
    elif license_files:
        status, label = "per-skill", "Per-skill licenses"
    else:
        status, label = "unknown", "No license detected"
    return {
        "spdx": value,
        "status": status,
        "label": label,
        "note": override,
        "files": license_files[:8],
    }


def days_since(iso: str | None) -> int | None:
    if not iso:
        return None
    try:
        d = dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return max(0, (NOW - d).days)
    except Exception:
        return None


def freshness(days: int | None) -> str:
    if days is None:
        return "unknown"
    if days <= 90:
        return "active"
    if days <= 365:
        return "maintained"
    return "stale"


def normalize_meta(meta: dict) -> dict:
    return {
        "repo": meta.get("full_name"),
        "owner": (meta.get("owner") or {}).get("login") or (meta.get("full_name") or "").split("/")[0],
        "name": meta.get("name"),
        "url": meta.get("html_url") or f"https://github.com/{meta.get('full_name')}",
        "homepage": meta.get("homepage") or None,
        "description": meta.get("description") or "",
        "stars": int(meta.get("stargazers_count") or 0),
        "forks": int(meta.get("forks_count") or 0),
        "openIssues": int(meta.get("open_issues_count") or 0),
        "language": meta.get("language"),
        "topics": meta.get("topics") or [],
        "branch": meta.get("default_branch") or "main",
        "pushedAt": meta.get("pushed_at"),
        "createdAt": meta.get("created_at"),
        "archived": bool(meta.get("archived")),
        "fork": bool(meta.get("fork")),
        "license": spdx(meta),
        "ownerType": (meta.get("owner") or {}).get("type"),
    }


def fetch_tree(repo: str, branch: str) -> tuple[str, dict]:
    ref = urllib.parse.quote(branch, safe="")
    data = GH.get(f"/repos/{repo}/git/trees/{ref}?recursive=1") or {}
    paths = [x["path"] for x in data.get("tree", []) if x.get("type") == "blob"]
    skill_paths = [p for p in paths if p == "SKILL.md" or p.endswith("/SKILL.md")]
    folders = []
    for p in skill_paths:
        folder = posixpath.basename(posixpath.dirname(p)) if "/" in p else repo.split("/")[1]
        if folder not in folders:
            folders.append(folder)
    license_files = [
        p for p in paths
        if posixpath.basename(p).lower().startswith(("license", "licence", "copying"))
        or posixpath.basename(p).lower().endswith(("license.md", "license.txt", "licence.md"))
    ]
    return repo, {
        "paths": paths,
        "skillPaths": skill_paths,
        "folders": folders,
        "licenseFiles": license_files,
        "truncated": bool(data.get("truncated")),
        "blobCount": len(paths),
    }


def discover(queries: list[str]) -> dict[str, dict]:
    found: dict[str, dict] = {}
    for q in queries:
        res = GH.get("/search/repositories", {"q": q, "sort": "stars", "order": "desc", "per_page": 50}) or {}
        items = res.get("items", [])
        for item in items:
            found[item["full_name"]] = item
        log(f"search {q!r}: {len(items)} results (total {res.get('total_count', '?')})")
        time.sleep(0.12)
    return found


def looks_like_skills(meta: dict) -> bool:
    text = " ".join([meta.get("name") or "", meta.get("description") or "", " ".join(meta.get("topics") or [])]).lower()
    return "skill" in text or "skills" in text


def guess_category(meta: dict) -> str:
    text = " ".join([meta.get("name") or "", meta.get("description") or "", " ".join(meta.get("topics") or [])]).lower()
    for cat, pattern in CATEGORY_HINTS:
        if re.search(pattern, text):
            return cat
    return "specialized"


def skill_category(name: str, description: str, folder: str, base_category: str) -> str:
    """Classify an individual skill from its own name/folder, not generic prose."""
    text = " ".join([folder.replace("-", " ").replace("_", " "), name]).lower()
    for cat, pattern in SKILL_CATEGORY_HINTS:
        if re.search(pattern, text):
            return cat
    return base_category


def collection_score(meta: dict, unique_skills: int, official: bool, featured: bool) -> float:
    stars = math.log10(meta["stars"] + 1) * 10
    breadth = math.log10(unique_skills + 1) * 4
    days = days_since(meta["pushedAt"]) or 9999
    recency = 8 if days <= 90 else 4 if days <= 365 else 0
    bonus = (6 if official else 0) + (5 if featured else 0)
    return round(stars + breadth + recency + bonus, 2)


def make_collection(meta: dict, tree: dict, lic: dict, *, category: str, tags: list[str],
                    official: bool, featured: bool, tier: str, reviewed: bool,
                    note: str | None, note_pl: str | None, packs: list[str]) -> dict:
    days = days_since(meta["pushedAt"])
    unique = len(tree["folders"])
    source_type = "directory" if unique == 0 else "single" if unique == 1 else "collection"
    install = f"npx skills add {meta['repo']}" if unique else f"git clone {meta['url']}.git  # directory: open its README"
    return {
        "id": meta["repo"],
        "repo": meta["repo"],
        "owner": meta["owner"],
        "name": meta["name"],
        "url": meta["url"],
        "homepage": meta["homepage"],
        "description": meta["description"],
        "note": note,
        "notePl": note_pl,
        "category": category,
        "tags": tags,
        "stars": meta["stars"],
        "forks": meta["forks"],
        "language": meta["language"],
        "topics": meta["topics"][:12],
        "branch": meta["branch"],
        "pushedAt": meta["pushedAt"],
        "daysSincePush": days,
        "freshness": freshness(days),
        "archived": meta["archived"],
        "license": lic,
        "skillCount": unique,
        "sourceType": source_type,
        "skillFileCount": len(tree["skillPaths"]),
        "truncatedTree": tree["truncated"],
        "official": official,
        "featured": featured,
        "tier": tier,
        "reviewed": reviewed,
        "packs": packs,
        "score": collection_score(meta, unique, official, featured),
        "install": install,
        "verifiedSkills": tree["truncated"] is False and unique > 0,
    }


def safe_use_notes(category: str, description: str, security_signal: bool = False) -> list[dict]:
    notes = []
    if category == "security" or security_signal:
        notes.append({"code": "security", **SAFE_USE["security"]})
    if len(CJK_RE.findall(description)) >= 8:
        notes.append({"code": "chinese", **SAFE_USE["chinese"]})
    return notes


def path_is_candidate(path: str) -> bool:
    parts = path.split("/")[:-1]
    if any(p in EXCLUDE_SEGMENTS or p.upper() == "SKILL.MD" for p in parts):
        return False
    if "PULL_REQUEST_TEMPLATE" in path or "ISSUE_TEMPLATE" in path:
        return False
    return True


def path_score(path: str) -> float:
    parts = path.split("/")[:-1]
    score = 0.0
    if parts and parts[0] == "skills":
        score -= 12
    if "skills" in parts:
        score -= 6
    if any(p.startswith(".") for p in parts):
        score += 8
    for penalty in ("plugins", "external_plugins", "bundled", "marketplace", "automations", "library", "vendor"):
        if penalty in parts:
            score += 3
    if any(p in (".curated", ".system") for p in parts):
        score += 1
    return score + len(parts) * 0.4


def folder_of(path: str, repo: str) -> str:
    return posixpath.basename(posixpath.dirname(path)) if "/" in path else repo.split("/")[1]


def parse_frontmatter(text: str) -> dict:
    out: dict = {}
    if not text.startswith("---"):
        return out
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return out
    end = None
    for i in range(1, min(len(lines), 80)):
        if lines[i].strip() in ("---", "..."):
            end = i
            break
    if end is None:
        return out
    block = lines[1:end]
    i = 0
    while i < len(block):
        line = block[i]
        m = re.match(r"^([A-Za-z0-9_.-]+)\s*:\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key, value = m.group(1).strip().lower(), m.group(2).strip()
        if value in (">", "|", ">-", ">- ", "|+", "+", ">-|", ">-+", ">-", ">+", ">- "):
            collected = []
            i += 1
            while i < len(block) and (block[i].startswith(" ") or block[i].startswith("\t") or not block[i].strip()):
                collected.append(block[i].strip())
                i += 1
            out[key] = " ".join(x for x in collected if x).strip()
            continue
        if value.startswith("[") and value.endswith("]"):
            out[key] = [x.strip().strip("'\"") for x in value[1:-1].split(",") if x.strip()]
        else:
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            out[key] = value
        i += 1
    return out


def clean_text(value: str, limit: int = 600) -> str:
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value or "")
    value = re.sub(r"\s+", " ", value).strip()
    value = value.replace("</", "<\\/")
    if len(value) > limit:
        value = value[:limit].rsplit(" ", 1)[0] + "…"
    return value


def short_text(value: str, limit: int = 190) -> str:
    if len(value) <= limit:
        return value
    return value[:limit].rsplit(" ", 1)[0] + "…"


def humanize(name: str) -> str:
    name = re.sub(r"[_-]+", " ", name).strip()
    return name[:1].upper() + name[1:] if name else name


def first_paragraph(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() in ("---", "..."):
                lines = lines[i + 1:]
                break
    for line in lines:
        s = line.strip()
        if not s or s.startswith(("#", "```", "---", "<!--", "|", ">")):
            continue
        if len(s) < 25:
            continue
        return clean_text(s)
    return ""


def detect_tags(text: str, base: list[str]) -> list[str]:
    hay = text.lower()
    tags = list(dict.fromkeys(base))
    for tag, pattern in KEYWORDS.items():
        if tag not in tags and re.search(pattern, hay):
            tags.append(tag)
    return tags[:16]


def review_flags(text: str, allowed_tools, siblings: list[str]) -> dict:
    low = text.lower()
    has_scripts = any(
        p.lower().endswith(SCRIPT_EXTS) or "/scripts/" in p.lower() or p.lower().endswith(".jar")
        for p in siblings
    )
    suspicious = any(x in low for x in ("curl ", "wget ", "sudo ", "rm -rf", "eval ", "chmod +x", "git clone ", "pip install", "npm install"))
    network = "http://" in low or "https://" in low
    shell = "```bash" in low or "```sh" in low or "```shell" in low
    tools = []
    if isinstance(allowed_tools, str):
        tools = [x.strip() for x in re.split(r"[,\s]+", allowed_tools) if x.strip()]
    elif isinstance(allowed_tools, list):
        tools = [str(x) for x in allowed_tools]
    return {
        "hasScripts": has_scripts,
        "network": network,
        "shell": shell,
        "allowedTools": tools[:12],
        "requiresReview": bool(has_scripts or suspicious or tools),
    }


def quote_path(path: str) -> str:
    return urllib.parse.quote(path, safe="/")


def skill_commands(meta: dict, folder: str, skill_dir: str) -> dict:
    repo, branch = meta["repo"], meta["branch"]
    if skill_dir:
        direct = f"npx skills add https://github.com/{repo}/tree/{branch}/{quote_path(skill_dir)}"
        manual = (
            f"git clone --depth 1 https://github.com/{repo}.git /tmp/{meta['name']} && "
            f"cp -r /tmp/{meta['name']}/{skill_dir} .agents/skills/{folder}"
        )
    else:
        direct = f"npx skills add {repo}"
        manual = (
            f"git clone --depth 1 https://github.com/{repo}.git /tmp/{meta['name']} && "
            f"cp -r /tmp/{meta['name']} .agents/skills/{folder}"
        )
    return {
        "direct": direct,
        "shorthand": f"npx skills add {repo} --skill {folder}",
        "global": direct + " -g -y",
        "use": f"npx skills use {repo}@{folder}",
        "manual": manual,
        "collection": f"npx skills add {repo}",
    }


def fetch_skill_text(repo: str, branch: str, path: str) -> str | None:
    ref = urllib.parse.quote(branch, safe="")
    p = f"/repos/{repo}/contents/{quote_path(path)}?ref={ref}"
    return GH.get(p, raw=True)


def build_collections(config: dict, discovered: dict[str, dict], trees: dict[str, dict], canonical: dict[str, str]) -> tuple[list[dict], dict[str, dict]]:
    by_repo: dict[str, dict] = {}
    for src in config["sources"]:
        repo = canonical.get(src["repo"], src["repo"])
        meta = discovered.get(repo)
        tree = trees.get(repo)
        if not meta or not tree:
            log("skipping curated source without metadata/tree:", src["repo"])
            continue
        lic = license_info(meta, tree["licenseFiles"], src.get("license_note"))
        owner = meta["owner"].lower()
        official = bool(src.get("official")) or owner in OFFICIAL_ORGS
        c = make_collection(
            meta, tree, lic,
            category=src["category"], tags=src["tags"], official=official,
            featured=bool(src.get("featured")), tier=src.get("tier", "curated"),
            reviewed=True, note=src.get("note"), note_pl=src.get("note_pl"),
            packs=src.get("packs", []),
        )
        c["maxSkills"] = src.get("maxSkills", 0)
        c["picks"] = src.get("picks", [])
        by_repo[repo] = c
    curated_repos = set(by_repo)
    exclude = set(config.get("excludeFromDiscovery", []))
    auto: list[dict] = []
    for repo, meta in discovered.items():
        if repo in curated_repos or repo in exclude:
            continue
        tree = trees.get(repo)
        if not tree or not tree["folders"] or not looks_like_skills(meta):
            continue
        if meta["archived"] or meta["fork"] or meta["stars"] < 2000:
            continue
        days = days_since(meta["pushedAt"]) or 9999
        if days > 730:
            continue
        lic = license_info(meta, tree["licenseFiles"])
        if lic["status"] == "unknown":
            continue
        c = make_collection(
            meta, tree, lic,
            category=guess_category(meta), tags=["auto-discovered", "community"],
            official=meta["owner"].lower() in OFFICIAL_ORGS, featured=False,
            tier="discovered", reviewed=False,
            note="Automatically discovered from GitHub search — not editorially reviewed. Verify the source before installing.",
            note_pl="Znalezione automatycznie w wyszukiwarce GitHub — bez ręcznej weryfikacji. Sprawdź źródło przed instalacją.",
            packs=[],
        )
        c["maxSkills"] = 0
        c["picks"] = []
        auto.append(c)
    auto.sort(key=lambda x: -x["stars"])
    auto = auto[:120]
    collections = list(by_repo.values()) + auto
    return collections, by_repo


def build_skills(config: dict, by_repo: dict[str, dict], trees: dict[str, dict], canonical: dict[str, str]) -> list[dict]:
    # Force-include every skill referenced from a starter pack or the spotlight.
    force: dict[str, list[str]] = {}
    for pack in config["packs"]:
        for repo, folder in pack["skills"]:
            force.setdefault(canonical.get(repo, repo), []).append(folder)
    for item in config["spotlight"]:
        force.setdefault(canonical.get(item["repo"], item["repo"]), []).append(item["folder"])
    spotlight_ids = {f"{canonical.get(x['repo'], x['repo'])}/{x['folder']}" for x in config["spotlight"]}

    tasks: list[tuple[dict, str, str, str]] = []
    for repo, col in by_repo.items():
        max_skills = col.get("maxSkills", 0)
        if max_skills <= 0:
            continue
        tree = trees[repo]
        candidates: dict[str, list[tuple[float, str]]] = {}
        for path in tree["skillPaths"]:
            if not path_is_candidate(path):
                continue
            folder = folder_of(path, repo)
            candidates.setdefault(folder, []).append((path_score(path), path))
        picks = list(dict.fromkeys(col.get("picks", []) + force.get(repo, [])))
        pick_rank = {f: i for i, f in enumerate(picks)}
        chosen: list[tuple[str, str, str]] = []
        for folder, options in candidates.items():
            options.sort(key=lambda x: (x[0], x[1]))
            chosen.append((folder, options[0][1], posixpath.dirname(options[0][1])))
        chosen.sort(key=lambda x: (pick_rank.get(x[0], 9999), path_score(x[1]), x[0]))
        limit = max(max_skills, len(picks))
        for folder, path, skill_dir in chosen[:limit]:
            tasks.append((col, path, folder, skill_dir))
    log(f"fetching {len(tasks)} SKILL.md frontmatters")

    def work(task):
        col, path, folder, skill_dir = task
        text = fetch_skill_text(col["repo"], col["branch"], path)
        return task, text

    results: list[tuple[tuple, str | None]] = []
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        for i, res in enumerate(ex.map(work, tasks)):
            results.append(res)
            if i and i % 100 == 0:
                log(f"  fetched {i}/{len(tasks)}")

    skills: list[dict] = []
    for (col, path, folder, skill_dir), text in results:
        if not text or len(text) > 400_000:
            continue
        fm = parse_frontmatter(text)
        name = clean_text(str(fm.get("name") or folder), 100)
        description = clean_text(str(fm.get("description") or ""), 600) or first_paragraph(text) or clean_text(col["description"], 300)
        if not description:
            description = "Open-source Agent Skill from " + col["repo"]
        spec = bool(fm.get("name")) and bool(fm.get("description"))
        tree = trees[col["repo"]]
        prefix = skill_dir + "/" if skill_dir else ""
        siblings = [p for p in tree["paths"] if p.startswith(prefix) and p != path]
        flags = review_flags(text, fm.get("allowed-tools") or fm.get("allowed_tools"), siblings)
        source_url = f"https://github.com/{col['repo']}/blob/{col['branch']}/{quote_path(path)}"
        raw_url = f"https://raw.githubusercontent.com/{col['repo']}/{col['branch']}/{quote_path(path)}"
        sid = f"{col['repo']}/{folder}"
        is_spotlight = sid in spotlight_ids
        category = skill_category(name, description, folder, col["category"])
        tags = detect_tags(" ".join([name, description, folder, " ".join(col["tags"])]), col["tags"])
        security_signal = bool(SECURITY_SKILL_RE.search(f"{folder} {name}"))
        skill_score = round(col["score"] + (12 if is_spotlight else 0) + (4 if spec else 0) + (3 if col["official"] else 0), 2)
        skills.append({
            "id": sid,
            "collectionId": col["id"],
            "repo": col["repo"],
            "owner": col["owner"],
            "folder": folder,
            "name": name,
            "title": humanize(name),
            "description": description,
            "shortDescription": short_text(description),
            "path": path,
            "skillDir": skill_dir,
            "sourceUrl": source_url,
            "rawUrl": raw_url,
            "category": category,
            "tags": tags,
            "license": {
                "status": col["license"]["status"],
                "label": col["license"]["label"],
                "spdx": col["license"]["spdx"],
                "note": col["license"]["note"],
            },
            "stars": col["stars"],
            "pushedAt": col["pushedAt"],
            "daysSincePush": col["daysSincePush"],
            "freshness": col["freshness"],
            "official": col["official"],
            "featured": col["featured"],
            "tier": col["tier"],
            "reviewed": col["reviewed"],
            "spotlight": is_spotlight,
            "specCompliant": spec,
            "verified": True,
            "contentLength": len(text),
            "frontmatter": {k: (v if isinstance(v, (str, int, float, bool)) else [str(x) for x in v]) for k, v in list(fm.items())[:12] if k in ("name", "description", "license", "compatibility", "metadata", "allowed-tools", "allowed_tools", "version")},
            "review": flags,
            "safeUse": safe_use_notes(category, description, security_signal),
            "install": skill_commands({"repo": col["repo"], "branch": col["branch"], "name": col["name"]}, folder, skill_dir),
            "score": skill_score,
        })
    skills.sort(key=lambda s: (-s["score"], s["repo"], s["folder"]))
    return skills


def resolve_packs(config: dict, skills: list[dict], canonical: dict[str, str]) -> list[dict]:
    by_id = {s["id"]: s for s in skills}
    out = []
    for pack in config["packs"]:
        ids, commands = [], []
        for repo, folder in pack["skills"]:
            sid = f"{canonical.get(repo, repo)}/{folder}"
            if sid in by_id:
                ids.append(sid)
                commands.append(by_id[sid]["install"]["direct"])
        out.append({
            "id": pack["id"], "icon": pack["icon"],
            "title": {"en": pack["en"], "pl": pack["pl"]},
            "description": {"en": pack["desc_en"], "pl": pack["desc_pl"]},
            "skills": ids,
            "commands": commands,
            "script": "\n".join(commands),
        })
    return out


AGENTS = [
    {"name": "Claude Code", "id": "claude-code", "project": ".claude/skills/", "global": "~/.claude/skills/"},
    {"name": "Codex / Copilot / Cursor / Gemini CLI", "id": "codex", "project": ".agents/skills/", "global": "~/.agents/skills/"},
    {"name": "Cursor (global)", "id": "cursor", "project": ".agents/skills/", "global": "~/.cursor/skills/"},
    {"name": "OpenCode / Amp / Replit", "id": "opencode", "project": ".agents/skills/", "global": "~/.config/opencode/skills/"},
    {"name": "Gemini CLI (global)", "id": "gemini-cli", "project": ".agents/skills/", "global": "~/.gemini/skills/"},
    {"name": "GitHub Copilot (global)", "id": "github-copilot", "project": ".agents/skills/", "global": "~/.copilot/skills/"},
    {"name": "Windsurf", "id": "windsurf", "project": ".windsurf/skills/", "global": "~/.codeium/windsurf/skills/"},
    {"name": "OpenClaw", "id": "openclaw", "project": "skills/", "global": "~/.openclaw/skills/"},
]


def build_catalog(config: dict, discovered: dict[str, dict], trees: dict[str, dict], canonical: dict[str, str], do_discover: bool) -> dict:
    collections, by_repo = build_collections(config, discovered, trees, canonical)
    skills = build_skills(config, by_repo, trees, canonical)
    packs = resolve_packs(config, skills, canonical)
    skill_by_id = {s["id"]: s for s in skills}
    spotlight = [x for x in (f"{canonical.get(i['repo'], i['repo'])}/{i['folder']}" for i in config["spotlight"]) if x in skill_by_id]

    scan_repos = len(trees)
    with_skills = sum(1 for t in trees.values() if t["folders"])
    files = sum(len(t["skillPaths"]) for t in trees.values())
    unique = sum(len(t["folders"]) for t in trees.values())
    curated = [c for c in collections if c["reviewed"]]
    auto = [c for c in collections if not c["reviewed"]]
    cats = []
    for cat in config["categories"]:
        cats.append({
            **cat,
            "skillCount": sum(1 for s in skills if s["category"] == cat["id"]),
            "collectionCount": sum(1 for c in collections if c["category"] == cat["id"]),
        })

    meta = {
        "version": 1,
        "generatedAt": NOW.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "generatedDate": TODAY,
        "repository": "rejson59/skills-library",
        "license": "MIT",
        "dataSource": "GitHub REST API: search/repositories, repos, git/trees, contents",
        "spec": "https://agentskills.io",
        "cliDocs": "https://github.com/vercel-labs/skills/blob/main/docs/commands.md",
        "criteria": {
            "en": "Public GitHub repositories with at least one exact SKILL.md file. Curated tier is manually reviewed; discovered tier is automatic and unverified. License flags come from the GitHub API and repository trees. This is metadata curation, not a behavioral security audit.",
            "pl": "Publiczne repozytoria GitHub z co najmniej jednym plikiem SKILL.md. Warstwa kuratowana jest sprawdzona ręcznie, warstwa odkryta — automatycznie i bez weryfikacji. Oznaczenia licencji pochodzą z API GitHub i drzew repozytoriów. To katalog metadanych, nie audyt zachowania skilli.",
        },
        "stats": {
            "searchQueries": len(config["searchQueries"]) if do_discover else 0,
            "reposScanned": scan_repos,
            "reposWithSkills": with_skills,
            "skillFilesFound": files,
            "uniqueSkillFoldersFound": unique,
            "curatedCollections": len(curated),
            "discoveredCollections": len(auto),
            "collections": len(collections),
            "indexedSkills": len(skills),
            "officialCollections": sum(1 for c in collections if c["official"]),
            "clearLicenseCollections": sum(1 for c in collections if c["license"]["status"] == "clear"),
            "specCompliantSkills": sum(1 for s in skills if s["specCompliant"]),
            "skillsNeedingReview": sum(1 for s in skills if s["review"]["requiresReview"]),
        },
        "notes": {
            "en": "skillFilesFound counts every SKILL.md path, including copies published into several agent folders. uniqueSkillFoldersFound deduplicates by folder name inside one repository; the same skill may still appear in different repositories.",
            "pl": "skillFilesFound liczy każdą ścieżkę SKILL.md, także kopie publikowane w kilku folderach agentów. uniqueSkillFoldersFound deduplikuje po nazwie folderu w jednym repozytorium; ten sam skill może nadal występować w różnych repozytoriach.",
        },
    }
    return {
        "meta": meta,
        "categories": cats,
        "agents": AGENTS,
        "packs": packs,
        "spotlight": spotlight,
        "collections": collections,
        "skills": skills,
    }


def write_json(path: Path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_js(path: Path, obj):
    payload = json.dumps(obj, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
    path.write_text("window.__SKILLS_LIBRARY__ = " + payload + ";\n", encoding="utf-8")


def md_escape(value: str) -> str:
    return (value or "").replace("|", "\\|").replace("\n", " ").strip()


def write_catalog_md(catalog: dict):
    m = catalog["meta"]
    s = m["stats"]
    lines = [
        "# Skills Library — full catalog",
        "",
        f"> Generated **{m['generatedDate']}** from the GitHub API. "
        f"{s['reposScanned']} repositories scanned · {s['skillFilesFound']:,} `SKILL.md` files found · "
        f"{s['collections']} collections · **{s['indexedSkills']} individually indexed skills**.",
        "",
        "This file is generated by `scripts/build_catalog.py`. Do not edit by hand — edit "
        "[`data/sources.json`](data/sources.json) instead. For the full machine-readable dataset "
        "see [`data/catalog.json`](data/catalog.json).",
        "",
        "## Editor's picks",
        "",
        "| Skill | Source | Category | Install |",
        "| --- | --- | --- | --- |",
    ]
    by_id = {x["id"]: x for x in catalog["skills"]}
    for sid in catalog["spotlight"]:
        sk = by_id.get(sid)
        if not sk:
            continue
        lines.append(f"| [{md_escape(sk['title'])}]({sk['sourceUrl']}) | `{sk['repo']}` | {sk['category']} | `{sk['install']['direct']}` |")
    lines += ["", "## Curated collections", "", "| Repository | ★ | Skills | License | Category | Why it is here |", "| --- | ---: | ---: | --- | --- | --- |"]
    for c in sorted((x for x in catalog["collections"] if x["reviewed"]), key=lambda x: -x["stars"]):
        note = md_escape(c.get("note") or c["description"])
        lines.append(
            f"| [{c['repo']}]({c['url']}) | {c['stars']:,} | {c['skillCount']:,} | "
            f"{md_escape(c['license']['label'])} | {c['category']} | {note[:180]} |"
        )
    auto = sorted((x for x in catalog["collections"] if not x["reviewed"]), key=lambda x: -x["stars"])
    if auto:
        lines += ["", "## Automatically discovered (not editorially reviewed)", "", "| Repository | ★ | Skills | License | Last push |", "| --- | ---: | ---: | --- | --- |"]
        for c in auto:
            lines.append(f"| [{c['repo']}]({c['url']}) | {c['stars']:,} | {c['skillCount']:,} | {md_escape(c['license']['label'])} | {(c['pushedAt'] or '')[:10]} |")
    lines += [
        "",
        "## Install",
        "",
        "```bash",
        "# one skill (direct path works even for nested plugin layouts)",
        "npx skills add https://github.com/anthropics/skills/tree/main/skills/pdf",
        "",
        "# a whole collection",
        "npx skills add obra/superpowers",
        "",
        "# global install for all your projects",
        "npx skills add obra/superpowers --skill test-driven-development -g -y",
        "```",
        "",
        "See [docs/INSTALL.md](docs/INSTALL.md) for the compatibility matrix and "
        "[SECURITY.md](SECURITY.md) for the trust model.",
        "",
    ]
    (ROOT / "CATALOG.md").write_text("\n".join(lines), encoding="utf-8")


def write_llms_txt(catalog: dict):
    m, s = catalog["meta"], catalog["meta"]["stats"]
    lines = [
        "# Skills Library",
        "",
        "> An open, reproducible index of the best open-source Agent Skills (SKILL.md) on GitHub.",
        "> Maintained at https://github.com/rejson59/skills-library",
        "",
        f"Generated: {m['generatedDate']}",
        f"Scanned repositories: {s['reposScanned']}",
        f"SKILL.md files found: {s['skillFilesFound']}",
        f"Collections in catalog: {s['collections']} ({s['curatedCollections']} curated, {s['discoveredCollections']} auto-discovered)",
        f"Individually indexed skills: {s['indexedSkills']}",
        "",
        "## Machine-readable data",
        "",
        "- data/catalog.json — full catalog: meta, categories, agents, packs, spotlight, collections, skills",
        "- data/catalog.js — the same object as `window.__SKILLS_LIBRARY__` for the static website",
        "- data/discovered.json — repositories found automatically but not editorially reviewed",
        "- data/schema.json — JSON Schema for catalog.json",
        "- CATALOG.md — human-readable markdown catalog",
        "",
        "## Skill record fields",
        "",
        ", ".join(catalog["skills"][0].keys()) + ".",
        "",
        "## Collection record fields",
        "",
        ", ".join(catalog["collections"][0].keys()) + ".",
        "",
        "## Install a skill",
        "",
        "npx skills add https://github.com/<owner>/<repo>/tree/<branch>/<path-to-skill-folder>",
        "npx skills add <owner>/<repo> --skill <folder>        # when the CLI can discover it",
        "npx skills add <owner>/<repo> --skill <folder> -g -y   # global",
        "",
        "## Top curated collections",
        "",
    ]
    for c in sorted((x for x in catalog["collections"] if x["reviewed"] and x["featured"]), key=lambda x: -x["stars"])[:25]:
        lines.append(f"- {c['repo']} — {c['stars']:,} stars, {c['skillCount']:,} unique skills — {c['url']}")
    lines += [
        "",
        "## Trust",
        "",
        "Skills are third-party instructions and may contain scripts. This catalog verifies",
        "metadata and SKILL.md existence; it does not audit behavior. Always read the source",
        "and check the upstream license before installing.",
        "",
    ]
    (ROOT / "llms.txt").write_text("\n".join(lines), encoding="utf-8")


def update_readme_stats(path: Path, catalog: dict, lang: str):
    if not path.exists():
        return
    s = catalog["meta"]["stats"]
    if lang == "pl":
        block = (
            f"| {s['reposScanned']} | {s['skillFilesFound']:,} | {s['uniqueSkillFoldersFound']:,} | "
            f"{s['curatedCollections']} | {s['indexedSkills']} | {catalog['meta']['generatedDate']} |"
        )
    else:
        block = (
            f"| {s['reposScanned']} | {s['skillFilesFound']:,} | {s['uniqueSkillFoldersFound']:,} | "
            f"{s['curatedCollections']} | {s['indexedSkills']} | {catalog['meta']['generatedDate']} |"
        )
    text = path.read_text(encoding="utf-8")
    start, end = "<!-- STATS:START -->", "<!-- STATS:END -->"
    if start in text and end in text:
        before, rest = text.split(start, 1)
        _, after = rest.split(end, 1)
        lines = [x for x in block.splitlines() if x.strip()]
        new = before + start + "\n" + "\n".join(lines) + "\n" + end + after
        path.write_text(new, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--no-discover", action="store_true", help="skip GitHub search discovery; use curated sources only")
    ap.add_argument("--max-repos", type=int, default=700, help="cap the number of repositories scanned")
    args = ap.parse_args()
    if not TOKEN:
        log("warning: no GitHub token found; unauthenticated API limits apply")
    config = json.loads((DATA / "sources.json").read_text(encoding="utf-8"))
    do_discover = not args.no_discover
    discovered: dict[str, dict] = discover(config["searchQueries"]) if do_discover else {}
    log(f"discovered {len(discovered)} unique repositories")

    canonical: dict[str, str] = {}
    for src in config["sources"]:
        original = src["repo"]
        if original in discovered:
            canonical[original] = original
            continue
        item = GH.get("/repos/" + original)
        if not item:
            log("curated source not found:", original)
            continue
        real = item["full_name"]
        canonical[original] = real
        discovered[real] = item
        if real != original:
            log(f"canonicalized {original} -> {real}")
    # canonicalize references
    for pack in config["packs"]:
        pack["skills"] = [(canonical.get(r, r), f) for r, f in pack["skills"]]
    for item in config["spotlight"]:
        item["repo"] = canonical.get(item["repo"], item["repo"])

    metas: dict[str, dict] = {}
    for repo, item in discovered.items():
        if len(metas) >= args.max_repos:
            break
        metas[repo] = normalize_meta(item)
    # curated sources must always be present
    for src in config["sources"]:
        repo = canonical.get(src["repo"], src["repo"])
        if repo not in metas and repo in discovered:
            metas[repo] = normalize_meta(discovered[repo])
    log(f"fetching recursive trees for {len(metas)} repositories")
    trees: dict[str, dict] = {}
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(fetch_tree, repo, meta["branch"]): repo for repo, meta in metas.items()}
        for i, fut in enumerate(cf.as_completed(futs)):
            repo = futs[fut]
            try:
                _, tree = fut.result()
                trees[repo] = tree
            except Exception as e:
                log("tree failed", repo, e)
                trees[repo] = {"paths": [], "skillPaths": [], "folders": [], "licenseFiles": [], "truncated": True, "blobCount": 0}
            if i and i % 100 == 0:
                log(f"  trees {i}/{len(futs)}")

    catalog = build_catalog(config, metas, trees, canonical, do_discover)
    DATA.mkdir(exist_ok=True)
    write_json(DATA / "catalog.json", catalog)
    write_js(DATA / "catalog.js", catalog)
    write_json(DATA / "discovered.json", {
        "generatedAt": catalog["meta"]["generatedAt"],
        "count": len([c for c in catalog["collections"] if not c["reviewed"]]),
        "repositories": [c for c in catalog["collections"] if not c["reviewed"]],
    })
    write_catalog_md(catalog)
    write_llms_txt(catalog)
    update_readme_stats(ROOT / "README.md", catalog, "en")
    update_readme_stats(ROOT / "README.pl.md", catalog, "pl")
    s = catalog["meta"]["stats"]
    log("DONE", json.dumps(s, ensure_ascii=False))
    log(f"catalog.json: {(DATA / 'catalog.json').stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
