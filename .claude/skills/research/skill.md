# Research Intelligence Processor

Process a link through the full intelligence pipeline. Read `config.json` at the project root for business context.

## Input

A URL to research: `/research <URL>`

## Before Starting

1. Read `config.json` to get the business name, categories, and voice settings
2. Read `data/research/intelligence-brief.md` to understand existing signals and context
3. Read `data/portfolio/projects.md` to know what projects are active

## Checkpointing

This skill uses the intake-log status as a checkpoint. Update the status after each major step so progress is visible and recoverable:

| Status | Meaning |
|--------|---------|
| `pending` | Logged but not yet started |
| `step-2/9` | Fetching content |
| `step-3/9` | Analyzing for business applicability |
| `step-4/9` | Updating knowledge base |
| `step-5/9` | Updating docs (bookmarks, brief, people) |
| `step-6/9` | Reporting to user |
| `processed` | Steps 1-7 complete |
| `actioned` | Steps 8-9 done — ideas logged |

**On failure:** The intake-log status shows exactly where it stopped. To resume, check the status and pick up from that step. Do NOT re-run completed steps.

## Pipeline

### Step 1: Log
Add to the TOP of `data/research/intake-log.md`:
```
`[YYYY-MM-DD HH:MM]` | pending | Title (@author if known) | URL
```

### Step 2: Fetch & Understand

**For tweets/X posts:**
- Use WebFetch on the URL
- If the tweet references an article, repo, or video — fetch THAT too
- If the tweet has a thread, try to get the full thread

**For articles:**
- Use WebFetch to read the full article
- Extract: thesis, key claims, methodology, data points, tools mentioned

**For videos (YouTube, X video, etc.):**
- Get title, description, duration from the page
- Mark as `pending-transcript` — the USER generates transcripts
- Create placeholder in `data/knowledge/transcripts/` with metadata

**For GitHub repos/tools:**
- Fetch README, check stars, recent activity
- Create evaluation in `data/knowledge/tools/`
- Do NOT install tools — add to user's task list

**For strategies/guides:**
- Read and extract the full methodology
- Create a file in `data/knowledge/strategies/`

**Checkpoint:** Update intake-log status to `step-2/9` before fetching. After successful fetch, update to `step-3/9`.

### Step 3: Analyze for Business Applicability

Read the business categories from `config.json` and evaluate the content through EACH lens. For every category, answer: "What does this mean for the business? What should they DO?"

If a category doesn't apply to this content, say so briefly and move on.

**Checkpoint:** After analysis, update to `step-4/9`.

### Step 4: Update Knowledge Base
- If this is a deep methodology or strategy: create a file in `data/knowledge/strategies/`
- If this is a tool evaluation: create a file in `data/knowledge/tools/`
- If it's a transcript: create placeholder in `data/knowledge/transcripts/`

**Checkpoint:** After knowledge base updates, update to `step-5/9`.

### Step 5: Update Docs
- Add to the appropriate topic section in `data/research/bookmarks.md`
- If this reveals a new signal or changes an existing one, update `data/research/intelligence-brief.md`
- If the author produces consistently valuable content, add to `data/research/people-to-watch.md`

**Checkpoint:** After docs updated, update to `step-6/9`.

### Step 6: Report
Show the user a structured summary:
```
## Research: "Title"

**Source:** domain.com | Date
**Relevance:** HIGH/MEDIUM/LOW — one sentence why

### Analysis

**[Category 1]:** What this means + what to do
**[Category 2]:** What this means + what to do
...

### Actions Added
- [ ] Specific action item (Project: which project)

### Updated Files
- file1.md (what changed)
```

### Step 7: Mark Processed
Change the intake-log entry from `pending` to `processed`.

### Step 8: Cross-Project Check
Read `data/portfolio/projects.md`. Does this research affect any active project? If yes, add a recommendation to the Recommendations table.

### Step 9: Log Ideas
If the research suggests something worth building, adopting, or offering — add it to `data/portfolio/implementation-backlog.md` with status `idea`.

**Checkpoint:** After backlog updated, change intake-log status to `actioned`.

## Content Access Workarounds

When encountering inaccessible content, use these before marking as user task:

| Content Type | Workaround |
|-------------|------------|
| X.com tweets | Syndication API: `cdn.syndication.twimg.com/tweet-result?id=<ID>&token=x` |
| PDFs | Search for web article summaries/reviews |
| JS-rendered pages | Try raw/API versions, search for content elsewhere |
| YouTube videos | Mark `pending-transcript` — user generates. Create placeholder in data/knowledge/transcripts/ |
| GitHub repos | Fetch raw README via `raw.githubusercontent.com/<owner>/<repo>/main/README.md` |

**When you can't access something:** Log it to `data/research/intelligence-brief.md` with what the content is, why it matters, what was attempted, and what user action is needed.

## Division of Labor

**Claude does:** Fetch, read, analyze, document, maintain all research files, create action items.
**User does:** Generate transcripts, install/test tools, engage on social, create published content.

## Principles

- Depth over speed — understand the content fully before analyzing
- Business lens — every insight must connect to an action
- Honest assessment — don't hype things that aren't ready
- Connect dots — link to existing signals and knowledge
- Follow the thread — if they reference something, fetch it
- Track people, not just content — add high-value producers to people-to-watch.md

ARGUMENTS: url
