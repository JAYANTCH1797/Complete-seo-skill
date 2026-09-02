# Complete SEO Skill

A Claude Code plugin for doing SEO work properly — scored audits, keyword research, content evaluation, and browser QA — with live data from Semrush or Ahrefs, content read and written in Payload CMS, and a real headless browser for verification.

It is opinionated on purpose. The rubrics encode *how* to judge a page, not just what to look at, so two audits of the same URL agree on the score.

**Version:** 1.2.0 · **Contents:** 3 skills · 11 reference modules · 4 bundled MCP servers · 4 Python CLIs

---

## Install

```bash
claude plugin marketplace add JAYANTCH1797/Complete-seo-skill
```

```bash
claude plugin install complete-seo-skill@complete-seo-skill
```

Or from inside a Claude Code session: `/plugin marketplace add JAYANTCH1797/Complete-seo-skill`, then `/plugin install complete-seo-skill@complete-seo-skill`.

Both names are `complete-seo-skill` — the first is the plugin, the second the marketplace.

### Setup after install

**1. Authorize your SEO data provider.** Run `/mcp` and authorize `semrush` and/or `ahrefs`. Both use OAuth and both need an active subscription. You only need one — the skills use whichever is connected.

**2. Payload CMS (optional).** Install prompts for two values. Skip both if you don't use Payload; that server shows as unconnected and nothing else breaks.

| Setting | Value |
|---|---|
| Payload CMS MCP URL | `https://your-site.com/api/mcp` |
| Payload MCP API key | Payload admin → **MCP → API Keys** |

