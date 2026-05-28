# On-Page Optimization Reference

---
name: on-page-optimization
description: >
  Weighted on-page SEO audit and optimization for a page.
  13 scored categories (100 points total) covering URL slug, title tag, meta description,
  H1, heading architecture, keyword & semantic coverage, schema markup, OG & social tags,
  linking, media optimization, content structure, E-E-A-T signals, and technical crawlability.
  Each category has granular pass/fail checks AND a numeric score.
  Can be used standalone for auditing, or as Step 5 in the content pipeline
  (after content-evaluation.md has passed).
tools: [WebFetch, Semrush MCP (keyword_research, organic_research), Playwright, Bash (curl for raw HTML)]
---

## When to Use This Reference

Load this when the user asks to:
- Audit on-page SEO for one or more URLs (full scored audit)
- Optimize tags/metadata for an existing page
- Fix on-page SEO issues flagged by an audit tool
- Review HTML structure before publishing (after content is finalized)
- Improve click-through rate from SERP
- Score or grade a page's on-page health

When used as Step 5 in the SEO content pipeline, it assumes:
- Primary keyword is confirmed
- Content has passed evaluation (content-evaluation.md) — subtopics covered, depth competitive, GEO optimized
- The task here is packaging: are the HTML elements correct?

> If content hasn't been evaluated yet, load `references/content-evaluation.md` first.

---

## Scoring System

### Grade Scale

| Score | Grade | Meaning |
|---|---|---|
| 90–100 | A | Excellent — minor polish only |
| 80–89 | B+ / B | Good — a few targeted fixes needed |
| 70–79 | B- / C+ | Average — multiple meaningful gaps |
| 60–69 | C / C- | Below average — significant rework |
| < 60 | D / F | Poor — foundational issues |

### Category Weights (13 categories, 100 points)

| # | Category | Weight | Focus |
|---|---|---|---|
| 1 | URL Slug | /5 | Structure, length, keyword presence |
| 2 | Title Tag | /10 | Length, keyword position, differentiation |
| 3 | Meta Description | /10 | Length, CTA, keyword, click-worthiness |
| 4 | H1 | /5 | Uniqueness, keyword placement, scope |
| 5 | Heading Architecture | /8 | Hierarchy, nesting, heading pollution |
| 6 | Keyword & Semantic Coverage | /7 | 5 core placements + entity coverage |
| 7 | Schema Markup | /10 | Required + conditional types, validation |
| 8 | OG & Social Tags | /5 | Open Graph, Twitter card, image sizing |
| 9 | Linking (Internal + External) | /10 | Outbound, inbound, citations, anchors |
| 10 | Media Optimization | /8 | Alt text, formats, sizing, lazy loading |
| 11 | Content Structure & UX | /7 | Key takeaways, ToC, FAQ, tables, layout |
| 12 | E-E-A-T Signals | /8 | Author, credentials, medical review, trust |
| 13 | Technical Crawlability | /7 | Robots, canonical, mobile, sitemap |
| | **Total** | **/100** | |

### How to Score Each Category

Each category has specific checks below. Score using judgment across these levels:

| Level | Points | Criteria |
|---|---|---|
| Full marks | Weight | All checks pass, no issues |
| Minor deductions | Weight × 0.75 | 1–2 small deviations (e.g., slightly short meta, one missing alt) |
| Moderate deductions | Weight × 0.50 | Meaningful gap (e.g., title too short, key schema missing) |
| Major deductions | Weight × 0.25 | Category mostly failing (e.g., no alt text on any image) |
| Zero | 0 | Category completely absent or broken |

Round each category score to the nearest integer. Sum all 13 for the overall score.

---

## Data Collection

Before scoring, extract all on-page elements. Use **two methods** to capture everything:

### 1. Raw HTML Extraction (for `<head>` elements)

