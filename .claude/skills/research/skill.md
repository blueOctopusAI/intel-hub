# Research Pipeline

Process a link through the full intelligence pipeline. Read `config.json` at the project root for business context.

## Input

A URL to research: `/research <URL>`

## Before Starting

1. Read `config.json` to get the business name, categories, and voice settings
2. Read `data/research/intelligence-brief.md` to understand existing signals and context
3. Read `data/portfolio/projects.md` to know what projects are active

## Pipeline

### Step 1: Log
Add to the TOP of `data/research/intake-log.md`:
```
`[YYYY-MM-DD HH:MM]` | pending | Title (@author if known) | URL
```

### Step 2: Fetch
Use WebFetch to retrieve the content. If it references other articles, repos, or threads — fetch those too. Follow the thread.

### Step 3: Analyze
Read the business categories from `config.json` and evaluate the content through EACH lens. For every category, answer: "What does this mean for the business? What should they DO?"

If a category doesn't apply to this content, say so briefly and move on.

### Step 4: Update Knowledge Base
- If this is a deep methodology or strategy: create a file in `data/knowledge/strategies/`
- If this is a tool evaluation: create a file in `data/knowledge/tools/`
- If it's a transcript: create in `data/knowledge/transcripts/`

### Step 5: Update Docs
- Add to the appropriate topic section in `data/research/bookmarks.md`
- If this reveals a new signal or changes an existing one, update `data/research/intelligence-brief.md`
- If the author produces consistently valuable content, add to `data/research/people-to-watch.md`

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
- [ ] ...

### Updated Files
- file1.md (what changed)
- file2.md (what changed)
```

### Step 7: Mark Processed
Change the intake-log entry from `pending` to `processed`.

### Step 8: Cross-Project Check
Read `data/portfolio/projects.md`. Does this research affect any active project? If yes, add a recommendation to the Recommendations table.

### Step 9: Log Ideas
If the research suggests something worth building, adopting, or offering — add it to `data/portfolio/implementation-backlog.md` with status `idea`.

## Principles

- Depth over speed — understand the content fully before analyzing
- Business lens — every insight must connect to an action
- Honest assessment — don't hype things that aren't ready
- Connect dots — link to existing signals and knowledge
- Follow the thread — if they reference something, fetch it

ARGUMENTS: url
