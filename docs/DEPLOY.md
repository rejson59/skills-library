# Deploy the website

The website is a **static directory**: `index.html`, `assets/`, `data/catalog.js`.
No build step, no npm dependencies, no server-side code, no environment variables.

```
/
├── index.html
├── assets/styles.css
├── assets/app.js
└── data/catalog.js   (+ catalog.json for API consumers)
```

## Local / live preview

```bash
python3 -m http.server 4173 --bind 0.0.0.0
# http://localhost:4173
```

`index.html` also works when opened directly as `file://`, because the site loads
`data/catalog.js` instead of `fetch()`-ing JSON.

## GitHub Pages

Option A — no workflow: in repository **Settings → Pages**, deploy from the
branch and `/ (root)`. Done.

Option B — included workflow
[`.github/workflows/pages.yml`](../.github/workflows/pages.yml) uses the official
`actions/upload-pages-artifact` + `actions/deploy-pages` actions. It runs on push
to `main`, on catalog updates and on `workflow_dispatch`. Enable
**Settings → Pages → Source: GitHub Actions** once.

Your URL will be `https://<owner>.github.io/<repo>/`. If the site is served from
a subpath, all asset URLs in `index.html` are relative, so nothing else changes.

## Vercel

Import the GitHub repository, choose framework **Other / Static**, and set:

| Setting | Value |
| --- | --- |
| Build command | *(leave empty)* |
| Output directory | *(leave empty / `.`)* |
| Install command | *(leave empty)* |
| Root directory | `.` |

The included [`vercel.json`](../vercel.json) enables clean URLs, caches JSON for
an hour and adds permissive CORS headers for `data/*.json` so other tools can
query the catalog. A Vercel deployment also works from uploaded files without
connecting Git: upload `index.html`, `assets/`, `data/` and `vercel.json`.

## Netlify / Cloudflare Pages

- **Netlify**: publish directory `.`, build command empty.
- **Cloudflare Pages**: build command empty, output directory `.`.
- Both serve `data/catalog.json` as a normal static asset.

## Any static host

Copy the whole repository (or just `index.html`, `assets/`, `data/`) to S3,
Nginx, Caddy, Firebase Hosting, etc. Example:

```bash
rsync -av index.html assets data user@server:/var/www/skills-library/
```

## After a data refresh

`scripts/build_catalog.py` rewrites `data/catalog.js` and `data/catalog.json`.
Commit those files (or let the weekly workflow do it) and redeploy/revalidate.
Static hosts usually update instantly; a CDN may need a cache purge.

## Checklist

- [ ] `data/catalog.js` exists and is not empty
- [ ] `python3 scripts/validate_catalog.py` passes
- [ ] `node --check assets/app.js` passes
- [ ] `/data/catalog.json` returns `200` on the deployed host
- [ ] PL/EN switch, theme switch, search and copy buttons work
- [ ] No mixed-content or localhost URLs in browser-facing code
