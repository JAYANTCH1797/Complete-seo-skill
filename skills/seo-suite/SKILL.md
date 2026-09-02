---
name: seo-suite
description: >
  Comprehensive SEO analysis and optimization suite. Routes to specialized
  reference modules for technical audits, keyword research, content optimization,
  backlink analysis, SERP analysis, and competitor benchmarking.
  Trigger on: "SEO", "audit", "keyword research", "backlinks", "technical SEO",
  "content optimization", "SERP", "competitor analysis", "content brief",
  "topic cluster", "content gap".
user-invocable: true
argument-hint: "[command] [url|keyword|topic]"
allowed-tools: Read, Grep, Glob, Bash, WebFetch, WebSearch, Agent
---

# SEO Suite

> **Sibling skills.** Two capabilities live in their own skills, not in this routing table:
> - `seo-audit` (`skills/seo-audit/SKILL.md`) — scored on-page audit. Shares this plugin's `references/on-page-optimization.md` rubric, and adds the pre-analysis intake plus live-URL vs. draft scoring modes.
> - `content-qa` (`skills/content-qa/SKILL.md`) — real-browser QA of a published page (render parity, mobile, broken assets, console errors). Use after a publish or deploy.

## Routing Table

Match the user's request to the correct reference module. Load the reference file with the Read tool, then follow its methodology.

| User Says | Load Reference | Description |
|-----------|---------------|-------------|
| "technical audit", "crawl issues", "site speed", "robots.txt", "CWV", "Core Web Vitals", "indexing issues", "redirect audit", "security headers" | `../../references/technical-seo.md` | 13-category technical SEO audit |
| "keyword research", "search volume", "keyword difficulty", "find keywords", "what to target", "fan-out", "sub-clusters", "what should this blog cover" | `../../references/keyword-research.md` | Query intent, volume analysis, KD scoring, sub-cluster fan-out (LLM + Semrush + PAA), existing content refresh |
| "content gap", "competitor keywords", "missing topics", "what are they ranking for" | `../../references/content-gap.md` | Competitor URL diffing, missing topic detection |
| "topic cluster", "pillar page", "content strategy", "content calendar", "content pruning" | `../../references/content-cluster.md` | Pillar/spoke mapping, internal linking strategy, cannibalization |
| "evaluate content", "is this good enough to rank", "content review", "compare against competitors", "pre-publish review", "GEO optimize", "AI optimization" | `../../references/content-evaluation.md` | Gate check: content competitiveness, competitor analysis (content + backlinks), E-E-A-T, GEO/AI extraction, featured snippets |
| "on-page", "audit this page/blog", "score this page", "is this optimized", "title tag", "meta description", "heading optimization", "optimize tags", "fix metadata", "on-page score", "audit my draft" | **`seo-audit` skill** → `../../references/on-page-optimization.md` | Scored on-page audit (14 categories, 100 points): intent alignment, URL slug, title, meta desc, H1, headings, keyword/entity coverage, schema, OG/social, linking, media, content structure, E-E-A-T, technical crawlability. Supports live-URL and pre-publish **draft mode**. Prefer invoking the standalone `seo-audit` skill — it carries the Step 0 intake and mode selection. |
| "SERP analysis", "SERP features", "what does the SERP look like" | `../../references/serp-analysis.md` | Feature detection, SERP layout, intent matching |
| "backlinks", "link building", "link profile", "referring domains", "toxic links" | `../../references/backlink-analysis.md` | Link profile audit, quality scoring, building strategy |
| "competitor analysis", "share of voice", "benchmarking", "compare domains" | `../../references/competitor-benchmarking.md` | Domain comparison, rank tracking, share of voice |
| "content brief", "write brief", "brief for [topic]" | `../../references/content-brief.md` | Brief generation from keyword + SERP + gap data |
| "test this page", "QA this blog", "did it publish correctly", "check on mobile", "is anything broken", "browser test" | **`content-qa` skill** | Real-browser test of a live/staging URL: JS render parity, mobile layout, soft 404, console/network errors, broken images and links, head survival, lab CWV. Delivery test, not a quality score. |
| "Payload", "the CMS", "pull the draft", "update the post", "publish this", "what's in the CMS" | `../../references/payload-cms.md` | Read/write content in Payload CMS over MCP: pull a draft, audit it in draft mode, write the approved slug/title/meta back, then QA the live URL. Write operations always require confirmation. |

