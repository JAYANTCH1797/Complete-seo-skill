# On-Page Optimization Reference

> This is the full 14-category scored rubric. It is loaded two ways: by the `seo-audit` skill (`skills/seo-audit/SKILL.md`), which routes here once the pre-analysis intake is done and the scoring mode is chosen, and directly by the `seo-suite` router for on-page requests — in which case run Step 0 (intake) and the mode selection from this file before scoring. Read it top-to-bottom before scoring; score every category against the keyword, intent, and page type captured in intake.

## When to Use This Reference

Load this when the user asks to:
- Audit on-page SEO for one or more URLs (full scored audit)
- Audit a draft before publishing (Google Doc, Markdown, or pasted content — see Draft-Mode Scoring)
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

## STEP 0 — Pre-Analysis Intake (do this BEFORE scoring)

> **Never analyse content without context.** A page can only be scored against the query it is meant to win and the page type it is meant to be. Auditing without this produces confident-but-wrong findings — most commonly, scoring a page well on every tag while missing that the whole page is pointed at the wrong intent.

**This is a soft gate.** Ask the questions below first. If the user answers, use their answers. If the user does not answer, or says "just audit it," **proceed anyway** — infer each unknown from the slug, H1, and body, **state every assumption explicitly at the top of the audit**, and flag that the score is provisional on those assumptions being correct.

Ask these before beginning:

1. **Primary keyword** — what single query should this page rank for? (If they give several, ask which is *primary*; the rest are secondary.)
2. **Search intent** — what does someone searching that query want? Map to one:
   | Intent | Looks like | Page should be |
   |---|---|---|
   | Informational / educational | "anovulation symptoms", "what is PdG" | Blog / explainer |
   | Commercial investigation | "best fertility monitor", "inito vs mira" | Comparison / listicle |
   | Review | "inito review", "inito fertility monitor review" | Review (ideally with first-hand use) |
   | Transactional | "buy inito", "inito price" | Product / PDP |
   | Navigational | "inito login", "inito app" | Brand utility page |
3. **Branded or non-branded?** — does the keyword contain the brand?
   - Non-branded → brand must NOT be in slug or lead the title.
   - Branded → brand belongs in slug and title.
4. **Page type as built** — is this a blog, comparison, review, or product page? (So Step 1 can check it matches the intent above.)
5. **Secondary keywords** — any others to cover? Do they share intent with the primary? (Mixed intent across "primary" keywords is itself a finding.)
6. **Live URL or draft?** — is there a published/staging URL, or is this a draft (Doc/Markdown/pasted)? This selects the scoring mode (see below).
7. *(Health/YMYL only)* **Domain & feasibility** — which domain is this publishing on, and what is its realistic KD ceiling? On-page perfection on a keyword above the domain's ceiling will not rank. If the keyword's KD materially exceeds the known ceiling, flag it as a feasibility issue before optimizing (see Category 1 note on feasibility).

Record the answers (or the inferred assumptions) in the audit header. Everything downstream is scored against them.

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

### Category Weights (14 categories, 100 points)

| # | Category | Weight | Focus |
|---|---|---|---|
| 0 | Intent Alignment | /6 | Page type matches keyword intent; slug/title/H1 point at the same query |
| 1 | URL Slug | /5 | Structure, length, keyword presence |
| 2 | Title Tag | /10 | Length, keyword position, differentiation |
| 3 | Meta Description | /10 | Length, CTA, keyword, click-worthiness |
| 4 | H1 | /5 | Uniqueness, keyword placement, scope |
| 5 | Heading Architecture | /8 | Hierarchy, nesting, heading pollution |
| 6 | Keyword & Semantic Coverage | /7 | 5 core placements + entity coverage |
| 7 | Schema Markup | /6 | Required + conditional types, validation |
| 8 | OG & Social Tags | /5 | Open Graph, Twitter card, image sizing |
| 9 | Linking (Internal + External) | /10 | Outbound, inbound, citations, anchors |
| 10 | Media Optimization | /8 | Alt text, formats, sizing, lazy loading |
| 11 | Content Structure & UX | /7 | Key takeaways, ToC, FAQ, tables, layout |
| 12 | E-E-A-T Signals | /8 | Author, credentials, medical review, trust |
| 13 | Technical Crawlability | /5 | Robots, canonical, mobile, sitemap |
| | **Total** | **/100** | |

