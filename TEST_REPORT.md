# Publication test report

Date: 2026-10-18

## Scope

- Home, projects catalogue, five project pages, about page and custom 404 page.
- GitHub Pages deployment at `https://migmcc.github.io/`.

## Automated checks

- `python tests/validate_portal.py` — passed. Checks all nine HTML pages,
  expected assets, one `h1` per page, descriptions, titles, viewport metadata,
  production `noindex` policy, Open Graph metadata, local links and anchors.
- `node --check assets/catalog.js` — passed.
- GitHub API checks — passed for all five project repositories and their linked
  technical-reference files.
- HTTPS checks — each required page, `sitemap.xml`, `robots.txt`, shared CSS
  and catalogue JavaScript returned HTTP 200.

## Browser checks

- Desktop viewport: 1440 × 900 — home page has no horizontal overflow, expected
  canonical URL and no console warnings/errors.
- Mobile viewport: 390 × 844 — all public pages and the 404 route have no
  horizontal overflow.
- Page rendering — each route has one `h1`, its expected title and canonical;
  public pages are indexable and the 404 is `noindex`.
- Catalogue — searching for `Agent Desk` produces one visible card and the
  counter `Showing 1 of 5 projects`.
- Keyboard — first Tab focuses the visible skip link; shared CSS supplies a
  high-contrast `:focus-visible` outline.

## Corrections made

- Replaced the stale `Unpublished review` footer copy in public pages.
- Aligned the pre-publication validator with the production indexing policy:
  public pages must not be `noindex`; 404 must be `noindex`.
- Added the missing Open Graph title, description and type to `404.html`.
- Added the root maintenance README.

## Evidence

Live desktop and mobile captures were taken during the browser review. They are
provided with the publication handoff; browser sandboxing prevented exporting
the image bytes into this repository directory.

## Limitations

No analytics, tracking, external fonts or paid services are used. GitHub Pages
is the only publishing dependency.
