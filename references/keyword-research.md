# Keyword Research Reference

## Overview

Keyword research is a multi-phase workflow. It starts with seed research (Phase 1), pauses for user review, then validates and prioritizes via Semrush (Phase 2), pauses again, and delivers a ranked content plan (Phase 3).

```
Phase 1: Seed Research (user picks one or combines)
├── Path A — Claude researches online (Reddit via PRAW, web, optionally Instagram/Apify)
├── Path B — User shares their insights (sales calls, ORM, support tickets, etc.)
├── Path C — Competitor gap → HAND OFF to content-gap.md, bring seeds back
└── Path D — User has a specific topic/keyword → Semrush expansion (with pre-checks)

>>> GATE: Present research + seed keywords (with intent tags). STOP. <<<

Phase 2: Keyword Validation (Semrush) — only after user says proceed
  2a. Batch validate seeds (phrase_these)
  2b. Expand top seeds into question clusters (phrase_questions)
  2c. Current rankings check (domain_organic) — skip if done in Path C
  2d. SERP feature check for top 5-10 seeds (phrase_organic)
  2e. Sub-cluster fan-out — map sub-topics each seed must cover
  2f. Prioritization scoring (6-factor incl. AI-surface gap + E-E-A-T flag)
  FALLBACK: If Semrush MCP unavailable → WebSearch-based validation

>>> GATE: Present ranked ideas with content types and funnel map. STOP. <<<

Phase 3: Deliverable
  - New content ideas table (with fan-out sub-clusters, content type, funnel stage)
  - Existing content refresh (low organic + no AIO → sub-cluster gap → add sections)
  - Quick wins table (position-based)
  - Funnel balance summary
```

---

## Phase 1 — Seed Research

### Opening Question

When keyword research is triggered, ask the user:

> **How should we find seed topics?** Pick one or combine:
>
> **A) I'll research online** — I'll mine Reddit, search the web, and surface what your audience is actually discussing. I'll need to know which communities to look at.
>
> **B) You share your research** — Paste in whatever you have: sales call notes, support ticket themes, community/ORM research, competitor reviews, anything.
>
> **C) Competitor gap analysis** — Give me your domain and 2-3 competitor domains. I'll find keywords they rank for that you don't.
>
> **D) I have a specific topic** — Give me a keyword or topic. I'll expand it into related terms, questions, and variants.

No default — let the user pick. Multiple paths can be combined.

---

### Path A — Claude Researches Online

> **Method:** harvest via `references/content-scraping.md` (Reddit PRAW/Apify, YouTube + subtitles, Instagram), then extract and roll up topics via `references/social-topic-mining.md` (L0→L2, entity-role peeling). `scripts/reddit_miner.py` is the Reddit Tier-1 adapter. Extracted L0/L1 topics become the seed keywords that feed the Research Gate below.

**Conversation before running anything.** Propose a research plan in one message:

> Here's what I'd suggest for [brand/product]:
>
> **Subreddits:**
> - Brand-owned: r/[BrandName] (if it exists)
> - Category: r/[relevant1], r/[relevant2], r/[relevant3] — [brief reason each is relevant]
>
> **Search approach:** I can browse top posts from the past year, or search for specific phrases. Here are some I'd try:
> - "[phrase 1]"
> - "[phrase 2]"
> - "[phrase 3]"
>
> I'll pull ~75 posts per subreddit with top 10 comments each. Want to adjust anything before I start?

Generate subreddit and phrase suggestions based on what you know about the user's product/category. User confirms, edits, or redirects. **Only then** run the script.

**Script execution:**
```bash
# Browse mode (top posts from past year)
python3 scripts/reddit_miner.py --subreddits X,Y,Z --limit 75 --sort top --comments 10 --json

# Search mode (specific phrase within subreddits)
python3 scripts/reddit_miner.py --subreddits X,Y,Z --search "phrase" --comments 10 --json
```

**Additionally:** Use WebSearch for broader web research (forums, Quora, review sites) beyond Reddit.

**Instagram/Apify (optional, not scripted):**
If the user wants Instagram, use Apify MCP tools to scrape captions by hashtag. Instagram is stronger for **content angles and hooks** than for search keywords — captions show what framing resonates, hashtag clusters show how the audience self-identifies. Mention as an available option, don't default to it.