Use `curl` or Bash to fetch raw HTML and parse:
- Title tag (exact text + character count)
- Meta description (exact text + character count)
- Canonical URL
- Robots meta tag
- All OG tags (og:title, og:description, og:image, og:type, og:url, og:image:width, og:image:height)
- All Twitter card tags (twitter:card, twitter:title, twitter:description, twitter:image)
- All JSON-LD schema types (search for `"@type"` patterns in full HTML)
- Elementor accordion widgets (search for `elementor-widget-accordion` — FAQ schema is often injected inline inside accordion widgets, not in `<head>`)

### 2. Content Extraction (for body elements)

Use WebFetch or HTML parsing for:
- H1, H2, H3 tags (full list in order)
- Word count
- Internal and external link counts
- Image alt text audit
- Author, reviewer, dates
- Content structure elements (Key Takeaways, ToC, FAQ sections, tables)

---

## Pre-Optimization: Confirm the Keyword

**Ask:** "What is the primary keyword this page should rank for?"

| Scenario | Action |
|---|---|
| User provides primary keyword | Proceed |
| User unsure | Infer from URL slug and H1. State assumption. |
| User provides secondary keywords too | Document them. Check they share intent with the primary. |

Also confirm: **Is this a branded or non-branded keyword?**

| Type | Example | Implication |
|---|---|---|
| Non-branded | "anovulation symptoms" | Blog/educational content. Brand name should NOT be in the slug or lead the title tag. |
| Branded | "Inito vs Mira" | Comparison/product page. Brand name belongs in slug and title. |

If the wrong page type is targeting the keyword (e.g., product page targeting a non-branded educational query), flag it — that's an intent mismatch, not an on-page fix.

---

## Category 1: URL Slug (/5)

- [ ] **3–5 words maximum** — every word earns its place
- [ ] **Primary keyword present** — exact match or close variant
- [ ] **No filler** — remove "everything-you-need-to-know", dates, tracking strings, numbers
- [ ] **Hyphens only** — no underscores, camelCase, or encoded characters
- [ ] **Lowercase** — consistent, no mixed case
- [ ] **No brand name in non-branded page slugs**

```
❌ /anovulation-everything-you-need-to-know-about-the-1-cause-of-infertility/
✅ /anovulation-symptoms-causes-treatment/
```

> Shorter slugs get higher CTR and are easier for AI systems to parse. Google truncates long slugs in SERPs.

---

## Category 2: Title Tag (/10)

- [ ] **50–60 characters** — avoids SERP truncation. Under 40 chars wastes SERP real estate.
- [ ] **Primary keyword in first 30 characters** — leads with the query, not the brand
- [ ] **Differentiation signal** — modifier that distinguishes from competitors: year, angle, number, format hint (e.g., "Chart", "Guide", "Explained")
- [ ] **Closely mirrors H1 in meaning** — doesn't need to be identical, shouldn't contradict. Ideally uses a keyword variant to capture both forms.
- [ ] **Brand at end for non-branded pages** — "— Inito" or "| Inito" suffix is fine (pick one format site-wide); never leads
- [ ] **Natural phrasing** — not keyword-stuffed. "HCG Levels Twins" fails; "hCG Levels for Twins" passes.

> Google rewrites 61.6% of title tags. It rewrites more when the title is too long, keyword-stuffed, or mismatched to content. A clear, accurate title reduces rewrites significantly.

**Scoring guidance:**
- 10: 50–60 chars, keyword-front, differentiation signal, natural phrasing
- 7–8: Good but minor issue (slightly short, brand format inconsistent)
- 4–6: Meaningful problem (under 40 chars, keyword-stuffed, or misleading)
- 0–3: Missing, severely truncated, or contradicts content

---

## Category 3: Meta Description (/10)

