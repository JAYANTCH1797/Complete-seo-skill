# Payload CMS Reference

> How this plugin reads and writes content in a [Payload CMS](https://payloadcms.com/docs/plugins/mcp) instance over MCP. Load this when the content being audited, optimized, or published lives in Payload — it closes the loop between "here's the fix" and "the fix is in the CMS."

## When to Use This Reference

Load this when the user asks to:
- Pull a draft or published post out of Payload to audit it
- Apply audit fixes (slug, title, meta description, headings) back into Payload
- Check what's in the CMS — list posts, find drafts, find posts missing meta descriptions
- Run a pre-publish workflow: draft → audit → fix → publish → QA

If the content is a pasted draft or a Google Doc rather than a CMS record, skip this file — go straight to the `seo-audit` skill in draft mode.

---

## Connection

The plugin declares a `payload` MCP server in `.mcp.json`. It needs two values, prompted at install as plugin user config:

| Setting | Value | Where it comes from |
|---|---|---|
| `payload_mcp_url` | `https://your-site.com/api/mcp` | The Payload MCP plugin mounts at `/api/mcp` on your Payload app |
| `payload_api_key` | An MCP API key | Payload admin panel → **MCP → API Keys** |

Server-side, the site must have `@payloadcms/plugin-mcp` installed and the relevant collections enabled:

```javascript
import { mcpPlugin } from '@payloadcms/plugin-mcp'

export default buildConfig({
  plugins: [
    mcpPlugin({
      collections: {
        posts: { enabled: true },
      },
    }),
  ],
})
```

**If it isn't configured, the `payload` server shows as unconnected and nothing else in the plugin breaks.** Say so plainly and continue with the non-CMS workflow rather than treating it as an error.

---

## Tool naming — do not hardcode

Payload **generates** MCP tools from the site's own collection and global slugs. The pattern is:

| Pattern | Example on a site with a `posts` collection |
|---|---|
| `find[Collection]` | `findPosts` |
| `create[Collection]` | `createPosts` |
| `update[Collection]` | `updatePosts` |
| `delete[Collection]` | `deletePosts` |
| `find[Global]` / `update[Global]` | `findSiteSettings` / `updateSiteSettings` (globals support find + update only) |

**Always list the connected server's actual tools before calling anything.** A site's collection may be `blog`, `articles`, `resources`, or anything else — the tool will be named after it. Never assume `findPosts` exists. Likewise, permissions are set per key: a key may be read-only, or scoped to some collections. If a write tool isn't exposed, that is a deliberate permission, not a bug — report it and hand the user the field values to paste in manually.

Field names are equally site-specific. Read one document first to learn the schema (is the meta description `meta.description`, `seo.metaDescription`, or `excerpt`?) before writing anything.

---

## ⚠️ Write safety — mandatory

Reads (`find*`) are free. **Writes are not.**

- **Confirm before every `update` or `create`.** Show the user the exact collection, document ID/slug, and a field-by-field before → after diff. Wait for an explicit yes. One approval covers one write, not a batch.
- **Never call a `delete` tool.** If deletion is genuinely what's needed, hand the user the document ID and let them delete it in the admin panel.
- **Prefer draft over published.** If the collection has drafts enabled, write to the draft and let a human publish.
- **Don't overwrite body content.** Confine writes to the SEO fields the audit actually scored — slug, title, meta description, headings. Rewriting the article body through an API is how content gets silently lost.
- **Slug changes break URLs.** Changing a published post's slug changes its URL and drops any accumulated links and rankings. Flag it as a redirect requirement every time, and default to *not* changing the slug on a page that already ranks.

---

## Workflow: draft → audit → fix → publish → QA

This is the loop the plugin is built around. It uses the `seo-audit` skill's **draft mode** — the CMS record has no live HTML yet, so the HTML-dependent categories are N/A and the score is normalized.

**1. Pull the record.**
List the server's tools, call the site's `find[Collection]` with a filter for the draft. Use the `select` parameter to pull only what you need (title, slug, meta fields, content) — full documents are large and mostly noise.

**2. Audit it in draft mode.**
Hand the content to the `seo-audit` skill. Run Step 0 intake first: primary keyword, intent, page type. Draft mode scores intent, slug, title, meta, H1, headings, keyword/entity coverage, linking (content side), structure, and E-E-A-T; it marks schema, OG, media, and technical crawlability N/A and normalizes the total.

**3. Propose the fixes.**
Produce the exact values — the recommended slug, title tag, meta description, revised H1 — not "improve the title." Show them as a before → after table.

**4. Write back, one confirmation at a time.**
On approval, call the site's `update[Collection]` with only the changed fields. Re-read the document afterward to confirm the write landed.

**5. Publish** — human step, in the admin panel. Don't publish via MCP.

**6. QA the live URL.**
Once published, run the `content-qa` skill against the real URL: render parity, mobile, images, links, and whether the head survived the CMS render. Then re-run `seo-audit` in live-URL mode to score the five categories that were N/A in draft.

---

## Useful read patterns

| Goal | Approach |
|---|---|
| Find all drafts | `find[Collection]` filtered on the draft/status field, `select` title + slug + updatedAt |
| Find posts missing meta descriptions | `find[Collection]` with `select` on the meta fields, then filter client-side for empty/short values — cheaper and more reliable than guessing the query syntax |
| Content inventory for a cluster audit | `find[Collection]` with `select` title + slug only, paginate, then diff against the keyword map |
| Learn the schema | `find[Collection]` with limit 1, no `select` — read one full document, then use `select` for everything after |

Payload MCP requests are JSON-RPC 2.0 over HTTP. Large result sets come back as large payloads; always narrow with `select` and a limit rather than pulling a whole collection.

---

## Error handling

| Situation | Action |
|---|---|
| `payload` server unconnected | Config missing or the site doesn't run the MCP plugin. State it, then continue in draft/paste mode. Don't retry in a loop. |
| 401 / 403 | API key invalid, revoked, or lacking permission for that collection/operation. Ask the user to check **MCP → API Keys**; never ask them to paste the key into the chat. |
| Expected tool doesn't exist | The collection is named something else, or the key isn't permitted that operation. List the actual tools and work with what's there. |
| Field names don't match the audit's fields | Read one document to learn the real schema before writing. Don't invent field paths. |
| Write rejected by validation | Payload enforces its own field validation (required fields, max lengths). Report the validation error verbatim and adjust the value. |
| User asks to bulk-update many posts | Do them one at a time with per-document confirmation, or generate a CSV of recommended values for a human to apply. Don't loop writes unattended. |

---

## Related

- `../skills/seo-audit/SKILL.md` — the scored audit; draft mode is what scores a CMS record pre-publish
- `../skills/content-qa/SKILL.md` — browser QA of the published URL
- `content-evaluation.md` — run before the on-page audit if the content hasn't been checked for depth and competitiveness