> **Rebalancing note (v2):** Intent Alignment (/6) was added as a new scored category because intent mismatch is consistently the single highest-impact on-page finding, yet in v1 it lived outside the 100-point system. To keep the total at 100, 4 points were taken from Schema Markup (10→6) and 2 from Technical Crawlability (7→5) — the two most mechanical, lowest-ranking-leverage categories. Schema and basic crawlability are easy to fix and rarely the reason a correctly-targeted page fails to rank; intent is. The new distribution puts points where ranking outcomes actually move.

### How to Score Each Category

Each category has specific checks below. Score using judgment across these levels:

| Level | Points | Criteria |
|---|---|---|
| Full marks | Weight | All checks pass, no issues |
| Minor deductions | Weight × 0.75 | 1–2 small deviations (e.g., slightly short meta, one missing alt) |
| Moderate deductions | Weight × 0.50 | Meaningful gap (e.g., title too short, key schema missing) |
| Major deductions | Weight × 0.25 | Category mostly failing (e.g., no alt text on any image) |
| Zero | 0 | Category completely absent or broken |

Round each category score to the nearest integer. Sum all categories for the overall score.

---

## Data Collection (live-URL mode)

> Skip this in draft mode — there is no rendered HTML to extract. Use the Draft-Mode Scoring Protocol below instead.

Before scoring a live or staging URL, extract all on-page elements. Use **two methods** to capture everything:

### 1. Raw HTML Extraction (for `<head>` elements)

Use `curl` or Bash to fetch raw HTML and parse (WebFetch frequently strips `<head>` — do not rely on it for meta/OG/schema):
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

## Draft-Mode Scoring Protocol

> Use this when there is **no live or staging URL** — the input is a Google Doc, Markdown file, or pasted content. The HTML doesn't exist yet, so the categories that score rendered HTML cannot be evaluated. Do not guess at them and do not invent scores for them — mark them **N/A** and normalize.

**Categories assessable from a draft (score these):**
0 Intent Alignment · 1 URL Slug* · 2 Title Tag* · 3 Meta Description* · 4 H1 · 5 Heading Architecture · 6 Keyword & Semantic Coverage · 9 Linking (content/anchor side only) · 11 Content Structure & UX · 12 E-E-A-T Signals (as written)

\* Slug/title/meta are scored against the **proposed/intended** values if the draft specifies them. **If the draft does not specify one, score that category 0, list it as unset in the findings, and supply the recommended value verbatim in the fixes section.** Do not score an inferred or hypothetical value — inferring is what makes two audits of the same draft disagree.

**Categories NOT assessable from a draft (mark N/A):**
7 Schema Markup · 8 OG & Social Tags · 10 Media Optimization · 13 Technical Crawlability · and the HTML-implementation half of 9 Linking (whether links resolve, canonical of targets).

**Normalization (required — do not report a raw sum as /100):**

```
Assessable weight = sum of weights of scored categories only
Normalized score   = (sum of scored points ÷ assessable weight) × 100
```

**Assessable weight is 71**, using the standard convention below. Category 9 is split: half its weight (5 of 10) is the content/anchor side you can score from a draft, half is link resolution you cannot.

| Scored | 0 Intent 6 · 1 Slug 5 · 2 Title 10 · 3 Meta 10 · 4 H1 5 · 5 Headings 8 · 6 Keyword 7 · 9 Linking 5 (half) · 11 Structure 7 · 12 E-E-A-T 8 | **71** |
|---|---|---|
| N/A | 7 Schema 6 · 8 OG 5 · 9 Linking 5 (half) · 10 Media 8 · 13 Technical 5 | 29 |

State it explicitly, e.g.: *"Scored 55 / 71 assessable points → normalized 77/100 (B-). Five HTML-dependent categories were N/A in draft mode; re-audit the live URL to score them."*

**Always close a draft audit** with the build-time checklist: the N/A categories become the post-publish to-do list (add schema, OG tags, alt text + next-gen formats, verify canonical/robots), followed by a full re-audit of the live URL.

---

## Category 0: Intent Alignment (/6)

> The most important question in on-page SEO: **is this the right type of page, pointed at the right query, consistently?** A page can score 90 on every tag and still fail to rank because it answers the wrong intent. This category captures that — and it is also a **score cap**: see below.

