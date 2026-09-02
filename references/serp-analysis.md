# SERP Analysis Reference

---
name: serp-analysis
description: >
  SERP feature detection, layout analysis, intent classification, CTR modeling, featured snippet
  opportunity assessment, AI Overview analysis, competitive SERP landscape evaluation, and
  SERP volatility measurement. Produces a SERP scorecard with a TARGET/DEFER/SKIP verdict
  and specific content direction. Includes AI-era CTR bifurcation, GEO signal assessment,
  and AI citation layer.
tools: [Semrush MCP (keyword_research, organic_research, url_research, trends_research), WebFetch, WebSearch, Bash (scripts/serp_scraper.py)]
---

## When to Use This Reference

Load this when the user asks to:
- Analyze what the SERP looks like for a keyword
- Check SERP features (featured snippets, AI Overviews, PAA, etc.)
- Assess whether a keyword is worth targeting based on SERP layout
- Understand click-through rate potential for a keyword
- Find featured snippet opportunities
- Analyze AI Overview presence and citation opportunities

**Cross-references:**
- Called from `keyword-research.md` at step 2d for SERP-level validation
- Feeds into `content-brief.md` with intent classification, SERP features to target, and competitive benchmarks
- Feeds into `content-evaluation.md` with SERP feature map and competitor landscape

---

## Step 1: SERP Data Collection

### 1.1 Keyword Metrics

```
Report: phrase_this
Params: phrase=<keyword>, database="us"
Columns: Ph, Nq, Kd, In, Co, Td, Fk
```

`Fk` column contains SERP feature codes. Record all features present.

### 1.2 Top 10 Organic Results + SERP Features

```
Report: phrase_organic
Params: phrase=<keyword>, database="us", display_limit=10, positions_type="all"
Columns: Ur, Dn, Fp, Fk
```

> **Critical:** Use `positions_type: "all"` — without this parameter, SERP features are invisible in the data.

### 1.3 Competitor Keyword Counts

For each domain in the top 10, note their overall organic keyword count (from the data) to gauge domain authority.

### 1.4 Live SERP Inspection

**WebSearch** the primary keyword to capture:
- AI Overview presence and what it says
- Featured snippet content and format
- PAA questions (expand 2-3 levels)
- Discussions and Forums section (Reddit/Quora results)
- "Things to Know" box
- Perspectives filter results
- Image/video carousels

> Semrush tracks 21 SERP feature codes, but three important features require live inspection: Discussions/Forums, Things to Know, and Perspectives filter.

---

## Step 2: SERP Feature Analysis

### 2.1 Feature Inventory

Map all features present on the SERP:

| Feature | Present? | Opportunity | Notes |
|---------|----------|-------------|-------|
| **AI Overview** | Yes/No | High — being cited drives brand visibility | See Step 5 for detailed analysis |
| **Featured Snippet** | Yes/No | High — ~42.9% CTR when captured (clean SERP) | See Step 6 for targeting |
| **People Also Ask** | Yes/No | Medium — mine for content subtopics | Record all visible questions |
| **Video Carousel** | Yes/No | Medium — if present, consider video content | Note if YouTube dominates |
| **Image Pack** | Yes/No | Low-Medium — optimize image alt text and file names | |
| **Knowledge Panel** | Yes/No | Low — hard to influence directly | Usually for entities with Wikipedia presence |
| **Local Pack** | Yes/No | Low for non-local businesses | Only relevant if you have physical locations |
| **Shopping Results** | Yes/No | N/A for content SEO | Signals strong commercial intent |
| **Top Stories** | Yes/No | Low — requires news publisher authority | |
| **Discussions/Forums** | Yes/No | High — Reddit is now #4 most visible domain in US Google | Reddit content strategy may be needed |
| **Things to Know** | Yes/No | Medium — structured, scannable content gets featured | Appears in 69.5% of healthcare queries (GrowByData — single-source stat) |
| **Sitelinks** | Yes/No | Low — indicates navigational dominance | |

### 2.2 Feature Density Assessment

Count total SERP features present:
- **0-1 features**: Clean SERP — standard organic competition. Best CTR opportunity
- **2-3 features**: Moderate feature density — organic CTR reduced but still viable
- **4+ features**: Heavy feature density — organic CTR significantly compressed. Must target features, not just rankings

---

## Step 3: Intent Classification

> What does Google's choice of results tell you about what content to create?

