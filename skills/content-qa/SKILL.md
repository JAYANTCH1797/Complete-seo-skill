---
name: content-qa
description: >-
  Browser-automated QA test of a published blog post or content page. Use this skill whenever
  the user wants to test, QA, verify, smoke-test, or "check it actually works" for a live or
  staging content URL — including checking whether the content renders without JavaScript,
  whether it looks right on mobile, whether images and internal links actually load, whether
  schema and meta tags survived the CMS render, whether the page is a soft 404, or whether
  anything broke after a publish, migration, template change, or deploy. Trigger this even
  when the user only says "test this blog", "QA this page", "did the post publish correctly",
  "check the page on mobile", "is anything broken on this URL", "run a browser check", or
  pastes a URL right after publishing. Runs a real headless browser (Playwright MCP, falling
  back to the bundled Playwright script) and returns a pass/warn/fail report with evidence.
  This is a rendering and delivery test — for scoring on-page SEO quality, use the seo-audit skill.
user-invocable: true
argument-hint: "[url] [--mobile|--full]"
allowed-tools: Read, Grep, Glob, Bash, WebFetch
---

# Content QA — Browser Automation Test

A real-browser test of a published (or staging) content page. It answers a different question from the on-page audit: **not "is this good SEO?" but "did the page actually ship correctly?"**

Use it right after a publish, a template change, a CMS migration, or a deploy — the moments when content that scored well in the audit silently breaks in delivery.

> **Scope boundary.** This skill tests *rendering and delivery*. It does not score content quality, tags, or intent — that is the `seo-audit` skill (`../seo-audit/SKILL.md`). A page can pass every check here and still be a poor SEO page, and vice versa. Run both after a publish.

## Step 0 — Confirm the target and depth

Ask (soft gate — if unanswered, infer and state assumptions, never refuse):

1. **URL** — the live or staging page to test. Required; there is nothing to test without it.
2. **Depth** — `smoke` (render + mobile + console errors, ~1 min) or `full` (all checks below). Default to `full` unless the user asks for speed.
3. **Expected primary keyword / title** — optional, but if given, the render check verifies the rendered H1 and title still match what was published.
4. **Authenticated or preview URL?** — a Payload draft-preview URL may need a token. If the page 401/403s, say so rather than reporting a false failure.

## Step 1 — Pick the automation tool

Try in this order and **state which one ran** in the report:

| Order | Tool | When |
|---|---|---|
| 1 | **Playwright MCP** (`browser_navigate`, `browser_take_screenshot`, `browser_evaluate`, `browser_wait_for`, `browser_console_messages`, `browser_network_requests`) | Preferred. Bundled with this plugin — no local install needed. |
| 2 | `../../scripts/browser_automation.py <url> --check js_render\|mobile\|mixed_content --json` | Fallback if the MCP server isn't connected. Requires local `pip install playwright && playwright install chromium`. **Only these three checks exist in the script** — do not claim it ran others. |
| 3 | `curl` + WebFetch (requests/BS4-equivalent) | Last resort. HTML-only: no JS rendering, no mobile layout, no console/network data. **Explicitly list every browser check you skipped.** |

## Step 2 — Run the checks

Each check is pass / warn / fail with evidence (a value, a count, or a screenshot).

### A. Render parity (JS on vs. JS off)
The single highest-value check. Fetch the raw HTML (`curl`) and the rendered DOM (browser), then compare:
- **Body text length** — if the raw HTML has a fraction of the rendered text, the content is client-side rendered and at risk of partial indexing. Fail if raw text is under ~50% of rendered.
- **H1 present in raw HTML** — a JS-injected H1 is a real ranking risk.
- **Title and canonical identical in both** — a JS-rewritten canonical or title is a common CMS/template bug.
- **Internal links present in raw HTML** — links injected by JS may not pass equity reliably.

