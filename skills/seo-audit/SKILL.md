---
name: seo-audit
description: >-
  Weighted, scored on-page SEO audit and optimization. Use this skill whenever the user
  wants to audit, score, grade, or improve the on-page SEO of a page or draft — including
  auditing a live/staging URL, auditing a Google Doc / Markdown / pasted draft before
  publishing, optimizing tags or metadata (slug, title tag, meta description, H1, headings),
  fixing issues flagged by another SEO tool, checking content for the right search intent,
  improving SERP click-through, or reviewing HTML structure before publishing. Trigger this
  even when the user only says "audit this blog", "is this optimized", "score this page",
  "check the SEO", "review my title and meta", "will this rank", or pastes a draft and asks
  what to fix — they want this scored framework, not ad-hoc advice. Produces a 0–100 score
  across 14 weighted categories with prioritized fixes. Especially suited to health/YMYL
  content (E-E-A-T, MedicalWebPage) and review/comparison pages.
user-invocable: true
argument-hint: "[url|draft] [primary keyword]"
allowed-tools: Read, Grep, Glob, Bash, WebFetch, WebSearch
---

# SEO Audit — On-Page Optimization

A reproducible, weighted on-page SEO audit. It scores a page (or a pre-publish draft) across **14 categories totaling 100 points**, and returns prioritized fixes. The full rubric — every category's checklist and scoring guidance — lives in `../../references/on-page-optimization.md`. This file is the workflow that gets you there.

> **Do not skip the intake and do not skip reading the rubric.** The single most common failure mode is producing a confident, well-formatted audit that scores every tag correctly while missing that the whole page is pointed at the wrong search intent. The intake (Step 0) and Category 0 (Intent Alignment) exist specifically to prevent that. Read `../../references/on-page-optimization.md` in full before scoring — the per-category checks are what make two audits agree.

## Workflow

### Step 0 — Pre-analysis intake (soft gate, always first)

**Never analyse content without context.** A page can only be scored against the query it is meant to win and the page type it is meant to be. Ask the user these before scoring:

1. **Primary keyword** — the single query this page should rank for. (If they give several, ask which is primary; the rest are secondary.)
2. **Search intent** — informational / commercial investigation / review / transactional / navigational. (This determines the correct page type — see the intent→page-type table in the reference.)
3. **Branded or non-branded** — does the keyword contain the brand? (Brand belongs in slug/title only for branded queries.)
4. **Page type as built** — blog, comparison, review, or product page.
5. **Secondary keywords** — any others, and do they share intent with the primary?
6. **Live URL or draft** — published/staging URL, or a Doc/Markdown/pasted draft? **This selects the scoring mode.**
7. *(Health/YMYL only)* **Domain & KD feasibility** — which domain, and is the keyword's difficulty within that domain's realistic ceiling? On-page work can't overcome a keyword above the domain's ceiling — flag it before optimizing.

**This is a soft gate, not a hard stop.** If the user answers, use their answers. If they don't, or say "just audit it," **proceed anyway**: infer each unknown from the slug, H1, and body, state every assumption explicitly in the audit header, and mark the score provisional on those assumptions. Never refuse to audit.

If you have Semrush / SERP tools available, use intake answers to pull the competitor SERP and build the expected-entity checklist (Category 6) — especially for review/comparison intents, where named competitors and price are table-stakes entities.

### Step 1 — Pick the scoring mode

| Input | Mode | What changes |
|---|---|---|
| Live or staging URL | **Live-URL audit** | Score all 14 categories. Use `curl`/Bash for raw `<head>` (title, meta, canonical, robots, OG, JSON-LD), and WebFetch/parsing for body (headings, links, alt text, author/dates). |
| Google Doc, Markdown, or pasted content | **Draft mode** | The HTML doesn't exist yet. Score only the content-assessable categories; mark the HTML-dependent ones **N/A** and normalize. See the Draft-Mode Scoring Protocol in the reference. |

