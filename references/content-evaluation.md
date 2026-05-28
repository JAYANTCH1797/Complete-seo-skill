# Content Evaluation Reference

---
name: content-evaluation
description: >
  Gate check: evaluate whether content is competitive enough to rank for its target keyword.
  Analyzes competitor content (subtopics, format, depth), competitor authority (backlinks, E-E-A-T),
  your content's gaps and unique value, GEO/AI extractability, and featured snippet targeting.
  Produces a pass/fail verdict with specific fixes. Load this AFTER content is written but BEFORE
  on-page optimization — if content isn't competitive, tag optimization is wasted effort.
tools: [WebFetch, Semrush MCP (keyword_research, organic_research, url_research, backlink_research), Playwright]
---

## When to Use This Reference

Load this when the user asks to:
- Evaluate if content is ready to publish / "good enough to rank"
- Compare their content against competitors for a keyword
- Check why a page isn't ranking despite good on-page tags
- Run a pre-publish content review
- Optimize content for AI search / GEO

This is Step 4 in the SEO content pipeline — after keyword selection and content writing, before on-page optimization.

---

## Pre-Evaluation: Confirm the Keyword

**Ask:** "What is the primary keyword this content should rank for?"

| Scenario | Action |
|---|---|
| User provides keyword | Proceed |
| User unsure | Infer from URL slug and H1. State assumption. If keyword looks wrong, flag it — trigger `keyword-research.md` separately |
| No content yet, just evaluating feasibility | Run Steps 1–2 only (competitor analysis + authority analysis) to assess whether the keyword is worth pursuing |

---

## Step 1: Competitor Content Analysis

> Understand what currently ranks and why. This defines the minimum bar your content must clear.

### 1.1 Fetch the SERP

Search the primary keyword. Identify the top 5 organic results (skip ads, skip non-content results like directories or aggregators).

Tools:
- **Semrush organic_research** → get the top-ranking URLs and their keyword counts
- **WebFetch** → fetch each competitor page for content analysis
- **Playwright** → render JS-heavy competitor pages if WebFetch returns thin content

### 1.2 Intent Analysis (3 Cs)

For each of the top 5 results, classify:

**Content Type** — What is the page?
- Blog post / guide
- Product page / landing page
- Tool / calculator
- Video
- Definition / encyclopedia entry

**Content Format** — How is it structured?
- How-to (step-by-step)
- Listicle (X ways, X causes)
- Comparison / vs.
- Definition + subtopics
- Data-driven / study

**Content Angle** — What perspective dominates?
- Beginner-friendly / 101
- Expert / clinical depth
- Personal experience / first-person
- Data-first / research-backed
- Problem → solution

Build a quick summary:

```
SERP INTENT PROFILE for "[keyword]":
Dominant type: [blog post / guide]
Dominant format: [listicle / how-to / definition+subtopics]
Dominant angle: [beginner / expert / data-driven]
Outliers: [any result that breaks the pattern — note if it's ranking despite a mismatch]
```

> If your content's type, format, or angle doesn't match the dominant pattern — stop. Rewrite before proceeding. No amount of optimization fixes an intent mismatch.

### 1.3 Subtopic Mapping

For each of the top 3 results, extract all H2 and H3 headings. Build a gap matrix:

| Subtopic | Comp 1 | Comp 2 | Comp 3 | Your page |
|---|---|---|---|---|
| [subtopic A] | ✓ | ✓ | ✓ | ✗ ← gap |
| [subtopic B] | ✓ | ✓ | ✗ | ✓ |
| [subtopic C] | ✗ | ✓ | ✓ | ✗ ← gap |
| [your unique section] | ✗ | ✗ | ✗ | ✓ ← differentiator |

Classification:
- **Table stakes** — covered by 2+ of the top 3. Your page MUST have these. Missing table-stakes subtopics is the most common cause of ranking ceilings.
- **Common** — covered by 1 competitor. Worth including if relevant.
- **Differentiator** — only on your page or not on any page. This is your information gain signal.

### 1.4 Content Depth Benchmark

