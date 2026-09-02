# Content Brief Generation Reference

---
name: content-brief
description: >
  Generate actionable, data-driven content briefs from keyword + SERP analysis + competitor content analysis.
  Produces a 10-section writer-ready brief covering target keywords, search intent, content outline,
  unique angle, E-E-A-T requirements, GEO/AI optimization, linking instructions, and SERP feature targets.
  The brief contains everything a writer needs to produce competitive content without access to SEO tools.
  Includes chunk-level optimization and answer-first architecture for AI-era content.
tools: [Semrush MCP (keyword_research, organic_research, url_research), WebFetch, WebSearch, Playwright]
---

## When to Use This Reference

Load this when the user asks to:
- Create a content brief for a topic or keyword
- "Write brief for [topic]"
- Plan content before writing
- Prepare writing instructions for a writer/freelancer

**Pipeline position:** `keyword-research.md` (pick keyword) → **content-brief.md (plan content)** → write content → `content-evaluation.md` (gate check) → `on-page-optimization.md` (tag optimization)

---

## Pre-Brief: Confirm the Keyword

**Ask:** "What is the primary keyword for this brief?"

| Scenario | Action |
|----------|--------|
| User provides keyword | Proceed to Step 1 |
| User provides topic but not a keyword | Run quick keyword validation via Semrush `phrase_this` to get volume/KD. Suggest the best target keyword. Confirm with user |
| User wants to discover the right keyword first | Handoff to `keyword-research.md`, then return here |

---

## Step 1: Keyword Metrics & Secondary Keywords

### 1.1 Primary Keyword Data

```
Report: phrase_this
Params: phrase=<keyword>, database="us"
Columns: Ph, Nq, Kd, In, Td, Co
```

Collect: search volume (`Nq`), keyword difficulty (`Kd`), intent (`In`), trend (`Td`), CPC (`Co`).

### 1.2 Secondary Keywords

```
Report: phrase_related
Params: phrase=<keyword>, database="us", display_limit=30, display_sort="nq_desc"
Columns: Ph, Nq, Kd, Nr
```

### 1.3 Question Keywords

```
Report: phrase_questions
Params: phrase=<keyword>, database="us", display_limit=20, display_sort="nq_desc"
Columns: Ph, Nq, Kd
```

Select 3-5 secondary keywords and 5-8 question keywords that:
- Share the same intent as the primary keyword
- Add topical coverage without diluting focus
- Have some search volume (>50/mo) or represent important user questions

---

## Step 2: SERP & Intent Analysis (3 Cs)

> Understand what Google rewards for this keyword. This defines the content direction.

### 2.1 Fetch the SERP

```
Report: phrase_organic
Params: phrase=<keyword>, database="us", display_limit=10
Columns: Ur, Dn, Fp, Fk
```

Also run **WebSearch** for the primary keyword to see the live SERP layout (AI Overviews, featured snippets, PAA, etc.).

### 2.2 Classify Top 5 Results (3 Cs Framework)

For each of the top 5 organic results:

**Content Type** — What is the page?
| Type | Examples |
|------|---------|
| Blog post / guide | "Complete Guide to...", "Everything About..." |
| Product page | Landing page with features, pricing |
| Tool / calculator | Interactive tool (ovulation calculator, BMI calculator) |
| Video | YouTube result, video-first page |
| Definition / reference | Encyclopedia-style, medical reference |
| Comparison / review | "X vs Y", "Best [category]" |

**Content Format** — How is it structured?
| Format | Examples |
|--------|---------|
| How-to (step-by-step) | Numbered steps, process flow |
| Listicle | "X Ways to...", "X Causes of..." |
| Definition + subtopics | Define term, then explore aspects |
| Comparison / vs | Side-by-side analysis |
| Data-driven / study | Original research, statistics |
| Q&A / FAQ | Question-answer pairs |

**Content Angle** — What perspective dominates?
| Angle | Signals |
|-------|---------|
| Beginner-friendly / 101 | Simple language, "what is", "for beginners" |
| Expert / clinical depth | Medical terminology, studies cited, detailed mechanisms |
| Personal experience | First-person, patient stories, "my journey" |
| Data-first / research-backed | Statistics, charts, study citations |
| Problem → solution | Symptom-focused, leads to actionable advice |
| Freshness / recency | "2026 update", "latest research" |

### 2.3 SERP Intent Summary

