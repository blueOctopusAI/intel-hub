# Add Project to Registry

Scan a project directory, auto-detect its stack and status, and add it to the project registry.

## Input

`/add-project <name|path>`

- If a path is given, scan the directory for stack detection
- If just a name, ask the user for details

## Workflow

### Step 1: Scan the Directory (if path provided)

Read these files if they exist:
- `README.md` — project description
- `package.json` — name, dependencies, scripts (Node.js)
- `Cargo.toml` — Rust projects
- `requirements.txt` / `pyproject.toml` — Python
- `*.csproj` — C#/.NET
- `go.mod` — Go
- `CLAUDE.md` — existing Claude Code configuration
- `.git/config` — remote URL

Run these commands:
- `git log --oneline -5` — recent commits (activity + last touched date)
- `git remote -v` — GitHub URL
- `ls` — top-level structure

### Step 2: Ask User for Tier

Present the tier options:
- **ACTIVE** — Getting regular work this week/month
- **READY** — Could start this week with minimal setup
- **INCUBATING** — Designed but not yet built
- **SUPPORTING** — Tools and systems that serve active projects
- **DORMANT** — Paused, could be revived

Ask which tier to place the project in.

### Step 3: Auto-Detect Fields

From the scan, fill in:
- **What** — from README or infer from structure
- **Stack** — from dependencies
- **Path** — absolute path scanned
- **GitHub** — from git remote
- **Status** — infer from git log recency
- **Lane** — ask user (use lanes from `config.json` if available)
- **Last touched** — from most recent git commit date

### Step 4: Verify .gitignore Security

**This step is mandatory.** Check the project's `.gitignore`:

- [ ] `.env*` pattern present
- [ ] `*.pem`, `*.key` patterns present
- [ ] `credentials.json` pattern present
- [ ] No `.env` files already tracked (`git ls-files | grep -i env`)

If secrets are missing from `.gitignore`, add them. If `.env` files are already tracked, **warn the user** and recommend `git rm --cached`.

Never register a project without confirming secrets are excluded from git.

### Step 5: Add to Registry

Insert the new project under the correct tier in `data/portfolio/projects.md`:

```markdown
### {project-name}

- **What:** {description}
- **Stack:** {detected or provided}
- **Path:** {path if local}
- **GitHub:** {detected or provided}
- **Status:** {initial status}
- **Lane:** {selected lane}
- **Synergies:** {connections to other projects}
- **Next actions:**
  - [ ] {first action}
- **Last touched:** {today}
```

Update the "Last updated" date at the top of projects.md.

### Step 6: Check for Synergies

Read existing projects. Identify:
- Does this project use data from another project?
- Does this project feed into another project?
- Does this project share tech stack?
- Could intelligence research help this project?

If synergies found, update BOTH projects' synergy fields.

### Step 7: Report

Show what was added, synergies detected, and suggested next actions.

## Principles

1. **Auto-detect everything possible** — minimize questions to the user
2. **Always check synergies** — the registry's value is in connections
3. **Always verify secrets** — security is mandatory, not optional
4. **Follow existing format** — consistency matters

ARGUMENTS: name_or_path
