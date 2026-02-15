# Security Audit

Evaluate security posture of tools, configurations, and the intelligence hub itself.

## Input

`/security [target]`

Targets:
- No argument: full hub audit
- A tool name: evaluate that specific tool
- A URL: assess a tool/service from its docs
- `deps`: check dependencies for vulnerabilities

## Full Hub Audit

### Step 1: Secrets Check
Scan the project for exposed secrets:
- `.env` files that aren't gitignored
- API keys, tokens, or credentials in tracked files
- Hardcoded secrets in scripts or config

### Step 2: File Permissions
- Is `config.json` in `.gitignore` (if it contains sensitive data)?
- Are there any files with overly broad permissions?

### Step 3: Dependency Audit
- Check `requirements.txt` for known vulnerable packages
- Check any `package.json` for vulnerable npm packages
- Flag dependencies that haven't been updated in 6+ months

### Step 4: Configuration Review
- Is the CLAUDE.md leaking business-sensitive instructions?
- Are there any MCP servers or plugins configured? Check their permissions.
- Review any scheduled tasks for overly broad access

### Step 5: Report

```markdown
## Security Audit Report

**Date:** YYYY-MM-DD
**Scope:** [what was audited]

### Findings

| # | Severity | Finding | Recommendation |
|---|----------|---------|----------------|
| 1 | HIGH/MED/LOW | Description | Fix |

### Summary
- Critical: X
- High: X
- Medium: X
- Low: X

### Recommended Actions
1. [Immediate fixes]
2. [This week]
3. [When convenient]
```

## Tool Evaluation

When evaluating a specific tool:
1. Check if it's open source (can we audit the code?)
2. What permissions does it request?
3. Does it phone home or send data externally?
4. What's the maintenance status? (last commit, open issues, bus factor)
5. Are there known CVEs?
6. What's the minimum viable permission set?

Rate the tool: SAFE / CAUTION / AVOID with reasoning.

ARGUMENTS: target
