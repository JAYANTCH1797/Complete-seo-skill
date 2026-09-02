# SEO Suite Plugin

## Structure
- `skills/` — Three skills: `seo-suite/SKILL.md` (master router — match user intent → load the right `references/*.md`), `seo-audit/SKILL.md` (scored 14-category on-page audit, live-URL + draft modes), `content-qa/SKILL.md` (browser QA of a published URL).
- `references/` — Deep knowledge files. Each is a self-contained methodology for one SEO domain.
- `scripts/` — Python CLIs (`crawl_audit.py`, `browser_automation.py`, `serp_scraper.py`, `reddit_miner.py`), all supporting `--json`. `utils.py` is a shared library, not a CLI. `semrush_api.py` is a **stub with no executable code** — never call it.
- `assets/templates/` — Output templates for reports and briefs.
- `assets/prompts/` — Reusable LLM prompts for enrichment steps.
- `config/` — User-configurable settings (competitors, API keys).
- `.mcp.json` — Bundled MCP servers: `semrush`, `ahrefs` (OAuth), `payload` (plugin user config), `playwright` (npx).

## Rules
- Always check SEO data provider MCP availability (Semrush **or** Ahrefs) before falling back to scripts. Name which provider supplied the numbers; never mix Semrush and Ahrefs metrics in one comparison.
- Use Playwright MCP for browser-level checks, then `scripts/browser_automation.py`, then requests+BS4 — and note every skipped check.
- Payload CMS writes always require explicit user confirmation with a before → after diff. Never call a Payload delete tool.
- Never reference FID — it was replaced by INP (March 2024).
- Never recommend HowTo schema (deprecated Sept 2023) or FAQ schema (restricted to gov/health Aug 2023).
- Keyword density is outdated. Use semantic coverage and topical completeness instead.
- Word count benchmarks should be competitive (vs top 3 for the keyword), not static minimums.