```
SERP INTENT PROFILE for "[keyword]":
Dominant Type: [e.g., Blog post / guide]
Dominant Format: [e.g., Definition + subtopics]
Dominant Angle: [e.g., Expert / clinical depth]
Agreement: [X/5 results match this pattern]
Content Direction: Create a [type] in [format] with a [angle] approach
```

If top 5 results show mixed intent (e.g., 3 guides + 2 product pages), note this — Google is testing and intent may shift.

---

## Step 3: Competitor Content Deep Dive

> Extract what top-ranking content covers, how it's structured, and where it's strong.

### 3.1 Fetch Top 5 Competitor Pages

Use **WebFetch** on the top 5 organic URLs from Step 2. If any page is JS-heavy (returns thin content via WebFetch), use **Playwright** as fallback.

### 3.2 Extract from Each Page

| Data Point | How |
|-----------|-----|
| Word count | Count words in body content (exclude nav, footer, sidebar) |
| H2/H3 headings | List all subheadings — these reveal subtopic coverage |
| Key entities | Medical terms, brand names, conditions, treatments, studies mentioned |
| Structural elements | Does it have: ToC, key takeaway box, FAQ section, comparison table, images/diagrams? |
| E-E-A-T signals | Author name and credentials, medical reviewer, citations, publish/update date |
| Cited sources | What medical/scientific sources are referenced? |
| Unique content | What does this page cover that others don't? |

### 3.3 Build Competitive Summary

```
COMPETITIVE LANDSCAPE for "[keyword]":

| Metric | Comp 1 | Comp 2 | Comp 3 | Comp 4 | Comp 5 |
|--------|--------|--------|--------|--------|--------|
| Word count | | | | | |
| H2 sections | | | | | |
| Has medical review | | | | | |
| Has citations | | | | | |
| Last updated | | | | | |
| Unique angle | | | | | |

Minimum bar to compete:
- Word count range: [min]-[max] of top 5
- Subtopics ALL top 5 cover: [list — these are mandatory]
- Subtopics only 1-2 cover: [list — opportunity for differentiation]
```

---

## Step 4: Subtopic Discovery & Outline Building

> Build a comprehensive, data-backed outline using three-source cross-validation.

### 4.1 Three-Source Cross-Match

**Source 1: Competitor headings** (from Step 3.2)
- List all unique H2/H3 headings across top 5 competitors
- Note which subtopics appear in 3+ competitors (must-cover) vs 1-2 (optional)

**Source 2: Semrush question/related keywords** (from Step 1.2, 1.3)
- Map question keywords to potential sections
- Group related keywords by subtopic

**Source 3: PAA questions**
- From WebSearch, expand PAA for the primary keyword
- Note which questions align with competitor headings vs which are new angles

### 4.2 Cross-Match Table

| Subtopic | In Competitors (X/5) | In Semrush Questions | In PAA | Confidence |
|----------|----------------------|---------------------|--------|------------|
| [subtopic] | 5/5 | Yes | Yes | ★★★ Must cover |
| [subtopic] | 3/5 | Yes | No | ★★★ Must cover |
| [subtopic] | 2/5 | No | Yes | ★★ Should cover |
| [subtopic] | 0/5 | Yes | Yes | ★★ Opportunity (competitors miss this) |
| [subtopic] | 1/5 | No | No | ★ Consider (low signal) |

### 4.3 Build the Outline

Order subtopics logically based on content format (from Step 2):

**Definition + subtopics:**
1. What is [X]? (definition)
2. Causes / why it happens
3. Signs and symptoms
4. Diagnosis / how to know
5. Treatment / management options
6. Prevention / lifestyle factors
7. [Product-relevant section if appropriate]
8. FAQ

**How-to (step-by-step):**
1. Overview / why this matters
2. Prerequisites / what you need
3. Step 1 → Step N
4. Troubleshooting / common mistakes
5. FAQ

**Comparison:**
1. Methodology / how we compared
2. Quick comparison table
3. Detailed review of each option
4. Who should choose what
5. FAQ

