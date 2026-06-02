# Content Gap Analysis Reference

---
name: content-gap
description: >
  Competitor keyword and content gap identification. Finds keywords competitors rank for that you don't,
  detects content format gaps, identifies subtopic gaps within existing pages, maps gaps to buyer journey
  stages, and prioritizes with a weighted scoring model. Five-layer filtering pipeline transforms raw
  Semrush data into an actionable, prioritized gap list.
  Includes AI citation gap layer and Information Gain gap detection for 2025-2026.
tools: [Semrush MCP (organic_research, keyword_research, overview_research, url_research, trends_research), WebFetch, WebSearch]
---

## When to Use This Reference

Load this when the user asks to:
- Find content gaps vs competitors ("what are they ranking for that we're not?")
- Identify missing topics or keywords
- Find keyword opportunities competitors have
- Do a content gap analysis or competitor keyword diffing
- Identify what content to create next (feeds into content calendar)

**Cross-references:**
- `competitor-benchmarking.md` → provides the competitor set and domain comparison
- `keyword-research.md` → validates discovered gap keywords (Path C: competitor gap)
- `content-brief.md` → generates briefs for prioritized gap keywords
- `content-evaluation.md` → scores existing content that needs improvement

**When called as a feeder for `keyword-research.md` Path C:**
Only run Steps 0-3 (setup, extraction, filtering). The filtered cluster list becomes the seed list for keyword-research.md's validation and sub-cluster fan-out.

---

## Step 0: Setup

### 0.1 Collect Inputs

**Ask:**
1. What is your domain?
2. Who are your 2-4 main competitors? (check `config/competitors.json`)
3. What's your business context? (What topics are relevant? What's irrelevant?)

### 0.2 Auto-Discover Competitors (if not provided)

```
Report: domain_organic_organic
Params: domain=<user_domain>, database="us", display_limit=15
Sort: np_desc
Columns: Dn, Cr, Np, Or, Ot
```

Present top 5-10 SEO competitors. Let user confirm.

### 0.3 Authority Baselines

```
Report: domain_rank
Params: domain=<domain>, database="us"
Columns: Dn, Rk, Or, Ot
```

Run for user domain + all competitors. Record Authority Score — this calibrates KD feasibility in Step 3.

---

## Step 1: Keyword Gap Extraction

> Pull all keywords competitors rank for that you don't, or rank weakly for.

### 1.1 domain_domains Sign Syntax Reference

The `domain_domains` report uses pipe-separated sign syntax:

| Sign | Meaning |
|------|---------|
| `*` | Domain ranks for this keyword (any position) |
| `+` | Domain ranks in top 10 |
| `-` | Domain does NOT rank for this keyword |
| `/` | Domain ranks but NOT in top 10 |

### 1.2 Three Gap Views

