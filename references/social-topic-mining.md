# Social Topic Mining Reference

---
name: social-topic-mining
description: >
  Scrape Reddit / YouTube / Instagram, extract a hierarchical topic label per item
  (L0 atomic → L1 cluster → L2 head → category), dedup and roll up by entity-role
  peeling, map the head entity into a user-provided taxonomy, and emit ranked seed
  keywords. Upstream of keyword-research.md Path A and its fan-out.
---

## When to Use
Discover what an audience actually discusses, turn it into seed keywords. Feeds `keyword-research.md` (Phase 1, Path A).

## Inputs
- **Sources**: subreddits, YouTube channels/queries, Instagram hashtags.
- **Taxonomy** (optional): user's `category → subcategory` list. If absent, cold-start mode proposes one.

## Pipeline

**1. Harvest** — one adapter per source, all normalized to `{source, url, text, engagement}`.
Reddit: post + top comments. YouTube: title + transcript. Instagram: caption.
Adapters + fallback chains: `content-scraping.md`.

**2. Extract** — one LLM call per item → the record below, schema-enforced.

**3. Roll up** — derive L1/L2 by peeling entity roles (rule below). Deterministic, no free text.

**4. Map** — match head entity (L2) to the provided taxonomy. No fit → `unmapped` bucket.

**5. Aggregate** — count each L0/L1/L2 node, weight by frequency × engagement → ranked seeds.

## Role + Peel Rule (the core)

Tag each entity with a role, then peel in fixed order: **comparator → aspect → head.** Head survives to L2.

| Entity | Role |
|---|---|
| endometriosis | head (the subject) |
| misdiagnosis | aspect |
| pcos | comparator ("as X") |

- **L0** = all entities → `endometriosis misdiagnosis as pcos` — LLM natural phrasing; the long-tail seed
- **L1** = drop comparator → `endometriosis misdiagnosis` — cluster key
- **L2** = drop aspect → `endometriosis` — head; maps to taxonomy
- **category** = taxonomy parent of head → `health condition`

Same roles → same L1/L2 keys → dedups by construction.

**Multiple co-equal heads:** emit one record per head so each maps cleanly. Don't force a single tree.

## Record Schema (enforced on the extractor)

```json
{
  "source": "reddit|youtube|instagram",
  "url": "...",
  "engagement": 0,
  "entities": [
    {"name": "endometriosis", "role": "head"},
    {"name": "misdiagnosis", "role": "aspect"},
    {"name": "pcos", "role": "comparator"}
  ],
  "l0": "endometriosis misdiagnosis as pcos",
  "l1": "endometriosis misdiagnosis",
  "l2": "endometriosis",
  "category": "health condition",
  "verbatim": "kept getting told it was just PCOS"
}
```

Roles: `head`, `aspect`, `comparator`, `other` (escape). Entities lowercase, singular — string-dedup safe.
`l1`/`l2` are derived by peeling, not emitted free-form. `l0` and `verbatim` are the keyword/voice seeds.

## Taxonomy: Input, Not Output
- **Provided** → classify head into it; unmapped heads pool for review. Default, stable.
- **Cold-start** (none provided) → cluster heads bottom-up, propose `category → subcategory`, user freezes it once, then switch to provided.

## Output
Ranked table per level. Each strong L0 = a seed keyword; L1 = a content cluster; L2 = a pillar / taxonomy node. Hand L0/L1 seeds to `keyword-research.md` fan-out for volume/KD validation.

| Level | Node | Posts | Engagement | → |
|---|---|---|---|---|
| L0 | endometriosis misdiagnosis as pcos | 14 | 3,200 | long-tail article |
| L1 | endometriosis misdiagnosis | 31 | 7,800 | cluster page |
| L2 | endometriosis | 88 | 21,000 | pillar / subcategory |
