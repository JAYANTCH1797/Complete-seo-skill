# Competitor Benchmarking Reference

---
name: competitor-benchmarking
description: >
  Domain comparison, share of voice analysis, rank tracking, competitive positioning,
  and trajectory assessment. Identifies SEO competitors (not just business competitors),
  builds keyword overlap/gap matrices, calculates visibility-weighted SOV, and produces
  a competitive moat assessment with prioritized response strategy.
  Includes AI Share of Voice layer for 2025-2026 search landscape.
tools: [Semrush MCP (overview_research, organic_research, backlink_research, tracking_research, trends_research, keyword_research), WebFetch, WebSearch]
---

## When to Use This Reference

Load this when the user asks to:
- Compare their domain against competitors
- Calculate share of voice for a keyword set
- Benchmark organic performance (traffic, rankings, authority)
- Understand competitive positioning or who's winning in their space
- Identify competitive threats or opportunities
- Track competitor trajectory (gaining or losing momentum)

This reference focuses on **comparison and strategy**. For executing on the findings:
- Keyword gaps found here → `keyword-research.md` for validation
- Content weaknesses → `content-evaluation.md` for scoring
- New content opportunities → `content-brief.md` for brief generation
- Backlink gaps → `backlink-analysis.md` for link building

---

## Step 0: Setup

**Ask the user:**
1. What is your domain?
2. Do you have known competitors? (both business competitors AND sites you compete with in search)
3. What are your target keywords or topic areas?

**Check** `config/competitors.json` for any pre-configured competitor list.

---

## Step 1: Competitor Identification

> Get the right competitor set. Wrong competitors = misleading analysis.

### 1a. Discover SEO Competitors (keyword overlap)

```
Report: domain_organic_organic
Params: domain=<user_domain>, database="us", display_limit=20
Sort: np_desc
Columns: Dn, Cr, Np, Or, Ot, Oc, Ad
```

