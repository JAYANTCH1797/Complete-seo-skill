"""Shared utilities for SEO Suite scripts."""

import json
import csv
import io
import re
from urllib.parse import urlparse, urljoin, urlunparse, parse_qs, urlencode


def normalize_url(url: str) -> str:
    """Normalize a URL: lowercase scheme/host, remove fragments, sort params."""
    parsed = urlparse(url)
    scheme = parsed.scheme.lower() or "https"
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip("/") or "/"
    params = parse_qs(parsed.query, keep_blank_values=True)
    sorted_query = urlencode(sorted(params.items()), doseq=True)
    return urlunparse((scheme, netloc, path, "", sorted_query, ""))


def is_internal_url(url: str, base_domain: str) -> bool:
    """Check if a URL belongs to the same domain."""
    parsed = urlparse(url)
    base_parsed = urlparse(base_domain)
    return parsed.netloc.lower().replace("www.", "") == base_parsed.netloc.lower().replace("www.", "")


def extract_domain(url: str) -> str:
    """Extract the domain from a URL."""
    parsed = urlparse(url)
    return parsed.netloc.lower()


def output_json(data: dict, filepath: str = None) -> str:
    """Output data as formatted JSON. Optionally write to file."""
    result = json.dumps(data, indent=2, default=str)
    if filepath:
        with open(filepath, "w") as f:
            f.write(result)
    return result


def output_csv(rows: list[dict], filepath: str = None) -> str:
    """Output data as CSV. Optionally write to file."""
    if not rows:
        return ""
    fieldnames = rows[0].keys()
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
    result = buf.getvalue()
    if filepath:
        with open(filepath, "w") as f:
            f.write(result)
    return result


SSRF_BLOCKED_RANGES = [
    "127.", "10.", "0.", "169.254.",
    "192.168.",
]


def is_safe_url(url: str) -> bool:
    """Basic SSRF check: block private IP ranges."""
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    if hostname == "localhost":
        return False
    for prefix in SSRF_BLOCKED_RANGES:
        if hostname.startswith(prefix):
            return False
    if hostname.startswith("172."):
        parts = hostname.split(".")
        if len(parts) >= 2 and 16 <= int(parts[1]) <= 31:
            return False
    return True
