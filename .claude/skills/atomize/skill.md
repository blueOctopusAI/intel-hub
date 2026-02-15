# Content Atomizer

Turn a blog post or long-form content into social media variations. Reads `config.json` for platforms, voice, and audience.

## Input

`/atomize <file-path-or-URL>`

The source can be:
- A markdown file path (e.g., `content/blog/my-post.md`)
- A URL to a published post

## Before Starting

1. Read `config.json` for business name, voice, audience, and platforms
2. Fetch/read the source content
3. Read `data/portfolio/content-pipeline.md` to understand existing content and avoid duplicates

## Checkpointing

Track progress through the content-pipeline.md entry status:

| Step | Checkpoint |
|------|-----------|
| 1 | Source content read and extracted |
| 2-3 | Posts generated (in memory) |
| 4 | Presented to user |
| 5 | content-pipeline.md updated |
| 6 | File saved to data/knowledge/social/ |

**On failure at step 5-6:** Posts are already generated and shown. Just re-run the file writes.

## Step 1: Read the Source

Read the full content. Extract:
- **Title** and **slug** (from frontmatter if available)
- **Key stats** (numbers, percentages, dollar amounts)
- **Opinions the author actually holds** (not generic observations)
- **Insights** the audience would find interesting
- **Anything surprising or counterintuitive**
- **Honest caveats** — what's overhyped, what's not ready

## Step 2: Generate Posts by Platform

For each platform configured in `config.json`, generate posts using the voice setting.

### X/Twitter (if configured)

**Post count:** 5-8 variations, each under 280 characters (HARD LIMIT)

**Voice calibration by config.json voice:**
- `casual` → First person, lowercase energy, opinions stated directly
- `friendly` → Warm, approachable, uses "you", asks questions
- `professional` → Clear, authoritative, data-driven
- `technical` → Precise, jargon-appropriate, practitioner-to-practitioner

**Platform rules:**
- Max 280 characters (count carefully)
- No hashtags unless they genuinely add value
- Max 1-2 posts with the source link. The rest are standalone.
- NEVER use .md filenames raw — X auto-links them. Write "the SKILL file format" instead of SKILL.md.

**Post variety requirements:**
- At least 1 post grounded in first-person experience or honest assessment
- At least 1 post that reveals something non-obvious or counterintuitive
- At least 1 post that invites the reader to DO or CHECK something
- At least 1 post with a clear verdict (works / doesn't / overhyped)

**Kill any post that:**
- Sounds like it came from a social media scheduler
- Uses "The X just Y'd" dramatic framing
- Could be posted by any generic account (not specific to what this content actually says)
- Makes claims the author can't verify

### Facebook (if configured)

**Post count:** 3-5 variations, 100-300 words each

**Voice:** Adapt from config.json but always more conversational than X. Assume the audience may not be technical. Use real-world analogies.

**Post types:**
1. **Explainer** — What the content is about in plain English
2. **Lesson** — One specific business lesson, expanded
3. **Listicle** — "3 things we learned:" with bullet points
4. **Question** — Ask something that invites comments

Always include the source link.

### LinkedIn (if configured)

**Post count:** 2-3 variations, professional tone, up to 3000 chars

**Voice:** Lead with insight, end with takeaway. More formal than X or Facebook.

### Other platforms

For any other configured platform, generate 3-5 posts adapting the voice and format to what's standard for that platform.

## Step 3: Output to User

Present content organized by platform. Include character counts for X posts. Flag any over 280.

## Step 4: Update Content Pipeline

Add entries to `data/portfolio/content-pipeline.md` for each platform:

```markdown
### [Title] — Atomized Posts
- **Stage:** Draft
- **Priority:** High
- **Source:** Atomized from [source]
- **Notes:** [N] posts generated [date]. Ready for manual posting.
```

## Step 5: Save the Posts

Write to `data/knowledge/social/<slug>-atomized.md`:

```markdown
# Social Posts: [Title]

*Atomized: [date]*
*Source: [source URL or path]*

---

## X Posts

[all X posts with character counts]

---

## Facebook Posts

[all Facebook posts]

---

## [Other Platform] Posts

[posts]
```

Create the `data/knowledge/social/` directory if it doesn't exist.

## Principles

1. **Authenticity over reach** — One genuine post beats five polished ones
2. **Platform-native voice** — X audience ≠ Facebook audience ≠ LinkedIn audience. Never cross-contaminate.
3. **Standalone value** — Each post should work without reading the original
4. **No hype** — If the content has caveats, the social posts should too
5. **Avoid .md auto-linking** — X renders SKILL.md, CLAUDE.md etc. as clickable links to random domains

ARGUMENTS: source