- [ ] **Page type matches keyword intent** — review keyword → review page; comparison keyword → comparison page; informational keyword → blog/explainer; transactional → product page. (Map per Step 0.)
- [ ] **Slug, title tag, and H1 all point at the same query** — they must not each chase a different keyword. (Common failure: H1 is review-framed while slug/title are explainer-framed, or vice versa.)
- [ ] **No self-defeating page type** — e.g. a brand reviewing its own product on its own domain for a "[brand] review" query ranks poorly; a product/PDP targeting a non-branded educational query is an intent mismatch. Flag these — they are strategy problems, not tag fixes.
- [ ] **Branded/non-branded handling is correct** — brand in slug/title only for branded queries.
- [ ] **Secondary keywords share intent with the primary** — a "primary" set that mixes informational + transactional intent cannot be served well by one page.

**Scoring guidance:**
- 6: Page type, slug, title, and H1 all align to one clear intent; branded/non-branded handled correctly.
- 4–5: Aligned but with a minor inconsistency (e.g., title leans slightly explainer while page is a review).
- 2–3: Real mismatch — slug/title and H1 chase different intents, or page type is a weak fit for the query.
- 0–1: Page type is wrong for the intent (e.g., explainer page targeting a review query; self-reviewing-own-product for a "[brand] review" query).

> **⚠️ Intent is also a score CAP.** If Category 0 scores **0–1 (fundamental mismatch)**, the **final reported /100 score cannot exceed 70**, regardless of how strong the other categories are. A beautifully optimized page aimed at the wrong intent does not deserve a B+.
>
> **Apply the cap last, to the /100 figure.** In live-URL mode that is the summed total. In draft mode it is the score *after* normalization — never cap the raw point sum, which is out of the assessable weight (71), not out of 100. State the cap in the audit even when it is non-binding, e.g. *"Intent scored 1 → cap applies; normalized score 34 is already below 70, so the cap does not change the result."*

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

> **Feasibility note (health/YMYL):** Before optimizing, sanity-check the keyword's difficulty against the publishing domain's realistic ceiling. On-page work cannot overcome a domain that can't rank the term — e.g. a subdomain with a low authority ceiling targeting a high-KD keyword. If the keyword is materially above the ceiling, surface it as a feasibility finding (consider a longer-tail variant, a different domain, or a third-party host) rather than spending on-page effort that can't convert.

---

## Category 2: Title Tag (/10)

- [ ] **50–60 characters** — avoids SERP truncation. Under 40 chars wastes SERP real estate.
- [ ] **Primary keyword in first 30 characters** — leads with the query, not the brand
- [ ] **Differentiation signal** — modifier that distinguishes from competitors: year, angle, number, format hint (e.g., "Chart", "Guide", "Explained")
- [ ] **Closely mirrors H1 in meaning** — doesn't need to be identical, shouldn't contradict. Ideally uses a keyword variant to capture both forms.
- [ ] **Single intent** — the title must not chase two intents at once (e.g., "[Brand] Review → How It Works" merges a review query and an explainer query; pick one). Cross-check against Category 0.
- [ ] **Brand at end for non-branded pages** — "— Inito" or "| Inito" suffix is fine (pick one format site-wide); never leads
- [ ] **Natural phrasing** — not keyword-stuffed. "HCG Levels Twins" fails; "hCG Levels for Twins" passes.

> Google rewrites 61.6% of title tags. It rewrites more when the title is too long, keyword-stuffed, or mismatched to content. A clear, accurate title reduces rewrites significantly.

**Scoring guidance:**
- 10: 50–60 chars, keyword-front, differentiation signal, single intent, natural phrasing
- 7–8: Good but minor issue (slightly short, brand format inconsistent)
- 4–6: Meaningful problem (under 40 chars, keyword-stuffed, two intents merged, or misleading)
- 0–3: Missing, severely truncated, or contradicts content

---

## Category 3: Meta Description (/10)