**Draft mode in brief** (full protocol + normalization formula in the reference):
- **Score:** 0 Intent · 1 Slug\* · 2 Title\* · 3 Meta\* · 4 H1 · 5 Headings · 6 Keyword/Entities · 9 Linking (content side) · 11 Structure · 12 E-E-A-T (\* against proposed values if specified).
- **Mark N/A:** 7 Schema · 8 OG/Social · 10 Media · 13 Technical · and the link-resolution half of 9.
- **Normalize:** `(scored points ÷ assessable weight) × 100`. Never report a raw sum as /100. State it, e.g. *"47/60 assessable → 78/100 (B-); 5 HTML categories N/A."*
- **Always close** with the build-time checklist (the N/A categories become the post-publish to-do list), then recommend a live-URL re-audit.

### Step 2 — Score against the rubric

Read `../../references/on-page-optimization.md` and score each applicable category. Categories and weights:

| # | Category | Wt | # | Category | Wt |
|---|---|---|---|---|---|
| 0 | Intent Alignment | /6 | 7 | Schema Markup | /6 |
| 1 | URL Slug | /5 | 8 | OG & Social Tags | /5 |
| 2 | Title Tag | /10 | 9 | Linking | /10 |
| 3 | Meta Description | /10 | 10 | Media Optimization | /8 |
| 4 | H1 | /5 | 11 | Content Structure & UX | /7 |
| 5 | Heading Architecture | /8 | 12 | E-E-A-T Signals | /8 |
| 6 | Keyword & Semantic Coverage | /7 | 13 | Technical Crawlability | /5 |

Two rules that override naive tallying:
- **Intent is a score CAP.** If Category 0 scores 0–1 (fundamental mismatch — e.g. an explainer page targeting a review query, or a brand self-reviewing its own product for a "[brand] review" query), the total **cannot exceed 70** regardless of the other categories. Apply the cap after summing and state it.
- **Review/comparison pages** get extra table-stakes checks: named competitors + price + comparison points are *required* entities (Cat 6), a comparison table is effectively mandatory (Cat 11), and first-hand "experience" signals are weighted and protected (Cat 12) — never strip an experience-demonstrating heading just to insert a keyword that's already placed elsewhere. See the "Review & Comparison Pages — Quick Reference" in the reference.

### Step 3 — Output

Use the audit output format in the reference (header block → score-breakdown table → detailed findings → prioritized fixes). Lead findings with the highest-leverage issue, which is frequently intent, not a tag. Keep fixes specific and actionable (give the recommended slug/title/meta verbatim, not "improve the title"). For draft mode, end with the build-time checklist.

## Reference files

- **`../../references/on-page-optimization.md`** — the full 14-category rubric: every checklist, scoring band, the intent→page-type map, the Draft-Mode Scoring Protocol, the review/comparison quick-reference, the complete output template, and an error-handling table. **Read this before scoring.**

> This skill ships inside the `complete-seo-skill` plugin. Load `../../references/technical-seo.md` when the task is a full technical crawl, and `../../references/content-evaluation.md` when content hasn't yet been evaluated for depth/coverage. This skill assumes content has already passed evaluation and focuses on on-page packaging + scoring. For anything outside on-page (keyword research, content gap, backlinks, SERP, competitor benchmarking), use the `seo-suite` skill's routing table.

## Notes

- **Data collection (live URL):** WebFetch often strips `<head>`; use `curl` via Bash for meta/OG/schema. FAQ schema on Elementor sites is injected *inside accordion widgets* in the body — check body HTML, not just `<head>`.
- **Platform facts drift.** Schema rich-result eligibility (FAQPage, Review) and deprecations (HowTo) change over time. The reference notes current state but says to re-verify SERP-feature eligibility rather than treat any single fact as permanent.
- **Feasibility before optimization (YMYL):** if the keyword's KD materially exceeds the publishing domain's realistic ceiling, surface that first — a longer-tail variant, a different domain, or a credible third-party host may be the real fix, not on-page tweaks.