**View A: Missing keywords** (competitors rank, you don't)
```
Report: domain_domains
Params: domains="*|or|<comp1>|*|or|<comp2>|-|or|<your_domain>", database="us", display_limit=100, display_sort="nq_desc", display_filter="+|Nq|Gt|50"
Columns: Ph, Nq, Kd, Co, P0, P1
```

**View B: Untapped keywords** (at least one competitor ranks, you don't)
```
Report: domain_domains
Params: domains="*|or|<comp1>|-|or|<your_domain>", database="us", display_limit=100, display_sort="nq_desc", display_filter="+|Nq|Gt|50"
```

Run separately for each competitor.

**View C: Weak keywords** (shared, but you rank poorly)
```
Report: domain_domains
Params: domains="+|or|<comp1>|/|or|<your_domain>", database="us", display_limit=50, display_sort="nq_desc"
```

These are keywords where competitors are in the top 10 and you're outside the top 10 — the "almost there" opportunities.

### 1.3 Pagination

For thorough analysis, check total results count. If >100 gaps exist, run multiple calls adjusting `display_offset` to page through results. For initial analysis, the top 100 by volume is sufficient.

---

## Step 2: Competitor Page-Level Analysis

> Beyond keywords — what content formats and page types do competitors have that you lack?

### 2.1 Top Traffic Pages

Per competitor:
```
Report: domain_organic_unique
Params: domain=<competitor>, database="us", display_limit=30, display_sort="tr_desc"
Columns: Ur, Pc, Tg, Tr
```

### 2.2 Format Classification

Classify each top competitor page by format:

| Format | URL Signals | Example |
|--------|------------|---------|
| Long-form guide | /guide/, /complete-guide, long word count | "Complete Guide to PCOS" |
| Listicle | /best-, /top-, numbered title | "10 Best Fertility Monitors" |
| Tool / Calculator | /calculator, /tool, interactive elements | "Ovulation Calculator" |
| Comparison | /vs, /compare, side-by-side | "Inito vs Modern Fertility" |
| Data / Statistics | /statistics, /data, /research | "PCOS Statistics 2026" |
| Video | youtube.com, video embed page | Video-first content |
| FAQ / Reference | /faq, Q&A structured | "PCOS FAQ" |

### 2.3 Format Gap Matrix

| Format | Your Site | Comp 1 | Comp 2 | Comp 3 | Gap? |
|--------|----------|--------|--------|--------|------|
| Guides | 5 | 12 | 8 | 10 | Moderate |
| Calculators/Tools | 0 | 2 | 1 | 0 | **Yes — critical** |
| Comparisons | 1 | 5 | 3 | 4 | **Yes** |
| Data/Statistics | 0 | 1 | 0 | 2 | **Yes** |

> **Key insight:** Format gaps are distinct from keyword gaps. A calculator ranks because Google wants a tool for that query — no amount of blog content fills a format gap. Identify these separately.

---

## Step 3: Filtering (Critical Step)

> The difference between a useful gap analysis and a useless one is filtering quality. Raw Semrush dumps are noise.

### Filter 1: Remove Branded Terms

Remove all keywords containing competitor brand names, product names, or clearly navigational queries.

**Examples to remove:** "flo app", "clue period tracker", "modern fertility reviews"
**Keep:** "fertility tracker" (generic), "hormone testing at home" (category)

### Filter 2: Remove Irrelevant Topics

Requires business context understanding. Ask the user if unclear.

**For Inito (examples):**
- **Keep:** PCOS, ovulation, fertility, progesterone, LH, hormone tracking, TTC, cycle tracking
- **Remove:** pregnancy (post-conception), baby names, parenting, menopause, contraception, IVF (unless Inito is relevant)

### Filter 3: KD Feasibility Check

Compare keyword difficulty against your Authority Score:

| Your AS | Feasible KD Range | Stretch KD | Skip |
|---------|------------------|------------|------|
| 20-30 | KD < 30 | KD 30-45 | KD > 45 |
| 30-50 | KD < 45 | KD 45-60 | KD > 60 |
| 50-70 | KD < 60 | KD 60-75 | KD > 75 |
| 70+ | KD < 75 | KD 75+ | Rare |

Don't hard-filter on KD alone — tag as "feasible", "stretch", or "long-term" and let the prioritization model handle it.

### Filter 4: Intent Alignment

Classify each remaining keyword by intent and filter:

| Intent | Keep? | Notes |
|--------|-------|-------|
| Informational | ✅ | Core content opportunity |
| Commercial investigation | ✅ | High-value — comparison/review content |
| Transactional | ✅ if product-relevant | Product pages or bottom-funnel content |
| Navigational | ❌ Remove | Competitor brand searches, specific site searches |

### Filter 5: Deduplicate & Cluster

Group keyword variants that represent the same topic:
- "PCOS symptoms" / "symptoms of PCOS" / "polycystic ovary syndrome symptoms" → one cluster
- Sum cluster volume for prioritization (use total cluster volume, not individual keyword volume)

Use Semrush `phrase_related` for borderline cases:
```
Report: phrase_related
Params: phrase=<keyword>, database="us", display_limit=10
```

### Post-Filter Summary

```
FILTERING FUNNEL:
Raw gap keywords extracted: [X]
After removing branded terms: [X] (-Y%)
After removing irrelevant topics: [X] (-Y%)
After KD feasibility tagging: [X feasible, Y stretch, Z long-term]
After intent filtering: [X] (-Y navigational removed)
After dedup/clustering: [X unique keyword clusters]
```

---

## Step 4: Subtopic Gap Analysis (Existing Content)

> For pages you already have — what are competitors covering in their version that you're missing?

### 4.1 Find Underperforming Pages

```
Report: domain_organic
Params: domain=<user_domain>, database="us", display_filter="+|Po|Gt|3|+|Po|Lt|21", display_limit=50, display_sort="tr_desc"
Columns: Ph, Po, Nq, Ur, Tr
```

These are pages ranking positions 4-20 — close to page 1 but not there yet.

### 4.2 Compare Against Competitors

For each underperforming page, identify the competitor page that outranks you:

```
Report: phrase_organic
Params: phrase=<target_keyword>, database="us", display_limit=5
Columns: Ur, Dn
```

Then **WebFetch** both your page and the top competitor page. Compare:

| Element | Your Page | Top Competitor | Gap |
|---------|----------|---------------|-----|
| H2 Sections | [list] | [list] | [missing sections] |
| Key entities mentioned | [list] | [list] | [missing entities] |
| Data/statistics cited | [count] | [count] | [difference] |
| Structural elements | [ToC, FAQ, tables?] | [ToC, FAQ, tables?] | [missing elements] |

### 4.3 Entity Gap Check (Optional, for high-priority pages)

For the top 5 most important underperforming pages, do a deeper entity comparison:
- Extract all medical terms, brand names, conditions, treatments, and studies from your page vs competitor
- Missing entities = content depth gaps
- This is the "entity gap" dimension from the CXL 4-gap framework (keyword gaps, topic gaps, entity gaps, originality gaps)

> **Boundary with content-evaluation.md:** This step DISCOVERS what's missing. Content-evaluation.md SCORES whether existing content is competitive. Use content-evaluation.md when you want a pass/fail verdict; use this step when you want a gap list.

---

## Step 5: Buyer Journey Mapping

> Map each gap to a funnel stage to ensure balanced content investment.

### 5.1 Classify Gaps by Funnel Stage

| Stage | Keyword Signals | Examples |
|-------|----------------|---------|
| **Awareness** | "what is", "symptoms", "causes", "signs of" | "what is PCOS", "anovulation symptoms" |
| **Consideration** | "how to", "best", "treatment", "management", "vs" | "PCOS treatment options", "best fertility monitors" |
| **Decision** | "reviews", "pricing", "buy", "worth it", "[brand] vs [brand]" | "Inito vs Mira", "Inito reviews" |
| **Post-purchase** | "how to use", "results", "not working", "tips" | "how to use Inito", "Inito results accuracy" |

### 5.2 Funnel Gap Summary

| Stage | Total Gap Keywords | Total Cluster Volume | Your Coverage | Priority |
|-------|-------------------|---------------------|---------------|----------|
| Awareness | [X] | [X] | [X pages exist] | Medium (AI synthesizes these) |
| Consideration | [X] | [X] | [X pages exist] | **High** |
| Decision | [X] | [X] | [X pages exist] | **Highest** (converts best, AI can't synthesize) |
| Post-purchase | [X] | [X] | [X pages exist] | Medium |

### 5.3 Strategic Implications

- **Heavy Awareness gaps:** Your topical authority is weak. Build foundational content, but expect lower organic traffic per piece (AI synthesizes top-funnel answers)
- **Heavy Consideration gaps:** Highest ROI for organic content. Users at this stage need depth that AI can't provide
- **Heavy Decision gaps:** Critical for conversion. These pages directly influence purchase decisions and AI can't fully synthesize them
- **Heavy Post-purchase gaps:** Retention and satisfaction. Lower SEO priority but important for customer experience

---

## Step 6: Gap Prioritization

### 6.1 Scoring Model (5 factors, max 30)

| Factor | Weight | 1 (Low) | 2 (Medium) | 3 (High) |
|--------|--------|---------|------------|----------|
| **Business Relevance** | 3x | Tangential to product/audience | Related to niche | Product is the direct answer |
| **KD Feasibility** | 2x | KD > AS+20 (long-term) | KD within AS+10 (stretch) | KD < AS (feasible) |
| **Traffic Potential** | 1x | Cluster volume <200/mo | 200-1K/mo | >1K/mo |
| **Competitive Weakness** | 2x | Competitors rank 1-3 with strong content | Competitors rank 4-10 | Competitors rank 11-20 or have thin content |
| **Content Investment** | 2x | Requires new format (tool, video, 8+ hrs) | New article (4-8 hrs) | Expand existing page (1-3 hrs) |

**Max score: 30.**

| Score | Priority | Action |
|-------|----------|--------|
| 24-30 | **Act Now** | Create content this month. Handoff to `content-brief.md` |
| 18-23 | **Next Quarter** | Add to content calendar |
| 12-17 | **Backlog** | Monitor, revisit when capacity allows |
| <12 | **Skip** | Not worth pursuing currently |

> **Note:** Business relevance is weighted 3x deliberately. A high-volume, low-KD keyword that's irrelevant to the product scores poorly. Do not guess business relevance — ask the user when uncertain.

### 6.2 Action Labels

| Label | Meaning |
|-------|---------|
| **NEW PAGE** | No existing content. Create from scratch |
| **EXPAND** | Existing page covers the topic partially. Add sections/depth |
| **NEW FORMAT** | Topic is covered but competitors rank with a different format (e.g., you have a blog post, they have a calculator) |
| **STRATEGIC SKIP** | Deliberately not pursuing. Document the reason to prevent re-flagging |

> **Strategic Skip** is a custom workflow feature. Documenting deliberate exclusions prevents the same gaps from surfacing every quarter.

### 6.3 AIO Click Discount (AI-Era Adjustment)

For keywords that trigger AI Overviews, reduce expected organic traffic by 40-60%:

```
Adjusted Traffic = Cluster Volume × Est. CTR × (1 - AIO_discount)
```

Where AIO_discount = 0.58 for keywords with AI Overviews (Ahrefs 2025 study).

Add a separate "citation value" assessment: even if organic clicks are low, being cited in the AI Overview has brand visibility value.

---

## Step 7: Deliverable

### 7.1 Prioritized Gap Table

| Rank | Keyword Cluster | Cluster Vol | KD | Competitor Positions | Business Relevance | Score | Action | AIO? |
|------|----------------|-------------|-----|---------------------|-------------------|-------|--------|------|
| 1 | [cluster] | [X] | [X] | Comp1: #5, Comp2: #8 | Product is the answer | 28 | NEW PAGE | No |
| 2 | [cluster] | [X] | [X] | Comp1: #3 | Related | 25 | EXPAND | Yes |

### 7.2 Format Gaps

| Format | Gap Description | Traffic Potential | Effort | Priority |
|--------|----------------|------------------|--------|----------|
| Calculator | No ovulation calculator — competitors rank for "ovulation calculator" (40K/mo) | High | High (development) | P1 |
| Comparison | Only 1 comparison page — competitors have 5+ | Medium | Medium | P2 |

### 7.3 Subtopic Gaps in Existing Content

| Your Page | Missing Subtopics | Competitor Example | Effort |
|-----------|-------------------|-------------------|--------|
| /blog/pcos-guide | Hormonal mechanisms, PMOS terminology update | healthline.com/pcos | 2-3 hrs |

### 7.4 Funnel Balance

```
Your content by funnel stage:
Awareness: [X pages] | Consideration: [X pages] | Decision: [X pages] | Post-purchase: [X pages]
Gaps by funnel stage:
Awareness: [X gaps] | Consideration: [X gaps] | Decision: [X gaps] | Post-purchase: [X gaps]
Recommendation: [e.g., "Prioritize Consideration and Decision gaps — they convert best and have the most gaps"]
```

### 7.5 Quick Wins

Pages where small effort could yield significant results:
| Page | Current Position | Issue | Fix | Est. Impact |
|------|-----------------|-------|-----|-------------|
| [url] | #12 | Missing 2 subtopics competitors cover | Add 500 words on [topics] | Move to page 1 |

### 7.6 Information Gain Opportunities

Gaps where you have unique data, proprietary research, or first-hand experience that competitors lack:

| Gap Topic | Your Unique Angle | Why It Matters |
|-----------|-------------------|---------------|
| PCOS hormone patterns | Inito user data on LH/progesterone patterns | No competitor has device-level data |
| Ovulation tracking accuracy | Inito clinical study data | Primary source, not derivative content |

> **Context:** Google's March 2026 core update elevated Information Gain as a dominant ranking signal. Me-too content that rehashes existing top results dropped 30-50% in visibility. Gaps where you can provide genuinely new information should be weighted highest.

---

## Step 8: Gap Monitoring

### 8.1 Re-Analysis Cadence

| Your Content Velocity | Re-Analysis Frequency |
|----------------------|----------------------|
| <5 pages/month | Every 6 months |
| 5-15 pages/month | Every quarter |
| 15+ pages/month | Every month |

### 8.2 Targeted Gap Check (Post-Publish)

After publishing content for a gap keyword, verify it's working:

```
Report: domain_organic
Params: domain=<user_domain>, database="us", display_filter="+|Ph|Co|<published_keyword>"
```

Check: Are you ranking? What position? Are you in the top 10?

### 8.3 New Competitor Content Detection

```
Report: domain_organic
Params: domain=<competitor>, database="us", display_positions="new", display_limit=30, display_sort="tr_desc"
```

Run monthly. Surfaces new keywords competitors have started ranking for — potential new gaps opening.

### 8.4 Gap Closure Tracking

Maintain a tracking table:

| Gap Keyword | Status | Date Found | Content Published | Current Position | Notes |
|------------|--------|-----------|-------------------|-----------------|-------|
| [keyword] | Open | [date] | — | Not ranking | In content calendar |
| [keyword] | Closing | [date] | [date + url] | #15 | Gaining, not page 1 yet |
| [keyword] | Closed | [date] | [date + url] | #4 | ✅ Goal reached |
| [keyword] | Skipped | [date] | — | — | Too high KD, revisit when AS grows |

---

## Fallbacks (When Semrush MCP Unavailable)

| Step | Alternative | Quality |
|------|------------|---------|
| Keyword gap | **Cannot replicate** without a keyword database | Critical limitation — flag to user |
| Page-level analysis | WebFetch on competitor sites + manual comparison | Good for format gaps |
| Subtopic gaps | WebFetch your page vs competitor page | Good quality |
| Buyer journey mapping | Manual classification of known keywords | Works if you have a keyword list |
| Prioritization | Skip volume/KD factors, use business relevance + effort only | Partial |

Step 1 fundamentally requires a keyword database. Without Semrush, the gap analysis is limited to qualitative content comparison (Steps 2, 4, 5).

---

## Notes & Lessons Learned

1. **Filtering is everything.** A raw Semrush gap dump can have 5,000+ keywords. Five sequential filters reduce this to 20-40 actionable items. Skipping filtering produces noise, not strategy.
2. **Cluster volume > raw volume.** A 200/mo keyword heading a 2,000/mo cluster is more valuable than it appears. Always estimate true cluster potential.
3. **Format gaps are often more actionable than keyword gaps.** If Google wants a calculator for "ovulation calculator," no blog post will rank. Identify format gaps as a separate workstream.
4. **Business relevance cannot be guessed.** The scoring model weights it 3x because a high-volume irrelevant keyword is worthless. Always confirm with the user.
5. **Information Gain is the new competitive advantage.** Post-March 2026, me-too content that rehashes what already ranks dropped 30-50%. The most valuable gaps are ones where you can bring unique data, research, or experience.
6. **AI citation gaps are the new content gaps.** "Competitor is cited in AI Overview, you're not" is as important as "competitor ranks organically, you don't." Track both layers.