- [ ] **Core message in first 105 characters** — safe zone for mobile and AI citation snippets
- [ ] **Full message 145–160 characters** — under 130 wastes SERP space; over 160 gets truncated
- [ ] **Primary keyword present** — naturally, not repeated multiple times
- [ ] **One secondary keyword** — if it fits naturally
- [ ] **Matches the page's intent** — a review page's description should read as a review, not an explainer. Cross-check against Category 0.
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
- 10: 145–160 chars, keyword present, intent-matched, CTA, specific, no filler
- 7–8: Good but slightly short (130–144) or slightly generic
- 4–6: Under 120 chars, or keyword stuffed, or intent-mismatched, or pure data with no CTA
- 0–3: Missing, under 100 chars, or misleading

---

## Category 4: H1 (/5)

- [ ] **Exactly one H1 per page** — no duplicates, no missing H1
- [ ] **Primary keyword within the first 4 words**
- [ ] **Matches the page's content scope** — the H1 is a contract with the reader
- [ ] **Consistent with slug and title intent** — all three point at the same query (Category 0)
- [ ] **Not identical to title tag** — H1 has no character constraint, so use a variant or expand. Different keyword forms in title vs H1 capture more queries.

---

## Category 5: Heading Architecture (/8)

- [ ] **H2s for major subtopics** — each should work as a standalone search query
- [ ] **H3s nest under H2s** — never skip levels (H2 → H4)
- [ ] **Primary keyword in at least one H2** — exact or close variant. (Note: *at least one*, not every — repeating the keyword across many H2s reads as stuffing and is penalized below.)
- [ ] **Secondary keywords in H2s where natural**
- [ ] **Descriptive, not clever** — headings are signals, not copywriting
- [ ] **No CTA/UI text as headings** — "Was this article helpful?", "Subscribe", "Take quiz", "Follow us", "Sign Up for Our Newsletter", related article titles, and footer sections should NOT be H2/H3 tags. Use `<div>`, `<span>`, or `<p>` instead.
- [ ] **No sentence-headings** — "Here are some of the potential causes for clear sperm:" is a paragraph, not a heading
- [ ] **No trailing punctuation on headings** — drop terminal periods; question marks are fine where the heading is a genuine question
- [ ] **No numbered prefixes baked into heading text** — "1. Not enough lubrication" should be a list item, not an H3

```
❌ "Ok, so what is anovulation?"  →  ✅ "What Is Anovulation?"
❌ "But first…"                   →  ✅ "How Does Ovulation Work?"
❌ "Let's talk treatment"         →  ✅ "Anovulation Treatment Options"
❌ "Here are some causes:"        →  ✅ (use a <p> tag, not a heading)
```

**Scoring guidance:**
- 8: Clean hierarchy, no pollution, keyword in ≥1 H2 (not stuffed), proper nesting
- 6: Good content headings but some template/CTA pollution, or keyword absent from all H2s, or keyword stuffed across many
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

> **Review & comparison pages have different table-stakes entities.** For a "[brand] review" or "[brand] vs [competitor]" query, the expected-entity set must include **named competitors** (the alternatives the reader is cross-shopping), **price / cost**, and **direct-comparison points** (what each option does or tracks). A review page that never names a competitor looks incomplete to Google for that intent — exactly as an anovulation page with no mention of PCOS would. Build the entity checklist from the *review/comparison* SERP, not a generic topic list. See the Review-Page note below.

Use Semrush if available:
```
keyword_research(keyword="[primary keyword]", type="phrase_related") → semantic term list
```

**Coverage check:**
- [ ] Each expected entity appears at least once — naturally, not stuffed
- [ ] Entities appear in context — because the content covers them, not because they're inserted
- [ ] Key entities appear in H2/H3 headings where they represent genuine subtopics

**Scoring guidance:**
- 7: All 5 core placements + 80%+ entity coverage (incl. competitors/price for review-comparison pages)
- 5: 4/5 placements + decent entity coverage
- 3: Keyword present but poorly placed; major entity gaps
- 0–1: Primary keyword missing from core locations

---

## Category 7: Schema Markup (/6)

### Required

- [ ] **`Article` or `BlogPosting`** — `headline`, `author`, `datePublished`, `dateModified`, `image`, `publisher`
- [ ] **`BreadcrumbList`** — navigation path (Home > Category > Article)

### Conditional