**What to extract:**
- Topic clusters ranked by post count + engagement
- Top 3 post titles per cluster (with engagement scores)
- Question-format seed phrases from titles
- Comment-sourced seeds (question fragments from top comments)
- Competitor mentions and how people compare products
- Real user language that differs from "tool language"

**Intent tagging at discovery:** Tag every seed with a preliminary intent:
| Pattern | Intent |
|---------|--------|
| "how to", "what is", "why does", explainer | Informational |
| "X vs Y", "best X", "recommend", "review" | Commercial Investigation |
| "buy X", "X price", "X coupon", "where to get" | Transactional |
| "[brand] login", "[brand] app" | Navigational |

---

### Path B — User Shares Insights

Ask:
> Share whatever you have — sales call notes, customer support themes, community/ORM research (Reddit, Facebook groups, forums), competitor review summaries, screenshots. Raw is fine, I'll organize it.

Read the input and extract:
- **Recurring themes** — group by topic, count frequency of mentions
- **Exact customer phrases** — preserve original language, don't paraphrase
- **Questions and pain points** — especially questions that imply a search intent
- **Competitor mentions** — which products named and in what context
- **Emotional triggers** — frustration, confusion, comparison anxiety (informs content angle)
- **Preliminary intent tag** on each extracted seed

---

### Path C — Competitor Gap → Hand Off to content-gap.md

Ask for the user's domain and 2-3 competitor domains. Then **load `references/content-gap.md`** and follow its methodology (uses `domain_domains`, `domain_organic`, etc.).

The gap keyword list from content-gap.md becomes the seed list that feeds back into this workflow at the Research Gate.

This avoids duplicating gap analysis logic. `keyword-research.md` owns the pipeline; `content-gap.md` owns the competitive analysis methodology.

---

### Path D — Specific Topic/Keyword

**Pre-checks before expanding:**

1. **Existing coverage:** Run `domain_organic` filtered for the keyword — does the user already rank? If yes, this is an optimization opportunity, not new content. Flag cannibalization risk if multiple pages target it.
2. **Scope assessment:** Is the input too broad or too narrow?
   - **Too broad** ("fertility", "ovulation") — this is a **seed topic**, not a seed keyword. Don't ask the user to narrow it. Instead, treat it as input for Phase 1 discovery: run Paths A/B/C to decompose the topic into specific seed keywords, then return to the Research Gate with those keywords. A seed topic yields multiple content pieces; a seed keyword yields one.
   - **Too narrow** ("inito test strip lot 2847") — suggest the parent topic.
   - **Just right** ("ovulation pain", "late ovulation pregnancy") — this is a seed keyword. Proceed with Semrush expansion below.

Then expand seed keywords via Semrush:
- `phrase_related` — semantically related terms
- `phrase_questions` — question variants (who/what/how/why)
- `phrase_fullsearch` — all keyword variations containing the seed

---

### Path Combinations

Paths can be combined. Common combos:
- **A + C:** Mine Reddit for audience language, then check competitor gap for what's already being captured
- **B + D:** User shares sales call themes, Claude expands each into keyword clusters
- **A + B:** Claude mines Reddit AND user pastes support ticket themes — merge signals

---

## Research Gate — MANDATORY STOP

After Phase 1 (any path or combo), present this summary:

```
## Research Summary

**Source:** [Reddit / User-provided / Competitor gap / Topic expansion / combo]
**Inputs analyzed:** [N posts / N notes / N competitor keywords]
**Themes found:** [N clusters]

### 1. [Theme Name] — [N posts/mentions, signal strength]
- "Sample quote or title 1"
- "Sample quote or title 2"
- "Sample quote or title 3"

### 2. [Theme Name] — ...

---

## Seed Keywords Extracted

| # | Seed Keyword | Intent | Source | Why it matters |
|---|-------------|--------|--------|----------------|
| 1 | ... | Informational | Reddit comment | ... |
| 2 | ... | Commercial | User input | ... |
| 3 | ... | Informational | Competitor gap | ... |

---

**Next step:** I can validate these seeds in Semrush — check volumes, difficulty, SERP features, and your current rankings. Shall I proceed?
```

