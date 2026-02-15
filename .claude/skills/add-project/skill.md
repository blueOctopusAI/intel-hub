# Add Project

Scan a project directory, auto-detect its stack and status, and add it to the project registry.

## Input

`/add-project <name|path>`

- If a path is given, scan the directory for stack detection
- If just a name, ask the user for details

## Process

### Step 1: Detect (if path provided)

Scan the directory for:
- **Stack:** Check for package.json (Node/React/Next), requirements.txt/pyproject.toml (Python), *.csproj (C#/.NET), Cargo.toml (Rust), go.mod (Go), Gemfile (Ruby)
- **GitHub:** Check `.git/config` for remote URL
- **Activity:** Check `git log -1 --format="%ci"` for last commit date

### Step 2: Gather Info

Read `config.json` for the business name and project lanes. Ask the user:
- **What:** One-line description of the project
- **Lane:** Which lane(s) from config? (show available lanes)
- **Tier:** Which tier? ACTIVE, READY, INCUBATING, SUPPORTING, DORMANT
- **Synergies:** Does this connect to any existing projects?

### Step 3: Add to Registry

Read `data/portfolio/projects.md` and add the project under the correct tier:

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

### Step 4: Update Header

Update the project count and tier counts in the projects.md header.

### Step 5: Check Synergies

Read through existing projects. If this new project has clear synergies (shared tech, shared audience, feeds into another project), note them on BOTH sides.

### Step 6: Report

Show what was added and any synergies detected.

ARGUMENTS: name_or_path
