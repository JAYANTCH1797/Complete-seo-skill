"""SERP rank checker — find where a domain ranks for given keywords.

Usage:
    python serp_scraper.py "keyword" [--json] [--domain blog.inito.com]
    python serp_scraper.py --keywords "kw1" "kw2" "kw3" [--json]
    python serp_scraper.py --batch keywords.txt [--json]

Engines:
    --engine ddg     DuckDuckGo HTML (default) — Bing index, no bot blocks
    --engine google  Google via Playwright — may trigger CAPTCHA, needs
                     headed mode. Solve CAPTCHAs manually in the browser.

Limitations:
    - Google blocks automated requests (both headless and headed Playwright,
      and direct HTTP requests). The Google engine requires manual CAPTCHA
      solving in a visible browser window.
    - DuckDuckGo uses Bing's index. Rankings will differ from Google.
    - DuckDuckGo rate-limits after ~2 queries per session. Use --delay to
      increase wait time between queries (default 6-10s).
    - For exact Google positions, use Semrush API or Google Search Console.

Requires: pip install requests beautifulsoup4
          pip install playwright && playwright install chromium  (for --engine google)
"""

import argparse
import json
import random
import sys
import time
from pathlib import Path
from urllib.parse import parse_qs, quote_plus, urlparse

import requests
from bs4 import BeautifulSoup


DEFAULT_DOMAIN = "blog.inito.com"
MAX_RESULTS = 30  # How many results to check
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36"
)


def _delay(lo=2.0, hi=5.0):
    time.sleep(random.uniform(lo, hi))


# ─── DuckDuckGo engine (requests + BS4) ────────────────────────────

def _ddg_search(keyword: str, target_domain: str) -> dict:
    """Search DuckDuckGo HTML and find target_domain's position."""
    result = {
        "keyword": keyword,
        "target_domain": target_domain,
        "engine": "duckduckgo (bing index)",
        "position": None,
        "url": None,
        "total_results_checked": 0,
        "top_results": [],
        "error": None,
    }

    try:
        url = f"https://html.duckduckgo.com/html/?q={quote_plus(keyword)}"
        headers = {"User-Agent": USER_AGENT}

        # Retry on 202 (rate limit) up to 3 times with increasing backoff
        resp = None
        for attempt in range(3):
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code == 200:
                break
            if resp.status_code == 202:
                wait = 8 + (attempt * 5)
                print(
                    f"    Rate limited (202), waiting {wait}s... (attempt {attempt+1}/3)",
                    file=sys.stderr,
                )
                time.sleep(wait)
            else:
                break

        if resp.status_code != 200:
            result["error"] = f"HTTP {resp.status_code} after retries"
            return result

        soup = BeautifulSoup(resp.text, "html.parser")
        links = soup.select(".result__a")

        for i, a in enumerate(links):
            href = a.get("href", "")
            title = a.text.strip()

            # DDG wraps URLs in a redirect — extract actual URL
            if "uddg=" in href:
                qs = parse_qs(urlparse(href).query)
                href = qs.get("uddg", [href])[0]

            if not href.startswith("http"):
                continue

            domain = urlparse(href).netloc.replace("www.", "")
            pos = i + 1

            entry = {
                "position": pos,
                "url": href,
                "domain": domain,
                "title": title,
            }
            result["top_results"].append(entry)

            if target_domain in domain or domain in target_domain:
                result["position"] = pos
                result["url"] = href

        result["total_results_checked"] = len(result["top_results"])

    except Exception as e:
        result["error"] = str(e)

    return result


# ─── Google engine (Playwright) ─────────────────────────────────────

def _google_search(keyword: str, target_domain: str, page) -> dict:
    """Search Google via Playwright page and find target_domain."""
    from playwright.sync_api import TimeoutError as PWTimeout

    result = {
        "keyword": keyword,
        "target_domain": target_domain,
        "engine": "google",
        "position": None,
        "url": None,
        "total_results_checked": 0,
        "top_results": [],
        "error": None,
    }

    try:
        search_url = (
            f"https://www.google.com/search?"
            f"q={quote_plus(keyword)}&num={MAX_RESULTS}&hl=en"
        )
        page.goto(search_url, wait_until="domcontentloaded", timeout=15000)
        _delay(1.0, 2.5)

        # Wait / handle CAPTCHA
        deadline = time.time() + 60
        while time.time() < deadline:
            if page.query_selector("div.g"):
                break
            consent = page.query_selector("button#L2AGLb")
            if consent:
                consent.click()
                _delay(1.0, 2.0)
                continue
            if "/sorry/" in page.url:
                print(
                    "  ⚠ CAPTCHA — solve it in the browser window...",
                    file=sys.stderr,
                )
                while "/sorry/" in page.url and time.time() < deadline:
                    time.sleep(2)
                if "/sorry/" not in page.url:
                    _delay(1.5, 2.5)
                    continue
                else:
                    result["error"] = "CAPTCHA not solved in time"
                    return result
            time.sleep(0.5)
        else:
            result["error"] = "Timeout waiting for results"
            return result

        # Extract organic results
        containers = page.query_selector_all("div.g")
        for container in containers:
            link_el = container.query_selector("a[href]")
            if not link_el:
                continue
            href = link_el.get_attribute("href") or ""
            if not href.startswith("http") or "google.com" in href:
                continue

            domain = urlparse(href).netloc.replace("www.", "")
            title_el = container.query_selector("h3")
            title = title_el.inner_text().strip() if title_el else ""
            pos = len(result["top_results"]) + 1

            entry = {
                "position": pos,
                "url": href,
                "domain": domain,
                "title": title,
            }
            result["top_results"].append(entry)

            if target_domain in domain or domain in target_domain:
                if result["position"] is None:
                    result["position"] = pos
                    result["url"] = href

        result["total_results_checked"] = len(result["top_results"])

    except Exception as e:
        result["error"] = str(e)

    return result


