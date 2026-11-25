# Methodology — how the catalog is built

Everything in `data/catalog.json` is reproducible: run
`python3 scripts/build_catalog.py` with a GitHub token and you get the same
shape of data (numbers move as GitHub moves). The script uses only Python's
standard library and the public GitHub REST API.

## 1. Discovery

We run the queries listed in `data/sources.json` against
`GET /search/repositories` (sorted by stars), covering:

- names/descriptions: `agent skills`, `claude skills`, `awesome skills`,
  `codex skills`, `skills in:name`, `agent skill in:description`,
- README mentions of `SKILL.md`,
- topics: `agent-skills`, `claude-skills`, `agent-skill`,
  `claude-code-skills`, `ai-skills`, `codex-skills`, `skills`,
  `anthropic-skills`.

The curated source list (`sources[]`) is added explicitly, so important
low-star or vendor repositories are never missed. GitHub redirects are
canonicalized (e.g. a renamed repo resolves to its current `full_name`).

## 2. Repository metadata

For each candidate we read: `full_name`, description, stars, forks, open issues,
language, topics, default branch, `pushed_at`, `created_at`, `archived`, `fork`,
homepage and the license SPDX identifier from the API.

## 3. Tree scan

`GET /repos/{repo}/git/trees/{branch}?recursive=1` gives every blob path. We
count only **exact** `SKILL.md` filenames (case-sensitive), because lowercase
`skill.md` files are often documentation templates rather than skills.

Two numbers are kept:

- `skillFileCount` — every `SKILL.md` path. Many repos publish the same skill
  into `.claude/skills/`, `.cursor/skills/`, `.agents/skills/` and `skills/`.
- `skillCount` — unique **folder names** inside that repository. This is the
  number shown on collection cards; it avoids the "10 000 skills!" inflation
  caused by harness copies.

We also collect `LICENSE*` paths. If GitHub reports no repo-level license but
per-skill `LICENSE.txt` files exist, we mark the collection `per-skill`.

## 4. Individual skill indexing

For curated collections only:

1. Drop paths inside `evals/`, `tests/`, `examples/`, `templates/`, `docs/`,
   `benchmarks/`, `.changeset/` and issue/PR templates.
2. Deduplicate by skill folder, preferring canonical `skills/<name>/SKILL.md`
   over copies in dot-directories or plugin bundles.
3. Force-include folders referenced by starter packs and the editor's spotlight.
4. Prefer the `picks` from `data/sources.json`, then take up to `maxSkills`.
5. Fetch the raw `SKILL.md` through
   `GET /repos/{repo}/contents/{path}?ref={branch}` with
   `Accept: application/vnd.github.raw`.
6. Parse YAML-ish frontmatter: `name`, `description`, `license`,
   `compatibility`, `allowed-tools`, `version`. Multi-line `>` / `|` values are
   supported. If `description` is missing, we fall back to the first prose line
   of the body and set `specCompliant: false`.

Every indexed skill therefore has a real, reachable source URL, a parsed
description, content length and a `verified: true` flag. Its `category` is
inferred from strong signals in the skill's own name and folder; the collection
category is only a fallback. This prevents a design skill inside a document
toolkit from being misfiled as a document skill, without letting generic words
in long descriptions push hundreds of unrelated skills into one category.

Security-oriented skills and skills whose upstream description is primarily
Chinese receive bilingual `safeUse[]` notes. These are visible on cards and in
the detail drawer; they are guidance, not a security audit.

## 5. Curation tiers

| Tier | Meaning |
| --- | --- |
| `essential` | A handful of reference / expert collections worth installing first |
| `curated` | Manually reviewed, annotated, categorized and assigned to packs |
| `discovered` | Automatic: ≥ 2 000 stars, ≥ 1 unique skill, skill-related name/description/topic, pushed within 2 years, visible license, not archived/fork. **Not editorially reviewed.** |

A manual `excludeFromDiscovery` list removes big projects that happen to contain
a `SKILL.md` but are not skill libraries (frameworks, checklists, apps).

## 6. License flags

| Status | Meaning |
| --- | --- |
| `clear` | GitHub returned a recognized SPDX license (MIT, Apache-2.0, BSD, CC-BY-*, MPL, GPL/AGPL, …) |
| `check` | An SPDX id exists but needs a human look (`NOASSERTION` or a rare id) |
| `per-skill` | No root license, but `LICENSE.txt` files exist next to individual skills |
| `unknown` | No license information found — flagged prominently on the site |

AGPL/CC-BY-SA are open-source/copyleft but have share-alike obligations; the
site shows the exact SPDX id rather than collapsing everything into "free".

## 7. Review heuristics

For each fetched `SKILL.md` and its sibling files we compute
`review.*` — never a verdict:

- `hasScripts`: sibling `.py/.sh/.js/.ts/...` files or a `scripts/` directory,
- `allowedTools`: parsed from frontmatter,
- `network` / `shell`: mentions of URLs or shell code fences,
- `requiresReview`: scripts, allowed tools, or suspicious commands
  (`curl`, `wget`, `sudo`, `rm -rf`, `eval`, `chmod +x`, `git clone`,
  `pip install`, `npm install`).

This is a **triage hint**. See [SECURITY.md](../SECURITY.md).

## 8. Ranking

`score` is a transparent relevance heuristic, not a quality certification:

```
collection = 10·log10(stars+1) + 4·log10(uniqueSkills+1)
           + recencyBonus (0/4/8) + officialBonus (6) + featuredBonus (5)
skill      = collection + spotlight(12) + specCompliant(4) + official(3)
```

The website can sort by score, stars, freshness, skill count or name instead.

## 9. Outputs & reproducibility

`build_catalog.py` writes `data/catalog.json`, `data/catalog.js`,
`data/discovered.json`, `CATALOG.md`, `llms.txt` and refreshes the README stats
blocks. `.github/workflows/update-catalog.yml` runs it weekly and on changes to
`sources.json` / the script. `scripts/validate_catalog.py` checks IDs, pack
references, licenses and generated-file consistency in CI.

## Known limitations

- GitHub search returns at most 1 000 results per query; we use 15 diverse
  queries plus a manual curated list, but no claim of literally *every* repo.
- Recursive trees can be truncated on enormous monorepos; those collections get
  `truncatedTree: true`.
- Star counts and `pushed_at` are a popularity/freshness proxy, not quality.
- We parse frontmatter with a small tolerant parser rather than a full YAML
  library, so exotic YAML may lose a field (the raw file link is always there).
- We do not audit upstream behavior, scripts or prompt-injection safety.
