# SEO Content Workflow

## Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: KEYWORD DISCOVERY                                  │
│  Skill: keyword-research.md (Phase 1)                       │
│                                                             │
│  Sources:                                                   │
│  • Reddit, forums, reviews, customer conversations          │
│  • Competitor gap analysis (what do they rank for?)          │
│  • Google Search Console (existing impressions)              │
│                                                             │
│  Output: Seed keyword list                                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: KEYWORD VALIDATION & SELECTION                     │
│  Skill: keyword-research.md (Phase 2)                       │
│  Tool: Semrush MCP (keyword_research, organic_research)     │
│                                                             │
│  Evaluate each candidate:                                   │
│  • Traffic Potential (TP) — not raw search volume            │
│  • Keyword Difficulty (KD) — realistic for your DR?          │
│  • Business Potential (0–3 scale)                            │
│  • Search Intent (informational / commercial / transactional)│
│                                                             │
│  Output: Finalized primary keyword + 2–5 secondary keywords │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: CONTENT CREATION                                   │
│  Skill: content-brief.md → write content                    │
│                                                             │
│  Generate brief from keyword + SERP analysis:               │
│  • Intent-matched format and angle                          │
│  • Subtopics from top competitors + PAA                     │
│  • Target word count (competitive benchmark, not static)     │
│  • Unique angle / information gain strategy                  │
│                                                             │
│  Output: Written draft                                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: CONTENT EVALUATION  ◀── GATE CHECK                │
│  Skill: content-evaluation.md (NEW)                         │
│  Tools: WebFetch, Semrush MCP, Playwright                   │
│                                                             │
│  4a. COMPETITOR CONTENT ANALYSIS                            │
│  ├── Fetch top 3–5 SERP results for primary keyword         │
│  ├── Map all H2/H3 subtopics → build gap matrix             │
│  ├── Compare format, depth (word count), angle               │
│  └── Identify SERP features present                          │
│                                                             │
│  4b. COMPETITOR AUTHORITY ANALYSIS (context, not action)     │
│  ├── Backlink profiles: DR, referring domains per page       │
│  ├── Author credentials / E-E-A-T signals                    │
│  └── Domain authority comparison vs your site                │
│  ➤ Purpose: calibrate how good your content needs to be.    │
│    Strong backlinks + weak content = content opportunity.    │
│    Strong content + strong backlinks = hard to crack.        │
│                                                             │
│  4c. YOUR CONTENT ASSESSMENT                                │
│  ├── Subtopic coverage vs gap matrix (table stakes met?)     │
│  ├── Depth: within ±20% of top 3 average                    │
│  ├── Unique value: ≥1 section/data/angle competitors lack    │
│  ├── E-E-A-T: author credentials, citations, review byline  │
│  ├── Readability: sentence complexity, structure              │
│  └── Freshness: current data, recent references              │
│                                                             │
│  4d. GEO / AI EXTRACTION OPTIMIZATION                       │
│  ├── First-sentence answer rule (every H2/H3)                │
│  ├── Pronoun cleanliness (no ambiguous "it/this/they")       │
│  ├── Self-contained definitions (term in the definition)     │
│  ├── Structured lists/tables for comparisons                 │
│  └── Named sources + specific data points (citable facts)    │
│                                                             │
│  4e. FEATURED SNIPPET TARGETING                             │
│  ├── Identify snippet type (paragraph/list/table)            │
│  └── Format content block to match                           │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  VERDICT                                              │  │
│  │                                                       │  │
│  │  ✓ Content competitive → proceed to Step 5            │  │
│  │  ✗ Content gaps → fix gaps → re-evaluate (loop)       │  │
│  │  ✗ Authority gap too large → build links first,       │  │
│  │    or pick different keyword (back to Step 2)         │  │
│  │  ✗ Intent mismatch → rewrite format (back to Step 3)  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────┬───────────────────────────────────────┘
                      │ Content passes gate
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 5: ON-PAGE OPTIMIZATION                               │
│  Skill: on-page-optimization.md                             │
│                                                             │
│  HTML structure and tag optimization:                        │
│  ├── URL slug (3–5 words, keyword present)                   │
│  ├── Title tag (50–60 chars, keyword in first 30)            │
│  ├── Meta description (core message in first 105 chars)      │
│  ├── H1 (keyword in first 4 words)                           │
│  ├── Heading architecture (H2 → H3, no skips)               │
│  ├── Keyword placement (5 core locations)                    │
│  ├── Schema markup (Article, Breadcrumb, FAQ if health/gov)  │
│  ├── Internal linking (outbound + queue inbound)             │
│  ├── Media optimization (alt text, WebP, lazy load)          │
│  └── Branded vs non-branded classification                   │
│                                                             │
│  Output: Tag recommendations with current → suggested        │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 6: TECHNICAL SEO                                      │
│  Skill: technical-seo.md                                    │
│                                                             │
│  Site-wide and page-level technical checks:                  │
│  ├── Crawlability (robots.txt, sitemap, noindex audit)       │
│  ├── Indexability (canonical, duplicates, soft 404s)          │
│  ├── Redirects (chains, loops, 404s with backlinks)          │
│  ├── Internal link topology (orphans, depth, distribution)   │
│  ├── Security (HTTPS, headers, mixed content)                │
│  ├── Core Web Vitals (LCP, INP, CLS)                        │
│  ├── Mobile optimization                                     │
│  ├── JS rendering (raw HTML vs rendered DOM)                 │
│  ├── Structured data validation                              │
│  └── AI crawler management                                   │
│                                                             │
│  Output: Scored audit with priority-tiered fixes             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
                  PUBLISH
                      │
                      ▼
              MONITOR & ITERATE
              (rank tracking, re-audit quarterly)
```

## Skill Routing Summary

| Step | Skill | What It Owns |
|---|---|---|
| 1 | `keyword-research.md` | Seed discovery + Semrush validation |
| 2 | `keyword-research.md` | Same skill, Phase 2 |
| 3 | `content-brief.md` | Brief generation → writing |
| 4 | `content-evaluation.md` | Content competitiveness, competitor analysis (incl. backlink context), E-E-A-T, GEO, snippet targeting |
| 5 | `on-page-optimization.md` | Tags, placement, schema, internal links, media |
| 6 | `technical-seo.md` | Crawlability, indexability, CWV, site-wide health |

## Supporting Skills (called from within the pipeline)

| Skill | Called By | Purpose |
|---|---|---|
| `content-gap.md` | Step 1, Step 4 | Site-wide keyword gap analysis (which keywords do competitors rank for that we don't?) |
| `backlink-analysis.md` | Step 4 | Competitor backlink profiles as context for content evaluation |
| `serp-analysis.md` | Step 3, Step 4 | SERP feature detection, intent classification |
| `competitor-benchmarking.md` | Step 1, Step 4 | Domain-level comparison, share of voice |
| `content-cluster.md` | Step 1, Step 5 | Pillar/spoke mapping, cannibalization check |

## Key Principle

Content evaluation (Step 4) is a GATE, not an optimization step. It answers:
**"Given who the competitors are, what they've written, and how many backlinks they have — is our content competitive enough to rank?"**

If the answer is no, the fix is NOT better tags. The fix is better content, a different keyword, or a link building campaign.
