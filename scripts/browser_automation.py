"""Playwright-based browser automation for SEO checks.

Usage:
    python browser_automation.py <url> [--check js_render|mobile|mixed_content] [--json]

Requires: pip install playwright && playwright install chromium
"""

import argparse
import json
import sys

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


def check_js_rendering(url: str) -> dict:
    """Compare raw HTML content vs JS-rendered DOM content."""
    if not PLAYWRIGHT_AVAILABLE:
        return {"error": "playwright_not_installed", "skipped": True}

    import requests
    raw_resp = requests.get(url, timeout=15, headers={
        "User-Agent": "Mozilla/5.0 (compatible; SEOSuiteBot/0.1)"
    })

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle", timeout=30000)

        rendered_title = page.title()
        rendered_content = page.content()
        rendered_text = page.evaluate("document.body.innerText")

        canonical_el = page.query_selector('link[rel="canonical"]')
        rendered_canonical = canonical_el.get_attribute("href") if canonical_el else None

        robots_el = page.query_selector('meta[name="robots"]')
        rendered_robots = robots_el.get_attribute("content") if robots_el else None

        h1_elements = page.query_selector_all("h1")
        rendered_h1s = [el.inner_text() for el in h1_elements]

        browser.close()

    from bs4 import BeautifulSoup
    raw_soup = BeautifulSoup(raw_resp.text, "lxml")
    raw_title = raw_soup.title.get_text(strip=True) if raw_soup.title else None
    raw_canonical_tag = raw_soup.find("link", rel="canonical")
    raw_canonical = raw_canonical_tag["href"] if raw_canonical_tag and raw_canonical_tag.get("href") else None
    raw_robots_tag = raw_soup.find("meta", attrs={"name": "robots"})
    raw_robots = raw_robots_tag.get("content") if raw_robots_tag else None
    raw_h1s = [h.get_text(strip=True) for h in raw_soup.find_all("h1")]
    raw_body = raw_soup.body.get_text(separator=" ", strip=True) if raw_soup.body else ""

    return {
        "url": url,
        "title": {"raw": raw_title, "rendered": rendered_title, "match": raw_title == rendered_title},
        "canonical": {"raw": raw_canonical, "rendered": rendered_canonical, "match": raw_canonical == rendered_canonical},
        "meta_robots": {"raw": raw_robots, "rendered": rendered_robots, "match": raw_robots == rendered_robots},
        "h1": {"raw": raw_h1s, "rendered": rendered_h1s, "match": raw_h1s == rendered_h1s},
        "content_length": {"raw_words": len(raw_body.split()), "rendered_words": len(rendered_text.split())},
        "js_dependent": len(rendered_text.split()) > len(raw_body.split()) * 1.2,
    }


def check_mobile_rendering(url: str) -> dict:
    """Render page with mobile device emulation."""
    if not PLAYWRIGHT_AVAILABLE:
        return {"error": "playwright_not_installed", "skipped": True}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        device = p.devices["iPhone 14"]
        context = browser.new_context(**device)
        page = context.new_page()
        page.goto(url, wait_until="networkidle", timeout=30000)

        viewport_meta = page.query_selector('meta[name="viewport"]')
        has_viewport = viewport_meta is not None

        has_horizontal_scroll = page.evaluate(
            "document.documentElement.scrollWidth > document.documentElement.clientWidth"
        )

        page.screenshot(path="/tmp/seo_mobile_screenshot.png")
        browser.close()

    return {
        "url": url,
        "has_viewport_meta": has_viewport,
        "has_horizontal_scroll": has_horizontal_scroll,
        "screenshot_path": "/tmp/seo_mobile_screenshot.png",
    }


def check_mixed_content(url: str) -> dict:
    """Monitor network requests for HTTP resources on HTTPS pages."""
    if not PLAYWRIGHT_AVAILABLE:
        return {"error": "playwright_not_installed", "skipped": True}

    mixed_requests = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        def on_request(request):
            if request.url.startswith("http://") and not request.url.startswith("http://localhost"):
                mixed_requests.append({
                    "url": request.url,
                    "resource_type": request.resource_type,
                })

        page.on("request", on_request)
        page.goto(url, wait_until="networkidle", timeout=30000)
        browser.close()

    return {
        "url": url,
        "is_https": url.startswith("https://"),
        "mixed_content_count": len(mixed_requests),
        "mixed_requests": mixed_requests[:20],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Browser-based SEO checks")
    parser.add_argument("url", help="URL to check")
    parser.add_argument("--check", choices=["js_render", "mobile", "mixed_content"], default="js_render")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not PLAYWRIGHT_AVAILABLE:
        print("Playwright not installed. Run: pip install playwright && playwright install chromium", file=sys.stderr)
        sys.exit(1)

    checks = {
        "js_render": check_js_rendering,
        "mobile": check_mobile_rendering,
        "mixed_content": check_mixed_content,
    }

    result = checks[args.check](args.url)

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print(json.dumps(result, indent=2, default=str))
