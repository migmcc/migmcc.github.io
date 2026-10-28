#!/usr/bin/env python3
"""Check unpublished portal structure without external dependencies.

Run: python site/tests/validate_portal.py
This checks structure, not live browser rendering, content truth or external links.
"""
from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

SITE = Path(__file__).resolve().parents[1]
EXPECTED = [
    "index.html",
    "404.html",
    "about/index.html",
    "projects/index.html",
    "projects/quality-docs-validator/index.html",
    "projects/public-repo-audit/index.html",
    "projects/agent-skill-quality-gate/index.html",
    "projects/project-pilot/index.html",
    "projects/AgentDesk/index.html",
    "projects/workattest/index.html",
]
ASSETS = [
    "assets/site.css",
    "assets/catalog.css",
    "assets/catalog.js",
    "assets/catalog-data.js",
    "assets/overview.css",
    "assets/projects-overview.svg",
]
FEATURED_SLUGS = [
    "quality-docs-validator",
    "agent-skill-quality-gate",
    "project-pilot",
    "AgentDesk",
    "workattest",
]
CATALOGUE_ACTIONS = {
    "quality-docs-validator": "https://github.com/migmcc/quality-docs-validator/releases/tag/v0.3.0",
    "agent-skill-quality-gate": "https://github.com/migmcc/agent-skill-quality-gate/releases/tag/v0.1.0",
    "project-pilot": "https://github.com/migmcc/project-pilot/tree/v1.0.0",
    "AgentDesk": "https://github.com/migmcc/AgentDesk/releases/tag/v0.4.2",
    "workattest": "https://github.com/migmcc/WorkAttest",
}
CATALOGUE_CARD_STATUSES = {
    "quality-docs-validator": "Stable release · v0.3.0",
    "agent-skill-quality-gate": "Alpha release · v0.1.0",
    "project-pilot": "Stable source tag · v1.0.0",
    "AgentDesk": "Stable release · v0.4.2",
    "workattest": "MVP · source only",
}
HOMEPAGE_SELECTED = {
    "quality-docs-validator",
    "agent-skill-quality-gate",
    "workattest",
}


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.h1 = 0
        self.description = False
        self.noindex = False
        self.og_properties: set[str] = set()
        self.viewport = False
        self.title = False
        self.links: list[str] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self.title = True
        if tag == "meta" and a.get("name") == "description" and a.get("content"):
            self.description = True
        if tag == "meta" and a.get("name") == "viewport":
            self.viewport = True
        if tag == "meta" and a.get("name") == "robots" and "noindex" in (a.get("content") or ""):
            self.noindex = True
        if tag == "meta" and a.get("property", "").startswith("og:") and a.get("content"):
            self.og_properties.add(a["property"])
        if a.get("id"):
            self.ids.add(a["id"])
        for key in ("href", "src"):
            if a.get(key):
                self.links.append(a[key])


