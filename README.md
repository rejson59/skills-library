# 🧠 Skills Library

**The open, reproducible index of the best open-source Agent Skills (`SKILL.md`) on GitHub — plus a fast, bilingual website to actually use them in your AI agents.**

[🇵🇱 Wersja po polsku](README.pl.md) · [📄 Full catalog](CATALOG.md) · [🤖 llms.txt](llms.txt) · [📊 JSON API](data/catalog.json) · [🌐 Website](index.html) · [📖 Install guide](docs/INSTALL.md)

---

## Why this exists

There are thousands of `SKILL.md` repositories on GitHub. Finding the trustworthy ones means opening dozens of READMEs, guessing which are maintained, which have a real license, and which are just 400 generated copies of the same template.

Skills Library fixes that:

- 🔎 **Real GitHub research.** The catalog is generated from the GitHub API: repository search, metadata, recursive git trees and actual `SKILL.md` frontmatter. No hand-typed star counts.
- ✅ **Verified skills.** Every indexed skill has a real, fetched `SKILL.md` with parsed `name` / `description`. We deduplicate the copies published into `.claude/`, `.cursor/`, `.agents/`, etc.
- ⚖️ **License transparency.** MIT / Apache / CC-BY-SA / per-skill licenses / *no license detected* are shown explicitly instead of hiding behind "open source".
- 🛡️ **Honest trust model.** Heuristics flag skills that ship scripts, declare `allowed-tools` or run shell/network commands. Security-oriented and primarily Chinese-language skills get explicit safe-use notes. We never claim a third-party skill is "safe".
- 📦 **Starter packs.** Ready-made bundles for a solid coding agent, frontend, documents, security, data research, product work and official vendor sets.
- 🤖 **Machine-readable.** `data/catalog.json`, `data/catalog.js`, `data/discovered.json`, `llms.txt` and a JSON Schema. The repo itself is also an installable skill: [`skills/skill-finder`](skills/skill-finder/SKILL.md).
- 🌍 **Two languages, zero dependencies.** The website is plain HTML/CSS/JS with Polish/English, dark/light mode, search, filters, saved skills, deep links and one-click install commands.

> We index metadata and link to upstream files — we do **not** copy other people's skill bodies into this repository. Every upstream project keeps its own license and attribution.

---

## Live numbers

| Repos scanned | `SKILL.md` files | Unique skill folders | Curated collections | Indexed skills | Generated |
| ---: | ---: | ---: | ---: | ---: | --- |
<!-- STATS:START -->
| 472 | 108,698 | 93,362 | 124 | 976 | 2026-11-25 |
<!-- STATS:END -->

*"SKILL.md files" counts every path, including copies published into several agent folders. "Unique skill folders" deduplicates by folder name within one repository. See [methodology](docs/METHODOLOGY.md).*

---

## 60-second start

```bash
# 1. Browse the website locally (no npm install, no build step)
python3 -m http.server 4173 --bind 0.0.0.0
# open http://localhost:4173

# 2. Install one skill into your agent
npx skills add https://github.com/anthropics/skills/tree/main/skills/pdf

# 3. Or install a whole expert collection
npx skills add obra/superpowers

# 4. Or use our CLI helper to find the right command
python3 scripts/query_catalog.py search "react best practices" --limit 5
python3 scripts/install.py search "pdf"
```