| Schema | When | Notes |
|---|---|---|
| `FAQPage` | **Detect and flag — do not recommend adding it.** | Rich-result eligibility was restricted to a narrow set of domain types in 2023 and keeps shifting; for most sites it earns nothing. Never deduct points for its absence. If it is already present, verify current eligibility and check the *body* HTML — on Elementor sites it is auto-generated inside accordion widgets, not in `<head>`. |
| `MedicalWebPage` | YMYL health content | `medicalSpecialty`, `reviewedBy`, `audience`. Strongly recommended for clinical/symptom content. Missing this on health content is a meaningful gap. |
| `Review` / `itemReviewed` | Review pages | For genuine first-party reviews: `itemReviewed`, `author`, `reviewRating`. Note Google restricts self-serving review markup — cleaner on a third-party domain than on the brand's own site. |
| `Person` (author) | Named author | `jobTitle`, `name`, `sameAs` → LinkedIn or institutional profile |
| `VideoObject` | Video embedded | Required for video SERP feature eligibility. Include transcript/summary nearby. |

> ⚠️ `HowTo` schema was deprecated by Google in 2023. Do not implement. If found on existing pages, flag for removal — it's dead JSON-LD bloat. (Platform schema support shifts over time; re-verify current SERP-feature eligibility rather than treating any single fact here as permanent.)

### Validation

- [ ] **Google Rich Results Test** — zero errors
- [ ] **Schema.org validator** — syntactically correct
- [ ] **No deprecated schema types present** — specifically check for `HowTo` and `HowToStep`

**Scoring guidance:**
- 6: All required + all applicable conditional schemas, no deprecated types, validated
- 4–5: Required schemas present, one conditional missing (e.g., MedicalWebPage on health content)
- 2–3: Required schemas present but `MedicalWebPage` missing on YMYL content, or a deprecated type (`HowTo`) present
- 0–1: Required schemas missing (no Article/BlogPosting or no BreadcrumbList)

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
- [ ] **Citations are independent, not the same 1–2 sources reused** — distinct authorities strengthen E-E-A-T more than repeat links to one study
- [ ] **Links support specific claims** — placed on or next to the claim they validate
- [ ] **No broken outbound links** — dead links are a negative trust signal

**Scoring guidance:**
- 10: 3–5+ contextual internal links with descriptive anchors, 5+ quality independent external citations, no broken links
- 7–8: Good link count but some generic anchors or fewer than 5 external citations
- 4–6: Minimal internal links or external citations below 3
- 0–3: No contextual internal links or no external citations

> **Draft mode:** score only the content/anchor side (link presence, anchor descriptiveness, citation count and independence). Whether links resolve and point at canonical destinations is N/A until the live URL exists.

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

> **Draft mode:** N/A. A draft's image captions are not alt attributes and filenames/formats aren't set. Spec the alt text + format requirements as a build-time task instead.

---

## Category 11: Content Structure & UX (/7)

> This category assesses how well the page structures its content for both readers and search engines, beyond just headings and keywords.

- [ ] **Key Takeaways / Summary box** — at the top of the article, gives readers (and AI) the core answer quickly
- [ ] **Table of Contents** — present on articles over 1,500 words, with anchor links to sections
- [ ] **FAQ section** — genuine Q&A section at the bottom (with accordion widget for FAQPage schema eligibility)
- [ ] **Data tables** — used where comparative or numeric data exists (strong for featured snippets). **For review/comparison pages a comparison table is effectively mandatory** — it is the format the SERP rewards and the cleanest path to a featured snippet.
- [ ] **Visual aids** — infographics, charts, or diagrams that break up text walls
- [ ] **Logical flow** — content progresses in a topic-appropriate order. For explainers: definition → causes → diagnosis → treatment. **For reviews: what it is → who it's for / why it matters → how it works → first-hand experience → pros & cons → comparison → cost → verdict.**
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
- [ ] **First-hand experience signals** — for review/experience content, demonstrated real use (the "Experience" in E-E-A-T). Headings and copy that show genuine first-hand use carry extra weight on review pages — do not strip them to insert a keyword.
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

## Category 13: Technical Crawlability (/5)

> Full technical audit → load `references/technical-seo.md`. These are page-level items most likely to suppress a specific URL.

