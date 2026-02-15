# Status Report

Generate a comprehensive but actionable status report. Read `config.json` for business context.

## Input

No arguments required. Optionally: `/status <project-name>` for a single-project deep dive.

## Data Sources

1. `config.json` — Business name and categories
2. `data/portfolio/projects.md` — Projects, tiers, statuses, blockers, recommendations
3. `data/research/intelligence-brief.md` — Key signals and action items
4. `data/research/intake-log.md` — Recent research activity (check for staleness)

## Full Status Output

### Project Pulse

| Project | Tier | Momentum | Blocker | Next Action |
|---------|------|----------|---------|-------------|

Momentum indicators:
- Active this week
- Touched recently
- Stale (7+ days since last activity)

### Recommended Focus

**Today:** 1-2 specific tasks with reasoning
**This week:** 3-5 tasks that compound
**Parking lot:** Important but not urgent

Priority framework:
1. Revenue-generating work and deadlines
2. Unblocking other projects (multipliers)
3. Revenue-adjacent (content, outreach)
4. Compounding work (tools, automation)
5. Portfolio polish

### Stale Items

Flag anything untouched for 7+ days:
- Projects with old "Last touched" dates
- Action items that haven't progressed
- Recommendations pending with no votes

### New Recommendations

If you spot opportunities the user hasn't considered, add 1-3 new recommendations to the Recommendations table in `data/portfolio/projects.md`.

## Single Project Deep Dive (`/status <project>`)

- Full current state
- All related action items from intelligence-brief.md
- Related bookmarks and strategy docs
- Recommended next 3 actions with reasoning

## After Reporting

Ask: "Want me to update any project statuses, or start on [recommended task]?"

ARGUMENTS: project
