---
name: skill-finder
description: Find the best open-source Agent Skill for a task using the Skills Library catalog (rejson59/skills-library). Use when the user asks "how do I do X", "find a skill for X", "is there a skill that can...", wants to extend an AI coding agent, or asks which Claude Code / Codex / Cursor / Gemini CLI skills to install.
license: MIT
compatibility: Works in any agent that can read files and optionally fetch one JSON file. No API keys required.
metadata:
  version: 1.0.0
  catalog: https://raw.githubusercontent.com/rejson59/skills-library/main/data/catalog.json
  website: https://github.com/rejson59/skills-library
---

# Skill Finder — Skills Library

You help the user find **existing, open-source Agent Skills** instead of
reinventing instructions from scratch. The source of truth is the Skills Library
catalog: a generated index of real `SKILL.md` files on GitHub with stars,
licenses, freshness and review flags.

## When to use this skill

- "How do I make my agent do X?"
- "Find a skill for PDF / React / security audit / TDD / market research"
- "Which skills should I install in Claude Code / Codex / Cursor?"
- "Is there a skill that can ...?"
- The user wants to extend, configure or audit an AI coding agent.

## Step 1 — Understand the request

Identify: the **domain**, the **concrete task**, the **target agent** (Claude
Code, Codex, Cursor, Gemini CLI, Copilot, OpenCode, …) and whether the user wants
one skill, a bundle, or a comparison. Ask one short clarifying question only if
the task is genuinely ambiguous.

Reply in the user's language. Polish in → Polish out.

## Step 2 — Query the catalog

Prefer the local catalog if you are inside the `skills-library` repository:

```bash
python3 scripts/query_catalog.py search "react best practices" --limit 5
python3 scripts/query_catalog.py collection anthropics/skills
python3 scripts/query_catalog.py install anthropics/skills/pdf
```

When installed as a standalone skill, only this folder is copied. Fetch the
catalog JSON instead (no authentication needed):

```bash
curl -fsSL https://raw.githubusercontent.com/rejson59/skills-library/main/data/catalog.json \
  | python3 -c 'import json,sys; c=json.load(sys.stdin); q=sys.argv[1].lower(); hits=[s for s in c["skills"] if q in " ".join([s["id"],s["title"],s["description"]," ".join(s["tags"])]).lower()][:5]; [print(s["id"],"|",s["shortDescription"],"|",s["install"]["direct"]) for s in hits]' "security audit"
```

Or read it directly with Python's `urllib.request`. Useful fields:

- `collections[]`: `repo`, `stars`, `skillCount`, `sourceType`, `license`, `tier`, `reviewed`, `install`
- `skills[]`: `id`, `title`, `shortDescription`, `tags`, `category`, `official`,
  `license`, `specCompliant`, `review.requiresReview`, `safeUse`, `sourceUrl`, `install.direct`
- `packs[]`: `id`, `title.en/pl`, `description.en/pl`, `script`
- `meta.stats`, `meta.generatedDate`

If the catalog is unreachable, fall back to `npx skills find "<query>"` and say
clearly that results are not covered by this catalog's verification.

A short offline shortlist is in `references/top-collections.md`.

## Step 3 — Rank and filter

Prefer, in this order:

1. `official: true` and vendor-maintained collections (`anthropics/skills`,
   `openai/skills`, `google/skills`, `vercel-labs/agent-skills`,
   `github/awesome-copilot`, `cloudflare/security-audit-skill`, …).
2. `reviewed: true` over `tier: "discovered"`.
3. `license.status` of `clear` or `per-skill`; always surface `unknown` /
   `check` and any `license.note`.
4. `specCompliant: true` (frontmatter has `name` + `description`).
5. Every `safeUse[]` note: security skills require explicit authorization and
   Chinese-language descriptions should be reviewed/translated before use.
6. Recently pushed, high stars, and matching tags/category.
7. Starter packs (`packs[]`) when the user needs several related skills.

Never treat `review.requiresReview === false` as "safe". It only means no
script/tool heuristic fired.

## Step 4 — Present 3–5 options

For each candidate show:

- **name + id** and one sentence of what it does,
- **source**: the `sourceUrl` (always let the user inspect the upstream file),
- **license**: exact label + status,
- **signals**: official / curated / stars / freshness / review flag,
- **safe-use notes**: surface every `safeUse[].en` / `.pl` note when present,
- **install command**: the `install.direct` string.

Example:

```text
PDF — anthropics/skills/pdf
Creates, reads, merges and fills real PDF files. Official Anthropic reference skill.
Source: https://github.com/anthropics/skills/blob/main/skills/pdf/SKILL.md
License: Per-skill licenses (check LICENSE.txt) · reviewed · spec-compliant

npx skills add https://github.com/anthropics/skills/tree/main/skills/pdf
```

For a bundle, show `packs[].script` and remind the user to review every line.

## Step 5 — Install only with consent

Always say: skills are third-party instructions and may contain scripts; read
the `SKILL.md` and check the license before installing. Then:

```bash
# one skill, project-local
npx skills add https://github.com/<owner>/<repo>/tree/<branch>/<path-to-skill-folder>

# global, non-interactive, one agent
npx skills add <owner>/<repo> --skill <folder> -g -a claude-code -y

# try without installing
npx skills use <owner>/<repo>@<folder>
```

Ask before executing anything. Prefer project-local first. If the user has no
Node.js, give the manual `git clone` + `cp -r <skill-folder> .agents/skills/<name>`
form from the `install.manual` field.

## Hard rules

- Do **not** invent skill IDs, star counts, licenses or descriptions.
- Do **not** claim a third-party skill is safe, audited or virus-free.
- Do **not** copy upstream skill bodies into the user's project; link to them.
- Do **not** execute an install command without explicit user confirmation.
- If nothing matches, say so and suggest `npx skills find` or contributing the
  missing source to `data/sources.json` in the Skills Library repo.
- Mention the catalog's `meta.generatedDate` when freshness matters.
