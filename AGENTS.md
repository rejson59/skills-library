# AGENTS.md — instructions for AI agents working in this repository

You are in `rejson59/skills-library`, a curated, generated catalog of open-source
Agent Skills (`SKILL.md`) from GitHub plus a static website.

## Ground rules

1. **Do not hand-edit generated files.** `data/catalog.json`, `data/catalog.js`,
   `data/discovered.json`, `CATALOG.md`, `llms.txt` and the README stats blocks
   are produced by `scripts/build_catalog.py`. Edit `data/sources.json` or the
   scripts instead, then run:
   ```bash
   python3 scripts/build_catalog.py
   python3 scripts/validate_catalog.py
   ```
2. **Never copy upstream skill bodies into this repo.** We index metadata and
   link to the original files. Upstream licenses stay upstream.
3. **Do not invent star counts, licenses or skill descriptions.** All facts come
   from the GitHub API and fetched `SKILL.md` frontmatter.
4. **The website has no build step.** `index.html` + `assets/*` + `data/catalog.js`.
   Keep it dependency-free and working from `file://` as well as HTTP.
5. **The repo is bilingual.** User-facing strings live in `assets/app.js` (`I18N`)
   and `index.html` (`data-i18n`). Add both `pl` and `en`.

## Useful commands

```bash
python3 scripts/query_catalog.py search "security audit" --limit 5
python3 scripts/query_catalog.py collection anthropics/skills
python3 scripts/query_catalog.py install anthropics/skills/pdf
python3 scripts/install.py search "pdf"
python3 scripts/validate_catalog.py
node --check assets/app.js
```

## Data model

- `data/catalog.json`: `meta`, `categories`, `agents`, `packs`, `spotlight`,
  `collections[]`, `skills[]`.
- A skill `id` is `<owner>/<repo>/<skill-folder>`, e.g. `anthropics/skills/pdf`.
- `install.direct` is the most robust install command (full GitHub tree URL).
- `license.status`: `clear` | `check` | `per-skill` | `unknown`.
- `tier`: `essential` | `curated` | `discovered`; `reviewed`: true/false.
- `review.requiresReview` is a heuristic flag, **not** a security guarantee.

See `docs/API.md` for the full schema and `docs/METHODOLOGY.md` for curation rules.
