# MigMCC Engineering portfolio

Static GitHub Pages portfolio for Miguel Santos. It presents five selected
open-source projects in quality engineering, Python automation and AI-assisted development.

## Structure

- `index.html` — home page.
- `projects/` — searchable catalogue and one page per project.
- `about/` — background and contact information.
- `assets/` — shared CSS, catalogue data and search JavaScript.
- `404.html`, `robots.txt`, `sitemap.xml` and `.nojekyll` — GitHub Pages and SEO files.
- `tests/validate_portal.py` — dependency-free structural regression check.

## Run locally

From this directory, start a static server:

```sh
python -m http.server 8000
```

Then open `http://localhost:8000/`.

## Add a project

1. Copy an existing page under `projects/` and keep one `h1`, a unique title,
   description, canonical URL and Open Graph URL.
2. Add a verified record to `assets/catalog-data.js`, then add the project card to `projects/index.html` and, when appropriate, to the
   selected-work section on `index.html`.
3. Add the canonical URL to `sitemap.xml` and update its `lastmod` date.
4. Use only claims and links supported by the project's own documentation.
5. Run the checks below and inspect desktop and mobile layouts.

`WorkAttest` is a source-only MVP. Do not label source archives or a Git tag as an
application download; show the release, tag or source-only status verified in the catalogue.

## Test

```sh
python tests/validate_portal.py
node --check assets/catalog.js
```

The Python check covers the expected pages, metadata basics, production
indexing policy, local links, anchors and release-copy regressions.

## Publish updates

GitHub Pages deploys from the `main` branch of `migmcc/migmcc.github.io`.
Commit and push changes to that branch. The site files live at the repository
root; do not place them under a `site/` subdirectory.

## Verify a deployment

After GitHub Pages completes, confirm the home page, `/projects/`, `/about/`,
all six project routes, `/sitemap.xml` and `/robots.txt` over HTTPS. Check
browser console errors, keyboard focus, the catalogue filter and responsive
layouts at 1440 × 900 and 390 × 844.