**Problem → solution:**
1. Describe the problem (validate the reader's experience)
2. Why it happens (causes)
3. Solutions (ordered by accessibility)
4. When to see a doctor
5. FAQ

### 4.4 Chunk-Level Optimization (AI-Era)

Structure each section as a self-contained 200-400 word chunk:
- **Repeat the entity name** within each section (AI retrieval strips context)
- **Use question-format H2 headers** where natural (3.4x more likely to be extracted by AI systems)
- **Each chunk must be independently understandable** — don't rely on context from previous sections
- **Place the primary answer in the first 40-150 words** of each section

> **Source:** AI retrieval breaks content into 200-500 word chunks. 44.2% of LLM citations come from the first 30% of text. Question-format headers are extracted at 3.4x the rate of declarative headers.

---

## Step 5: Unique Value Angle

> The most important section of the brief. This is what makes the content worth creating.

### 5.1 Identify Differentiation Opportunities

Review competitor content from Step 3 and identify which of these 8 differentiation types apply:

| Type | Example | Applicability |
|------|---------|--------------|
| **First-party data** | "Based on data from 100K Inito users" | High for Inito — proprietary device data |
| **Expert quotes** | Named OB-GYN or RE providing original commentary | High for YMYL |
| **Original visuals** | Custom diagrams, charts from proprietary data | Medium |
| **Personal experience** | Patient stories, user testimonials | Medium |
| **Deeper specificity** | Cover a sub-angle competitors treat superficially | High |
| **Contrarian insight** | Challenge a common misconception with evidence | Use sparingly |
| **Interactive elements** | Calculator, quiz, assessment tool | High when applicable |
| **Recency** | Latest 2026 research competitors haven't incorporated | High for fast-moving topics |

### 5.2 Angle Statement

Write a one-sentence statement the writer uses as a north star:

> "This article should be the only guide to [topic] that [unique differentiator], making it the definitive resource for [target reader]."

**Examples:**
- "This article should be the only PCOS and fertility guide that includes real Inito user hormone data, making it the definitive resource for women with PCOS trying to conceive."
- "This article should be the only ovulation tracking comparison that includes hands-on testing of all 5 devices, making it the definitive resource for women choosing a fertility monitor."

---

## Step 6: E-E-A-T Requirements

> For YMYL health content, E-E-A-T signals are non-negotiable.

### 6.1 Author Requirements

| Requirement | Specification |
|-------------|--------------|
| Named author | Full name, not "Inito Team" or anonymous |
| Author credentials | Relevant medical or health science qualifications |
| Author bio page | Dedicated page with qualifications, experience, publications |
| Author experience signal | Personal or clinical experience with the topic area |

### 6.2 Medical Review

| Requirement | Specification |
|-------------|--------------|
| Medical reviewer | Board-certified OB-GYN, RE, or endocrinologist for fertility content |
| Reviewer byline | "Medically reviewed by [Name], [Credentials]" |
| Review date | Visible date of medical review |

### 6.3 Citation Standards

Every medical claim must be backed by a credible source. Focus on quality and relevance:

**Acceptable sources (prioritize):**
- Peer-reviewed journals (via PubMed)
- Professional guidelines (ACOG, ASRM, Endocrine Society, WHO)
- Government health agencies (NIH, NHS, CDC)
- Established medical references (UpToDate, Cochrane)

**Unacceptable as sole source:**
- Other blog posts
- Wikipedia
- Social media
- Outdated studies (>10 years for fast-moving topics, >5 years for treatment guidelines)

> **Important:** There is no fixed minimum citation count. Google's Quality Rater Guidelines emphasize that every medical claim should be backed by a credible source — the standard is "every claim supported," not "at least N citations per article."

### 6.4 Pre-Identified Sources

Based on the topic, pre-find 5-8 authoritative sources the writer can cite:
- Search PubMed for recent studies on the topic
- Check ACOG/ASRM practice bulletins
- Find relevant systematic reviews or meta-analyses

List these in the brief with titles and URLs to save the writer research time.

---

## Step 7: Featured Snippet Targeting

> Only pursue if conditions are met. Don't waste brief space on unreachable targets.

### 7.1 Prerequisites

- [ ] Primary keyword triggers a featured snippet (check from Step 2 WebSearch)
- [ ] You can reasonably rank in top 10 for this keyword (KD is feasible for your AS)

If either is false, skip this section in the brief.

### 7.2 Match Snippet Format

| Current Snippet Format | Optimization |
|-----------------------|-------------|
| **Paragraph** | Write a direct answer in 40-50 words. Place at top of the relevant section. Start with the keyword or a close variant. No preamble before the answer |
| **List** (ordered or unordered) | Use an H2 or H3 with the query, followed immediately by a list. Include 8+ items to trigger Google's "More items..." link (drives clicks) |
| **Table** | Create an HTML table with clear headers. 5-9 rows is the display range. Include row data that's not visible in the snippet (drives click-through) |

### 7.3 Brief Instructions

Add to the brief:
```
FEATURED SNIPPET TARGET:
Query: [keyword]
Current format: [paragraph/list/table]
Your section: Place in [section name], [position in article — top third preferred]
Format: [specific format instructions]
Key rule: Answer the question directly. No preamble, no "In this section we'll explore..."
```

---

## Step 8: GEO/AI Extraction Optimization

> Make the content easily extractable by AI search systems.

### 8.1 Seven GEO Writing Rules

Include these as writing guidelines in the brief:

| Rule | Instruction | Impact |
|------|------------|--------|
| **Answer-first** | Start each section by directly answering the heading question in the first 2-3 sentences (40-60 words). No introductory filler | High — 44.2% of LLM citations come from first 30% of text |
| **Self-contained definitions** | When defining a term, include the term in the definition sentence. "PCOS is a hormonal disorder..." not "It's a hormonal disorder..." | High — AI extracts individual sentences |
| **Statistics density** | Include a specific statistic every 200-300 words. "PCOS affects approximately 8-13% of women of reproductive age (WHO, 2023)" | Statistics Addition boosts AI citation by +40-41% (Princeton GEO) |
| **Source attribution** | Use inline attribution: "according to [named source]" or "a 2024 study in [journal] found..." | Cite Sources boosts AI citation by +30% (Princeton GEO) |
| **Quotation inclusion** | Include 2-3 direct quotes from medical experts or studies per article | Quotation Addition boosts AI citation by +27-28% (Princeton GEO) |
| **Pronoun cleanliness** | Minimize pronouns in key sentences. Every sentence should be understandable without reading the previous one | High — AI may extract a single sentence |
| **Structured data preference** | Use tables, numbered lists, and clear headers over paragraph-heavy prose. Structure makes extraction easier | Medium |

> **Source:** Princeton/Georgia Tech GEO study (KDD 2024). Correct ranges: Statistics Addition +40-41%, Cite Sources +30%, Quotation Addition +27-28%.

### 8.2 AI-Era Brief KPIs

In addition to traditional metrics (traffic, rankings), the brief should note:
- **AI Citation Rate**: Is this content being cited in AI Overviews?
- **Prompt Coverage**: Does this content answer common AI-directed queries?
- These are tracked post-publication, not during brief creation, but setting the expectation guides writing quality.

---

## Step 9: Linking Instructions

### 9.1 Internal Links FROM This Article

Use Semrush to find existing pages on your site that are relevant:

```
Report: domain_organic
Params: domain=<user_domain>, database="us", display_filter="+|Ph|Co|<topic_keyword>", display_limit=20
```

Or use **WebSearch**: `site:<user_domain> [related topic]`

Specify 3-5 internal links:
| Link To | Suggested Anchor Text | Where in Article |
|---------|----------------------|-----------------|
| /blog/pcos-guide | "PCOS and fertility" | Section on causes |
| /blog/ovulation-tracking | "tracking your ovulation" | Section on management |
| /product | "Inito fertility monitor" | Section on solutions |

### 9.2 Existing Pages That Should Link TO This Article

Identify 3-5 existing pages on the site that should add a link to the new content after it publishes:

| Link From | Context for Link | Suggested Anchor |
|-----------|-----------------|-----------------|
| /blog/pcos-guide | Add in the [relevant section] | "[new article topic]" |

### 9.3 External Sources to Cite

Pre-identified from Step 6.4:
| Source | URL | Use For |
|--------|-----|---------|
| [Study title] | [PubMed URL] | [Which claim it supports] |
| [Guideline] | [URL] | [Which recommendation it backs] |

---

## Step 10: Assemble the Brief

Compile all data into the writer-ready brief template below.

---

## Brief Output Template

```
═══════════════════════════════════════════
CONTENT BRIEF: [Primary Keyword]
Generated: [date]
═══════════════════════════════════════════

SECTION 1: KEYWORD TARGETS
─────────────────────────
Primary keyword: [keyword] | Volume: [X]/mo | KD: [X] | Intent: [type]
Secondary keywords: [3-5 keywords with volume]
Question keywords: [5-8 questions with volume]
Natural usage: Weave keywords into headings and body naturally. Do not force exact-match phrases.

SECTION 2: SEARCH INTENT & CONTENT DIRECTION
─────────────────────────────────────────────
Content type: [e.g., Long-form guide]
Content format: [e.g., Definition + subtopics]
Content angle: [e.g., Expert / clinical depth with patient-friendly language]
Basis: [X/5 top results follow this pattern]

SECTION 3: COMPETITIVE LANDSCAPE
─────────────────────────────────
Word count range: [min]-[max] of top 5 (target [recommended range])
Must-cover subtopics: [list from 3+ competitors]
Common structure: [what structural elements top 5 all use]
Competitors' weaknesses: [what's outdated, thin, or missing]

SECTION 4: CONTENT OUTLINE
──────────────────────────
[Ordered H2 sections with sub-points]

H2: [Section Title] (★★★ Must cover | [X/5 competitors, Semrush, PAA])
  - [Key point to cover]
  - [Key point to cover]
  - Target length: [X-Y words]

H2: [Section Title] (★★ Should cover | [sources])
  ...

[Continue for all sections]

Note: Each H2 section should be a self-contained 200-400 word chunk.
Use question-format headers where natural.

SECTION 5: UNIQUE ANGLE
────────────────────────
Angle statement: "[one sentence — the north star for this piece]"

Differentiation opportunities:
- [Specific opportunity 1]
- [Specific opportunity 2]
- [Specific opportunity 3]

What this content must do that competitors DON'T:
- [Specific unique value]

SECTION 6: E-E-A-T REQUIREMENTS
────────────────────────────────
Author: [Name or credential requirements]
Medical reviewer: [Required — specialty]
Citations: Back every medical claim with a credible source (see pre-identified sources below)

Pre-identified sources:
1. [Source title] — [URL] — use for [which claim]
2. [Source title] — [URL] — use for [which claim]
...

SECTION 7: WRITING RULES
─────────────────────────
1. Answer-first: Start each section by answering the heading question in the first 2-3 sentences
2. Self-contained: Every sentence should make sense without reading the previous one
3. Statistics: Include a specific statistic every 200-300 words with source attribution
4. Quotes: Include 2-3 direct expert or study quotes
5. Attribution: Use "according to [source]" format for key claims
6. Structure: Use tables, lists, and subheadings over dense paragraphs
7. No filler: Cut "in this section we'll explore" — get to the point

SECTION 8: LINKING INSTRUCTIONS
────────────────────────────────
Internal links FROM this article:
[Table from Step 9.1]

Pages to update with links TO this article (post-publish):
[Table from Step 9.2]

External citations:
[Table from Step 9.3]

SECTION 9: SERP FEATURE TARGETS
─────────────────────────────────
[Featured snippet instructions if applicable, from Step 7]
[AI Overview optimization notes]

SECTION 10: CHECKLIST
──────────────────────
Before sending to writer, verify:
[ ] Primary keyword confirmed with volume/KD data
[ ] Outline covers all ★★★ must-cover subtopics
[ ] Unique angle is specific and actionable (not generic)
[ ] E-E-A-T requirements specified (author, reviewer, sources)
[ ] Internal linking targets identified (both directions)
[ ] Featured snippet format specified (if applicable)
[ ] Word count guidance based on competitive analysis (not arbitrary)
```

---

## Fallbacks (When Semrush MCP Unavailable)

| Step | Alternative | Quality |
|------|------------|---------|
| Keyword metrics | WebSearch for "[keyword] search volume" or use free tools | Approximate only |
| Secondary keywords | WebSearch autocomplete, PAA expansion | Good for questions, weak for volume data |
| SERP analysis | WebSearch for primary keyword | Full quality for live SERP features |
| Competitor deep dive | WebFetch on top results from WebSearch | Full quality |
| Internal linking | WebSearch `site:<domain> [topic]` | Full quality |

The brief can be generated without Semrush — the competitor content analysis (Steps 2-5) is the most valuable part and runs entirely on WebFetch.

---

## Notes & Lessons Learned

1. **The unique angle is the brief's most important section.** A brief without a unique angle produces me-too content that Google's March 2026 core update penalizes. Every brief must answer: "Why should this page exist when 10 others already cover this topic?"
2. **Word count is a competitive benchmark, not a target.** Never specify a minimum word count without competitive data. Ahrefs found 53.4% of AI Overview citations go to pages under 1,000 words — correlation between word count and AI citation position is 0.04 (essentially zero).
3. **Pre-finding sources saves the writer hours.** The #1 complaint from health content writers is spending hours finding medical citations. Pre-identify 5-8 authoritative sources with URLs.
4. **Chunk-level optimization is the new page-level optimization.** AI systems extract individual sections, not whole pages. Each H2 section must stand alone as a complete, useful answer.
5. **Answer-first beats narrative suspense.** The old practice of building to a conclusion actively harms AI citation rates. Lead with the answer, then support it.
