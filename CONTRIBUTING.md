# Contributing

Thanks! The most valuable contribution is **a better source list**.

## Add or fix a collection

Edit [`data/sources.json`](data/sources.json) → `sources[]`:

```json
{
  "repo": "owner/repo",
  "category": "engineering",
  "tags": ["review", "tdd"],
  "official": false,
  "featured": false,
  "tier": "curated",
  "maxSkills": 12,
  "picks": ["folder-name", "another-folder"],
  "note": "One sentence: why is this worth installing?",
  "note_pl": "Jedno zdanie po polsku: dlaczego warto to zainstalować?",
  "packs": ["starter"],
  "license_note": "Optional: explain a non-obvious license situation"
}
```

Rules:

- The repo must be public, open-source and contain at least one real `SKILL.md`.
- `picks` are **folder names** (the parent directory of `SKILL.md`), not plugin
  names. They are force-included even if `maxSkills` is small.
- Prefer 8–20 representative skills for large libraries; avoid indexing 800
  near-identical generated integrations.
- Add a factual, non-promotional `note` / `note_pl`. Do not paste star counts.
- `official: true` is for vendor-maintained repositories only.
- `tier: "essential"` is reserved for the handful of reference collections.
- If the repo has no root LICENSE, set `license_note` explaining what you found.

Then regenerate and validate:

```bash
export GITHUB_TOKEN=...   # optional but recommended
python3 scripts/build_catalog.py
python3 scripts/validate_catalog.py
node --check assets/app.js
git add data/sources.json data/ CATALOG.md llms.txt README.md README.pl.md
```

## Add a starter pack

Add an object to `packs[]` in `data/sources.json`. Each `skills` entry is a
`[repo, folder]` pair; the build script resolves it to a skill ID and generates
the copyable multi-command install script. Missing IDs are skipped with a
warning, so run the validator.

## Improve the website

`index.html`, `assets/styles.css` and `assets/app.js` are dependency-free. New
user-facing strings need both `pl` and `en` entries in `I18N` (or a
`data-i18n` attribute). Keep it working from `file://` — that is why the site
loads `data/catalog.js` instead of `fetch()`-ing JSON.

## Report bad data

Open an issue with the repo name, skill path and what is wrong (404, wrong
license, stale description, malicious content, spam). We will either fix the
source annotation, exclude it from discovery, or remove it.

## Commit style

Small, focused commits: `feat: add X to curated sources`, `fix: correct license
note for Y`, `site: add Z filter`. Generated files should only change as a
result of running `scripts/build_catalog.py`.
