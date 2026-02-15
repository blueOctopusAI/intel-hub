# Atomize

Turn a blog post or long-form content into social media variations.

## Input

`/atomize <file-path-or-URL>`

The source can be:
- A markdown file path (e.g., `content/blog/my-post.md`)
- A URL to a published post

## Before Starting

1. Read `config.json` for business name, voice, audience, and platforms
2. Fetch/read the source content
3. Read `data/portfolio/content-pipeline.md` to understand existing content and avoid duplicates

## Process

### Step 1: Extract Key Points
Pull out 8-12 distinct insights, quotes, statistics, or takeaways from the source.

### Step 2: Generate Variations

For each configured platform (from `config.json` platforms field), generate posts:

**X/Twitter (if configured):**
- 10-15 variations, each under 280 characters
- Mix of: hooks, insights, questions, hot takes, lists, quotes
- No hashtags unless they add value
- Write in the configured voice — sound like a person, not a brand

**Facebook (if configured):**
- 5-8 variations, 1-3 paragraphs each
- More conversational and story-driven than X
- Can include a call to action
- Questions that invite comments

**LinkedIn (if configured):**
- 3-5 variations, professional tone
- Lead with insight, end with takeaway
- Can be longer (up to 3000 chars)

### Step 3: Save Output

Create a file at `data/knowledge/social/<slug>-atomized.md`:

```markdown
# Atomized: "Post Title"

Source: [title](URL or path)
Generated: YYYY-MM-DD
Voice: {voice from config}

## X Posts

1. Post text here

2. Post text here

...

## Facebook Posts

1. Post text here

...
```

### Step 4: Update Content Pipeline

Add entries to `data/portfolio/content-pipeline.md` for each platform with stage "Draft".

## Principles

- Sound human — match the configured voice, not corporate speak
- Each post should stand alone (reader hasn't seen the original)
- Vary the format: questions, statements, lists, stories
- Front-load the hook — first line must grab attention
- No emojis unless the configured voice is casual and the user uses them

ARGUMENTS: source