**CRITICAL INSTRUCTION:** Do NOT call any Semrush MCP tool (`phrase_these`, `phrase_questions`, `domain_organic`, `domain_domains`, `phrase_organic`, or any `execute_report`) until the user explicitly says to proceed. The research summary is the deliverable of Phase 1. The user may want to:
- Add or remove seeds
- Ask follow-up questions about the research
- Share additional context
- Save the research and come back later
- Skip Semrush entirely and use the seeds as-is

---

## Phase 2 — Keyword Validation (Semrush)

Only runs after user explicitly confirms.

### 2a. Batch Validate Seeds

```
phrase_these — semicolon-separated seed list, database: "us"
Returns: volume, CPC, competition, trend (12-month index)
```

**Key columns:**
| Column | Meaning | How to use |
|--------|---------|------------|
| Nq (volume) | Avg monthly searches | Directional signal, not gospel |
| Cp (CPC) | Cost-per-click | High CPC = commercial intent, money keyword |
| Co (competition) | Advertiser competition 0–1 | Proxy for commercial value |
| Kd (keyword difficulty) | 0–100, links needed | <30 = winnable without heavy link building |
| Td (trend) | 12-month index 0–1 | Rising = growing demand |

**Read trends correctly:** Td returns 12 comma-separated values (oldest → newest). `0.67,0.55,...,1.00,1.00` = growing. Flat = stable. Declining = fading.

### 2b. Expand Top Seeds Into Question Clusters

```
phrase_questions — one seed at a time, sort: nq_desc
Returns: who/what/where/when/why/how variants with volume + KD
```

Pick the top 2-3 seeds by business value and expand. These question variants become sub-keywords that a single content piece can rank for.

### 2c. Current Rankings Check

*Skip if already done in Path C.*

```
domain_organic — user's domain, database: "us", sort by traffic desc
export_columns: Ph, Po, Nq, Tr, Co, Kd
```

**Quick wins** = positions 4–20 with volume > 500. A targeted on-page optimization pass can push these to page 1 without new content.

**Gap** = topic cluster not present in rankings at all. These need new content.

### 2d. SERP Feature Check

For the top 5-10 seeds by priority score:

```
phrase_organic — one seed at a time, database: "us"
Returns: domains ranking, positions, SERP features present
```

Use this to determine:
- **Featured snippet present?** → content needs structured answer (definition paragraph, list, table)
- **PAA (People Also Ask)?** → content needs FAQ sections
- **Video carousel?** → consider video content
- **Who ranks #1-3?** → assess competitive difficulty from actual SERPs, not just KD score

### 2e. Sub-cluster Fan-out

For the top 3-5 seeds by business value, map the sub-topics the content must cover. Three sources, cross-matched:

**Source 1 — LLM decomposition (Claude):**
Prompt Claude with the seed as a natural question:
> "For the topic '[seed]', list every sub-question a searcher might need answered. Include conversational phrasings, not just keyword-style queries."

Run 2-3 times, keep recurring sub-questions. This is the **generation** step — broad, fast, zero-cost.

**Source 2 — Semrush `phrase_questions`:**
Already run in step 2b. These are data-backed question variants with volume + KD. This is the **validation** step — confirms which sub-topics have measurable search demand.

**Source 3 — Google PAA (user-provided):**
Ask the user:
> "Google your top 3-5 seed keywords and share the People Also Ask questions you see (usually 5-10 per keyword). These are the sub-queries Google itself thinks this topic decomposes into."

PAA is ground truth — it's what Google actually shows searchers. Can't be scraped reliably, but takes the user 2 minutes per seed.

**Cross-match and output:**

| Sub-cluster | LLM | Semrush | PAA | Vol | KD | In existing content? | Action |
|---|:---:|:---:|:---:|---|---|---|---|

- **All 3 sources agree** → must-cover, high confidence
- **2 of 3 agree** → strong sub-cluster, include
- **Semrush-only** → data-backed addition, include with volume/KD
- **LLM-only** → hypothesis — may be real demand at zero tool volume (validate against Reddit/user data if available)
- **PAA-only** → Google thinks it matters — include

This table feeds into both:
- **New content:** defines the sections/headings the piece must answer before publishing
- **Existing content refresh:** compare against current page → missing sub-clusters = sections to add/rewrite (see Phase 3)

---

### 2f. Prioritization Scoring

