"""Technical SEO crawler for auditing a website.

Usage:
    python crawl_audit.py <url> [--max-pages 100] [--json]

Checks: status codes, canonicals, robots.txt, redirects, internal links,
orphan pages, crawl depth, sitemap validation.
"""

import argparse
import json
import sys
from urllib.parse import urlparse, urljoin
from collections import defaultdict

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Required: pip install requests beautifulsoup4 lxml", file=sys.stderr)
    sys.exit(1)

from utils import normalize_url, is_internal_url, is_safe_url, extract_domain


DEFAULT_MAX_PAGES = 100
USER_AGENT = "Mozilla/5.0 (compatible; SEOSuiteBot/0.1; +https://github.com/JAYANTCH1797/claude-seo)"


def fetch_robots_txt(base_url: str) -> dict:
    """Fetch and parse robots.txt."""
    robots_url = urljoin(base_url, "/robots.txt")
    try:
        resp = requests.get(robots_url, timeout=10, headers={"User-Agent": USER_AGENT})
        if resp.status_code == 200:
            return {
                "exists": True,
                "status_code": 200,
                "content": resp.text,
                "sitemaps": [
                    line.split(":", 1)[1].strip()
                    for line in resp.text.splitlines()
                    if line.lower().startswith("sitemap:")
                ],
            }
        return {"exists": False, "status_code": resp.status_code}
    except requests.RequestException as e:
        return {"exists": False, "error": str(e)}


def fetch_sitemap(sitemap_url: str) -> dict:
    """Fetch and parse an XML sitemap."""
    try:
        resp = requests.get(sitemap_url, timeout=15, headers={"User-Agent": USER_AGENT})
        if resp.status_code != 200:
            return {"valid": False, "status_code": resp.status_code}
        soup = BeautifulSoup(resp.text, "lxml-xml")
        urls = [loc.text for loc in soup.find_all("loc")]
        return {
            "valid": True,
            "url_count": len(urls),
            "urls": urls[:500],
            "is_index": bool(soup.find("sitemapindex")),
        }
    except Exception as e:
        return {"valid": False, "error": str(e)}


def crawl_page(url: str, session: requests.Session) -> dict:
    """Crawl a single page and extract SEO-relevant data."""
    if not is_safe_url(url):
        return {"url": url, "error": "blocked_private_ip"}

    result = {
        "url": url,
        "status_code": None,
        "redirect_chain": [],
        "canonical": None,
        "title": None,
        "meta_robots": None,
        "h1": [],
        "internal_links": [],
        "external_links": [],
        "images_without_alt": 0,
        "word_count": 0,
    }

    try:
        resp = session.get(url, timeout=15, allow_redirects=True)
        result["status_code"] = resp.status_code

        if resp.history:
            result["redirect_chain"] = [
                {"url": r.url, "status_code": r.status_code}
                for r in resp.history
            ]

        if resp.status_code != 200:
            return result

        soup = BeautifulSoup(resp.text, "lxml")
        base_domain = f"{urlparse(url).scheme}://{urlparse(url).netloc}"

        canonical_tag = soup.find("link", rel="canonical")
        if canonical_tag and canonical_tag.get("href"):
            result["canonical"] = canonical_tag["href"]

        title_tag = soup.find("title")
        if title_tag:
            result["title"] = title_tag.get_text(strip=True)

        robots_meta = soup.find("meta", attrs={"name": "robots"})
        if robots_meta:
            result["meta_robots"] = robots_meta.get("content", "")

        result["h1"] = [h.get_text(strip=True) for h in soup.find_all("h1")]

        for a in soup.find_all("a", href=True):
            href = urljoin(url, a["href"])
            if is_internal_url(href, base_domain):
                result["internal_links"].append({
                    "url": normalize_url(href),
                    "anchor": a.get_text(strip=True)[:100],
                })
            else:
                result["external_links"].append(normalize_url(href))

        for img in soup.find_all("img"):
            if not img.get("alt", "").strip():
                result["images_without_alt"] += 1

        body = soup.find("body")
        if body:
            text = body.get_text(separator=" ", strip=True)
            result["word_count"] = len(text.split())

    except requests.RequestException as e:
        result["error"] = str(e)

    return result


def run_audit(start_url: str, max_pages: int = DEFAULT_MAX_PAGES) -> dict:
    """Run a technical SEO crawl audit starting from start_url."""
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    base_domain = f"{urlparse(start_url).scheme}://{urlparse(start_url).netloc}"

    robots = fetch_robots_txt(base_domain)

    sitemap_data = None
    if robots.get("sitemaps"):
        sitemap_data = fetch_sitemap(robots["sitemaps"][0])

    crawled = {}
    to_crawl = [normalize_url(start_url)]
    internal_link_targets = defaultdict(int)

    while to_crawl and len(crawled) < max_pages:
        url = to_crawl.pop(0)
        if url in crawled:
            continue

        page_data = crawl_page(url, session)
        crawled[url] = page_data

        for link in page_data.get("internal_links", []):
            link_url = link["url"]
            internal_link_targets[link_url] += 1
            if link_url not in crawled and link_url not in to_crawl:
                to_crawl.append(link_url)

    orphan_pages = []
    if sitemap_data and sitemap_data.get("urls"):
        sitemap_urls = {normalize_url(u) for u in sitemap_data["urls"]}
        crawled_urls = set(crawled.keys())
        for surl in sitemap_urls:
            if surl not in crawled_urls and internal_link_targets.get(surl, 0) == 0:
                orphan_pages.append(surl)

    return {
        "base_url": base_domain,
        "pages_crawled": len(crawled),
        "robots_txt": robots,
        "sitemap": sitemap_data,
        "pages": crawled,
        "internal_link_counts": dict(internal_link_targets),
        "orphan_pages": orphan_pages[:50],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Technical SEO crawl audit")
    parser.add_argument("url", help="URL to audit")
    parser.add_argument("--max-pages", type=int, default=DEFAULT_MAX_PAGES)
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    result = run_audit(args.url, args.max_pages)

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print(f"Crawled {result['pages_crawled']} pages on {result['base_url']}")
        print(f"Robots.txt: {'Found' if result['robots_txt'].get('exists') else 'Not found'}")
        print(f"Sitemap: {'Valid' if result.get('sitemap', {}).get('valid') else 'Not found/invalid'}")
        print(f"Orphan pages: {len(result['orphan_pages'])}")

        errors = [p for p in result["pages"].values() if p.get("status_code") and p["status_code"] >= 400]
        redirects = [p for p in result["pages"].values() if p.get("redirect_chain")]
        no_canonical = [p for p in result["pages"].values() if p.get("status_code") == 200 and not p.get("canonical")]

        print(f"4xx/5xx errors: {len(errors)}")
        print(f"Pages with redirects: {len(redirects)}")
        print(f"Pages missing canonical: {len(no_canonical)}")
