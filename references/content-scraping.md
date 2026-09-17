# Content Scraping Reference (Secondary Research)

---
name: content-scraping
description: >
  Harvest adapters for keyword/secondary research. Reddit (PRAW if configured, else
  Apify with a comment-fallback chain), YouTube (Apify + subtitles), Instagram.
  Each adapter returns items normalized to {source, url, text, engagement}, which
  feed social-topic-mining.md Stage 2 (extract).
---

Rule: prefer the free/configured tool, fall down the chain, and if every option for a source fails, **move ahead without it** — note the skipped source.

Apify actors run via the Apify MCP: `fetch-actor-details` (get input schema) → `call-actor` (run) → `get-actor-output` (dataset).

## Reddit

**Tier 1 — PRAW (preferred if configured)**
`scripts/reddit_miner.py` — needs `config/reddit_config.json` (gitignored, not in repo). Posts + top comments, free, no Apify spend. Already in the skill.

**Tier 2 — Apify `trudax/reddit-scraper-lite`**
- Scrape posts.
- Comments: append `.json` to the post permalink and fetch Reddit's public JSON, e.g. `https://www.reddit.com/r/PCOS/comments/<id>/<slug>/.json`.
- If `.json` is blocked/rate-limited → Apify `crawlerbros/reddit-comment-scraper`.
- If that also fails → proceed with posts only.

## YouTube

**Apify `streamers/youtube-scraper`**
- Input **must** include `"downloadSubtitles": true` → analyze title + transcript, not just metadata.
- No transcript available → use title + description, flag the item as transcript-less.

## Instagram

**Apify** (hashtag/caption scraper). Captions only — strongest for content angles and audience language, weak for search volume. Optional, not default.

## Normalized output

Every adapter returns:

```json
{ "source": "reddit|youtube|instagram", "url": "...", "text": "post+comments | title+transcript | caption", "engagement": 0 }
```

Engagement is source-specific, collapsed to one number: Reddit `score + comments×3`, YouTube views (or likes), Instagram likes + comments. Hand the list to `social-topic-mining.md` Stage 2.