- [ ] **Core message in first 105 characters** — safe zone for mobile and AI citation snippets
- [ ] **Full message 145–160 characters** — under 130 wastes SERP space; over 160 gets truncated
- [ ] **Primary keyword present** — naturally, not repeated multiple times
- [ ] **One secondary keyword** — if it fits naturally
- [ ] **Active voice, verb-driven CTA** — "Learn the 4 symptoms", "Find out if you're ovulating"
- [ ] **Specific** — tells the reader exactly what they'll get. Data + CTA beats data alone.
- [ ] **No filler phrases** — remove "Read on to find out", "Click here", "This guide covers"
- [ ] **No leading ellipsis or hedging** — "... Technically yes" reads poorly in SERPs

```
❌ "Explore this 101 guide on anovulation to get all your infertility-related answers."
✅ "Anovulation stops egg release and causes ~30% of female infertility. Learn the symptoms, 
    diagnosis steps, and treatment options."
```

> Google uses meta descriptions ~37% of the time. Even when overridden, a good description signals relevance and improves CTR when shown.

**Scoring guidance:**
- 10: 145–160 chars, keyword present, CTA, specific, no filler
- 7–8: Good but slightly short (130–144) or slightly generic
- 4–6: Under 120 chars, or keyword stuffed, or pure data with no CTA
- 0–3: Missing, under 100 chars, or misleading

---

## Category 4: H1 (/5)

- [ ] **Exactly one H1 per page** — no duplicates, no missing H1
- [ ] **Primary keyword within the first 4 words**
- [ ] **Matches the page's content scope** — the H1 is a contract with the reader
- [ ] **Not identical to title tag** — H1 has no character constraint, so use a variant or expand. Different keyword forms in title vs H1 capture more queries.

---

## Category 5: Heading Architecture (/8)

- [ ] **H2s for major subtopics** — each should work as a standalone search query
- [ ] **H3s nest under H2s** — never skip levels (H2 → H4)
- [ ] **Primary keyword in at least one H2** — exact or close variant
- [ ] **Secondary keywords in H2s where natural**
- [ ] **Descriptive, not clever** — headings are signals, not copywriting
- [ ] **No CTA/UI text as headings** — "Was this article helpful?", "Subscribe", "Take quiz", "Follow us", "Sign Up for Our Newsletter", related article titles, and footer sections should NOT be H2/H3 tags. Use `<div>`, `<span>`, or `<p>` instead.
- [ ] **No sentence-headings** — "Here are some of the potential causes for clear sperm:" is a paragraph, not a heading
- [ ] **No numbered prefixes baked into heading text** — "1. Not enough lubrication" should be a list item, not an H3

```
❌ "Ok, so what is anovulation?"  →  ✅ "What Is Anovulation?"
❌ "But first…"                   →  ✅ "How Does Ovulation Work?"
❌ "Let's talk treatment"         →  ✅ "Anovulation Treatment Options"
❌ "Here are some causes:"        →  ✅ (use a <p> tag, not a heading)
```

**Scoring guidance:**
- 8: Clean hierarchy, no pollution, keywords in H2s, proper nesting
- 6: Good content headings but some template/CTA pollution
- 4: Multiple CTA headings polluting structure, or broken nesting
- 0–2: No heading structure, or headings contradict content

---

## Category 6: Keyword & Semantic Coverage (/7)

### 6.1 Keyword Placement (5 Core Locations)

- [ ] **URL slug** — primary keyword present
- [ ] **H1** — primary keyword in first 4 words
- [ ] **First 100 words of body copy** — stated explicitly, not buried under intro fluff
- [ ] **At least one H2** — primary keyword or close variant
- [ ] **At least one image alt text** — primary keyword appears naturally

Secondary keyword placement:
- [ ] Each secondary keyword appears at least once in body copy
- [ ] At least 2 secondary keywords appear in H2s
- [ ] Meta description includes one secondary keyword

> Keyword density is obsolete. These placement checks replace it entirely. Natural frequency from covering the topic well is sufficient.

### 6.2 Semantic Entity Coverage

> Google evaluates whether content covers the entities it expects for a topic. A page about "anovulation" that never mentions PCOS, LH, or progesterone looks incomplete.