| Factor | Score 1 | Score 2 | Score 3 | Weight |
|--------|---------|---------|---------|--------|
| Business Value | Tangential | Related | Product IS the answer | **3×** |
| KD (ease) | >70 | 30–70 | <30 | **2×** |
| Intent Match | Informational | Commercial investigation | Transactional | **2×** |
| Content Gap | Already ranking | Partial coverage | No coverage + competitor ranks | **2×** |
| AI-surface gap | Cited in AIO / no fan-out gap | Fan-out exists, parity with competitors | Competitors cited, you absent | **2×** |
| Search Volume | <100/mo | 100–1K/mo | >1K/mo | **1×** |

**Weighted total** = (BV × 3) + (KD × 2) + (Intent × 2) + (Gap × 2) + (AI_gap × 2) + (Vol × 1)

Max = 36. **Prioritize 30+.** Volume is a tiebreaker, not the gate — a zero-volume sub-cluster that appears in all three fan-out sources can still score high.

**Traffic potential > raw volume:** A page ranking #1 for a 400-volume keyword typically ranks for 100+ related variants. Use `phrase_related` to estimate true cluster size before dismissing a "low volume" seed.

**E-E-A-T / YMYL flag:** For each seed, assess whether the topic is YMYL (health, medical, financial). If yes, flag it with `YMYL` in the output. This means:
- Content likely needs expert review, medical citations, or author credentials
- Domain authority matters more — head terms may be unrealistic for newer sites
- Google holds these pages to a higher quality standard

Flag YMYL seeds but do **not** auto-deprioritize them. The user decides whether their domain can credibly rank. Present the flag, let them make the call.

---

### Fallback — Semrush MCP Unavailable

If Semrush MCP tools are not connected:

- **Phase 1 still works fully** — Paths A and B are independent of Semrush. Path D falls back to WebSearch for expansion.
- **Phase 2 falls back to WebSearch-based validation:**
  - Search each seed on Google, note who ranks on page 1
  - Estimate difficulty from domain authority of top results (all major brands = hard, mix of forums/small sites = easier)
  - Note visible SERP features (snippets, PAA, video)
  - Volume: use Google Trends relative comparison, or note "volume data unavailable — connect Semrush for precise numbers"
- Flag to user: "Semrush MCP is not connected. Using web search for validation — results are directional, not precise."

---

## Phase 3 — Deliverable

Present after Phase 2 validation.

### New Content Ideas

| Priority | Title | Head Keyword | Vol | KD | Intent | Funnel | Content Type | YMYL | SERP Opp. | Score |
|----------|-------|-------------|-----|----|--------|--------|-------------|------|-----------|-------|
| 1 | … | … | … | … | Commercial | Decision | Comparison page | — | Featured snippet | 34 |
| 2 | … | … | … | … | Informational | Awareness | Blog post / guide | YMYL | PAA | 31 |

**Fan-out sub-clusters per content piece:** For each new content idea, include the sub-cluster table from step 2e. This defines the sections/headings the piece must answer. Hand off to `references/content-brief.md` with the sub-cluster list attached — the brief should map each sub-cluster to a section.

**Content type mapping:**
| Intent | Default Content Type |
|--------|---------------------|
| Informational | Blog post, guide, explainer |
| Commercial Investigation | Comparison page, "best X" roundup, vs page |
| Transactional | Product landing page, pricing page |
| Navigational | Optimized brand/feature page |

**Funnel stage mapping:**
| Stage | Signals |
|-------|---------|
| Awareness | "what is", "how does", "why do", educational queries |
| Consideration | "best X", "X vs Y", "X review", comparison queries |
| Decision | "buy X", "X price", "[brand] + product", transactional queries |

### Existing Content Refresh (sub-cluster gap)

**Priority signal:** pages with low organic ranking (positions 4-20) AND/OR low/no AI Overview appearance for their main keyword.

**Workflow:**
1. Identify candidate pages: `domain_organic` → positions 4-20 with volume, OR pages the user flags as having no AIO citation
2. For each candidate's main keyword, run sub-cluster fan-out (step 2e) — LLM decomposition + Semrush `phrase_questions` + user-provided PAA
3. Compare sub-clusters against the page's current content — which clusters does it adequately cover?
4. Prioritize missing clusters by KD + volume
5. Recommend: add sections for missing clusters, rewrite sections with weak coverage