Check word counts of the top 3 results. Compare against your content.

```
Competitor 1: ~X words
Competitor 2: ~Y words
Competitor 3: ~Z words
Average: ~A words
Your page: ~B words
Gap: ±C%
```

Your content should be within ±20% of the average. Word count is a proxy for coverage completeness, not a target. If competitors average 2,000 words and you have 800, you're likely missing subtopics — the fix is coverage, not padding.

> Being exhaustive doesn't mean being long. A 1,200-word page that covers every subtopic concisely beats a 3,000-word page that rambles.

### 1.5 PAA Mining

Expand the People Also Ask box for your primary keyword.

- [ ] Map each PAA question to your H2/H3 headings
- [ ] Any unanswered PAA question = missed entity signal
- [ ] Add unanswered questions as H3s with direct 40–60 word answers

### 1.6 SERP Features Present

| Feature | Present? | Implication for your content |
|---|---|---|
| Featured snippet (paragraph) | | Format a 40–60 word answer directly after the matching H2 |
| Featured snippet (list) | | Clean `<ul>`/`<ol>` with 5–8 items, no prose preamble |
| Featured snippet (table) | | `<table>` for comparisons or data sets |
| AI Overview | | Strong entity coverage + cited sources needed |
| Image pack | | Image filenames and alt text must be keyword-relevant |
| Video carousel | | Video embed with transcript adds SERP feature coverage |
| PAA box | | Cover questions as H3s with direct answers (see 1.5) |

---

## Step 2: Competitor Authority Analysis

> Backlinks are NOT an action item in this skill. They're context. You need to know how strong the competition is to calibrate how good your content needs to be and whether this keyword is worth pursuing at all.

### 2.1 Backlink Profiles

For the top 3 ranking pages, pull backlink data:

Tools:
- **Semrush backlink_research** → referring domains, DR, anchor text distribution
- **Semrush url_research** → page-level authority metrics

```
| Metric | Comp 1 | Comp 2 | Comp 3 | Your page |
|---|---|---|---|---|
| Referring domains | | | | |
| Domain Rating (DR) | | | | |
| Page-level backlinks | | | | |
```

### 2.2 Authority Calibration

Use backlink data to calibrate your content strategy:

| Scenario | What it means | Action |
|---|---|---|
| Competitors have strong backlinks + strong content | Hard keyword. You need exceptional content AND links. | Consider whether your DR can compete. If not, target a longer-tail variant or build links first. |
| Competitors have strong backlinks + thin content | Content opportunity. Better content can overcome a link deficit. | Invest in depth and uniqueness — this is where content quality wins. |
| Competitors have weak backlinks + strong content | Content quality is the primary ranking factor. | Match or exceed their content. Links are less critical here. |
| Competitors have weak backlinks + weak content | Low-competition keyword. | Content quality alone should be enough to rank. Quick win. |

### 2.3 E-E-A-T Competitor Signals

For each top 3 competitor, check:
- [ ] Named author with visible credentials?
- [ ] Medical/expert review byline (for YMYL)?
- [ ] Author bio page with linked profiles?
- [ ] Inline citations to authoritative sources?
- [ ] Published date and last-updated date?

If competitors consistently show strong E-E-A-T signals and your content doesn't — that's a gap that must be fixed regardless of content quality.

---

## Step 3: Your Content Assessment

### 3.1 Subtopic Coverage

Using the gap matrix from Step 1.3:

- [ ] **All table-stakes subtopics covered** — every subtopic in 2+ competitors appears in your content
- [ ] **PAA questions answered** — each mapped question has a clear answer in your content
- [ ] **No filler subtopics** — every section earns its place. Remove sections that don't serve the searcher's intent.

### 3.2 Content Depth

- [ ] **Word count within ±20% of top 3 average** — not padded, genuinely covering the topic
- [ ] **No thin sections** — each H2 section has enough substance to stand alone as a useful answer
- [ ] **Appropriate detail level** — matches the angle (beginner content shouldn't use unexplained jargon; expert content shouldn't over-explain basics)