### 3.1 Three Cs Framework

Classify the top 5 organic results (same framework as `content-brief.md`):

**Content Type:**
- Blog post / guide
- Product page / landing page
- Tool / calculator
- Video
- Definition / encyclopedia entry
- Comparison / review

**Content Format:**
- How-to (step-by-step)
- Listicle (X ways, X causes)
- Comparison / vs
- Definition + subtopics
- Data-driven / study
- Q&A / FAQ

**Content Angle:**
- Beginner-friendly / 101
- Expert / clinical depth
- Personal experience / first-person
- Data-first / research-backed
- Problem → solution
- Freshness / recency

### 3.2 Dominant Pattern

If 3+ of 5 results share the same type/format/angle, that's the dominant pattern. Your content should match it.

If the top 5 are mixed (no clear dominant pattern), Google is likely testing — opportunity to try a differentiated approach, but with higher risk.

### 3.3 Primary Intent Label

| Intent | SERP Signals |
|--------|-------------|
| **Informational** | Blog posts, guides, Wikipedia, PAA, Knowledge Panel, AI Overview answering a question |
| **Commercial Investigation** | Comparison pages, "best" lists, review sites, shopping results mixed with reviews |
| **Transactional** | Product pages, shopping results dominant, pricing info, "buy" CTAs |
| **Navigational** | Single brand dominates, sitelinks, knowledge panel for a specific entity |
| **Mixed** | Multiple intent types in top 10 — Google is uncertain |

### 3.4 Content Direction Statement

```
INTENT ANALYSIS for "[keyword]":
Primary intent: [Informational/Commercial/Transactional/Navigational/Mixed]
Dominant type: [e.g., Blog post / guide]
Dominant format: [e.g., Definition + subtopics]
Dominant angle: [e.g., Expert / clinical depth]
Agreement: [X/5 results match]

CONTENT DIRECTION: Create a [type] in [format] with a [angle] approach.
```

---

## Step 4: CTR Modeling & Traffic Estimation

> Estimate realistic traffic potential given the SERP layout.

### 4.1 Bifurcated CTR Model

**AIO-absent SERP:**

| Position | Desktop CTR | Mobile CTR |
|----------|------------|------------|
| 1 | 28-35% | 25-30% |
| 2 | 15-17% | 13-15% |
| 3 | 10-12% | 9-11% |
| 4 | 7-8% | 6-7% |
| 5 | 5-6% | 4-5% |
| 6-7 | 3-4% | 2-3% |
| 8-10 | 2-3% | 1.5-2% |

**AIO-present SERP:**

| Position | Estimated CTR | Source |
|----------|--------------|--------|
| 1 | 10-18% | GrowthSRC 2025 (~19% average), varies by query |
| 2 | 6-10% | ~45-51% reduction from AIO-absent |
| 3 | 4-6% | ~40-46% reduction |
| 4-10 | 1-3% | Heavily compressed |
| Cited in AIO | +35% organic clicks, +91% paid clicks | Seer Interactive 2025 |

> **Key data points:**
> - AIO reduces overall organic CTR by 40-58% (Ahrefs, 300K keywords, Dec 2023 vs Dec 2025)
> - On heavily AIO-affected queries, position 1 CTR can drop as low as 0.61% (Seer Interactive)
> - The "clean SERP" CTR ranges above are already somewhat optimistic for 2025-2026 — actual averages across all queries (Backlinko) put position 1 at ~27.6%
> - Sources disagree: First Page Sage says 39.8% (clean), Backlinko says 27.6% (all), GrowthSRC says 19% (post-AIO)

### 4.2 Traffic Estimation Formula

```
Estimated Monthly Clicks = Volume × CTR_for_target_position × (1 - AIO_discount) × Seasonality_factor
```

Where:
- `CTR_for_target_position` = from the appropriate table above
- `AIO_discount` = 0.58 if AIO present, 0 if absent (Ahrefs 2025)
- `Seasonality_factor` = from Semrush `Td` trend data (1.0 = average)

### 4.3 Zero-Click Assessment

| SERP Layout | Est. Zero-Click Rate | Implication |
|-------------|---------------------|-------------|
| Clean (no features) | ~45-50% | Best organic opportunity |
| Featured snippet + PAA | ~55-60% | Moderate — snippet captures some clicks |
| AI Overview present | ~65-80% | High zero-click. Consider: is brand visibility in AIO worth targeting even without clicks? |
| AI Overview + Featured Snippet + Knowledge Panel | ~80%+ | Very high zero-click. Target only if the keyword is strategically important (brand visibility, citation) |