**Identify expected entities:**
- **PAA + Related Searches** on Google — entities appearing consistently are table stakes
- **Semrush Keyword Magic Tool** — related terms and questions
- **Top 3 competitor pages** — terms, conditions, processes, named concepts they cover

Build a checklist of 10–15 expected entities.

```
# Example: "anovulation"
Expected: PCOS, LH surge, FSH, progesterone, ovarian reserve,
menstrual cycle, corpus luteum, follicle, hypothalamus, pituitary gland,
irregular periods, anovulatory cycle, ovulation induction, clomiphene
```

Use Semrush if available:
```
keyword_research(keyword="[primary keyword]", type="phrase_related") → semantic term list
```

**Coverage check:**
- [ ] Each expected entity appears at least once — naturally, not stuffed
- [ ] Entities appear in context — because the content covers them, not because they're inserted
- [ ] Key entities appear in H2/H3 headings where they represent genuine subtopics

**Scoring guidance:**
- 7: All 5 core placements + 80%+ entity coverage
- 5: 4/5 placements + decent entity coverage
- 3: Keyword present but poorly placed; major entity gaps
- 0–1: Primary keyword missing from core locations

---

## Category 7: Schema Markup (/10)

### Required

- [ ] **`Article` or `BlogPosting`** — `headline`, `author`, `datePublished`, `dateModified`, `image`, `publisher`
- [ ] **`BreadcrumbList`** — navigation path (Home > Category > Article)

### Conditional

| Schema | When | Notes |
|---|---|---|
| `FAQPage` | Page has a genuine Q&A accordion section | Restricted to health/gov domains (Aug 2023). Applicable for health brands. Note: on Elementor sites, FAQ schema is auto-generated inside accordion widgets — check the body HTML, not just `<head>`. |
| `MedicalWebPage` | YMYL health content | `medicalSpecialty`, `reviewedBy`, `audience`. Strongly recommended for clinical/symptom content. Missing this on health content is a meaningful gap. |
| `Person` (author) | Named author | `jobTitle`, `name`, `sameAs` → LinkedIn or institutional profile |
| `VideoObject` | Video embedded | Required for video SERP feature eligibility. Include transcript/summary nearby. |

> ⚠️ `HowTo` schema was deprecated by Google in September 2023. Do not implement. If found on existing pages, flag for removal — it's dead JSON-LD bloat.

### Validation

- [ ] **Google Rich Results Test** — zero errors
- [ ] **Schema.org validator** — syntactically correct
- [ ] **No deprecated schema types present** — specifically check for `HowTo` and `HowToStep`

**Scoring guidance:**
- 10: All required + all applicable conditional schemas, no deprecated types, validated
- 7–8: Required schemas present, one conditional missing (e.g., MedicalWebPage on health content)
- 4–6: Required schemas present but FAQPage missing despite FAQ content, or deprecated HowTo present
- 0–3: Required schemas missing (no Article/BlogPosting or no BreadcrumbList)

---

## Category 8: OG & Social Tags (/5)

- [ ] **`og:title`** — present, matches or closely mirrors title tag
- [ ] **`og:description`** — present, matches or closely mirrors meta description
- [ ] **`og:image`** — present, ideally 1200×630px for optimal social sharing
- [ ] **`og:type`** — set to `article` for blog posts
- [ ] **`og:url`** — present, matches canonical URL
- [ ] **`og:locale`** and **`og:site_name`** — present
- [ ] **`twitter:card`** — set to `summary_large_image`
- [ ] **`twitter:title`**, **`twitter:description`**, **`twitter:image`** — all present
- [ ] **Image dimensions appropriate** — 1200×630 ideal. Under 800px wide is undersized; over 1920px is oversized.
- [ ] **Image format consistency** — all social images should use same format (WebP preferred) across the site