### 3.3 Unique Value / Information Gain

> Google's patent on "Contextual Estimation of Link Information Gain" rewards content that provides genuinely new information beyond what already exists. Pure replication of competitor structure rarely breaks into top positions.

- [ ] **At least one unique section** that no top 3 competitor covers
- [ ] **At least one original element**: proprietary data, expert quote, personal experience, original framework, case study, or original visual
- [ ] **Specific over generic** — named studies, specific numbers, attributable quotes beat vague claims

```
❌ "Anovulation is a common cause of infertility."
✅ "Anovulation accounts for approximately 25–30% of infertility cases 
    in women of reproductive age (ACOG, 2022)."
```

### 3.4 E-E-A-T Signals on Your Content

- [ ] **Named author with byline and bio page** — bio includes relevant credentials
- [ ] **Medical/expert review byline (YMYL)** — qualified reviewer named with credentials
- [ ] **Every statistic has a traceable inline citation** — link on or immediately after the claim, not in a disconnected footnote
- [ ] **Minimum 3 external citations for YMYL** — PubMed, ACOG, WHO, NIH, peer-reviewed journals
- [ ] **"Last updated" date visible** — reflects actual content review
- [ ] **No stale data** — statistics reference the most recent available source

### 3.5 Readability

- [ ] **Sentence length** — average under 20 words. Break long compound sentences.
- [ ] **Passive voice** — under 15% of sentences. Active voice is clearer and more extractable.
- [ ] **Jargon check** — technical terms are defined on first use (or link to a definition page)
- [ ] **Visual breaks** — no wall of text. Images, lists, tables, or callouts every 200–300 words.
- [ ] **Grade level** — aim for 8th–10th grade reading level for consumer health content

### 3.6 Content Freshness

- [ ] **Statistics are current** — no data older than 2 years for fast-moving topics
- [ ] **Guidelines reference latest versions** — medical guidelines, Google algorithm updates, tool interfaces
- [ ] **Examples are contemporary** — nothing dated that undermines credibility

---

## Step 4: GEO / AI Extraction Optimization

> AI Overviews reduce clicks on the #1 organic position by ~34.5%. 60% of searches are zero-click. Your content needs to be extractable by AI systems — or it loses traffic even if it ranks.

### 4.1 First-Sentence Answer Rule

The sentence immediately after every H2/H3 must directly answer the question implied by that heading. No preamble.

```
❌ "Your doctor may suggest a variety of treatment options depending upon the cause."
✅ "Anovulation treatment depends on the underlying cause and typically involves 
    lifestyle changes, fertility medication, or surgery."
```

Scan every H2 and H3. If the first sentence doesn't answer the heading — rewrite it.

### 4.2 Pronoun Cleanliness

AI systems extract individual sentences out of context. Every sentence must stand alone.

- [ ] Replace ambiguous "it", "this", "they", "that", "these" with the explicit subject

```
❌ "This causes another gland to release FSH."
✅ "GnRH causes the pituitary gland to release FSH."
```

### 4.3 Self-Contained Definitions

When defining a term, include the term in the definition sentence. Don't rely on the heading.

```
❌ (under H2 "Anovulation") "It is the absence of ovulation."
✅ "Anovulation is the absence of ovulation during a menstrual cycle."
```

### 4.4 Structured Content

When comparing items, listing causes/symptoms, or describing steps — use lists or tables, not prose.

- Lists: 5–8 items. More than 8 → split into categories.
- Tables: side-by-side comparisons, data with clear rows/columns.
- Numbered lists: processes and steps only. Use `<ol>`, not `<ul>`.

### 4.5 Citable Facts

AI systems preferentially cite content with specific, attributable data points over vague claims.

- [ ] **Named sources** — "according to ACOG" beats "according to experts"
- [ ] **Specific numbers** — "25–30% of cases" beats "a significant proportion"
- [ ] **Named studies** — "a 2023 study in Fertility & Sterility" beats "research shows"
- [ ] **Dates on claims** — "(WHO, 2024)" beats "(WHO)"

---

## Step 5: Featured Snippet Targeting