| Page URL | Main Keyword | Position | Vol | Missing Sub-clusters | Priority Additions | Effort |
|----------|-------------|----------|-----|---------------------|-------------------|--------|
| … | … | 12 | 8K | [cluster 1], [cluster 2] | Add 2 sections | Moderate (half day) |
| … | … | 7 | 5K | [cluster 3] | Rewrite 1 section | Quick (1-2 hrs) |

Fan-out applies to existing content too — the same sub-cluster analysis that structures new content also diagnoses gaps in existing content.

### Quick Wins (Position-based)

Pages where no sub-cluster gap exists — the content is adequate but needs on-page optimization to move up.

| Page URL | Current Keyword | Position | Volume | Fix Required | Effort |
|----------|----------------|----------|--------|-------------|--------|
| … | … | 12 | 60,500 | On-page optimization | Quick (1-2 hrs) |
| … | … | 8 | 40,500 | Heading structure + internal links | Moderate (half day) |

### Funnel Balance Summary

After the tables, include:

> **Funnel coverage:** X awareness pieces, Y consideration pieces, Z decision pieces.
> **Gap:** [e.g., "Decision-stage content is missing — no comparison or vs pages. 3 of the top 5 ideas fill this gap."]

---

## Tools Reference

### Scripts
```bash
python3 scripts/reddit_miner.py --limit 75 --sort top --comments 10          # human-readable
python3 scripts/reddit_miner.py --limit 75 --sort top --comments 10 --json   # JSON for piping
python3 scripts/reddit_miner.py --subreddits X,Y --search "phrase" --json     # search mode
```

### Semrush MCP Reports
| Report | Use for |
|--------|---------|
| `phrase_these` | Batch-validate multiple seeds (semicolon-separated) |
| `phrase_questions` | Expand a seed into question-format keyword cluster |
| `phrase_related` | Broaden a seed — content ideation, cluster sizing |
| `phrase_fullsearch` | All keyword variations containing the seed |
| `phrase_this` | Single keyword deep-dive |
| `phrase_kdi` | Keyword difficulty for prioritization |
| `phrase_organic` | SERP results — who ranks, SERP features present |
| `domain_organic` | Domain's current rankings + traffic; find quick wins |
| `domain_domains` | Keyword gap between 2–5 domains |
| `domain_organic_organic` | Find who competes for the same keywords |

**Always call `get_report_schema(report=<name>)` before `execute_report` if params are unknown.**

---

## Notes & Lessons Learned

**Reddit "top/year" > "hot" for SEO seeds.** Hot posts are noise-heavy (memes, emotional support). Top/year surfaces the highest-signal content — questions and pain points validated over time.

**Keyword tools undercount conversational queries.** "did I actually ovulate" shows zero Semrush volume but appears in dozens of Reddit threads. The SEO opportunity is the search-engine phrasing ("confirm ovulation", "how to know if you ovulated"). Reddit gives you the intent, tools give you the indexed form.

**Zero-KD keywords with high business value are rare and urgent.** When you find one (e.g., "does LH surge in anovulatory cycle" — KD=0, directly supports Inito's core message), prioritize it immediately regardless of volume.

**Community signals validate what tools can't.** A subreddit thread with 200 upvotes is confirmed demand. A keyword tool might show that query at 10 or zero volume. Both are true — the demand exists but people phrase it conversationally, not as bare keywords.

**YMYL topics need E-E-A-T awareness, not avoidance.** Health/fertility keywords are YMYL, but that doesn't mean they're unrankable. It means the content needs expert backing (citations, medical review, author credentials). Flag it so the user can plan for the extra effort.

**Fan-out cross-validation beats any single source.** Claude generates broad sub-questions, Semrush validates with volume/KD, and Google PAA shows what the engine actually decomposes the query into. The intersection of all three is the highest-confidence sub-cluster list. Claude-only items may represent real demand at zero tool volume — cross-check against Reddit/user data before dismissing.

**Existing content gaps hide in sub-clusters.** A page can rank position 8 for its main keyword but miss 3 of 5 sub-clusters entirely. Fan-out analysis on existing pages surfaces these gaps — adding the missing sections is often higher-ROI than writing new content from scratch.
