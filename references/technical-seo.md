# Technical SEO Audit Reference

Run a technical SEO audit across 13 categories. For each category, follow the checks below and classify every finding as Critical / High / Medium / Low priority.

Use `scripts/crawl_audit.py` for HTTP-level checks and `scripts/browser_automation.py` (Playwright) for browser-level checks. Fall back to `requests` + BeautifulSoup when Playwright is unavailable, and note which browser checks were skipped.

---

## 1. Crawlability

Goal: Ensure search engines can discover and access all important pages.

### robots.txt Validation
- Fetch `{domain}/robots.txt` — if missing, flag as **High** (not critical; Google still crawls without it, but you lose control)
- Parse syntax: check for malformed rules, wildcard misuse, conflicting allow/disallow
- **Check for accidental blocks**: Are important pages or sections disallowed? Are CSS/JS resources blocked? (Blocking CSS/JS prevents Google from rendering the page correctly)
- Verify `Sitemap:` directive is present and points to a valid XML sitemap URL
- Check for overly permissive rules (e.g., `Allow: /` with no disallows may be intentional but review)

### XML Sitemap Quality
- Fetch sitemap URL from robots.txt or try `{domain}/sitemap.xml`, `{domain}/sitemap_index.xml`
- If missing entirely: flag as **High** — sitemaps help Google discover pages, especially for large or new sites
- Validate XML format (well-formed, correct namespace)
- Check URL count: max 50,000 URLs per sitemap file, max 50MB uncompressed. If exceeded, need sitemap index.
- **Sample 20-50 URLs from the sitemap**: Do they return 200? Are any 404, 301, or noindex? Sitemap should only contain canonical, indexable, 200-status URLs.
- Check `<lastmod>` dates: Are they present? Are they accurate or all the same date? (Fake freshness = all dates set to today. Google has said it will ignore lastmod if it's unreliable.)
- Are important pages missing from the sitemap? Cross-reference with pages found during crawl.
- For large sites: Is a sitemap index used to organize sitemaps by section?

### Noindex Audit
- Crawl pages and check for `<meta name="robots" content="noindex">` or `X-Robots-Tag: noindex` HTTP header
- Flag pages that have noindex but appear to be important (product pages, service pages, blog posts with traffic)
- Check for noindex on paginated pages — Google has said this can prevent link equity flow
- Cross-reference: pages in the sitemap should NOT have noindex (contradiction)

### Crawl Depth
- Map the internal link structure starting from the homepage
- Flag pages that are >3 clicks from the homepage — these are deprioritized by crawlers
- Important pages (money pages, pillar content) should be within 1-2 clicks
- Flag pages only reachable through the sitemap (no internal links) — these are effectively orphaned for crawling purposes

### JavaScript Rendering Check
- **Requires Playwright**: Fetch the page with a simple HTTP request (raw HTML) and with Playwright (rendered DOM). Compare the content.
- If significant content only appears after JS execution: flag as **Medium** to **High** depending on content importance
- Identify the framework: React, Vue, Angular, Next.js, Nuxt, Gatsby, etc.
- Check if the site uses SSR, SSG, or pure CSR. Pure CSR is highest risk for SEO.
- See Category 11 (JavaScript Rendering) for detailed Dec 2025 guidance.

---

## 2. Indexability

Goal: Ensure the right pages are indexed, and duplicate/thin pages are not.

### Canonical Audit
- Every indexable page should have a self-referencing `<link rel="canonical">` tag
- Check for conflicts: canonical tag in HTML vs `Link:` HTTP header — if both present and different, flag **Critical**
- Canonical should not point to: a 404 page, a redirecting URL, a noindex page, a non-existent URL
- Canonical URL should match the protocol (https), domain (www vs non-www), and trailing slash convention of the live URL
- **JS canonical conflicts** (Dec 2025): If raw HTML canonical differs from JS-injected canonical, Google may use either. Flag as **Critical** — serve the correct canonical in initial HTML.

### Duplicate Content Detection
- Check for multiple URL variations resolving to the same content:
  - `http://` vs `https://`
  - `www.` vs non-www
  - Trailing slash vs no trailing slash
  - URL parameters creating duplicates (e.g., `?sort=price`, `?ref=email`, `?page=1`)
- All variations should 301 redirect to one canonical version
- For parameter duplicates: recommend canonical tags or robots.txt Disallow for parameter URLs
- Check for near-duplicate pages: same template with minimal content differences (especially location pages, product variants)

### Index Bloat
- Estimate indexed page count: use `site:domain.com` search operator or GSC Index Coverage report
- Compare against the number of pages that *should* be indexed (unique, valuable content pages)
- If indexed count is significantly higher than useful pages, identify the source of bloat:
  - Tag/category archive pages with thin or duplicate content
  - Internal search result pages (should always be noindex)
  - Paginated archive pages (evaluate whether they add value)
  - Faceted navigation / filter URLs (e-commerce especially)
  - Old, outdated content that should be pruned or consolidated
  - Auto-generated pages with no unique content

### Soft 404 Detection
- **Requires Playwright**: Render pages returning HTTP 200 and check if they actually show:
  - "Page not found" or similar error messaging
  - Empty or near-empty content (<50 words of unique text)
  - "No results found" (e.g., empty search results, empty category pages)
  - Generic template with no real content
- These waste crawl budget and confuse Google's index. Flag as **High**.
- Google's own documentation says it tries to detect soft 404s, but it's not always accurate — explicit handling is better.

### Thin Content Flags
- Pages with <200 words of unique content (excluding navigation, footer, sidebar)
- Pages that are mostly boilerplate with minimal unique text
- Doorway pages: nearly identical pages targeting different locations/keywords with only minor text swaps
- Note: thin content is NOT just about word count. A 100-word page that perfectly answers a query is fine. Flag only when content is clearly insufficient for the page's purpose.

---

## 3. Redirects

Goal: Ensure redirects pass link equity efficiently and don't create crawl issues.

### Redirect Chain Detection
- Crawl the site and follow all redirects
- Flag chains of 2+ hops: A → B → C (or longer). Google follows up to 10 hops but recommends max 1.
- Each hop in a chain leaks a small amount of link equity and adds latency
- **Fix**: Update all redirect sources to point directly to the final destination

### Redirect Loop Detection
- Flag any URL that redirects back to itself (A → B → A) or creates a cycle
- These are **Critical** — pages are completely inaccessible to crawlers and users

### 302 vs 301 Audit
- Find all 302 (temporary) redirects
- If the redirect has been in place for >30 days, it should almost certainly be a 301 (permanent)
- 301s explicitly signal to Google that the destination is the canonical URL and should receive the link equity
- 302s may eventually be treated as 301s by Google, but it's not guaranteed and takes longer
- Flag long-standing 302s as **High**

### 404 Pages with Backlinks
- **This is the #1 technical SEO quick win** (Ahrefs)
- Find pages returning 404 that have referring domains pointing to them (use Semrush backlink_research or check the site's backlink profile)
- Each 404 with backlinks = wasted link equity that could be recovered
- **Fix**: 301 redirect each 404 to the closest relevant live page on the site
- If no relevant page exists, consider recreating the content or redirecting to a parent category page
- Priority is proportional to the number and quality of backlinks the 404 has

### HTTP-to-HTTPS Redirect
- `http://domain.com` should 301 redirect to `https://domain.com` in a single hop
- Check for chains: `http://domain.com` → `http://www.domain.com` → `https://www.domain.com` (should be a single redirect)
- Also check: `http://www.` → `https://www.` and `https://non-www` → `https://www` (or vice versa) — all should be single hops to the canonical version

### Redirect to Non-Canonical
- Redirect destinations should be the canonical version of the target URL
- Flag redirects pointing to URLs that themselves redirect or have a different canonical tag

---

## 4. Internal Linking

Goal: Ensure important pages are discoverable, well-connected, and receive link equity.

### Orphan Page Detection
- An orphan page has zero internal links pointing to it from other pages on the site
- It can only be discovered by crawlers via the sitemap or external links — low crawl priority
- Identify orphaned pages by crawling all internal links from the homepage outward, then comparing against the sitemap or full URL list
- Flag as **High** if the orphan is an important page (product, service, content), **Medium** if it's a minor page
- **Fix**: Add internal links from relevant, contextually related pages

### Crawl Depth Audit
- Calculate the minimum number of clicks required to reach each page from the homepage
- Distribution target: 95%+ of indexable pages within 3 clicks
- Flag pages at depth 4+, especially if they're important (money pages, pillar content)
- **Fix**: Add internal links from higher-level pages. Improve navigation. Add related content sections.

### Internal Link Distribution
- Count internal links pointing to each page
- Compare: Are the site's most important pages (top revenue, target keywords) receiving the most internal links?
- Common problem: All internal links go to the blog while product/service pages are under-linked
- Check for pages with only 1-2 internal links that should have more
- Look at the homepage: What does it link to? The homepage passes the most equity — its links are the most valuable.

### Broken Internal Links
- Find internal links pointing to 404 pages, 5xx pages, or redirect chains
- Each broken link wastes link equity and creates a poor user experience
- Flag as **High** — broken internal links are entirely within your control to fix
- **Fix**: Update the link to point to the correct live URL, or remove it if the content no longer exists

### Anchor Text Quality
- Sample internal links and check their anchor text
- Good: Descriptive text that tells the user and Google what the target page is about (e.g., "keyword research guide")
- Bad: Generic "click here", "read more", "learn more", naked URLs
- Over-optimized: Exact-match keyword anchors on every internal link (looks manipulative, though Google is more lenient on internal links than external)
- Recommend: Natural, varied, descriptive anchor text

### Hub-and-Spoke Check
- Does the site organize content into topic clusters?
- A hub (pillar) page should link to all its spoke (cluster) pages, and each spoke should link back to the hub
- Check if existing content clusters have complete bidirectional linking
- Missing links between related content = missed topical authority signals

---

## 5. Crawl Budget

Goal: Ensure crawlers spend their time on pages that matter, not on waste URLs.

This category matters most for large sites (10,000+ pages). For small sites (<500 pages), crawl budget is rarely an issue — note this and move on.

### Crawl Waste Identification
- Look for URL patterns that generate many low-value pages:
  - **Parameter URLs**: `?sort=`, `?filter=`, `?color=`, `?ref=`, `?utm_*`, `?session_id=`
  - **Faceted navigation**: Combination filters creating thousands of near-duplicate URLs (e.g., `/shoes?color=red&size=10&brand=nike`)
  - **Internal search**: `/search?q=` pages should always be noindex + ideally disallowed
  - **Calendar/date archives**: Infinite past/future date pages
  - **Pagination without value**: `/page/47/` of a blog archive with no unique content
  - **Tracking/session URLs**: URLs with session IDs or user-specific parameters
- **Fix options**: noindex, Disallow in robots.txt, canonical tags, URL parameter handling in GSC

### noindex vs Disallow — When to Use Which
- `<meta name="robots" content="noindex">` — Page is crawled but not indexed. Use when you want Google to see the page (follow its links) but not index it. Example: thank-you pages, internal search results.
- `Disallow` in robots.txt — Page is not crawled at all. Use when you want to save crawl budget by preventing the request entirely. Example: admin pages, parameter URLs, development/staging sections.
- **Common mistake**: Using noindex for crawl budget savings. noindex still gets crawled. For budget, use Disallow.
- **Common mistake**: Using Disallow to de-index pages. Disallowed pages can still appear in the index (from external links, anchors, etc.) with a "no information is available for this page" snippet.
- To fully remove a page: noindex + allow crawling (so Google sees the noindex directive), OR noindex via HTTP header + Disallow (since X-Robots-Tag works even if page isn't crawled... actually, if crawling is blocked, Google can't see the header. Use the URL Removal tool for immediate de-indexing.)

### URL Parameter Handling
- Identify query parameters that create duplicate or near-duplicate content
- For each parameter, determine: Does it change the page content meaningfully, or just the sort/filter/tracking?
- Recommend: canonical tags pointing to the parameter-free version for filter/sort params
- For tracking parameters (utm_*, ref, fbclid): These should never create indexable URLs. Canonical to the clean URL.

### Crawl Stats (GSC)
- If GSC access is available, check:
  - Total pages crawled per day (trend: stable, increasing, decreasing?)
  - Average response time (increasing = server performance issue)
  - Crawl request breakdown by response code (too many 404s or 301s = waste)
  - Crawl request breakdown by file type (are crawlers spending time on PDFs, images instead of HTML?)
- Flag anomalies: sudden drops in crawl rate, spikes in error responses

### Log File Analysis Guidance
- Server access logs show exactly what Googlebot crawls, how often, and what response it gets
- Useful for: verifying Googlebot visits important pages, finding pages it never crawls, detecting crawl traps
- We can't directly analyze log files, but recommend:
  - Check server access logs for Googlebot user-agent requests
  - Tools: Screaming Frog Log Analyzer, Botify, or custom grep/awk on access logs
  - Key questions: Which pages does Googlebot crawl most? Which important pages does it skip? Are there crawl traps (infinite URL patterns)?

---

## 6. Security

Goal: Ensure the site is secure and signals trustworthiness.

### HTTPS
- The site must serve all pages over HTTPS. Flag HTTP-only as **Critical**.
- Check for valid SSL certificate (not expired, not self-signed, covers the correct domain)
- **Certificate expiry**: Flag if expiring within 30 days as **High**
- Check for mixed content: HTTPS pages loading resources (images, scripts, fonts, iframes) over HTTP
  - **Requires Playwright**: Monitor network requests during page load to catch all mixed content
  - Mixed content breaks the padlock icon and can cause browser warnings. Flag as **High**.

### Security Headers
Check for the presence and correct configuration of:

| Header | Purpose | Recommendation |
|--------|---------|---------------|
| `Strict-Transport-Security` (HSTS) | Forces HTTPS | `max-age=31536000; includeSubDomains; preload` |
| `Content-Security-Policy` (CSP) | Prevents XSS, injection | At minimum, restrict script-src |
| `X-Frame-Options` | Prevents clickjacking | `DENY` or `SAMEORIGIN` |
| `X-Content-Type-Options` | Prevents MIME sniffing | `nosniff` |
| `Referrer-Policy` | Controls referrer info | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | Controls browser features | Restrict camera, microphone, geolocation |

- Missing security headers: flag as **Medium** (not a direct ranking factor, but signals site quality and prevents attacks)
- HSTS preload: For high-security sites, check if the domain is on the HSTS preload list (hstspreload.org)

### Security.txt
- Check for `/.well-known/security.txt` (RFC 9116)
- Not an SEO factor, but signals site maturity and responsible security practices
- Flag absence as **Low**

---

## 7. URL Structure

Goal: Clean, descriptive, consistent URLs.

### Checks
- **Format**: Lowercase, hyphen-separated, no underscores, no spaces, no special characters
- **Descriptive**: URL should indicate page content (e.g., `/blog/keyword-research-guide` not `/blog/post-12847`)
- **Length**: Flag URLs >100 characters
- **No parameters for content pages**: Content should live at clean URLs, not behind `?id=` or `?p=`
- **Hierarchy**: Logical folder structure matching site architecture (e.g., `/products/shoes/running/`)
- **Trailing slash consistency**: Pick one convention (with or without) and be consistent site-wide. Flag mixed usage.
- **No double slashes**: `//` in URL paths (after protocol) indicates misconfiguration
- **URL migration risk**: If many pages redirect from a different URL pattern, the site may have recently changed its URL structure. Flag for investigation — check for missed redirects, broken links, traffic loss.

---

## 8. Mobile Optimization

Goal: The mobile version of the site is fully functional and fast.

Google crawls exclusively with the mobile Googlebot user-agent as of July 5, 2024. The mobile version IS the version Google sees.

### Checks
- **Viewport meta tag**: `<meta name="viewport" content="width=device-width, initial-scale=1">` must be present
- **Responsive CSS**: Page adapts to different screen widths. Test at 375px (iPhone SE) and 414px (iPhone 14).
- **Touch targets**: Interactive elements minimum 48x48px with 8px spacing between adjacent targets
- **Font size**: Minimum 16px base font. No text requiring zoom to read.
- **No horizontal scroll**: Content stays within viewport at all screen widths
- **Mobile content parity**: All content on desktop is also on mobile. No hidden tabs, collapsed sections that Google can't see.
- **No intrusive interstitials**: Full-screen pop-ups on mobile that cover content before the user can interact. Google penalizes these.
- **Requires Playwright**: Use mobile device emulation to render the page and visually verify layout.

---

## 9. Core Web Vitals

Goal: Meet Google's page experience benchmarks.

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | <=2.5s | 2.5s-4.0s | >4.0s |
| INP (Interaction to Next Paint) | <=200ms | 200ms-500ms | >500ms |
| CLS (Cumulative Layout Shift) | <=0.1 | 0.1-0.25 | >0.25 |

- INP replaced FID on March 12, 2024. FID was fully removed September 9, 2024. **Never reference FID.**
- Evaluation uses the **75th percentile** of real user data (CrUX field data)
- CWV are a **tiebreaker** ranking signal — they matter when content quality is similar between competitors

### Data Sources
1. **Field data (what Google uses for ranking)**: CrUX via PageSpeed Insights API, Search Console CWV report
2. **Lab data (for debugging)**: Lighthouse, WebPageTest, Chrome DevTools, Playwright + Performance API

If CrUX data is unavailable (low-traffic sites), use lab data and note that it's simulated, not real-user metrics.

For detailed LCP subparts breakdown, common bottlenecks per metric, and optimization priorities, load `references/cwv-thresholds.md`.

---

## 10. Structured Data

Goal: Correct and complete schema markup for rich result eligibility.

### Checks
- Detect existing markup: JSON-LD (preferred by Google), Microdata, RDFa
- Validate against Google's Rich Results Test requirements
- Check for required vs recommended properties (required missing = won't show rich result)
- Flag deprecated types: HowTo (Sept 2023), FAQ (restricted to gov/health only since Aug 2023), SpecialAnnouncement (July 2025)
- Check for structured data injected via JS — may face delayed processing for time-sensitive types (Product, Offer)
- Identify missing opportunities: Does the page type warrant schema it doesn't have? (e.g., blog post without Article schema, product page without Product schema)

For full schema type reference and generation, cross-reference the schema-specific reference module if available.

---

## 11. JavaScript Rendering

Goal: Critical SEO content is accessible without JavaScript execution.

### Checks
- **Requires Playwright**: Fetch page with raw HTTP request and with Playwright (full browser render). Compare:
  - Title tag
  - Meta description
  - Canonical tag
  - Meta robots
  - H1 and heading structure
  - Main body content
  - Structured data
  - Internal links
- If any critical SEO element only appears after JS execution: flag based on importance
- Identify the rendering strategy: SSR (server-side), SSG (static generation), CSR (client-side), or hybrid
- Flag pure CSR as **High** risk — Google's rendering is delayed and resource-intensive

### December 2025 Google Guidance
1. **Canonical conflicts**: If HTML canonical differs from JS-injected canonical, Google may use EITHER. Serve correct canonical in initial HTML. Flag conflicts as **Critical**.
2. **noindex in HTML + JS removes it**: Google MAY honor the raw HTML noindex. Serve correct robots directives in initial HTML.
3. **Non-200 status codes**: Google does NOT render JS on error pages. JS-injected content on 404/5xx pages is invisible.
4. **Structured data in JS**: Time-sensitive markup (Product, Offer, Event) may face delayed processing when JS-injected. Serve in initial HTML for fastest indexing.

**Best practice**: All critical SEO elements (canonical, meta robots, structured data, title, description, OG tags) should be in the initial server-rendered HTML.

---

## 12. AI Crawler Management

Goal: Make a strategic decision about AI crawler access based on your visibility goals.

### Known AI Crawlers

| Crawler | Company | robots.txt Token | Purpose |
|---------|---------|-----------------|---------|
| GPTBot | OpenAI | `GPTBot` | Model training |
| OAI-SearchBot | OpenAI | `OAI-SearchBot` | ChatGPT web search (citations) |
| ChatGPT-User | OpenAI | `ChatGPT-User` | Real-time user browsing |
| ClaudeBot | Anthropic | `ClaudeBot` | Model training |
| PerplexityBot | Perplexity | `PerplexityBot` | Search index + training |
| Bytespider | ByteDance | `Bytespider` | Model training |
| Google-Extended | Google | `Google-Extended` | Gemini training (NOT Google Search) |
| CCBot | Common Crawl | `CCBot` | Open dataset |

### Key Distinctions
- Blocking `Google-Extended` prevents Gemini training but does NOT affect Google Search or AI Overviews (those use `Googlebot`)
- Blocking `GPTBot` prevents training but does NOT prevent ChatGPT from citing your content (that's `OAI-SearchBot` and `ChatGPT-User`)
- Blocking AI crawlers while expecting AI search visibility is contradictory — flag this as a strategic issue

### Strategy Matrix

| Strategy | Allow | Block | Tradeoff |
|----------|-------|-------|----------|
| **Maximum AI visibility** | All crawlers | None | Content used for training + cited in AI search |
| **Search only, no training** | OAI-SearchBot, ChatGPT-User, PerplexityBot | GPTBot, ClaudeBot, Bytespider, Google-Extended, CCBot | Cited in AI search but content not used for model training |
| **No AI access** | None | All AI crawlers | Content protected but invisible to AI search platforms |

Check the site's robots.txt and report which strategy they're currently implementing. If they're blocking search crawlers but allowing training crawlers (or vice versa), flag the mismatch.

---

## 13. IndexNow Protocol

Goal: Faster indexing on non-Google search engines.

### Checks
- Does the site implement IndexNow? Check for API key file at `{domain}/{key}.txt`
- IndexNow is supported by: Bing, Yandex, Naver, Seznam, Yep
- Google does NOT support IndexNow (it uses its own crawling and the Indexing API for eligible content types)
- For sites that care about Bing traffic (or other supported engines): recommend implementation
- Flag absence as **Low** — nice to have, not critical

---

## Technical Quick Wins

Surface these at the top of every audit. Ordered by typical ROI:

1. **404 pages with backlinks** → 301 redirect to the closest relevant live page. Recovers link equity that's currently being wasted. Check with Semrush backlink_research or the site's backlink data.

2. **Pages ranking positions 4-20 with high impressions** → Add internal links from high-authority pages on the site. These are "striking distance" keywords that need a small boost. Check GSC data if available.

3. **Redirect chains** → Flatten to single-hop 301 redirects. Stops link equity leakage and improves crawl efficiency.

4. **Orphan pages** → Add internal links from contextually relevant pages. Makes important content discoverable to crawlers.

5. **Broken internal links** → Fix or remove. Each broken link wastes the linking page's equity and creates a dead end for crawlers and users.

---

## Output Format

```
## Technical SEO Audit: {domain}

### Technical Score: XX/100

### Category Breakdown
| Category | Status | Score | Issues |
|----------|--------|-------|--------|
| Crawlability | pass/warn/fail | XX/100 | N issues |
| Indexability | pass/warn/fail | XX/100 | N issues |
| Redirects | pass/warn/fail | XX/100 | N issues |
| Internal Linking | pass/warn/fail | XX/100 | N issues |
| Crawl Budget | pass/warn/fail | XX/100 | N issues |
| Security | pass/warn/fail | XX/100 | N issues |
| URL Structure | pass/warn/fail | XX/100 | N issues |
| Mobile | pass/warn/fail | XX/100 | N issues |
| Core Web Vitals | pass/warn/fail | XX/100 | N issues |
| Structured Data | pass/warn/fail | XX/100 | N issues |
| JS Rendering | pass/warn/fail | XX/100 | N issues |
| AI Crawlers | pass/warn/fail | XX/100 | N issues |
| IndexNow | pass/warn/fail | XX/100 | N issues |

### Quick Wins (do these first)
[Top 5 from the quick wins section, with specific URLs and actions]

### Critical Issues (fix immediately)
### High Priority (fix within 1 week)
### Medium Priority (fix within 1 month)
### Low Priority (backlog)
```

Each issue should include: what's wrong, where (specific URL), why it matters, and how to fix it.

---

## Error Handling

| Scenario | Action |
|----------|--------|
| URL unreachable | Report connection error with status code. Suggest verifying URL, DNS, and public accessibility. |
| robots.txt not found | Note absence. Recommend creating one. Continue audit on remaining categories. |
| HTTPS not configured | Flag as **Critical**. Report HTTP-only, mixed content, or certificate issues. |
| CWV field data unavailable | Note CrUX unavailable (common for low-traffic sites). Use Lighthouse lab data as proxy. |
| Playwright not available | Fall back to requests + BeautifulSoup. Note skipped checks: JS rendering comparison, soft 404 detection, mixed content monitoring, mobile rendering, CWV lab data. |
| Sitemap not found | Note absence. Try common locations. Recommend creating and submitting via GSC. |
| GSC data not available | Skip crawl stats and striking-distance keyword analysis. Note in output. |
| Semrush MCP not available | Skip backlink-based quick wins (404s with backlinks). Note in output. |
