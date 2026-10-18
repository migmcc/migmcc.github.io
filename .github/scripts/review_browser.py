"""Headless browser smoke tests against local static pages; screenshots are evidence artifacts."""
from __future__ import annotations
import contextlib
import functools
import http.server
from pathlib import Path
import threading
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "evidence"
OUT.mkdir(exist_ok=True)
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
base = f"http://127.0.0.1:{server.server_port}"
routes = ["/", "/projects/", "/about/", "/projects/quality-docs-validator/",
          "/projects/public-repo-audit/", "/projects/agent-skill-quality-gate/",
          "/projects/project-pilot/", "/projects/AgentDesk/"]
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for name, width, height in [("desktop", 1440, 900), ("mobile", 390, 844)]:
            page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            for route in routes:
                response = page.goto(base + route, wait_until="networkidle")
                assert response and response.status == 200, f"{route}: HTTP error"
                assert page.locator("h1").count() == 1, route
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), f"{name} overflow: {route}"
                assert not errors, f"{route}: {errors}"
                if route in ["/", "/projects/quality-docs-validator/", "/projects/project-pilot/"]:
                    suffix = ("home" if route == "/" else route.strip("/").split("/")[-1])
                    page.screenshot(path=str(OUT / f"{suffix}-{name}.png"), full_page=True)
            page.goto(base + "/projects/", wait_until="networkidle")
            page.locator("#project-search").fill("Agent Desk")
            assert page.locator("#project-grid .card:visible").count() == 1
            page.close()
        browser.close()
finally:
    server.shutdown()
print("PASS: 8 routes on 1440x900 and 390x844; search, h1, browser errors, overflow, captures")