# ─── Runner ─────────────────────────────────────────────────────────

def run(
    keywords: list[str],
    target_domain: str = DEFAULT_DOMAIN,
    engine: str = "ddg",
) -> list[dict]:
    """Check rankings for all keywords."""
    all_results = []

    if engine == "google":
        from playwright.sync_api import sync_playwright

        with sync_playwright() as pw:
            browser = pw.chromium.launch(
                headless=False,
                args=["--disable-blink-features=AutomationControlled"],
            )
            context = browser.new_context(
                user_agent=USER_AGENT,
                viewport={"width": 1440, "height": 900},
                locale="en-US",
            )
            page = context.new_page()
            page.goto("https://www.google.com", wait_until="domcontentloaded", timeout=15000)
            _delay(1.5, 3.0)

            for i, kw in enumerate(keywords):
                if i > 0:
                    _delay(4.0, 8.0)
                r = _google_search(kw, target_domain, page)
                all_results.append(r)
                _print_progress(i, len(keywords), r)

            browser.close()
    else:
        for i, kw in enumerate(keywords):
            if i > 0:
                _delay(6.0, 10.0)  # Longer delay to avoid DDG rate limits
            r = _ddg_search(kw, target_domain)
            all_results.append(r)
            _print_progress(i, len(keywords), r)

    return all_results


def _print_progress(i: int, total: int, r: dict):
    pos = r["position"]
    pos_str = f"#{pos}" if pos else "not found"
    n = r["total_results_checked"]
    err = f" [ERROR: {r['error']}]" if r["error"] else ""
    print(
        f"  [{i+1}/{total}] \"{r['keyword']}\" → {pos_str} (checked {n}){err}",
        file=sys.stderr,
    )


# ─── Output formatting ─────────────────────────────────────────────

def format_table(results: list[dict]) -> str:
    lines = []
    engine = results[0]["engine"] if results else "unknown"
    td = results[0]["target_domain"] if results else DEFAULT_DOMAIN

    lines.append(f"\nSERP Rank Check — {td}")
    lines.append(f"Engine: {engine}")
    if "bing" in engine.lower() or "duck" in engine.lower():
        lines.append("Note: DuckDuckGo uses Bing's index. Google rankings may differ.")
        lines.append("      For Google positions, use Semrush or Google Search Console.")
    lines.append("")
    lines.append(f"{'#':<4} {'Keyword':<50} {'Position':<16} {'URL'}")
    lines.append("─" * 115)

    found = 0
    for i, r in enumerate(results, 1):
        kw = r["keyword"][:49]
        if r["error"]:
            pos_str = "ERROR"
        elif r["position"]:
            pos_str = f"#{r['position']}"
            found += 1
        else:
            pos_str = f"Not in top {r['total_results_checked']}"
        url = r.get("url") or "—"
        lines.append(f"{i:<4} {kw:<50} {pos_str:<16} {url}")

    lines.append("─" * 115)
    lines.append(f"Found: {found}/{len(results)} keywords ranking for {td}\n")

    # Top 5 per keyword
    lines.append("── Top results per keyword ──\n")
    for r in results:
        if r["error"]:
            lines.append(f'  "{r["keyword"]}": ERROR — {r["error"]}')
            continue
        lines.append(f'  "{r["keyword"]}":')
        for t in r["top_results"][:5]:
            marker = "  ★" if td in t["domain"] else "   "
            lines.append(
                f"   {marker} #{t['position']:<3} {t['domain']:<35} {t['title'][:55]}"
            )
        lines.append("")

    return "\n".join(lines)


# ─── CLI ────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Check SERP rankings for a domain"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("keyword", nargs="?", help="Single keyword")
    group.add_argument("--batch", metavar="FILE", help="File with keywords (one per line)")
    group.add_argument("--keywords", nargs="+", metavar="KW", help="Multiple keywords")

    parser.add_argument("--domain", default=DEFAULT_DOMAIN, help=f"Target domain (default: {DEFAULT_DOMAIN})")
    parser.add_argument("--json", action="store_true", dest="json_output", help="JSON output")
    parser.add_argument("--engine", choices=["ddg", "google"], default="ddg",
                        help="Search engine: ddg (default, reliable) or google (needs Playwright, may CAPTCHA)")

    args = parser.parse_args()

    if args.batch:
        kw_path = Path(args.batch)
        if not kw_path.exists():
            print(f"Error: {args.batch} not found", file=sys.stderr)
            sys.exit(1)
        keywords = [l.strip() for l in kw_path.read_text().splitlines() if l.strip() and not l.startswith("#")]
    elif args.keywords:
        keywords = args.keywords
    else:
        keywords = [args.keyword]

    engine_label = "DuckDuckGo (Bing index)" if args.engine == "ddg" else "Google (Playwright)"
    print(f"Engine: {engine_label}", file=sys.stderr)
    print(f"Checking {len(keywords)} keyword(s) for {args.domain}...\n", file=sys.stderr)

    results = run(keywords, target_domain=args.domain, engine=args.engine)

    if args.json_output:
        print(json.dumps(results, indent=2))
    else:
        print(format_table(results))


if __name__ == "__main__":
    main()