`npx skills` is the open-source [Vercel Labs skills CLI](https://github.com/vercel-labs/skills). It detects Claude Code, Codex, Cursor, Gemini CLI, Copilot, OpenCode and many other agents and installs into the right folder. Requires Node.js 22.20+.

---

## What you get

### 1. A searchable website
Open [`index.html`](index.html) (or serve the repo as a static site). It reads `data/catalog.js` and gives you:

- full-text search across names, descriptions, repos and tags (`/` focuses the search box),
- category, license, official, curated-only and saved-only filters,
- sort by relevance, stars, freshness, skill count or name,
- a detail drawer with four install variants, source links, license and review flags,
- starter packs with a copyable multi-command install script,
- PL/EN switch, dark/light switch, URL deep links (`?q=pdf&view=skills&lang=pl`),
- a compatibility matrix for agent directories.

### 2. A real awesome-list
[`CATALOG.md`](CATALOG.md) contains the editor's picks, every curated collection with a reason, and the automatically discovered repositories — generated, never stale-by-hand.

### 3. A data API for agents and tools
```bash
python3 scripts/query_catalog.py search "security audit" --limit 5
python3 scripts/query_catalog.py collection anthropics/skills
python3 scripts/query_catalog.py install anthropics/skills/pdf
```
The stable endpoint is [`data/catalog.json`](data/catalog.json). [`llms.txt`](llms.txt) tells LLM agents where to look. The schema lives in [`data/schema.json`](data/schema.json).

### 4. The library is itself a skill
```bash
npx skills add https://github.com/rejson59/skills-library/tree/main/skills/skill-finder
```
Install [`skill-finder`](skills/skill-finder/SKILL.md) and your agent can query this catalog before answering "how do I do X?".

---

## How a repository qualifies

| Signal | Rule |
| --- | --- |
| Format | At least one exact `SKILL.md` file in the repository tree |
| Source | Public GitHub repository, not archived, not a fork |
| Curated tier | Manually reviewed, annotated with category, note and starter-pack membership |
| Discovered tier | Found automatically by GitHub search, ≥ 2 000 stars, pushed within 2 years, clearly skill-related, license visible — **not** editorially reviewed |
| License | Read from the GitHub API; `NOASSERTION`, per-skill licenses and missing licenses are flagged, not silently treated as MIT |
| Safety | We verify metadata and file existence. We never execute or audit upstream skill behavior |

Full details: [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) · Trust model: [`SECURITY.md`](SECURITY.md)

---

## Repository layout

```
├── index.html                 # static website (no build step)
├── assets/                    # styles.css + app.js
├── data/
│   ├── sources.json           # curated source list + categories + packs   ← edit this
│   ├── catalog.json           # generated full catalog (the API)
│   ├── catalog.js             # generated window.__SKILLS_LIBRARY__ bundle
│   ├── discovered.json        # generated auto-discovered repositories
│   └── schema.json            # JSON Schema for catalog.json
├── scripts/
│   ├── build_catalog.py       # reproducible GitHub → catalog pipeline
│   ├── query_catalog.py       # search/install lookup CLI
│   ├── install.py             # friendly installer helper
│   └── validate_catalog.py    # CI consistency checks
├── skills/skill-finder/       # the library as an installable Agent Skill
├── docs/                      # install, methodology, API, deployment
├── CATALOG.md                 # generated markdown catalog
├── llms.txt                   # generated agent-facing index
└── .github/workflows/         # weekly refresh + validation
```

---

## Refresh the data

```bash
export GITHUB_TOKEN=...        # optional but recommended; falls back to `gh auth token`
python3 scripts/build_catalog.py
python3 scripts/validate_catalog.py
```

The [weekly workflow](.github/workflows/update-catalog.yml) runs the same script and commits refreshed data. To add or fix a collection, edit [`data/sources.json`](data/sources.json) — see [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## Deploy the site

It is a static directory: GitHub Pages, Vercel, Netlify, Cloudflare Pages or `python3 -m http.server` all work. See [`docs/DEPLOY.md`](docs/DEPLOY.md). No secrets, no database, no telemetry.

---

## Credits

Huge thanks to the upstream authors and organizations whose open work makes this index possible — Anthropic, OpenAI, Google, GitHub, Vercel Labs, Cloudflare, DuckDB, Obsidian, Hugging Face, Android, Trail of Bits, OpenZeppelin, Matt Pocock, Jesse Vincent (obra), Addy Osmani, Emil Kowalski and hundreds of community contributors. Every entry links back to its source and shows its license status.

## License

Our catalog code, website and documentation are **MIT** licensed — see [`LICENSE`](LICENSE). Upstream skills remain under their own licenses; this repository redistributes metadata and links only.

<p align="center"><sub>Built with the GitHub API, Python's standard library and a lot of curiosity. ⭐ Star the repo if it saved you an afternoon.</sub></p>