Check if a featured snippet exists for your primary keyword (incognito browser).

| Snippet type | Required format | Length |
|---|---|---|
| Paragraph | Prose directly after an H2/H3 matching the query | 40–60 words |
| List (ordered) | `<ol>` with concise items, no preamble | 5–8 items |
| List (unordered) | `<ul>` with concise items | 5–8 items |
| Table | `<table>` with clear headers | 3–8 rows |

- [ ] **Snippet query identified** — may be a PAA question or phrase related to primary keyword
- [ ] **Format matches exactly** — paragraph needs prose; list needs `<ul>`/`<ol>`
- [ ] **Answer directly under the heading** — Google extracts the first eligible block after an H tag
- [ ] **No preamble** — start with the answer, not "Great question" or "There are many reasons"

---

## Evaluation Output Format

```
## Content Evaluation: [URL or draft title]
**Primary keyword:** [keyword]
**Date:** [date]

---

### SERP Intent Profile
Dominant type: [blog post / guide / ...]
Dominant format: [listicle / how-to / ...]
Dominant angle: [beginner / expert / ...]
Your content matches: ✓ / ✗ [detail if mismatch]

### Competitor Landscape
| Metric | Comp 1 | Comp 2 | Comp 3 | Your page |
|---|---|---|---|---|
| Word count | | | | |
| Referring domains | | | | |
| DR | | | | |
| Author credentials | | | | |
| Citations count | | | | |

### Authority Calibration
[One of: content opportunity / hard keyword / quality wins / quick win]
[Brief explanation of why]

### Subtopic Gap Matrix
| Subtopic | Comp 1 | Comp 2 | Comp 3 | Yours | Status |
|---|---|---|---|---|---|
| [subtopic] | ✓ | ✓ | ✓ | ✗ | GAP — table stakes |
| [subtopic] | ✓ | ✗ | ✓ | ✓ | ✓ covered |
| [unique section] | ✗ | ✗ | ✗ | ✓ | DIFFERENTIATOR |

### Content Depth
Your page: ~X words | Competitor avg: ~Y words | Gap: ±Z%

### PAA Coverage
| Question | Answered? |
|---|---|
| [question] | ✓ / ✗ |

### E-E-A-T Assessment
| Signal | Competitors | Your page | Status |
|---|---|---|---|
| Named author + bio | ✓ / ✗ | ✓ / ✗ | |
| Expert review byline | ✓ / ✗ | ✓ / ✗ | |
| Inline citations | X avg | Y | |
| Updated date visible | ✓ / ✗ | ✓ / ✗ | |

### GEO / AI Extraction Issues
[List specific sentences failing the first-sentence rule, pronoun check, or definition check]

### Featured Snippet Opportunity
Type: [paragraph / list / table / none]
Current owner: [competitor URL]
Your content formatted correctly: ✓ / ✗

---

### VERDICT

[One of:]

✅ **PASS — Content is competitive.** Proceed to on-page optimization.

⚠️ **CONDITIONAL PASS — Fix these gaps first:**
1. [specific gap + fix]
2. [specific gap + fix]
Then re-evaluate.

❌ **FAIL — Content is not competitive.**
Reason: [content gaps too large / authority gap insurmountable / intent mismatch]
Recommended action: [rewrite sections X,Y,Z / target different keyword / build links first]
```

---

## Error Handling

| Scenario | Action |
|---|---|
| URL returns 404 | Report error. Ask for correct URL or staging URL. |
| Semrush MCP unavailable | Fall back to WebFetch for competitor pages. Backlink data unavailable — note that authority calibration is estimated. |
| Competitor pages behind paywall | Use Semrush organic_research for keyword data. Note limitation in output. |
| Cannot determine SERP intent | SERP is mixed (multiple intent types ranking). Note ambiguity — user must decide which intent to target. |
| Your content is a draft (not yet published) | Skip backlink comparison for your page. Focus on content quality vs competitors. |
| Playwright unavailable | Fall back to WebFetch + requests. Note JS-rendered competitor content may be incomplete. |