**Scoring guidance:**
- 5: All OG + Twitter tags present, image correctly sized
- 3–4: All tags present but image undersized/oversized
- 1–2: Tags partially present (e.g., missing twitter:image)
- 0: No social tags at all

---

## Category 9: Linking — Internal + External (/10)

### 9.1 Outbound Internal Links (From This Page)

- [ ] **3–5 contextual internal links** to related cluster content (within body copy, not nav/footer)
- [ ] **Descriptive anchor text** — describes the destination page

```
❌ "Click here to learn more."
✅ "Learn more about the LH surge and ovulation timing."
```

- [ ] **Links to pillar and sibling cluster pages** — cluster page links to pillar; pillar links to clusters
- [ ] **No links to 404 pages or redirect URLs** — link to canonical destination directly

### 9.2 Inbound Internal Links (Pre-Publish Queue)

Before publishing, queue edits to existing pages:

- [ ] **3–5 existing pages** that mention the keyword or cover related subtopics should link to this page
- [ ] **Anchor text variety** — don't use identical anchors across all linking pages
- [ ] **Queue edits to go live alongside the new page**

### 9.3 External Outbound Links (Citations)

- [ ] **Credible, high-authority destinations** — .gov, .edu, peer-reviewed journals, recognized medical sources (NCBI, PubMed, Mayo Clinic, NHS)
- [ ] **Minimum 5 external citations** for YMYL/health content — more is better for E-E-A-T
- [ ] **Links support specific claims** — placed on or next to the claim they validate
- [ ] **No broken outbound links** — dead links are a negative trust signal

**Scoring guidance:**
- 10: 3–5+ contextual internal links with descriptive anchors, 5+ quality external citations, no broken links
- 7–8: Good link count but some generic anchors or fewer than 5 external citations
- 4–6: Minimal internal links or external citations below 3
- 0–3: No contextual internal links or no external citations

---

## Category 10: Media Optimization (/8)

### Images

- [ ] **Descriptive filename** — hyphen-separated, keyword-relevant (`anovulation-symptoms-infographic.webp`)
- [ ] **Alt text on every meaningful image** — 125 chars or fewer. Describes the image. No "image of…" prefix. Empty `alt=""` on content images is a failure.
- [ ] **Primary keyword in at least one alt** — naturally
- [ ] **Next-gen format** — WebP or AVIF. Compressed JPEG/PNG as fallback. Inconsistent formats (some .jpg, some .webp) should be standardized.
- [ ] **Lazy loading** — `loading="lazy"` on images below the fold
- [ ] **Sized correctly** — source dimensions match display. No 2000px served at 800px.

### Video (if applicable)

- [ ] **`VideoObject` schema** (see Category 7)
- [ ] **Transcript or summary text** near the video for crawlability
- [ ] **Target keyword in video title and description** if hosted on YouTube

**Scoring guidance:**
- 8: All images have descriptive alt text, correct format, correct sizing
- 6: Most images have alt text, minor format/sizing issues
- 3–4: Many images missing alt text, or mix of formats
- 0–2: Majority of images have `alt=""` empty, or filename-only alt text

---

## Category 11: Content Structure & UX (/7)

> This category assesses how well the page structures its content for both readers and search engines, beyond just headings and keywords.

- [ ] **Key Takeaways / Summary box** — at the top of the article, gives readers (and AI) the core answer quickly
- [ ] **Table of Contents** — present on articles over 1,500 words, with anchor links to sections
- [ ] **FAQ section** — genuine Q&A section at the bottom (with accordion widget for FAQPage schema eligibility)
- [ ] **Data tables** — used where comparative or numeric data exists (strong for featured snippets)
- [ ] **Visual aids** — infographics, charts, or diagrams that break up text walls
- [ ] **Logical flow** — content progresses from definition → causes → diagnosis → treatment (or equivalent topic-appropriate flow)
- [ ] **Conclusion / summary section** — wraps up the article, reinforces key points