### B. Mobile rendering
Emulate a mobile viewport (375×812 or Playwright's device preset) and check:
- No horizontal scroll / content wider than the viewport
- Tap targets not overlapping; text legible without zoom
- Above-the-fold content is the article, not an interstitial or cookie wall
- Take a screenshot as evidence

### C. Soft 404 / empty render
A page can return HTTP 200 and still be empty. Fail if the rendered page shows "not found", "no results", an empty article body, or a body word count far below what was published.

### D. Console and network errors
- Console errors on load (JS exceptions that could block render)
- Failed requests (4xx/5xx) for images, CSS, JS, fonts
- **Mixed content** — any `http://` subresource on an `https://` page

### E. Images and media actually load
- Every `<img>` resolves (no 404s, no zero natural width)
- Alt attributes present on content images (report the count; the *quality* of alt text is scored by `seo-audit`)
- Lazy-loaded images below the fold do load on scroll

### F. Links resolve
- Internal links on the page return 2xx (report any 3xx chains and all 4xx/5xx)
- External citations resolve — a dead citation is an E-E-A-T liability

### G. Head survived the render
Confirm the rendered DOM still contains what the CMS was supposed to emit: title, meta description, canonical, robots, OG tags, and JSON-LD blocks. On Elementor-style builders, check the **body** for JSON-LD too — FAQ schema is injected inside accordion widgets, not `<head>`.

### H. Core Web Vitals — lab only
If the browser can measure it, capture LCP and CLS as **lab** figures and label them lab. Do not present lab numbers as the field data Google actually ranks on; note that CrUX/Search Console is the source of truth and is often unavailable for low-traffic pages. INP replaced FID in March 2024 — never report FID.

## Step 3 — Output

```markdown
## Content QA: [URL]
**Tested with:** Playwright MCP / browser_automation.py / HTML-only fallback
**Viewport(s):** desktop 1280×800, mobile 375×812
**Result:** PASS / PASS WITH WARNINGS / FAIL

| # | Check | Result | Evidence |
|---|---|---|---|
| A | Render parity (JS on/off) | ✓/⚠/✗ | raw 4,120 chars vs rendered 4,180 (99%) |
| B | Mobile rendering | ✓/⚠/✗ | no horizontal scroll; screenshot attached |
| C | Soft 404 / empty render | ✓/⚠/✗ | 1,840 words rendered |
| D | Console & network errors | ✓/⚠/✗ | 0 console errors, 1 failed request |
| E | Images load | ✓/⚠/✗ | 11/12 loaded; 1× 404 |
| F | Links resolve | ✓/⚠/✗ | 14 internal 2xx, 1 external 404 |
| G | Head survived render | ✓/⚠/✗ | title, canonical, OG, 2 JSON-LD blocks |
| H | CWV (lab) | ✓/⚠/✗ | LCP 2.1s, CLS 0.04 (lab, not field) |

### Failures — fix before this page is left live
1. [issue] → [exact fix]

### Warnings — worth fixing
1. [issue] → [exact fix]

### Skipped
- [check] — [why: tool unavailable / auth required / not applicable]
```

Lead with failures. Give the specific broken URL, selector, or asset — never "some images are broken."

## Error handling

| Situation | Action |
|---|---|
| Playwright MCP not connected | Fall back to `../../scripts/browser_automation.py`; say which tool ran. |
| Playwright not installed locally either | Drop to `curl`/WebFetch, and list every skipped browser check explicitly. |
| Page requires auth (401/403) | Report as blocked, not failed. Ask for a preview token or an authenticated staging URL. |
| Page redirects | Follow it, and report the redirect chain — a publish that lands on a redirect is itself a finding. |
| Staging blocked by robots | Expected on staging. Note it; don't score it as a crawlability failure for the production page. |
| Timeout / flaky load | Retry once. If it fails twice, report as fail with the error — a page too slow to load twice is a real user-facing problem. |

## Related

- `../seo-audit/SKILL.md` — scored 14-category on-page audit (quality, not delivery). Run this after a QA pass.
- `../../references/technical-seo.md` — site-wide technical crawl, when the problem isn't one page.
- `../../references/payload-cms.md` — publish/update the page in Payload, then QA the resulting URL.