Your Payload app needs [`@payloadcms/plugin-mcp`](https://payloadcms.com/docs/plugins/mcp) installed with the relevant collections enabled.

**3. Playwright.** Nothing to do — it runs via `npx` on first use.

---

## The three skills

### `seo-audit` — scored on-page audit

Scores a page across **14 weighted categories totaling 100 points** and returns prioritized fixes with the exact recommended values, not "improve the title."

Triggers on things like *"audit this blog"*, *"score this page"*, *"is this optimized"*, *"review my title and meta"*, *"will this rank"*, or a pasted draft.

| # | Category | Wt | # | Category | Wt |
|---|---|---|---|---|---|
| 0 | Intent Alignment | /6 | 7 | Schema Markup | /6 |
| 1 | URL Slug | /5 | 8 | OG & Social Tags | /5 |
| 2 | Title Tag | /10 | 9 | Linking | /10 |
| 3 | Meta Description | /10 | 10 | Media Optimization | /8 |
| 4 | H1 | /5 | 11 | Content Structure & UX | /7 |
| 5 | Heading Architecture | /8 | 12 | E-E-A-T Signals | /8 |
| 6 | Keyword & Semantic Coverage | /7 | 13 | Technical Crawlability | /5 |

Three things make it different from a generic audit:

- **Intent is a score cap.** Category 0 asks whether this is the right *type* of page for the query, and whether slug, title, and H1 all point at the same one. If it scores 0–1 — an explainer targeting a review query, a brand self-reviewing its own product — the total is capped at 70 no matter how clean the tags are. A well-optimized page aimed at the wrong intent doesn't deserve a B+.
- **Draft mode.** Audit a Google Doc, Markdown file, or pasted draft *before* publishing. The five HTML-dependent categories are marked N/A, the score is normalized against the assessable weight of 71, and the audit closes with a build-time checklist. No invented scores for HTML that doesn't exist yet.
- **A soft intake gate.** It asks for primary keyword, intent, branded/non-branded, and page type first — but if you say "just audit it," it infers them, states every assumption in the header, and marks the score provisional. It never refuses to audit.

### `content-qa` — browser test of a published page

A real headless browser against a live or staging URL. This is a **delivery** test, not a quality score — it answers "did the page actually ship correctly?" Run it after a publish, template change, CMS migration, or deploy.

Triggers on *"test this blog"*, *"QA this page"*, *"did the post publish correctly"*, *"check it on mobile"*, *"is anything broken"*.

Checks: JS render parity (raw HTML vs rendered DOM), mobile layout, soft 404 / empty render, console and network errors, mixed content, broken images and links, whether the head survived the CMS render, and lab-only Core Web Vitals.

Tool order, and it tells you which tier ran: Playwright MCP → `scripts/browser_automation.py` → HTML-only, with every skipped browser check listed explicitly.

### `seo-suite` — router for everything else

Matches your request to the right reference module and follows its methodology. Also the entry point for multi-area work like a full site audit.

---

## The 11 reference modules

Each is a self-contained methodology, not a checklist.

| Reference | Lines | What it does |
|---|---|---|
| `technical-seo.md` | 480 | 13-category technical audit: crawlability, indexability, redirects, internal linking, crawl budget, security, URL structure, mobile, Core Web Vitals, structured data, JS rendering, **AI crawler management**, **IndexNow** |
| `keyword-research.md` | 440 | Three phases with a mandatory research gate between seeds and validation. Sub-cluster fan-out cross-matches Claude decomposition, Semrush `phrase_questions`, and your own Google PAA data |
| `content-gap.md` | 460 | Competitor URL diffing through a 5-layer filter pipeline; Information Gain gaps |
| `content-cluster.md` | 567 | Pillar/spoke mapping, internal linking strategy, cannibalization detection, content pruning |
| `content-evaluation.md` | 404 | The gate check before on-page work: is the content actually competitive? Competitor content + authority analysis, GEO/AI extraction, featured snippet targeting |
| `on-page-optimization.md` | 703 | The full 14-category rubric behind `seo-audit` — every checklist, scoring band, the intent→page-type map, draft-mode protocol, review/comparison quick reference, output template |
| `serp-analysis.md` | 521 | SERP feature detection, AI Overview analysis, TARGET/DEFER/SKIP scorecard |
| `backlink-analysis.md` | 521 | 7-step link profile audit, brand mention auditing, AI citation tracking |
| `competitor-benchmarking.md` | 527 | 8-step benchmarking, bifurcated CTR model for AIO-present vs AIO-absent queries, AI Share of Voice |
| `content-brief.md` | 569 | 10-step brief generator with GEO optimization and chunk-level targeting |
| `payload-cms.md` | 129 | Read/write content in Payload over MCP; the draft → audit → fix → publish → QA loop |

---

## The content pipeline

The sequence the plugin is built around:

```
keyword-research  →  content-brief  →  [write]  →  content-evaluation
                                                          │
                                             gate: is it competitive?
                                                          │
                                                          ▼
                                              seo-audit (draft mode)
                                                          │
                                                   [publish in CMS]
                                                          │
                                                          ▼
                                     content-qa  →  seo-audit (live URL)
```

The gate matters. `content-evaluation` runs *before* on-page work, because perfect tags on thin content don't rank. If content fails the gate, fix the content or change the keyword — don't proceed to tag optimization.

---

## Data providers

Both Semrush and Ahrefs are declared. Skills use whichever is connected, and **must name which provider supplied the numbers in every report**. Their volume and difficulty figures are not interchangeable — never mix them in one comparison.

Preference order: Semrush MCP → Ahrefs MCP → public SERP data via WebSearch/`serp_scraper.py`, with the limitation stated in the report.

There is no working direct-API fallback. If neither provider is connected, the skills say the figures are unavailable rather than estimating them.

---

## Payload CMS: write safety

Reads are free. Writes are not, and the reference treats them that way:

- **Every `update`/`create` needs explicit confirmation** with a field-by-field before → after diff. One approval covers one write, not a batch.
- **Delete tools are never called.** If you need to delete, you get the document ID and do it in the admin panel.
- **Body content is never rewritten** — writes are confined to the SEO fields the audit actually scored.
- **Slug changes are always flagged as a redirect requirement**, and the default on a page that already ranks is not to change it.

One gotcha worth knowing: Payload **generates** its MCP tool names from your site's own collection slugs. A site with a `blog` collection gets `findBlog`, not `findPosts`. The reference teaches the `find/create/update/delete[Collection]` pattern and instructs listing the server's actual tools first — never assuming names.

---

## Scripts

Run via Bash. All CLIs support `--json`.

| Script | Status | What it does |
|---|---|---|
| `crawl_audit.py <url>` | CLI | Technical SEO spider: status codes, canonicals, robots.txt, redirects, internal links, orphan pages, sitemap validation |
| `browser_automation.py <url> --check js_render\|mobile\|mixed_content` | CLI | Playwright checks. **Three checks only** — no CWV, no soft-404, no link crawling |
| `serp_scraper.py` | CLI | SERP feature extraction |
| `reddit_miner.py` | CLI | Reddit topic and language mining for seed research |
| `utils.py` | library | Shared helpers (URL normalization, HTTP fetching, output formatting) — not a CLI |
| `semrush_api.py` | **stub** | Documents Semrush MCP tool names. **No executable code — never call it** |

`browser_automation.py` needs `pip install playwright && playwright install chromium`. The bundled Playwright MCP server needs none of that and is the preferred tier.

---

## What this plugin refuses to do

These are enforced across every reference and skill:

- **No FID.** It was replaced by INP in March 2024.
- **No HowTo schema.** Deprecated by Google in 2023 — flagged for removal where found, never recommended.
- **No recommending FAQ schema.** Rich-result eligibility was restricted to a narrow set of domain types in 2023 and keeps shifting. Detected and flagged if present; never a scoring deduction when absent.
- **No keyword density.** Semantic coverage and topical completeness instead.
- **No static word-count minimums.** Benchmarks are competitive — measured against the top 3 for the actual keyword.
- **No fabricated numbers.** If a data provider isn't connected, the report says the figure is unavailable.

---

## Repository structure

```
.
├── .claude-plugin/
│   ├── plugin.json           # Manifest: version, userConfig for Payload
│   └── marketplace.json      # Marketplace listing
├── .mcp.json                 # Bundled MCP servers
├── skills/
│   ├── seo-suite/SKILL.md    # Master router
│   ├── seo-audit/SKILL.md    # Scored on-page audit
│   └── content-qa/SKILL.md   # Browser QA
├── references/               # 11 methodology modules
├── scripts/                  # Python CLIs
├── assets/
│   ├── templates/            # Report and brief output templates
│   ├── prompts/              # Reusable LLM prompts for enrichment steps
│   └── workflow.md           # End-to-end pipeline diagram
├── config/
│   ├── competitors.json      # Your competitor domains
│   ├── semrush_config.json   # gitignored
│   └── reddit_config.json    # gitignored
└── CLAUDE.md                 # Project rules for Claude
```

### Bundled MCP servers

| Server | Transport | Auth |
|---|---|---|
| `semrush` | http → `mcp.semrush.com/claude/v1/mcp` | OAuth, needs a subscription |
| `ahrefs` | http → `api.ahrefs.com/mcp/mcp` | OAuth, needs a subscription |
| `payload` | http → your configured URL | Bearer key from plugin config |
| `playwright` | stdio, `npx @playwright/mcp@latest` | none |

---

## Configuration

`config/competitors.json` — your competitor domains, used by gap analysis and benchmarking:

```json
{ "competitors": ["competitor1.com", "competitor2.com"] }
```

API key files (`semrush_config.json`, `reddit_config.json`) are gitignored. Keys for the MCP servers are handled by Claude Code — OAuth for Semrush/Ahrefs, and the Payload key is stored in your OS keychain via plugin `userConfig`. Never paste a key into chat.

---

## Development

The rubrics are the product. When changing one:

- Category weights must still sum to **100**.
- Draft mode's assessable weight must match the categories it actually scores (currently **71** — Category 9 counts half).
- Update every place a count appears: the reference, `skills/seo-audit/SKILL.md`, `skills/seo-suite/SKILL.md`, and `assets/templates/audit_report_template.md`.
- Never claim a script does something it doesn't. Read the source before documenting it.

```bash
claude plugin validate .
```

---

## License

Not yet specified.