**Scoring guidance:**
- 7: Key Takeaways + ToC + FAQ + data tables/visuals where appropriate + logical flow
- 5: Most structural elements present, one missing
- 3: Basic structure only (no ToC, no Key Takeaways, or no FAQ)
- 0–1: Wall of text with no structural aids

---

## Category 12: E-E-A-T Signals (/8)

> Google's E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) is especially critical for YMYL health content.

- [ ] **Named author** with visible byline — not "Admin" or "Staff"
- [ ] **Author credentials** — role, qualifications displayed (e.g., "RN, BSN", "Women's Health Writer")
- [ ] **Medical reviewer** — named with credentials (e.g., "Dr. X, MBBS") for health content
- [ ] **Medical review badge / trust statement** — "Our content is medically reviewed by experts" or equivalent
- [ ] **Published date** — visible to readers
- [ ] **Last updated date** — visible and recent (within 12 months for health content)
- [ ] **Author bio / profile link** — links to author page or professional profile
- [ ] **Engagement signals** — helpful vote widget, comments, social sharing

**Scoring guidance:**
- 8: Named author + credentials + medical reviewer + dates + trust badge
- 6: Author + reviewer present but missing credentials or outdated dates
- 3–4: Generic author ("Admin") or no medical review on health content
- 0–2: No author attribution, no dates, no trust signals

---

## Category 13: Technical Crawlability (/7)

> Full technical audit → load `references/technical-seo.md`. These are page-level items most likely to suppress a specific URL.

- [ ] **`index, follow` robots meta** — not accidentally noindexed. Permissive snippet settings preferred: `max-snippet:-1, max-video-preview:-1, max-image-preview:large`
- [ ] **Canonical tag** — self-referencing, no mismatches, no conflicts with HTTP header
- [ ] **No canonical pointing to redirect or 404**
- [ ] **Mobile rendering** — content renders correctly on 375px viewport
- [ ] **Sitemap inclusion** — verify after publishing (usually automatic via CMS)
- [ ] **Reachable within 3 clicks** — not an orphan page
- [ ] **Hreflang tags** — present if content exists in multiple languages/regions

**Scoring guidance:**
- 7: All checks pass, permissive robots directives, self-referencing canonical
- 5: Minor issue (e.g., missing hreflang on multi-language site)
- 2–3: Canonical mismatch or restrictive robots settings
- 0: Noindexed accidentally, or canonical points to 404

---

## Audit Output Format

When auditing a single URL:

```
## On-Page Audit: [URL]
**Primary keyword:** [keyword]
**Keyword type:** branded / non-branded
**Date:** [date]
**Overall Score:** XX/100 (Grade)

---

### Score Breakdown
| # | Category | Score | Weight | Key Finding |
|---|---|---|---|---|
| 1 | URL Slug | X | /5 | [one-line finding] |
| 2 | Title Tag | X | /10 | [one-line finding] |
| 3 | Meta Description | X | /10 | [one-line finding] |
| 4 | H1 | X | /5 | [one-line finding] |
| 5 | Heading Architecture | X | /8 | [one-line finding] |
| 6 | Keyword & Semantic Coverage | X | /7 | [one-line finding] |
| 7 | Schema Markup | X | /10 | [one-line finding] |
| 8 | OG & Social Tags | X | /5 | [one-line finding] |
| 9 | Linking | X | /10 | [one-line finding] |
| 10 | Media Optimization | X | /8 | [one-line finding] |
| 11 | Content Structure | X | /7 | [one-line finding] |
| 12 | E-E-A-T Signals | X | /8 | [one-line finding] |
| 13 | Technical Crawlability | X | /7 | [one-line finding] |
| | **TOTAL** | **XX** | **/100** | |

---

### Detailed Findings

#### Tag Placement
| Element | Status | Current | Recommended |
|---|---|---|---|
| URL slug | ✓/✗ | /current/ | /suggested/ |
| Title tag | ✓/✗ | "Current" (XX chars) | "Suggested" (XX chars) |
| Meta description | ✓/✗ | "Current…" (XX chars) | "Suggested…" (XX chars) |
| H1 | ✓/✗ | "Current" | "Suggested" |
| Keyword in first 100w | ✓/✗ | | |
| Keyword in ≥1 H2 | ✓/✗ | | |
| Keyword in image alt | ✓/✗ | | |

#### Heading Architecture
[H1 → H2 → H3 tree with issues flagged]

#### Entity Coverage
| Entity | Present? |
|---|---|
| [entity] | ✓/✗ |

#### Schema
| Type | Status | Notes |
|---|---|---|
| Article/BlogPosting | ✓/✗ | |
| BreadcrumbList | ✓/✗ | |
| FAQPage | ✓/✗/N/A | Check inside Elementor accordion widgets |
| MedicalWebPage | ✓/✗/N/A | Required for YMYL health content |
| HowTo (deprecated) | Present?/Absent | Flag for removal if present |
| [other conditional] | ✓/✗/N/A | |

#### OG & Social Tags
| Tag | Status | Value |
|---|---|---|
| og:title | ✓/✗ | "…" |
| og:description | ✓/✗ | "…" |
| og:image | ✓/✗ | URL (WxH) |
| twitter:card | ✓/✗ | summary_large_image |
| twitter:image | ✓/✗ | URL |

#### Linking
| Direction | Count | Status |
|---|---|---|
| Contextual internal | X | ✓/✗ (need Y more) |
| Inbound internal | X | ✓/✗ (queue Z pages) |
| External citations | X | ✓/✗ |
| Broken links | X | ✓/✗ |

#### Media
| Check | Status |
|---|---|
| Alt text coverage | X/Y images have descriptive alt |
| Next-gen formats | ✓/✗ |
| Lazy loading | ✓/✗ |
| Sizing correct | ✓/✗ |

#### Content Structure
| Element | Present? |
|---|---|
| Key Takeaways box | ✓/✗ |
| Table of Contents | ✓/✗ |
| FAQ accordion section | ✓/✗ |
| Data tables | ✓/✗/N/A |
| Visual aids (infographics) | ✓/✗ |

#### E-E-A-T Signals
| Signal | Status | Detail |
|---|---|---|
| Named author | ✓/✗ | [name, credentials] |
| Medical reviewer | ✓/✗ | [name, credentials] |
| Published date | ✓/✗ | [date] |
| Updated date | ✓/✗ | [date] |
| Trust badge | ✓/✗ | |

### Priority Fixes
1. [P0 — Highest impact] — [specific action]
2. [P1] — [specific action]
3. [P2] — [specific action]
...
```

When auditing **multiple URLs**, use the comparison table format:

```
| Category (/weight) | URL 1 | URL 2 | URL 3 | ... |
|---|:---:|:---:|:---:|:---:|
| URL Slug (/5) | X | X | X | ... |
| Title Tag (/10) | X | X | X | ... |
| ... | ... | ... | ... | ... |
| **TOTAL** | **XX/100** | **XX/100** | **XX/100** | ... |
| **Grade** | **X** | **X** | **X** | ... |
```

Then list per-page findings and priority fixes below the table.

---

## Error Handling

| Scenario | Action |
|---|---|
| URL returns 404 | Can't audit — ask for correct URL or staging URL |
| Page noindexed | Flag as critical first. Audit can proceed but note it. |
| Semrush unavailable | Entity coverage is estimated from manual SERP analysis |
| Page requires login | Ask for rendered HTML or staging URL |
| WebFetch strips `<head>` tags | Use `curl` via Bash to fetch raw HTML for meta/OG/schema data |
| FAQ schema not found in `<head>` | Check body HTML for inline JSON-LD inside Elementor accordion widgets |
| Deprecated schema found (HowTo) | Flag for removal — dead since September 2023 |
