# Prioritize

Manage project tiers and recommendation votes.

## Input

`/prioritize <command>`

## Commands

### Move projects between tiers
```
/prioritize <project> up          — Promote one tier
/prioritize <project> down        — Demote one tier
/prioritize <project> to ACTIVE   — Move to specific tier
```

Tiers (in order): ACTIVE > READY > INCUBATING > SUPPORTING > DORMANT

### Vote on recommendations
```
/prioritize rec <#> up      — Upvote (+1)
/prioritize rec <#> down    — Downvote (-1)
/prioritize rec <#> done    — Mark as done
/prioritize rec <#> reject  — Mark as rejected
/prioritize rec <#> defer   — Mark as deferred
```

## Implementation

1. Read `data/portfolio/projects.md`
2. Find the project or recommendation
3. Make the change
4. Save the file
5. Report what changed

## Rules

- When promoting to ACTIVE, ask what the first next action should be
- When demoting to DORMANT, ask for a reason (add to project notes)
- When marking a rec as done, update the status AND remove/update any related next actions
- Always update the "Last touched" date on affected projects
- Always update the "Last updated" date at the top of projects.md

ARGUMENTS: command
