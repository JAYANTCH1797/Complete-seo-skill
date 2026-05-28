---
name: seo-suite
description: >
  Comprehensive SEO analysis and optimization suite. Routes to specialized
  reference modules for technical audits, keyword research, content optimization,
  backlink analysis, SERP analysis, and competitor benchmarking.
  Trigger on: "SEO", "audit", "keyword research", "backlinks", "technical SEO",
  "content optimization", "SERP", "competitor analysis", "content brief",
  "topic cluster", "content gap".
user-invokable: true
argument-hint: "[command] [url|keyword|topic]"
allowed-tools: Read, Grep, Glob, Bash, WebFetch, WebSearch, Agent
metadata:
  author: jayant
  version: "0.1.0"
  license: MIT
---

# SEO Suite

## Routing Table

Match the user's request to the correct reference module. Load the reference file with the Read tool, then follow its methodology.

| User Says | Load Reference | Description |
|-----------|---------------|-------------|
| "technical audit", "crawl issues", "site speed", "robots.txt", "CWV", "Core Web Vitals", "indexing issues", "redirect audit", "security headers" | `../../references/technical-seo.md` | 13-category technical SEO audit |
| "keyword research", "search volume", "keyword difficulty", "find keywords", "what to target" | `../../references/keyword-research.md` | Query intent, volume analysis, KD scoring, keyword clustering |
| "content gap", "competitor keywords", "missing topics", "what are they ranking for" | `../../references/content-gap.md` | Competitor URL diffing, missing topic detection |
| "topic cluster", "pillar page", "content strategy", "content calendar", "content pruning" | `../../references/content-cluster.md` | Pillar/spoke mapping, internal linking strategy, cannibalization |
| "evaluate content", "is this good enough to rank", "content review", "compare against competitors", "pre-publish review", "GEO optimize", "AI optimization" | `../../references/content-evaluation.md` | Gate check: content competitiveness, competitor analysis (content + backlinks), E-E-A-T, GEO/AI extraction, featured snippets |
| "on-page", "title tag", "meta description", "heading optimization", "optimize tags", "fix metadata", "on-page score", "on-page audit" | `../../references/on-page-optimization.md` | Scored on-page audit (13 categories, 100 points): URL slug, title, meta desc, H1, headings, keyword/entity coverage, schema, OG/social, linking, media, content structure, E-E-A-T, technical crawlability |
| "SERP analysis", "SERP features", "what does the SERP look like" | `../../references/serp-analysis.md` | Feature detection, SERP layout, intent matching |
| "backlinks", "link building", "link profile", "referring domains", "toxic links" | `../../references/backlink-analysis.md` | Link profile audit, quality scoring, building strategy |
| "competitor analysis", "share of voice", "benchmarking", "compare domains" | `../../references/competitor-benchmarking.md` | Domain comparison, rank tracking, share of voice |
| "content brief", "write brief", "brief for [topic]" | `../../references/content-brief.md` | Brief generation from keyword + SERP + gap data |

If the request spans multiple areas (e.g., "full SEO audit"), load references in this order:
1. technical-seo.md (site health first)
2. keyword-research.md (what to target)
3. content-gap.md (what's missing across the site)
4. content-evaluation.md (is the content competitive for its keyword?)
5. on-page-optimization.md (are the tags and structure correct?)

## Content Pipeline (for new or existing content)

When auditing or creating a specific piece of content, follow this sequence:
1. keyword-research.md → finalize keyword
2. content-brief.md → generate brief, write content
3. **content-evaluation.md → gate check: is content competitive?** (if no → fix content or change keyword)
4. on-page-optimization.md → optimize tags and structure
5. technical-seo.md → verify page-level technical health

## Available Tools

### Scripts (run via Bash)
- `../../scripts/crawl_audit.py <url>` — Technical SEO spider: status codes, canonicals, robots.txt, redirects, internal links
- `../../scripts/browser_automation.py <url>` — Playwright: JS rendering comparison, mobile emulation, mixed content, CWV lab data
- `../../scripts/semrush_api.py` — Semrush API wrapper for keyword/domain/backlink data
- `../../scripts/serp_scraper.py` — SERP feature extraction
- `../../scripts/utils.py` — Shared helpers (URL normalization, HTTP fetching, output formatting)

### Semrush MCP Tools (if available)
- `keyword_research` — Search volume, difficulty, intent, related keywords
- `organic_research` — Domain's organic keyword rankings and traffic
- `backlink_research` — Backlink profile, referring domains, anchor text
- `overview_research` — Domain overview (traffic, keywords, authority)
- `url_research` — Single URL metrics
- `siteaudit_research` — Site-wide technical audit data
- `tracking_research` — Rank tracking data
- `trends_research` — Keyword trend data

### Browser Automation (Playwright)
For checks requiring a real browser: JS rendering, soft 404 detection, mobile rendering, mixed content, CWV lab data, lazy loading, broken link crawling. Falls back to requests + BeautifulSoup when Playwright is unavailable.

## General Workflow

1. **Identify intent** — Match user request to routing table above
2. **Load reference** — Read the relevant reference file for methodology
3. **Gather data** — Use scripts, Semrush MCP, or WebFetch to collect data
4. **Ask when needed** — If the user hasn't specified a URL, keyword, or topic, ask before proceeding. For keyword research, also ask about their audience and what topics they hear discussed (Reddit, forums, reviews, customer conversations).
5. **Analyze** — Follow the reference file's framework to analyze the data
6. **Deliver** — Output actionable findings with priority levels and specific fixes

## Keyword Discovery Note

Keyword research is a multi-phase workflow with multiple entry points. Load `../../references/keyword-research.md` for the full process.

Phase 1 starts with seed research — Claude offers four paths: online research (Reddit/web), user-provided insights (sales calls, support, ORM), competitor gap analysis (defers to `../../references/content-gap.md`), or specific topic expansion. Paths can be combined. Claude presents findings and waits before moving to Semrush validation.
