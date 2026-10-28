#!/usr/bin/env python3
"""Check unpublished portal structure without external dependencies.

Run: python site/tests/validate_portal.py
This checks structure, not live browser rendering, content truth or external links.
"""
from __future__ import annotations

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
ASSETS = ["assets/site.css", "assets/catalog.css", "assets/catalog.js", "assets/catalog-data.js"]
FEATURED_SLUGS = [
    "quality-docs-validator",
    "agent-skill-quality-gate",
    "project-pilot",
    "AgentDesk",
    "workattest",
]


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

    project_index = (SITE / "projects/index.html")
    if project_index.is_file():
        index_text = project_index.read_text(encoding="utf-8")
        if "projects/workattest/index.html" not in index_text:
            errors.append("projects/index.html: WorkAttest is missing from featured cards")
        if "projects/public-repo-audit/index.html" in index_text:
            errors.append("projects/index.html: Public Repo Audit must not be featured")
        if index_text.count('class="status') != 5:
            errors.append("projects/index.html: expected five visible project status labels")

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
    return errors


if __name__ == "__main__":
    problems = validate()
    for issue in problems:
        print(f"FAIL: {issue}")
    if problems:
        raise SystemExit(1)
    print(f"PASS: {len(EXPECTED)} HTML pages, assets, metadata and local paths checked.")