def validate() -> list[str]:
    errors: list[str] = []
    for name in EXPECTED + ASSETS:
        if not (SITE / name).is_file():
            errors.append(f"Missing file: {name}")
    for name in EXPECTED:
        html = SITE / name
        if not html.is_file():
            continue
        raw_html = html.read_text(encoding="utf-8")
        if "Unpublished review" in raw_html:
            errors.append(f"{name}: contains pre-publication footer copy")
        parser = Page()
        parser.feed(raw_html)
        if parser.h1 != 1:
            errors.append(f"{name}: expected 1 h1, got {parser.h1}")
        for field in ("description", "title", "viewport"):
            if not getattr(parser, field):
                errors.append(f"{name}: missing {field}")
        if name == "404.html" and not parser.noindex:
            errors.append(f"{name}: missing noindex")
        if name != "404.html" and parser.noindex:
            errors.append(f"{name}: must not contain noindex")
        for property_name in ("og:title", "og:description", "og:type", "og:url"):
            if property_name not in parser.og_properties:
                errors.append(f"{name}: missing {property_name}")
        if "main" not in parser.ids:
            errors.append(f"{name}: missing main landmark id")
        for url in parser.links:
            parsed = urlsplit(url)
            if parsed.scheme or url.startswith("//"):
                continue
            if parsed.path:
                target = (html.parent / unquote(parsed.path)).resolve()
                if not target.is_relative_to(SITE.resolve()):
                    errors.append(f"{name}: link escapes site: {url}")
                elif not target.is_file():
                    errors.append(f"{name}: broken internal link: {url}")
            elif url.startswith("#") and parsed.fragment and parsed.fragment not in parser.ids:
                errors.append(f"{name}: missing anchor: {url}")

    catalogue = SITE / "assets/catalog-data.js"
    if catalogue.is_file():
        catalogue_text = catalogue.read_text(encoding="utf-8")
        for slug in FEATURED_SLUGS:
            if f'"slug":"{slug}"' not in catalogue_text:
                errors.append(f"catalogue: missing featured project: {slug}")
        for mode in ("stable-release", "stable-source-tag", "source-only-mvp"):
            if f'"distribution":"{mode}"' not in catalogue_text:
                errors.append(f"catalogue: missing distribution mode: {mode}")
        if "public-repo-audit" in catalogue_text:
            errors.append("catalogue: public-repo-audit must not be featured")
        for slug, action_url in CATALOGUE_ACTIONS.items():
            if action_url not in catalogue_text:
                errors.append(f"catalogue: missing verified action URL for {slug}")

    project_index = (SITE / "projects/index.html")
    if project_index.is_file():
        index_text = project_index.read_text(encoding="utf-8")
        if "projects/workattest/index.html" not in index_text:
            errors.append("projects/index.html: WorkAttest is missing from featured cards")
        if "projects/public-repo-audit/index.html" in index_text:
            errors.append("projects/index.html: Public Repo Audit must not be featured")
        if index_text.count('class="status') != 5:
            errors.append("projects/index.html: expected five visible project status labels")
        cards = dict(re.findall(r'<article class="card" data-slug="([^"]+)">(.*?)</article>', index_text))
        if set(cards) != set(FEATURED_SLUGS):
            errors.append("projects/index.html: card slugs must match the approved catalogue")
        for slug, action_url in CATALOGUE_ACTIONS.items():
            card = cards.get(slug, "")
            if f'../projects/{slug}/index.html' not in card:
                errors.append(f"projects/index.html: missing project card link for {slug}")
            if action_url not in card:
                errors.append(f"projects/index.html: missing verified action URL for {slug}")
            if CATALOGUE_CARD_STATUSES[slug] not in card:
                errors.append(f"projects/index.html: status diverges from catalogue for {slug}")

    catalogue_css = SITE / "assets/catalog.css"
    if catalogue_css.is_file():
        css_text = catalogue_css.read_text(encoding="utf-8")
        for selector in (".projects-hero", ".release-guide", ".card-actions", ".primary-action"):
            if selector not in css_text:
                errors.append(f"assets/catalog.css: missing {selector} styling")
        if "@media(max-width:580px)" not in css_text:
            errors.append("assets/catalog.css: missing mobile layout rules")

    catalogue_script = SITE / "assets/catalog.js"
    if catalogue_script.is_file():
        script_text = catalogue_script.read_text(encoding="utf-8")
        for class_name in ("projects-hero", "release-guide", "card-actions", "primary-action", "secondary-action"):
            if class_name not in script_text:
                errors.append(f"assets/catalog.js: missing {class_name} presentation hook")

    for project in FEATURED_SLUGS:
        page = SITE / "projects" / project / "index.html"
        if page.is_file() and "Download" in page.read_text(encoding="utf-8"):
            errors.append(f"projects/{project}/index.html: must not describe a source archive as a download")

    homepage = SITE / "index.html"
    if homepage.is_file():
        homepage_text = homepage.read_text(encoding="utf-8")
        if "projects/workattest/index.html" not in homepage_text:
            errors.append("index.html: WorkAttest must appear in selected work")
        if "projects/public-repo-audit/index.html" in homepage_text:
            errors.append("index.html: Public Repo Audit must not appear in selected work")
        homepage_cards = set(re.findall(
            r'<article class="card"[^>]*>.*?href="projects/([^/]+)/index.html"',
            homepage_text,
        ))
        if homepage_cards != HOMEPAGE_SELECTED:
            errors.append("index.html: selected work must match the approved homepage set")
        if 'src="assets/projects-overview.svg"' not in homepage_text:
            errors.append("index.html: missing approved project overview map")
        if "Five focused tools. One shared engineering approach." not in homepage_text:
            errors.append("index.html: missing approved project overview title")
        if "Five focused tools. One practical system." in homepage_text:
            errors.append("index.html: contains superseded project overview title")
        mobile_map = re.search(
            r'<div class="project-map-mobile">(.*?)</div>', homepage_text, re.DOTALL
        )
        if not mobile_map:
            errors.append("index.html: missing mobile project overview links")
        else:
            for slug in FEATURED_SLUGS:
                if f'projects/{slug}/index.html' not in mobile_map.group(1):
                    errors.append(f"index.html: missing project overview link for {slug}")

    overview = SITE / "assets/projects-overview.svg"
    if overview.is_file():
        overview_text = overview.read_text(encoding="utf-8")
        for title in (
            "Quality Docs Validator",
            "Agent Skill Quality Gate",
            "ProjectPilot",
            "Agent Desk",
            "WorkAttest",
        ):
            if title not in overview_text:
                errors.append(f"assets/projects-overview.svg: missing approved project: {title}")
        if "Public Repo Audit" in overview_text:
            errors.append("assets/projects-overview.svg: Public Repo Audit must not be featured")

    overview_css = SITE / "assets/overview.css"
    if overview_css.is_file():
        overview_css_text = overview_css.read_text(encoding="utf-8")
        for selector in (".project-system", ".project-map", ".project-map-mobile"):
            if selector not in overview_css_text:
                errors.append(f"assets/overview.css: missing {selector} styling")
        if "@media(max-width:1000px)" not in overview_css_text:
            errors.append("assets/overview.css: missing mobile map layout rule")

    workattest = SITE / "projects/workattest/index.html"
    if workattest.is_file():
        workattest_text = workattest.read_text(encoding="utf-8")
        for phrase in (
            "MVP",
            "source-only",
            "development key storage",
            "trusted operator",
            "not a production security control",
        ):
            if phrase not in workattest_text:
                errors.append(f"projects/workattest/index.html: missing documented limitation: {phrase}")
    return errors


if __name__ == "__main__":
    problems = validate()
    for issue in problems:
        print(f"FAIL: {issue}")
    if problems:
        raise SystemExit(1)
    print(f"PASS: {len(EXPECTED)} HTML pages, assets, metadata and local paths checked.")