If the request spans multiple areas (e.g., "full SEO audit"), load references in this order:
1. technical-seo.md (site health first)
2. keyword-research.md (what to target)
3. content-gap.md (what's missing across the site)
4. content-evaluation.md (is the content competitive for its keyword?)
5. on-page-optimization.md via the `seo-audit` skill (are intent, tags, and structure correct?)

## Content Pipeline (for new or existing content)

When auditing or creating a specific piece of content, follow this sequence:
1. keyword-research.md → finalize keyword
2. content-brief.md → generate brief, write content
3. **content-evaluation.md → gate check: is content competitive?** (if no → fix content or change keyword)
4. `seo-audit` skill (on-page-optimization.md) → score intent + tags + structure; use draft mode pre-publish
5. technical-seo.md → verify page-level technical health

## Available Tools

### Scripts (run via Bash)
- `../../scripts/crawl_audit.py <url>` — Technical SEO spider: status codes, canonicals, robots.txt, redirects, internal links
- `../../scripts/browser_automation.py <url> --check js_render|mobile|mixed_content` — Playwright: JS render comparison, mobile emulation, mixed content. **Three checks only — no CWV, no soft-404, no link crawling.**
- `../../scripts/semrush_api.py` — **stub, not runnable.** Documents the Semrush MCP tool names only; contains no executable code. Do not call it as a fallback.
- `../../scripts/serp_scraper.py` — SERP feature extraction
- `../../scripts/utils.py` — Shared helpers (URL normalization, HTTP fetching, output formatting)

### SEO Data Provider — Semrush *or* Ahrefs (MCP)

This plugin bundles both. **Check which is actually connected before assuming**, and say which one supplied the numbers in every report — the two providers' volume and difficulty figures are not interchangeable, so never mix them in one comparison.

Preference order: Semrush MCP → Ahrefs MCP → public SERP data via WebSearch/`serp_scraper.py`, with the limitation stated in the report. There is **no working direct-API fallback** — `scripts/semrush_api.py` is a stub. If neither provider is connected, say the volume/KD figures are unavailable rather than estimating them.

**Semrush MCP tools:**
- `keyword_research` — Search volume, difficulty, intent, related keywords
- `organic_research` — Domain's organic keyword rankings and traffic
- `backlink_research` — Backlink profile, referring domains, anchor text
- `overview_research` — Domain overview (traffic, keywords, authority)
- `url_research` — Single URL metrics
- `siteaudit_research` — Site-wide technical audit data
- `tracking_research` — Rank tracking data
- `trends_research` — Keyword trend data

**Ahrefs MCP:** covers the same ground — keyword metrics, organic rankings, backlink profiles, domain and URL authority, site audit data. List the server's actual tools before calling them; don't assume Semrush's names.

Both connect over OAuth on first use and require an active subscription. If neither is connected, tell the user to run `/mcp` to authorize, and continue with what's available rather than stalling.

### Payload CMS (MCP)
Read and write the content itself — pull a draft, apply approved on-page fixes, check the content inventory. See `../../references/payload-cms.md`. Tool names are generated from the site's own collection slugs, so list them first. **Every write needs explicit confirmation; never call a delete tool.**

### Browser Automation (Playwright MCP)
For checks requiring a real browser: JS render parity, mobile rendering, soft 404 detection, console and network errors, mixed content, broken images and links, lab CWV. Use the `content-qa` skill — it owns this workflow. Fallback order: Playwright MCP → `../../scripts/browser_automation.py` (three checks only: `js_render`, `mobile`, `mixed_content`) → requests + BeautifulSoup, noting every skipped browser check.

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

Phase 2 now includes **sub-cluster fan-out** (step 2e): for each priority seed, map the sub-topics the content must cover using three sources — Claude decomposition (generation), Semrush `phrase_questions` (validation with volume/KD), and user-provided Google PAA questions (ground truth). The cross-matched sub-cluster table feeds into both new content (defines sections to write) and existing content refresh (surfaces missing sections to add).