> **Note on zero-click data:** The often-cited 83% zero-click rate for AIO queries (SparkToro/Datos) is from one source. Semrush found zero-click rates actually decreased slightly for keywords that gained AIOs, suggesting selection bias in some studies. Treat specific percentages as directional, not precise.

---

## Step 5: AI Overview & GEO Analysis

> The new frontier: understanding and targeting AI-generated results.

### 5.1 AIO Detection

From Step 1.4 WebSearch: does the keyword trigger an AI Overview?

| Detection | Notes |
|-----------|-------|
| **AIO present** | Record: what it says, how many sources cited, which domains cited |
| **AIO absent** | Good — standard organic competition applies |
| **AIO flickering** | Appears sometimes, not always. Google is testing. Check multiple times |

### 5.2 AIO Citation Analysis

If AIO is present, analyze what sources Google cites:

| Cited Domain | Domain Type | In Top 10? | Content Format |
|-------------|------------|-----------|---------------|
| [domain] | [type] | Yes/No | [format of cited page] |

**Patterns to look for:**
- Are top-10 results being cited, or are citations pulling from outside the top 10? (Only 38% of AIO citations come from top-10 pages)
- What content format gets cited most? (articles, reference pages, medical sources?)
- Are any of your pages cited? If not, what do cited pages have that you don't?

### 5.3 AIO Trigger Rate by Query Type