This returns domains ranked by keyword overlap (`Cr` = common keywords, `Np` = competitor's total keywords). Filter out generic sites (Wikipedia, Reddit, .gov, WebMD unless specifically relevant).

### 1b. Discover Backlink-Profile Competitors

```
Report: backlinks_competitors
Params: target=<user_domain>, target_type="root_domain", display_limit=15
```

Surfaces sites linked to by the same sources — catches competitors the keyword overlap method misses.

### 1c. Discover AI Competitors

Run category-relevant prompts across AI platforms to discover competitors that appear in AI answers but not in organic SERPs:

**WebSearch:** Query ChatGPT/Perplexity-style questions like:
- "best [product category] for [use case]"
- "top [product category] brands"
- "[your product] alternatives"

Note which brands appear in AI answers — these are your AI competitors.

### 1d. Classify Competitors

| Type | Definition | How to Use |
|------|-----------|-----------|
| **Product competitors** | Sell similar products/services | Primary comparison set. Their gains are your losses |
| **Content competitors** | Rank for your target keywords but aren't direct business competitors (media sites, health portals) | Study their content strategy. Beat their content quality |
| **Aspirational competitors** | Massive DR domains (WebMD, Healthline, Mayo Clinic) | Set the content quality bar. Don't target head terms they dominate; find gaps they don't cover |

Select **3-5 competitors** for the working set. Include at least 1 product competitor and 1 content competitor.

### GATE: Present the competitor set to the user. Stop. Wait for confirmation before proceeding.

---

## Step 2: Domain-Level Snapshot

> Side-by-side comparison of all domains on core metrics.

### 2a. Domain Overview (per domain)

```
Report: domain_rank
Params: domain=<domain>, database="us"
Columns: Dn, Rk, Or, Ot, Oc, Ad, At, Ac
```

Run for user domain + all competitors.

### 2b. Backlink Comparison

```
Report: backlinks_comparison
Params: targets=[user_domain, comp1, comp2, comp3], target_types=[root_domain, root_domain, root_domain, root_domain]
```

### 2c. Top Pages Per Competitor

```
Report: domain_organic_unique
Params: domain=<competitor>, database="us", display_limit=20, display_sort="tr_desc"
Columns: Ur, Pc, Tg, Tr
```

### 2d. Build Comparison Table

| Metric | Your Domain | Comp 1 | Comp 2 | Comp 3 |
|--------|------------|--------|--------|--------|
| Organic Keywords | | | | |
| Est. Monthly Traffic | | | | |
| Authority Score / DR | | | | |
| Referring Domains | | | | |
| Total Backlinks | | | | |
| Top Page Traffic | | | | |
| Traffic/Keyword (efficiency) | | | | |
| Traffic/Ref Domain (content vs authority) | | | | |

**Efficiency ratios explained:**
- **Traffic/Keyword**: Higher = better targeting (fewer keywords driving more traffic). Shows who picks keywords well vs who ranks for a lot of low-value terms
- **Traffic/Ref Domain**: Higher = content strength; lower = authority-dependent. Shows who relies on content quality vs raw link count

> **Note:** These normalization ratios are custom analytical metrics, not industry standards. They're useful for comparing domains of very different scales.

### 2e. Tag Each Competitor

Based on the data, classify each competitor:
- **Authority-led**: High DR, moderate content. Wins on domain strength
- **Content-led**: Moderate DR, deep content coverage. Wins on topical authority
- **Niche-focused**: Lower overall metrics but strong in specific clusters
- **Rising challenger**: Lower authority but rapid growth trajectory

---

## Step 3: Keyword Overlap & Gap Matrix

> Who ranks for what? Where do you overlap, and where are the gaps?

### 3a. Shared Keywords (intersection)

```
Report: domain_domains
Params: domains="*|or|<your_domain>|*|or|<comp1>|*|or|<comp2>", database="us", display_limit=50, display_sort="nq_desc"
Columns: Ph, Nq, Kd, P0, P1, P2
```

These are keywords ALL domains rank for. Assess your position vs competitors.

### 3b. Competitor-Only Keywords (what they have, you don't)

Run per competitor:
```
Report: domain_domains
Params: domains="*|or|<competitor>|-|or|<your_domain>", database="us", display_limit=50, display_sort="nq_desc", display_filter="+|Nq|Gt|100"
Columns: Ph, Nq, Kd, P0, P1
```

The `-` sign means your domain does NOT rank. Filter `Nq > 100` to focus on meaningful volume.

### 3c. Your-Only Keywords (your uniques)

```
Report: domain_domains
Params: domains="*|or|<your_domain>|-|or|<comp1>|-|or|<comp2>", database="us", display_limit=50, display_sort="nq_desc"
```

These are keywords you rank for that NO competitor does. Often niche strengths or brand terms.

### 3d. Prioritize Gaps

Score each competitor-only keyword on 5 factors:

| Factor | Weight | 1 | 2 | 3 |
|--------|--------|---|---|---|
| Business Relevance | 3x | Tangential | Related to niche | Product is the answer |
| KD Feasibility | 2x | KD > your AS+20 | KD within AS+10 | KD < your AS |
| Competitor Position | 2x | Positions 1-3 (hard to unseat) | Positions 4-10 | Positions 11-20 (weak, you can overtake) |
| Volume | 1x | < 100/mo | 100-1K/mo | > 1K/mo |
| Existing Content | 1x | No relevant page | Related page exists (can expand) | Page exists, just needs optimization |

**Max score: 27.** Present top 20 gaps sorted by score.

| Priority | Score | Action |
|----------|-------|--------|
| Act Now | 20-27 | Create content or optimize existing page → handoff to `content-brief.md` |
| Next Quarter | 14-19 | Add to content calendar |
| Backlog | 9-13 | Monitor, revisit when capacity allows |
| Skip | < 9 | Not worth pursuing currently |

---

## Step 4: Share of Voice (SOV)

> What percentage of visibility do you own for your target keyword set?

### 4a. Define the Keyword Universe

Choose one approach (best to worst):
1. **Tracked keyword list** — if the user has a defined target keyword set (best)
2. **Competitor overlap set** — use shared + competitor-only keywords from Step 3
3. **Topic-defined set** — use Semrush `keyword_research` to build a keyword universe for target topics

### 4b. Calculate Visibility-Weighted SOV

Use a **bifurcated CTR model** — different curves for AIO-present vs AIO-absent queries:

**AIO-absent queries:**

| Position | Estimated CTR |
|----------|--------------|
| 1 | 27% |
| 2 | 15% |
| 3 | 11% |
| 4 | 8% |
| 5 | 6% |
| 6 | 4.5% |
| 7 | 3.5% |
| 8 | 2.8% |
| 9 | 2.4% |
| 10 | 2.1% |
| Not ranking | 0% |

**AIO-present queries:**

| Position | Estimated CTR |
|----------|--------------|
| 1 | 10-12% |
| 2 | 6-8% |
| 3 | 4-5% |
| 4-10 | 1-3% |
| Not ranking | 0% |

> **Source:** AIO-absent model from Backlinko/Advanced Web Ranking 2024. AIO-present model from Seer Interactive Sept 2025 (61% average CTR reduction) and GrowthSRC 2025. Note: on heavily AIO-affected queries, position 1 CTR can drop as low as 0.6%.

**Formula:**
```
SOV(domain) = SUM(volume_i * CTR_of_domain_position_i) / SUM(volume_i * max_CTR_i)
```

Where `max_CTR_i` is the position-1 CTR for that query's SERP type (AIO or clean).

### 4c. Segment SOV by Topic Cluster

Don't just calculate overall SOV. Break it down:

| Cluster | Your SOV | Comp 1 SOV | Comp 2 SOV | Strategy |
|---------|----------|-----------|-----------|----------|
| PCOS | X% | Y% | Z% | Attack / Defend / Monitor |
| Ovulation tracking | X% | Y% | Z% | |
| Fertility hormones | X% | Y% | Z% | |

**Strategy labels:**
- **Defend**: You lead. Protect position with content freshness and internal linking
- **Attack**: Competitor leads but you have content. Optimize and build links
- **Build**: Competitor leads and you have no content. Long-term investment
- **Monitor**: Low SOV from everyone. Market may not be ready

### 4d. SERP Feature Flag

For clusters where >50% of keywords trigger AI Overviews or featured snippets, add a flag:

> ⚠️ AIO-heavy cluster: Actual organic CTR is 40-60% lower than model assumes. Consider AI citation tracking as a parallel metric.

### 4e. AI Share of Voice (supplementary)

For the same keyword universe, check which brands get cited in AI answers:
- Query representative keywords through WebSearch to check AI Overview citations
- Track frequency of brand mention (not position — AI recommendation ordering is stochastic with <1% consistency per SparkToro)
- Minimum 30 query samples for statistical significance

> **Note:** Binet's research showing SOV as a leading indicator of market share was about ad-spend SOV and branded search volume, not organic SERP visibility. The organic SOV → market share correlation is weaker but still directionally useful.

---

## Step 5: Content Strategy Comparison

> What are competitors publishing, how often, and in what formats?

### 5a. Content Format Analysis

Use **WebFetch** on competitors' top 20 pages (from Step 2c) to classify:

| Format | Examples |
|--------|---------|
| Long-form guide | "Complete Guide to PCOS", 3000+ words |
| Listicle | "15 PCOS Symptoms", "10 Best Fertility Apps" |
| How-to | "How to Track Ovulation with PCOS" |
| Comparison | "Inito vs Modern Fertility", "Best Fertility Monitors" |
| Tool / Calculator | "Ovulation Calculator", "Due Date Calculator" |
| Data / Research | "PCOS Statistics 2026", original studies |
| FAQ / Reference | "PCOS FAQ", "Progesterone Levels Chart" |
| Video | YouTube content ranking in organic results |

Build a format distribution table per competitor. **Format gaps are often more actionable than keyword gaps** — if competitors rank with calculators and you only have blog posts, no amount of blog optimization will close that gap.

### 5b. Content Velocity

```
Report: domain_organic
Params: domain=<competitor>, database="us", display_positions="new", display_limit=50
```

Also run with `display_positions="lost"`.

Summarize net keyword gains/losses per competitor over last 3 months.

| Competitor | New Keywords (3mo) | Lost Keywords (3mo) | Net | Interpretation |
|-----------|-------------------|--------------------|----|---------------|
| Comp 1 | +500 | -200 | +300 | Actively growing |
| Comp 2 | +100 | -400 | -300 | Losing ground |

### 5c. Content Freshness

For top pages, check via WebFetch:
- Published date
- Last updated date
- Are they citing recent studies (2024-2026)?
- Update frequency pattern

---

## Step 6: Authority & Technical Comparison

### 6a. Backlink Trend Lines

```
Report: backlinks_historical
Params: target=<domain>, target_type="root_domain", display_limit=24
```

Run for all domains. Classify each:
- **Steady growth**: Consistent RD acquisition month-over-month
- **Spike-then-flat**: Got a burst of links, then stagnated
- **Declining**: Losing referring domains (links being removed or sites dying)
- **Accelerating**: Growth rate increasing — competitor investing in link building

### 6b. E-E-A-T Comparison

WebFetch on top 3 pages per competitor. Check and build comparison matrix:

| E-E-A-T Signal | Your Site | Comp 1 | Comp 2 | Comp 3 |
|----------------|-----------|--------|--------|--------|
| Named author with credentials | | | | |
| Medical reviewer byline | | | | |
| Author bio page with qualifications | | | | |
| Inline citations to medical sources | | | | |
| Editorial policy page | | | | |
| Visible publish/update dates | | | | |
| "Reviewed by" badge | | | | |

### 6c. Technical Spot-Check (Lightweight)

> This is NOT a full technical audit (see `technical-seo.md` for that). Just compare key signals.

- Schema usage: What types of structured data do competitors use? (Article, FAQPage, MedicalWebPage, HowTo — note: HowTo schema deprecated Sept 2023, FAQ schema restricted to gov/health Aug 2023)
- Page speed: Quick check via WebFetch response time or Playwright
- Mobile experience: Basic mobile rendering check

---

## Step 7: Trajectory Analysis

> Is each competitor gaining or losing momentum?

### 7a. 12-Month Traffic Trends

```
Report: domain_rank_history
Params: domain=<domain>, database="us", display_limit=12, display_sort="dt_asc"
Columns: Rk, Or, Ot, Oc, Ad, At, Dt
```

Run for all domains. Build trend table:

| Domain | Traffic 12mo Ago | Traffic Now | 12mo Change | Trajectory |
|--------|-----------------|------------|-------------|-----------|
| your_domain | | | +X% | Growing / Flat / Declining |
| comp1 | | | | |

**Classify:**
- **Growing fast**: >20%/year increase
- **Growing steady**: 5-20%/year
- **Flat**: -5% to +5%
- **Declining**: >10% decrease

### 7b. Keyword Movement

Summarize from Step 5b:
- Net new keywords per competitor
- Which specific keyword clusters are they growing in?
- Are they expanding into your territory or different topics?

### 7c. Link Velocity

From Step 6a history:
- Calculate monthly referring domain growth rate over last 6 months per domain
- Who's investing most aggressively in link building?

---

## Step 8: Competitive Moat Assessment & Strategy

> What can you realistically replicate, and what requires a different strategy?

### 8a. Classify Competitive Advantages

| Advantage Type | Hard Moat (>12 months to replicate) | Catchable (<12 months) |
|---------------|--------------------------------------|----------------------|
| Brand recognition | ✅ Hard — requires sustained marketing investment | |
| Topical authority / content depth | ✅ Hard — requires comprehensive content covering hundreds of subtopics over time | |
| Proprietary data / UGC | ✅ Hard — user-generated content, first-party data, community | |
| Institutional trust (gov, medical, academic) | ✅ Hard — cannot be manufactured | |
| Domain Rating / backlink volume | | ✅ Catchable — DR can be built with consistent link earning |
| Technical SEO | | ✅ Catchable — can be fixed in weeks |
| Specific keyword clusters | | ✅ Catchable — create better content + build links |
| E-E-A-T signals | | ✅ Catchable — add author bios, medical review, citations |
| Content formats (tools, calculators) | | ✅ Catchable — build what's missing |

> **Important correction:** Some workflows incorrectly classify DR as a "hard moat." DR/backlink volume is explicitly NOT a durable moat (Ritner Digital). It can be built with consistent effort. Content depth/topical authority IS one of the hardest moats to replicate because it requires sustained, comprehensive investment.

### 8b. Prioritize Responses

| Priority | Trigger | Action |
|----------|---------|--------|
| **P0: Defend** | You're losing existing positions to a competitor | Refresh content, strengthen internal links, build links to affected pages |
| **P1: Quick Win** | High-volume gaps where competitor content is weak (thin, outdated, no E-E-A-T) | Create better content. Handoff: `content-brief.md` |
| **P2: Format Gap** | Competitors rank with content formats you lack (tools, videos, comparisons) | Build the missing format |
| **P3: Opportunistic** | Competitor is losing ground in a cluster you care about | Accelerate content creation in that cluster |
| **P4: Long-term** | Competitor has hard moat (brand, trust, UGC). Head terms unreachable | Target long-tail and subtopics around the moat. Build authority over 12+ months |

### 8c. Action Plan

Map each priority to a specific handoff:

| Finding | Handoff |
|---------|---------|
| Keyword gaps to close | `keyword-research.md` for validation, then `content-brief.md` |
| Existing content underperforming vs competitors | `content-evaluation.md` for scoring and fix recommendations |
| Link authority gap | `backlink-analysis.md` for link building strategy |
| Content cluster gaps | `content-cluster.md` for cluster architecture and calendar |
| Technical gaps | `technical-seo.md` for audit |

---

## Output Template

```
COMPETITIVE BENCHMARKING REPORT: [your domain] vs [competitors]
Date: [date]
Keyword Universe: [X keywords across Y clusters]

== DOMAIN COMPARISON ==
[Table from Step 2d]

== SHARE OF VOICE ==
Overall SOV: [your domain] = X%, [comp1] = Y%, [comp2] = Z%
[Table by cluster from Step 4c]
AI SOV note: [summary of AI visibility comparison]

== KEYWORD OVERLAP & GAPS ==
Shared keywords: [X]
Competitor-only (gap): [X] → [Y after filtering]
Your-only (unique strengths): [X]
Top 10 gaps by priority score:
[Table from Step 3d]

== CONTENT STRATEGY ==
Format distribution: [comparison]
Content velocity: [who's publishing most/fastest]
Key format gaps: [what you're missing]

== TRAJECTORY ==
[Table from Step 7a]
Momentum winner: [domain] — [why]
Momentum loser: [domain] — [why]

== COMPETITIVE MOAT ASSESSMENT ==
[Table of competitor advantages: hard moat vs catchable]

== PRIORITY ACTIONS ==
P0 (Defend): [specific actions]
P1 (Quick Win): [specific actions]
P2 (Format Gap): [specific actions]
P3 (Opportunistic): [specific actions]
P4 (Long-term): [specific actions]
```

---

## Fallbacks (When Semrush MCP Unavailable)

| Step | Alternative | Quality |
|------|------------|---------|
| Competitor discovery | WebSearch "[your product] alternatives", "[your product] vs" | Finds business competitors only, not SEO competitors |
| Domain overview | Free tools (Ahrefs free webmaster tools, Ubersuggest) | Limited data |
| Keyword overlap/gap | **Cannot replicate** without a keyword database | Flag as unavailable |
| SOV calculation | **Cannot replicate** without position data | Flag as unavailable |
| Content analysis | WebFetch on competitor sites | Full quality |
| Backlink comparison | Free backlink checkers | Limited to top links only |
| Trajectory | **Cannot replicate** without historical data | Flag as unavailable |

Steps 3, 4, and 7 fundamentally require a keyword/rank database. Without Semrush, the analysis is limited to qualitative content and backlink comparison.

---

## Notes & Lessons Learned

1. **SEO competitors ≠ business competitors.** A media site ranking for your target keywords is a competitor in search even if they don't sell what you sell. Always discover SEO competitors via keyword overlap, don't just use a pre-defined business competitor list.
2. **SOV is a leading indicator, not a lagging one.** When your SOV for a cluster drops, expect traffic to follow within 2-3 months. When it rises, traffic follows. Use it for early warning.
3. **Bifurcate the CTR model.** A single CTR curve is no longer valid. AIO-present queries have dramatically lower organic CTR. Segment SOV calculation by SERP type.
4. **AI SOV is stochastic.** Don't track AI recommendation position — it varies on every query. Track frequency of brand mention across 30+ query samples.
5. **Content depth is the hardest moat to replicate.** Don't underestimate competitors with deep topical coverage. DR can be built; 200 comprehensive articles covering every subtopic of PCOS cannot be replicated quickly.
