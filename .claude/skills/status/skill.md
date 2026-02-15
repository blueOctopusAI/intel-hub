# Status Report

Generate a comprehensive but actionable status report. Read `config.json` for business context.

## Input

No arguments required. Optionally: `/status <project-name>` for a single-project deep dive.

## Data Sources

1. `config.json` — Business name and categories
2. `data/portfolio/projects.md` — Projects, tiers, statuses, blockers, recommendations
3. `data/research/intelligence-brief.md` — Key signals and action items
4. `data/research/intake-log.md` — Recent research activity (check for staleness)

## Pre-Report Check: Active Worktrees

Before generating the report, run `git worktree list` to check for active secondary sessions. If any worktrees exist besides the main one:
- Report them: "Active parallel sessions: [branch name] at [path]"
- Remind the user to merge when done

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

### Synergy Alerts

Check the synergy map in `data/portfolio/projects.md`. Flag:
- Research that applies to a tracked project
- Tools evaluated but not installed that would help active projects
- Content ideas that are ready to write (research done, just needs authoring)
- Pipeline gaps between projects

### New Recommendations

If you spot opportunities the user hasn't considered, add 1-3 NEW recommendations to the Recommendations table in `data/portfolio/projects.md`. Each needs:
- A specific, actionable suggestion
- The source (which data led you to this)
- Initial vote of +0
- Status: pending

### Stale Items

Flag anything untouched for 7+ days:
- Projects with old "Last touched" dates
- Action items that haven't progressed
- Recommendations pending with no votes

## Single Project Deep Dive (`/status <project>`)

- Full current state
- All related action items from intelligence-brief.md
- Related bookmarks and strategy docs
- Synergies and how they're performing
- Recommended next 3 actions with reasoning

## Principles

1. **Actionable over informational** — Every section should end with "do X"
2. **Honest momentum** — Don't sugarcoat stale projects
3. **Connect dots** — The value is in seeing cross-project patterns
4. **Respect user time** — Be concise. Tables over paragraphs.
5. **Decision framework** — Revenue > deadlines > unblocking > compounding

## After Reporting

Ask: "Want me to update any project statuses, or start on [recommended task]?"

ARGUMENTS: project