| Query Type | AIO Trigger Rate | Source |
|-----------|-----------------|--------|
| Informational | ~30-40% | Multiple studies |
| Commercial | ~4-10% | Ahrefs/Semrush (NOT 25% — that's the share of AIOs that are commercial, not trigger rate) |
| Transactional | ~2-5% | Rare |
| YMYL / Health | Higher than average | Google uses AIO to provide authoritative health answers |

### 5.4 GEO Signal Assessment

For each cited page (and your competing page), check the 5 GEO signals:

| Signal | Check | Your Page | Cited Page |
|--------|-------|-----------|-----------|
| Answer-first architecture | First 2-3 sentences directly answer the heading question | ✅/❌ | ✅/❌ |
| Statistics density | Specific stat every 200-300 words with attribution | ✅/❌ | ✅/❌ |
| Source attribution | "According to [named source]" format | ✅/❌ | ✅/❌ |
| Expert quotations | Direct quotes from experts or studies | ✅/❌ | ✅/❌ |
| Self-contained definitions | Term included in definition sentence, no pronoun references | ✅/❌ | ✅/❌ |

### 5.5 AIO Strategy Decision

| Scenario | Strategy |
|----------|---------|
| AIO present, you're cited | **Defend** — maintain content quality, keep information current |
| AIO present, competitor cited, you're not | **Attack** — improve GEO signals, match/exceed cited content's quality and structure |
| AIO present, no one from your niche cited | **Optimize** — create the most authoritative, well-structured content for this topic |
| AIO absent | **Standard SEO** — focus on traditional ranking factors |

### 5.6 Content Freshness for AIO

85% of AIO-cited pages were published or updated within 2 years. If your content is older than 2 years, refresh it before expecting AI citation.

---

## Step 6: Featured Snippet Opportunity Assessment

### 6.1 Prerequisites Check

- [ ] Does this keyword trigger a featured snippet? (from Step 1)
- [ ] Can you realistically rank in the top 10? (from KD vs AS comparison)

If either is No → skip featured snippet optimization. Focus on basic ranking first.

> **Context:** Featured snippets have declined 64% as AI Overviews have grown (correlation: -0.90, Ahrefs). The optimization target is shifting from winning the snippet box to being cited in the AI Overview. Still optimize for snippets when they exist, but recognize they're less common than in 2023.

### 6.2 Snippet Vulnerability Assessment

A featured snippet is "vulnerable" (capturable) when:
1. The current snippet holder is **outside position 1** (snippet can be taken by a better-positioned result)
2. The snippet content is **thin or incomplete** (partial answer, poorly formatted)
3. The snippet is in a **format you can match** (you can produce a better table, list, or paragraph)
4. The snippet holder has **lower authority** than your site
5. The snippet is **factually outdated** (wrong data, old statistics)

3+ vulnerability signals = good opportunity.

### 6.3 Format-Specific Optimization

**Paragraph snippet:**
- Write a direct answer in **40-50 words** (the sweet spot for display)
- Start with the keyword or a close variant
- No preamble — get to the answer immediately
- Place in the relevant section, top third of article preferred

**List snippet (ordered or unordered):**
- Use an H2/H3 with the query, followed immediately by a list
- Include **8+ items** to trigger Google's "More items..." link (drives click-through)
- Each item should be concise (one line)

**Table snippet:**
- Create an HTML table with clear headers
- **5-9 rows** is the typical display range (varies by source: Portent says 5, Ahrefs says up to 9)
- Include data rows that extend beyond the visible snippet (drives click-through for "more rows")

---

## Step 7: Competitive SERP Landscape

> Who dominates this SERP, and can you realistically break in?

### 7.1 Domain Type Classification

From the top 10 results (Step 1.2), classify each domain:

| Type | Examples | Difficulty to Compete |
|------|---------|----------------------|
| Major brand / high-authority | WebMD, Healthline, Mayo Clinic, Wikipedia | Very hard — don't target head terms they dominate |
| Niche authority | Specialized fertility/PCOS sites with strong DR | Hard but possible with better content |
| Mid-tier content sites | Health blogs, media sites with moderate authority | Medium — beatable with quality + authority |
| UGC / Forums | Reddit, Quora, patient forums | Medium — can outrank with expert content, but Google increasingly values UGC |
| Small sites | Low-DR blogs, new sites | Easy to beat |
| Your domain | Where you currently rank (if at all) | — |

### 7.2 Authority Distribution

| Domain | Est. DR/AS | Domain Type | Position |
|--------|-----------|------------|---------|
| [domain1] | 85 | Major brand | #1 |
| [domain2] | 60 | Niche authority | #2 |
| ... | | | |

### 7.3 "Weakest Link" Identification

Find the most replaceable result in the top 10:
- Lowest authority domain in top 5
- Content that's outdated, thin, or poorly structured
- Page that's ranking due to domain authority, not content quality

This is your entry point. Create content significantly better than the weakest link.

---

## Step 8: SERP Volatility Assessment

> How stable are the rankings? Don't invest heavily in volatile SERPs where positions change weekly.

### 8.1 Historical SERP Comparison

```
Report: phrase_organic
Params: phrase=<keyword>, database="us", display_limit=10, display_date="20260302"
```

Set `display_date` to 3 months ago. Compare current top 10 vs historical top 10.

### 8.2 Stability Classification

| Level | Criteria | Implication |
|-------|----------|-------------|
| **Stable** | 7+ of 10 same domains, positions changed <3 spots | Safe to invest — rankings are durable |
| **Moderate** | 5-7 same domains, some position shuffling | Normal — invest with confidence |
| **Volatile** | 3-5 same domains, significant reshuffling | Caution — Google may be re-evaluating intent. Harder to maintain rankings |
| **Highly Volatile** | <3 same domains, complete turnover | Wait — Google hasn't settled on what this SERP should look like. Revisit in 3 months |

### 8.3 Feature-Level Volatility

Also check:
- Is the AI Overview appearing/disappearing? (flickering = Google testing)
- Did a featured snippet appear or disappear?
- Did the dominant content type change? (e.g., guides replaced by videos)

Feature-level volatility reduces confidence in CTR estimates.

---

## Step 9: SERP Scorecard Output

Synthesize all findings into a decision-ready scorecard:

```
═══════════════════════════════════════════
SERP SCORECARD: [keyword]
Generated: [date]
═══════════════════════════════════════════

KEYWORD METRICS
Volume: [X]/mo | KD: [X] | Intent: [type] | Trend: [rising/stable/declining]
CPC: $[X] (commercial signal)

SERP FEATURE MAP
[Feature 1]: Present ✅ / Absent ❌
[Feature 2]: Present ✅ / Absent ❌
...
Feature density: [Clean / Moderate / Heavy]
AI Overview: [Present / Absent / Flickering]

INTENT CLASSIFICATION
Type: [type] | Format: [format] | Angle: [angle]
Agreement: [X/5] | Confidence: [High/Medium/Low]

TRAFFIC POTENTIAL
Estimated monthly clicks (position 1): [X] (with AIO adjustment)
Estimated monthly clicks (position 3): [X]
Zero-click risk: [Low / Medium / High]
AIO citation value: [High / Medium / Low / N/A]

COMPETITIVE LANDSCAPE
Dominant domain types: [brands / niche / mixed]
Average DR of top 5: [X]
Weakest link: [domain at position X — reason]
SERP stability: [Stable / Moderate / Volatile / Highly Volatile]

══════════════════════════════════════════
VERDICT: [TARGET / DEFER / SKIP]
══════════════════════════════════════════

[If TARGET:]
Content type to create: [type]
Content format: [format]
SERP features to aim for: [snippet type, AIO citation, etc.]
GEO priority: [High / Medium / Low]
Estimated effort: [X hours]
Next steps:
1. [specific action]
2. [specific action]
3. [specific action]

[If DEFER:]
Reason: [why not now]
Prerequisite: [what needs to happen first — e.g., "build more topical authority in this cluster"]
Revisit condition: [when to reconsider — e.g., "when AS reaches X" or "after publishing Y supporting pages"]

[If SKIP:]
Reason: [why not worth targeting]
Alternative: [suggest a related keyword with better opportunity]
```

---

## Step 10: PAA-Driven Content Expansion (Optional)

> Mine People Also Ask for additional content opportunities.

### 10.1 Expand PAA

From Step 1.4, collect all visible PAA questions. Click through 2-3 levels to get deeper questions.

### 10.2 Classify PAA

| PAA Question | Volume (if available) | Classification |
|-------------|----------------------|---------------|
| [question] | [X/mo] | Standalone page — enough depth for its own content |
| [question] | [X/mo] | Section within primary content |
| [question] | [X/mo] | FAQ item — brief answer |

For high-volume PAA questions, validate volume:
```
Report: phrase_this
Params: phrase=<paa_question>, database="us"
```

---

## Batch Mode (Multiple Keywords)

When analyzing multiple keywords at once (e.g., for a content calendar), run Steps 1-4 and 7-8 for each keyword and produce a summary table:

| Keyword | Vol | KD | Intent | AIO? | Snippet? | Feature Density | CTR Est (Pos 1) | Stability | Verdict |
|---------|-----|-----|--------|------|----------|----------------|-----------------|-----------|---------|
| [kw1] | [X] | [X] | Info | Yes | No | Heavy | [X] | Stable | TARGET |
| [kw2] | [X] | [X] | Comm | No | Yes | Moderate | [X] | Volatile | DEFER |

Skip the detailed deep-dive (Steps 5, 6, 9, 10) in batch mode — those are for individual keyword analysis.

---

## Fallbacks (When Semrush MCP Unavailable)

| Step | Alternative | Quality |
|------|------------|---------|
| Keyword metrics | WebSearch for free keyword tools | Approximate |
| Top 10 results | WebSearch directly | Good — but no DR/keyword count data |
| SERP features | WebSearch + scripts/serp_scraper.py | Good for live features |
| CTR modeling | Apply standard curves manually | Approximate |
| Historical SERP | **Cannot replicate** without historical data | Flag as unavailable |
| AIO analysis | WebSearch directly | Full quality |

Most SERP analysis can be done with WebSearch alone — it's the most tool-independent reference file.

---

## Notes & Lessons Learned

1. **Featured snippets are declining.** They've dropped 64% as AI Overviews have grown (correlation: -0.90). Optimize for snippets when they exist, but recognize the target is shifting to AIO citation.
2. **Bifurcate the CTR model.** A single CTR curve is dead. AIO-present queries have 40-60% lower organic CTR. Always check for AIO before estimating traffic.
3. **Zero-click rates are directional, not precise.** Different studies report wildly different numbers (60% vs 83%) depending on methodology. Use them for relative comparison, not absolute forecasting.
4. **Reddit and forums are rising SERP players.** Reddit is #4 most visible domain in US Google. For queries where forums dominate, consider Reddit content strategy alongside traditional SEO.
5. **AIO citation > organic position for some queries.** Being cited in the AI Overview with no organic ranking may be more valuable than ranking #5 organically, because cited brands earn 35% more organic clicks and 91% more paid clicks.
6. **Google removed num=100.** Since September 2025, the SERP parameter for showing 100 results is gone. Focus rank tracking on top-10 positions — tracking beyond page 1 is now 10x more expensive.
7. **"Things to Know" in healthcare.** This feature appears in ~69.5% of healthcare queries (GrowByData). However, this is a single-source statistic — treat directionally, not as a hard benchmark.
