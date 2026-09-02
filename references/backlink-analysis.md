# Backlink Analysis Reference

---
name: backlink-analysis
description: >
  Link profile audit, quality scoring, toxic link detection, competitor backlink gap analysis,
  link building strategy, brand mention auditing, and AI citation tracking.
  Evaluates five link quality dimensions (Authority, Relevance, Anchor text, Placement, Destination),
  produces a scored profile with prioritized actions. Includes AI-era off-page visibility layer
  covering unlinked brand mentions and LLM citation tracking.
tools: [Semrush MCP (backlink_research, organic_research, overview_research), WebFetch, WebSearch, Bash (scripts/crawl_audit.py)]
---

## When to Use This Reference

Load this when the user asks to:
- Audit a site's backlink profile or link health
- Find toxic or spammy links, evaluate disavow need
- Analyze competitor backlinks and find link building opportunities
- Build a link building strategy or find linkable asset ideas
- Track link velocity or diagnose unnatural link patterns
- Audit internal link equity distribution
- Track brand mentions and AI citation visibility (post-2023 off-page)

---

## Step 1: Link Profile Overview

> Get the big picture: how large, how authoritative, and how diverse is the link profile?

### 1.1 Pull Profile Metrics

**Semrush MCP:**
```
Report: backlinks_overview
Params: target=<domain>, target_type="root_domain"
```

Collect:
| Metric | What It Tells You |
|--------|------------------|
| Authority Score (AS) | Overall domain strength (0-100) |
| Trust Score | Spam risk indicator |
| Total backlinks | Raw link count |
| Referring domains (RD) | Unique linking sites (more important than raw count) |
| Follow vs nofollow ratio | Link attribute distribution |
| Text vs image vs redirect | Link type distribution |

### 1.2 Geographic & TLD Distribution

```
Report: backlinks_tld
Params: target=<domain>, target_type="root_domain", display_limit=20
```
```
Report: backlinks_geo
Params: target=<domain>, target_type="root_domain", display_limit=20
```

