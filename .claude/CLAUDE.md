# SEO Suite Plugin — developer notes

This file loads only when the repo is opened as a project. It does **not** ship to people who install the plugin — anything installers need must live in a `skills/*/SKILL.md`.

## SEO rules

The standing SEO rules (no FID, no HowTo, no recommending FAQ schema, no keyword density, provider naming, Payload write confirmation, browser-check order) live in `skills/seo-suite/SKILL.md` → **Standing rules**, with the audit-relevant subset repeated in `skills/seo-audit/SKILL.md`. Read them before editing any reference file, and keep the two copies in step — change one, change both. Don't add a third copy here.

## Structure
- `skills/` — Three skills: `seo-suite/SKILL.md` (master router — match user intent → load the right `references/*.md`), `seo-audit/SKILL.md` (scored 14-category on-page audit, live-URL + draft modes), `content-qa/SKILL.md` (browser QA of a published URL).
- `references/` — Deep knowledge files. Each is a self-contained methodology for one SEO domain.
- `scripts/` — Python CLIs (`crawl_audit.py`, `browser_automation.py`, `serp_scraper.py`, `reddit_miner.py`), all supporting `--json`. `utils.py` is a shared library, not a CLI. `semrush_api.py` is a **stub with no executable code** — never call it.
- `assets/templates/` — Output templates for reports and briefs.
- `assets/prompts/` — Reusable LLM prompts for enrichment steps.
- `config/` — User-configurable settings (competitors, API keys).
- `.mcp.json` — Bundled MCP servers: `semrush`, `ahrefs` (OAuth), `payload` (plugin user config), `playwright` (npx).
- `evals/` — Hermetic eval suite (`evals.json` + frozen fixtures). Re-baseline when rubric weights or the draft-mode protocol change.

## When editing
- Never document a capability a script or tool doesn't have. Read the source first.
- Category weights must sum to 100; draft-mode assessable weight is 71. Update the reference, both skills, the audit template, and the README together.
- Validate before merging: `claude plugin validate --strict .claude-plugin/plugin.json` (needs Claude Code 2.x — the desktop app bundles one).