- [ ] **`index, follow` robots meta** — not accidentally noindexed. Permissive snippet settings preferred: `max-snippet:-1, max-video-preview:-1, max-image-preview:large`
- [ ] **Canonical tag** — self-referencing, no mismatches, no conflicts with HTTP header
- [ ] **No canonical pointing to redirect or 404**
- [ ] **Mobile rendering** — content renders correctly on 375px viewport
- [ ] **Sitemap inclusion** — verify after publishing (usually automatic via CMS)
- [ ] **Reachable within 3 clicks** — not an orphan page
- [ ] **Hreflang tags** — present if content exists in multiple languages/regions

**Scoring guidance:**
- 5: All checks pass, permissive robots directives, self-referencing canonical
- 4: Minor issue (e.g., missing hreflang on multi-language site)
- 2–3: Canonical mismatch or restrictive robots settings
- 0: Noindexed accidentally, or canonical points to 404

> **Draft mode:** N/A. Robots, canonical, mobile rendering, and sitemap inclusion don't exist until the page is built. Move to the build-time checklist.

---

## Review & Comparison Pages — Quick Reference

> Review ("[brand] review") and comparison ("[brand] vs [competitor]", "best X") queries behave differently from informational queries. When Step 0 identifies one of these intents, apply these on top of the standard checks:

- **Entity table-stakes (Cat 6):** named competitors, price/cost, and direct comparison points are required entities, not optional. Build the checklist from the review/comparison SERP.
- **Comparison table (Cat 11):** effectively mandatory. It's the snippet-winning format for this intent.
- **First-hand experience (Cat 12):** the "Experience" signal is weighted more heavily here. Preserve experience-demonstrating headings and copy; don't sacrifice them for a keyword that's already placed elsewhere.
- **Hosting / self-review caution (Cat 0):** a brand reviewing its own product on its own domain ranks poorly for "[brand] review" and triggers self-serving `Review` markup restrictions. A credible third-party domain is usually the stronger play and sidesteps both the authority ceiling and the self-review penalty — when that's the case, the on-page work applies to the third-party page.
- **Honest cons:** genuinely stated tradeoffs (not immediately walked back) read as more trustworthy and align with Google's review-content guidance. Soft, rescued-on-the-spot cons weaken a review.

---

## Audit Output Format

When auditing a single URL or draft:

```
## On-Page Audit: [URL or "Draft — <title>"]
**Mode:** live URL / draft
**Primary keyword:** [keyword]
**Search intent:** informational / commercial / review / transactional / navigational
**Keyword type:** branded / non-branded
**Page type as built:** blog / comparison / review / product
**Assumptions (if intake unanswered):** [list any inferred values]
**Date:** [date]
**Overall Score:** XX/100 (Grade)   [note any intent cap applied]
[Draft mode: "Scored XX / YY assessable points → normalized ZZ/100. N HTML-dependent categories N/A."]

---

### Score Breakdown
| # | Category | Score | Weight | Key Finding |
|---|---|---|---|---|
| 0 | Intent Alignment | X | /6 | [one-line finding] |
| 1 | URL Slug | X | /5 | [one-line finding] |
| 2 | Title Tag | X | /10 | [one-line finding] |
| 3 | Meta Description | X | /10 | [one-line finding] |
| 4 | H1 | X | /5 | [one-line finding] |
| 5 | Heading Architecture | X | /8 | [one-line finding] |
| 6 | Keyword & Semantic Coverage | X | /7 | [one-line finding] |
| 7 | Schema Markup | X | /6 | [one-line finding] |
| 8 | OG & Social Tags | X | /5 | [one-line finding] |
| 9 | Linking | X | /10 | [one-line finding] |
| 10 | Media Optimization | X | /8 | [one-line finding] |
| 11 | Content Structure | X | /7 | [one-line finding] |
| 12 | E-E-A-T Signals | X | /8 | [one-line finding] |
| 13 | Technical Crawlability | X | /5 | [one-line finding] |
| | **TOTAL** | **XX** | **/100** | |

[If draft: show assessable subtotal and normalized score; list N/A categories.]
[If intent cap applied: "Intent Alignment scored 0–1 → total capped at 70."]

---

### Detailed Findings

#### Intent Alignment
| Check | Status | Note |
|---|---|---|
| Page type matches intent | ✓/✗ | |
| Slug/title/H1 same query | ✓/✗ | |
| No self-defeating page type | ✓/✗ | |
| Branded/non-branded correct | ✓/✗ | |

#### Tag Placement
| Element | Status | Current | Recommended |
|---|---|---|---|
| URL slug | ✓/✗ | /current/ | /suggested/ |
| Title tag | ✓/✗ | "Current" (XX chars) | "Suggested" (XX chars) |
| Meta description | ✓/✗ | "Current…" (XX chars) | "Suggested…" (XX chars) |
| H1 | ✓/✗ | "Current" | "Suggested" |
| Keyword in first 100w | ✓/✗ | | |
| Keyword in ≥1 H2 | ✓/✗ | | |
| Keyword in image alt | ✓/✗/N/A | | |

#### Heading Architecture
[H1 → H2 → H3 tree with issues flagged]

#### Entity Coverage
| Entity | Present? |
|---|---|
| [entity] | ✓/✗ |
[Review/comparison pages: include competitors, price, comparison points]

#### Schema
| Type | Status | Notes |
|---|---|---|
| Article/BlogPosting | ✓/✗/N/A | N/A in draft mode |
| BreadcrumbList | ✓/✗/N/A | |
| FAQPage | ✓/✗/N/A | Verify current eligibility; check Elementor accordions |
| MedicalWebPage | ✓/✗/N/A | Required for YMYL health content |
| Review | ✓/✗/N/A | Review pages; self-serving markup restricted |
| HowTo (deprecated) | Present?/Absent | Flag for removal if present |

#### OG & Social Tags
[N/A in draft mode]

#### Linking
| Direction | Count | Status |
|---|---|---|
| Contextual internal | X | ✓/✗ (need Y more) |
| Inbound internal | X | ✓/✗ (queue Z pages) |
| External citations | X | ✓/✗ (independent?) |
| Broken links | X | ✓/✗/N/A |

#### Media
[N/A in draft mode — list as build-time task]

#### Content Structure
| Element | Present? |
|---|---|
| Key Takeaways box | ✓/✗ |
| Table of Contents | ✓/✗ |
| FAQ accordion section | ✓/✗ |
| Data / comparison tables | ✓/✗/N/A |
| Visual aids (infographics) | ✓/✗ |

#### E-E-A-T Signals
| Signal | Status | Detail |
|---|---|---|
| Named author | ✓/✗ | [name, credentials] |
| First-hand experience | ✓/✗ | |
| Medical reviewer | ✓/✗ | [name, credentials] |
| Published date | ✓/✗ | [date] |
| Updated date | ✓/✗ | [date] |
| Trust badge | ✓/✗ | |

### Priority Fixes
1. [P0 — Highest impact] — [specific action]
2. [P1] — [specific action]
3. [P2] — [specific action]
...

### Build-Time Checklist (draft mode only)
- [ ] Schema: [types to add]
- [ ] OG & Twitter tags
- [ ] Image alt text + next-gen formats
- [ ] Canonical + robots verification
- [ ] Re-audit live URL for the N/A categories
```

When auditing **multiple URLs**, use the comparison table format:

```
| Category (/weight) | URL 1 | URL 2 | URL 3 | ... |
|---|:---:|:---:|:---:|:---:|
| Intent Alignment (/6) | X | X | X | ... |
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
| Intake unanswered | Soft gate — infer primary keyword/intent/page type from slug, H1, body; state assumptions in header; mark score provisional. Do not refuse. |
| No live/staging URL (draft) | Use Draft-Mode Scoring Protocol — mark HTML-dependent categories N/A and normalize against assessable weight. |
| URL returns 404 | Can't audit — ask for correct URL or staging URL |
| Page noindexed | Flag as critical first. Audit can proceed but note it. |
| Intent mismatch detected | Flag as P0. Score Category 0 low; apply the ≤70 cap if mismatch is fundamental. |
| Keyword KD above domain ceiling | Surface as a feasibility finding before optimizing (longer-tail variant, different domain, or third-party host). |
| Semrush unavailable | Entity coverage is estimated from manual SERP analysis |
| Page requires login | Ask for rendered HTML or staging URL |
| WebFetch strips `<head>` tags | Use `curl` via Bash to fetch raw HTML for meta/OG/schema data |
| FAQ schema not found in `<head>` | Check body HTML for inline JSON-LD inside Elementor accordion widgets |
| Deprecated schema found (HowTo) | Flag for removal — dead since 2023 |