Check: Does geographic distribution align with target market? Unusual concentration in irrelevant countries (e.g., 40% from a country where you don't operate) is a spam signal.

### 1.3 Top Linked Pages

```
Report: backlinks_pages
Params: target=<domain>, target_type="root_domain", display_limit=20, display_sort="backlinks_num_desc"
```

Check: Are links going to the right pages (money pages, pillar content) or are they concentrated on the homepage or irrelevant pages?

### 1.4 Evaluate Profile Health

| Signal | Healthy | Investigate |
|--------|---------|------------|
| Follow/nofollow ratio | **Benchmark against niche competitors** — there is no universal ideal (web average is ~89% dofollow per Semrush 2024, but varies heavily by niche) | Dramatically different from competitors in same niche |
| Link type distribution | 85%+ text links | High image link % without good reason, high redirect % |
| IP diversity | Wide distribution across Class C subnets | Heavy concentration on few IP blocks (PBN signal) |
| RD growth | Steady growth correlating with content output | Stagnant, or sudden spikes without content to explain them |
| Geographic alignment | Matches target market | 30%+ from irrelevant geographies |

> **Important:** Do NOT cite a fixed "ideal" follow/nofollow ratio. Ahrefs, Semrush, and LinkResearchTools all agree there is no universal standard. Always compare against niche competitors.

---

## Step 2: Anchor Text Analysis

> Anchor text distribution reveals whether link building has been natural or manipulated.

### 2.1 Pull Anchor Data

```
Report: backlinks_anchors
Params: target=<domain>, target_type="root_domain", display_limit=50, display_sort="backlinks_num_desc"
```

### 2.2 Classify Anchors

Categorize every anchor into one of 6 types:

| Type | Example | What It Means |
|------|---------|---------------|
| Branded | "Inito", "inito.com" | Natural, safe, should be dominant |
| Naked URL | "https://www.inito.com/blog/..." | Natural, common in citations |
| Generic | "click here", "read more", "this article" | Low SEO value but natural |
| Topical / Partial match | "fertility monitor reviews", "PCOS hormone tracking" | Moderate SEO value, natural when contextual |
| Exact match | "[target keyword]" exactly | High SEO value but over-optimization risk |
| Image (no alt) | [image] | From image links without alt text |

### 2.3 Benchmark Distribution

Industry-observed ranges (not prescriptive targets — benchmark against your niche):

| Type | Typical Range | Alert If |
|------|---------------|----------|
| Branded + Naked URL | 50-70% combined | Below 40% (over-optimized profile) |
| Exact match | 3-10% | >15% (High severity), >25% (Critical — likely manual action risk) |
| Topical / Partial | 10-20% | >30% (may look manipulative) |
| Generic | 5-15% | Not concerning unless near zero |

> **2026 context:** Google now weights surrounding paragraph text alongside anchor text. An exact-match anchor in an irrelevant context matters less than a generic anchor in a deeply relevant paragraph. Evaluate anchor context, not just the anchor string.

> **Note:** Ahrefs explicitly refuses to recommend specific anchor text percentages. These ranges are observed patterns, not targets. Always compare against competitors in the same niche.

### 2.4 Decision Points

| Finding | Severity | Action |
|---------|----------|--------|
| Exact match >25% | Critical | Audit links, check for manual action in GSC. Consider diversifying future link building |
| Exact match 15-25% | High | Stop exact-match link building. Focus future links on branded/topical anchors |
| Foreign-language anchors >10% | Medium | Investigate — may indicate negative SEO or irrelevant link schemes |
| Single anchor dominates >30% (non-branded) | Medium | Unnatural concentration. Diversify |
| Healthy distribution | Low | No action needed |

---

## Step 3: Toxic Link Detection

> Conservative approach: Google mostly ignores bad links rather than penalizing for them. Disavow only in specific situations.

### 3.1 When to Actually Worry

**Disavow is warranted ONLY when:**
1. You have an active **manual action** in Google Search Console
2. You knowingly participated in a **link scheme** (paid links, PBN, link exchanges at scale)

**Do NOT disavow when:**
- A third-party tool flags links as "toxic" (these scores are vendor inventions, not Google metrics)
- You see some spammy-looking links (Google's algorithms ignore these automatically)
- As a "precautionary" measure (Gary Illyes has stated disavow hurts more sites than it helps)

> **Context:** Only ~39% of SEO practitioners still use disavow (2024 industry survey). Google's John Mueller and Gary Illyes have both indicated the algorithm handles most spam links automatically.

### 3.2 Identify Suspicious Links (if manual action exists)

```
Report: backlinks
Params: target=<domain>, target_type="root_domain", display_limit=100, display_sort="page_ascore_asc"
```

Sorting by `page_ascore_asc` surfaces lowest-quality links first.

Also check IP clustering:
```
Report: backlinks_refips
Params: target=<domain>, target_type="root_domain", display_limit=50
```

### 3.3 Spam Pattern Recognition

**PBN indicators:**
- Multiple referring domains on the same IP range or hosting provider
- Thin content sites with no real audience (check via WebFetch)
- Sites that exist solely to link out (high outbound link ratio)
- Same template/CMS across multiple linking domains
- Keyword-stuffed content with contextual links

**Link farm indicators:**
- Sitewide links from irrelevant sites (footer, sidebar, blogroll)
- Links from sites with no organic traffic
- Unnatural link velocity spikes (50+ links from new domains in a day)
- Foreign-language sites linking with English exact-match anchors

**Negative SEO patterns:**
- Sudden spike of thousands of low-quality links over a few days
- Links from adult, gambling, or pharma sites with no relevance
- Anchor text spam (same exact-match keyword from hundreds of domains)

### 3.4 Manual Spot-Check

For the 10 most suspicious source pages, use **WebFetch** to visit and evaluate:
- Does the page have real content or is it auto-generated?
- Does the site have organic traffic (check via Semrush `domain_rank`)?
- Is the link contextually placed or injected into unrelated content?
- Does the site link to obviously spammy destinations?

### 3.5 Action Decision

| Scenario | Action |
|----------|--------|
| Manual action in GSC + confirmed spam links | Create disavow file, submit via GSC, request reconsideration |
| No manual action + some spammy links | **Do nothing.** Google ignores them. Document and monitor |
| Negative SEO attack (thousands of spam links overnight) | Monitor for 2-4 weeks. If rankings drop AND manual action appears, then disavow. Otherwise Google handles it |
| Known past link scheme participation | Disavow the specific scheme links proactively |

---

## Step 4: Competitor Backlink Gap Analysis

> Find who links to competitors but not to you. Prioritize by quality and replicability.

### 4.1 Side-by-Side Metrics

```
Report: backlinks_comparison
Params: targets=["your_domain.com", "competitor1.com", "competitor2.com", "competitor3.com"], target_types=["root_domain", "root_domain", "root_domain", "root_domain"]
```

Compare: total backlinks, referring domains, Authority Score, follow/nofollow split.

### 4.2 Find Gap Domains

```
Report: backlinks_matrix
Params: targets=["your_domain.com", "competitor1.com", "competitor2.com"], target_types=["root_domain", "root_domain", "root_domain"], display_limit=100, display_sort="matchesnum_desc"
```

Sorting by `matchesnum_desc` surfaces domains that link to the most competitors — these are the most replicable opportunities.

### 4.3 Score & Prioritize Gap Domains

For each gap domain (links to competitors, not to you), score on 4 factors:

| Factor | Weight | 1 (Low) | 2 (Medium) | 3 (High) |
|--------|--------|---------|------------|----------|
| Authority | 2x | AS < 20 | AS 20-50 | AS > 50 |
| Relevance | 3x | Unrelated industry | Adjacent topic | Same niche (health, fertility, women's health) |
| Competitor Coverage | 2x | Links to 1 competitor | Links to 2 | Links to 3+ |
| Replicability | 2x | Seems editorial/earned (hard to replicate) | Resource page, directory, or guest post opportunity | Active outreach program, accepts contributions |

**Max score: 27.** Prioritize 20+ for outreach.

### 4.4 Classify Link Types

For the top 20 gap domains, use **WebFetch** to classify the link type:

| Link Type | Outreach Play |
|-----------|---------------|
| Resource page | Request inclusion — provide your best resource on the topic |
| Editorial mention | Pitch a story, data, or expert quote via journalist outreach |
| Guest post | Offer an expert contribution on a relevant topic |
| Directory / listing | Submit if legitimate (niche-specific, not general web directory) |
| Statistics citation | Create original data/research they'd want to cite |
| Digital PR | Create a newsworthy angle (study, survey, tool launch) |
| Sponsored / paid | **Skip.** Do not replicate paid link placements |

### 4.5 Output: Prioritized Outreach Target List

| Domain | AS | Relevance | Links to Comps | Link Type | Score | Outreach Play | Priority |
|--------|-----|-----------|---------------|-----------|-------|---------------|----------|
| example.com | 65 | Health/fertility | 3/3 comps | Resource page | 25 | Request inclusion | P1 |
| ... | | | | | | | |

---

## Step 5: Link Velocity & Growth Tracking

> Is the link profile growing naturally? Are there anomalies that need investigation?

### 5.1 Pull Historical Data

```
Report: backlinks_historical
Params: target=<domain>, target_type="root_domain", display_limit=24
```

Pull 24 months for your domain AND each competitor.

### 5.2 Velocity Benchmarks

| Site Maturity | Healthy RD Growth/Month | Notes |
|---------------|------------------------|-------|
| New (< 1 year, AS < 20) | 5-15 new referring domains | Expect irregular cadence |
| Growing (1-3 years, AS 20-40) | 10-50 new RDs | Should correlate with content output |
| Established (3+ years, AS 40+) | 20-100+ new RDs | Steady baseline + spikes around launches/PR |

### 5.3 What Looks Natural vs Suspicious

| Natural | Suspicious |
|---------|-----------|
| Irregular cadence (some months more, some less) | Perfectly consistent month-over-month (looks automated) |
| Correlates with content publishing | Links arriving without new content |
| Diverse sources across months | Same sources repeatedly |
| Branded + topical anchor diversity | Same anchor text across new links |
| Gradual acceleration as authority grows | Sudden 10x spike without explanation |

### 5.4 Anomaly Alerts

| Pattern | Likely Cause | Action |
|---------|-------------|--------|
| Sudden spike (5x+ normal) | Viral content, PR hit, OR negative SEO | Check if a specific page drove it. If no content explains it, investigate link quality |
| Steady decline over 6+ months | Content becoming outdated, competitors outpacing | Refresh top linked pages, create new linkable assets |
| Competitor acceleration (their velocity 3x+ yours) | Active link building campaign | Analyze their new links via `backlinks` sorted by date. Identify replicable tactics |
| Zero growth for 3+ months | No new content, no outreach | Critical — link profile is stagnating. Prioritize linkable asset creation |

---

## Step 6: Internal Link Equity Distribution

> External links bring authority IN. Internal links distribute it to the pages that matter.

### 6.1 Crawl Internal Links

**Bash:**
```
python3 scripts/crawl_audit.py <url> --json
```

Or use WebFetch to manually check key pages if the crawl script isn't available.

### 6.2 Orphan Page Detection

Orphan pages = pages with no internal links pointing to them.

| Scenario | Severity | Action |
|----------|----------|--------|
| Orphan page + has external backlinks | **Critical** — link equity is trapped, not flowing to the site | Add internal links from relevant hub/pillar pages immediately |
| Orphan page + no backlinks + no traffic | Low | Either add to the internal link structure or consider removing |
| Orphan page + some organic traffic | Medium | Integrate into relevant cluster with internal links |

### 6.3 Hub-and-Spoke Completeness

For each topic cluster (cross-reference with `content-cluster.md` if loaded):
- [ ] Pillar page links to ALL cluster pages
- [ ] ALL cluster pages link back to pillar page (in intro or first section, not footer)
- [ ] Each cluster page links to 2-3 sibling cluster pages
- [ ] Cross-cluster links exist only where topics genuinely overlap

### 6.4 Link Equity Flow Analysis

Trace the path from external link authority to money pages:
1. Which pages receive the most external backlinks? (`backlinks_pages` from Step 1.3)
2. Do those pages link internally to money pages (product pages, conversion pages)?
3. How many hops from the linked page to the money page? (Fewer = more equity transferred)

If top-linked pages don't connect to money pages within 2-3 clicks, add strategic internal links.

### 6.5 Internal Anchor Text

- Use descriptive, keyword-relevant anchors for internal links (not "click here")
- Vary anchors — don't use the exact same anchor for every link to a page
- Place the most important internal links in the body content, top half of the page (not sidebar/footer)
- Guideline: 2-5 internal links per 1,000 words, scaling naturally with content length

---

## Step 7: Brand Mention Audit (AI-Era Off-Page)

> In 2025-2026, unlinked brand mentions predict AI visibility better than backlinks. Ahrefs 75K-brand study: mentions correlate at 0.664 vs backlinks at 0.218.

### 7.1 Find Unlinked Mentions

**WebSearch:**
```
"inito" OR "inito.com" -site:inito.com -link:inito.com
```

Also search for product mentions without brand name:
```
"fertility monitor" "at home" "hormone" -site:inito.com
```

### 7.2 Classify Mentions

| Type | Action |
|------|--------|
| Unlinked brand mention on high-authority site | **Outreach** — request they add a link to the mention |
| Brand mentioned in a listicle/comparison without link | **Outreach** — provide a specific URL to link to |
| Product category mentioned, brand not included | **Content opportunity** — pitch for inclusion |
| Brand mentioned in AI Overview but not in the cited sources | **Monitor** — you're getting AI visibility without traditional backlinks |

### 7.3 AI Citation Tracking

Track whether your brand/content is cited in:
- Google AI Overviews
- ChatGPT search results
- Perplexity answers

**Tools:** Semrush AI Visibility Toolkit (if available via MCP), Ahrefs Brand Radar, or manual WebSearch queries prefixed with AI platform names.

> **Key insight (Lily Ray, SEO Week 2025):** Traditional backlink/authority metrics predict only 4-7% of AI citation behavior. Brand mentions, content clarity, and information uniqueness drive AI citations more than link equity.

### 7.4 AI Crawler Management

Check robots.txt for AI crawler directives:

| Crawler | Owner | Purpose | Recommendation |
|---------|-------|---------|---------------|
| GPTBot | OpenAI | ChatGPT web browsing + training | Allow for search; block for training if concerned |
| OAI-SearchBot | OpenAI | ChatGPT search only | Allow (search citations drive traffic) |
| ClaudeBot | Anthropic | Claude web access | Allow for visibility |
| PerplexityBot | Perplexity | Perplexity answers | Allow (drives referral traffic) |
| Google-Extended | Google | Gemini/AI training | Allow or block based on training preference |

> **Distinction:** Training crawlers (GPTBot, Google-Extended) use your content for model training. Search crawlers (OAI-SearchBot, PerplexityBot) cite you in real-time answers. You may want to allow search crawlers while blocking training crawlers.

---

## Link Building Strategy Framework (YMYL / Health Sites)

### Tier 1: Editorial / Earned (Highest Value, Highest Effort)

| Tactic | How | Expected Yield | Effort |
|--------|-----|---------------|--------|
| Original research / data studies | Publish proprietary data (e.g., "What 100K Inito users reveal about PCOS cycle patterns") | 20-50 links per study | High |
| Statistics / data hub pages | Create the definitive statistics page for your niche (e.g., "PCOS Statistics 2026") | 10-30 links over time | Medium |
| Digital PR | Pitch data-driven stories to health journalists | 5-20 links per campaign | High |
| Expert commentary | Offer expert quotes to journalists covering fertility/PCOS topics | 3-10 links per month | Low-Medium |

### Tier 2: Proactive / Legitimate Outreach

| Tactic | How | Expected Yield | Effort |
|--------|-----|---------------|--------|
| Resource page outreach | Find health resource pages linking to competitors, request inclusion | 2-5 links per campaign | Medium |
| HARO / journalist platforms | Respond to journalist queries. Platforms: **HARO** (relaunched April 2025 by Featured.com), **Qwoted**, **Featured**, **Source of Sources**, **MentionMatch** (formerly Help a B2B Writer), **#JournoRequest**, **ResponseSource** | 3-8 links per month | Low |
| Broken link building | Find broken links on relevant sites, offer your content as replacement | 1-3 links per campaign | Medium |
| Niche directories | Submit to legitimate health/fertility/medical directories | 5-10 total (one-time) | Low |

### Tier 3: Low Value / Risk (Document, Don't Pursue)

| Tactic | Risk | Recommendation |
|--------|------|---------------|
| Blog comments / forums | Low value, nofollow | Don't pursue for SEO. OK for community engagement |
| Link exchanges | Medium risk if at scale | Avoid systematic exchanges |
| Paid links | High risk | Never for YMYL/health sites |
| PBNs | High risk | Never |
| Guest posts on low-quality sites | Medium risk | Only contribute to sites with real audiences and editorial standards |

### Linkable Asset Ideas for Health/Fertility

1. **PCOS/PMOS Statistics page** — Comprehensive, regularly updated, cite-worthy
2. **Ovulation calculator or fertility window tool** — Interactive tools earn links naturally
3. **Hormone level reference ranges** — Medical reference content that practitioners link to
4. **Research roundups** — Monthly digest of new fertility/PCOS studies with plain-language summaries
5. **Patient journey guides** — Comprehensive guides that patient advocacy sites link to

---

## Output Template

```
BACKLINK PROFILE AUDIT: [domain]
Date: [date]

== PROFILE OVERVIEW ==
Authority Score: [X/100]
Referring Domains: [X] ([trend] over 12 months)
Total Backlinks: [X]
Follow/Nofollow: [X%/Y%] (niche benchmark: [A%/B%])
Link Types: [X% text, Y% image, Z% redirect]
Top TLDs: [list]
Geographic concentration: [aligned/misaligned with target market]

== ANCHOR TEXT HEALTH ==
Branded + Naked URL: [X%] — [OK / LOW / HIGH]
Exact Match: [X%] — [OK / WARNING / CRITICAL]
Topical/Partial: [X%] — [OK / OVER-OPTIMIZED]
Notable anchors: [any red flags]

== TOXIC LINK ASSESSMENT ==
Manual Action in GSC: [Yes/No]
Spam patterns detected: [Yes (details) / No]
Recommendation: [No action needed / Disavow specific links / Monitor]

== COMPETITOR GAP ==
[Table of top 15 outreach targets with score, link type, outreach play]

== LINK VELOCITY ==
Your growth: [X RDs/month over 6 months]
Competitor 1: [X RDs/month]
Competitor 2: [X RDs/month]
Trend: [Growing / Flat / Declining / Anomaly detected]

== INTERNAL LINK HEALTH ==
Orphan pages found: [X] (Critical: [Y])
Hub-spoke completeness: [X/Y clusters fully linked]
Equity flow to money pages: [OK / Gaps identified]

== BRAND MENTION & AI VISIBILITY ==
Unlinked mentions found: [X]
AI citation status: [Cited in AIO / Not cited / Partially cited]
Outreach opportunities: [X high-priority mentions to convert]

== PRIORITY ACTIONS ==
1. [Highest priority action]
2. [Second priority]
3. [Third priority]
...
```

---

## Fallbacks (When Semrush MCP Unavailable)

| Step | Alternative |
|------|------------|
| Profile overview | Use `scripts/semrush_api.py` with backlink endpoints, or WebSearch for free backlink checkers (Ahrefs free backlink checker) |
| Anchor text | Partial data from free tools. Note: limited to top anchors only |
| Competitor gap | Manual approach: WebSearch "[competitor] backlinks" and compare visually. Much less comprehensive |
| Link velocity | Cannot replicate without historical database. Flag as unavailable |
| Internal links | `scripts/crawl_audit.py` works without Semrush |
| Brand mentions | WebSearch works fully for this step |

---

## Notes & Lessons Learned

1. **Nofollow ≠ worthless for AI visibility.** LLMs train on Common Crawl and do not distinguish link attributes. Evaluate link value on two axes: traditional SEO value (attribute matters) and AI visibility value (attribute irrelevant).
2. **Disavow is almost never needed.** The threshold for action should be a confirmed manual action in GSC, not a third-party "toxicity score."
3. **Brand mentions > backlinks for AI.** Ahrefs 75K-brand study: web mentions correlate with AI visibility at 0.664 vs backlinks at 0.218. Unlinked mention tracking is now a core backlink analysis activity.
4. **Don't chase ratios.** Neither follow/nofollow ratios nor anchor text percentages have universal "ideal" values. Always benchmark against same-niche competitors.
5. **For YMYL sites, link SOURCE authority matters more than link COUNT.** One link from a medical journal outweighs 100 links from generic blogs. Prioritize relevance and authority in gap analysis.
