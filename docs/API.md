# Catalog API

The catalog is a **static JSON file**, so it works as an API without a server:

- [`data/catalog.json`](../data/catalog.json) — pretty-printed, full dataset
- [`data/catalog.js`](../data/catalog.js) — the same object as
  `window.__SKILLS_LIBRARY__` (used by the website, works from `file://`)
- [`data/discovered.json`](../data/discovered.json) — auto-discovered, unreviewed repos
- [`data/sources.json`](../data/sources.json) — human-editable input
- [`data/schema.json`](../data/schema.json) — JSON Schema
- [`llms.txt`](../llms.txt) — short agent-facing index

CORS: when served by GitHub Pages / Vercel / Netlify, `catalog.json` is a normal
static asset. The included `vercel.json` adds `Access-Control-Allow-Origin: *`
for `/data/*.json`.

## Top-level shape

```jsonc
{
  "meta":        { "generatedAt", "generatedDate", "stats", "criteria", ... },
  "categories":  [ { "id", "en", "pl", "icon", "skillCount", "collectionCount" } ],
  "agents":      [ { "name", "id", "project", "global" } ],
  "packs":       [ { "id", "title": {"en","pl"}, "skills": [ids], "script" } ],
  "spotlight":   [ "anthropics/skills/pdf", ... ],
  "collections": [ ... ],
  "skills":      [ ... ]
}
```

## `collections[]`

| Field | Type | Notes |
| --- | --- | --- |
| `id` / `repo` | string | `owner/repo`; the stable ID |
| `url`, `homepage` | string | GitHub URL and optional project site |
| `description` | string | Upstream GitHub description |
| `note` / `notePl` | string \| null | Curator's reason, EN / PL |
| `category`, `tags` | string, string[] | From `sources.json` |
| `stars`, `forks` | number | At generation time |
| `skillCount` | number | **Unique** skill folders |
| `sourceType` | string | `directory` / `single` / `collection` |
| `skillFileCount` | number | All `SKILL.md` paths, including harness copies |
| `license` | object | `{ status, label, spdx, note, files }` |
| `daysSincePush`, `freshness` | number, string | `active` / `maintained` / `stale` |
| `official`, `featured` | boolean | Vendor-maintained / editor's pick |
| `tier`, `reviewed` | string, boolean | `essential` / `curated` / `discovered` |
| `score`, `install` | number, string | Relevance heuristic and CLI command |

## `skills[]`

| Field | Notes |
| --- | --- |
| `id` | `<owner>/<repo>/<folder>` — use this everywhere |
| `name`, `title`, `description`, `shortDescription` | Parsed from `SKILL.md` |
| `path`, `skillDir`, `sourceUrl`, `rawUrl` | Exact upstream location |
| `collectionId`, `repo`, `owner`, `folder` | Back-reference |
| `category`, `tags` | Per-skill category inferred from its own name/folder, with the collection category as fallback, plus keyword tags |
| `license` | Same shape as collection license |
| `official`, `featured`, `spotlight`, `tier`, `reviewed` | Curation flags |
| `specCompliant` | Frontmatter had both `name` and `description` |
| `verified` | We actually fetched this `SKILL.md` |
| `frontmatter` | Selected parsed fields from upstream |
| `review` | `{ hasScripts, network, shell, allowedTools, requiresReview }` |
| `safeUse` | Array of `{ code, en, pl }` notes for security-oriented or primarily Chinese-language skills |
| `install` | `{ direct, shorthand, global, use, manual, collection }` |
| `score`, `stars`, `pushedAt` | Sorting / freshness |

Always prefer `install.direct`: it is a full GitHub tree URL and works even when
a skill lives inside `plugins/.../skills/...`.

## Examples

### jq

```bash
jq '.meta.stats' data/catalog.json
jq -r '.skills[] | select(.official and .specCompliant) | [.id,.title] | @tsv' data/catalog.json
jq -r '.skills[] | select(.category=="security" and .license.status=="clear") | .install.direct' data/catalog.json
jq '.collections | sort_by(-.stars) | .[0:10] | map({repo,stars,skillCount,license:.license.label})' data/catalog.json
```

### Python

```python
import json
c = json.load(open("data/catalog.json"))
for s in c["skills"]:
    if "pdf" in s["tags"] and s["license"]["status"] == "clear":
        print(s["id"], "-", s["shortDescription"])
```

### Helper CLI

```bash
python3 scripts/query_catalog.py search "react best practices" --limit 5
python3 scripts/query_catalog.py collection anthropics/skills
python3 scripts/query_catalog.py install anthropics/skills/pdf
python3 scripts/query_catalog.py stats
python3 scripts/query_catalog.py random --category security
```

### JavaScript (browser)

```html
<script src="data/catalog.js"></script>
<script>
  const skills = window.__SKILLS_LIBRARY__.skills;
  const pdf = skills.filter(s => s.tags.includes("pdf"));
</script>
```

## Stability

`id`, `repo`, `path`, `sourceUrl` and `install` are the stable contract.
Descriptions, stars, scores and ordering may change on every weekly refresh.
New fields may be added; existing field names will not be silently repurposed
within major version `1` (`meta.version`).

For AI agents: read [`llms.txt`](../llms.txt) first, then query
`data/catalog.json`, and always show the user the upstream source URL before
recommending an install.
