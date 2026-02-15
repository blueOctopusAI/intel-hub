# Security Auditor

Evaluate security implications of tools, configurations, plugins, and the intelligence hub itself.

## Input

`/security [target]`

Targets:
- No argument: full hub audit
- A tool name: evaluate that specific tool
- A URL: assess a tool/service from its docs
- `deps`: check dependencies for vulnerabilities

## Full Hub Audit

### 1. Secrets Check
- Scan for `.env` files committed to git across the project
- Check for hardcoded API keys, tokens, passwords in source
- Verify `.gitignore` covers: `.env*`, `*.pem`, `*.key`, `credentials.json`
- Check `settings.local.json` for leaked credentials

### 2. Plugin & MCP Security
- Review installed plugins in `~/.claude/plugins/`
- Check MCP server permissions (what can they read/write?)
- For each MCP server, grep source for:
  - `exec`, `spawn`, `child_process` — shell execution
  - `writeFile`, `readFile` — file system access scope
  - `fetch`, `http` — network access
  - `process.env` — environment variable access
- Verify permission scopes are minimal

### 3. Dependency Audit
- Run `npm audit` on Node.js projects
- Check `pip audit` or safety on Python projects
- Flag outdated dependencies with known CVEs
- Review lockfile integrity
- Check if versions are pinned or using `@latest`

### 4. Configuration Review
- Is the CLAUDE.md leaking business-sensitive instructions?
- Are any scheduled tasks running with overly broad access?
- Are file permissions appropriate?

### 5. Report

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
4. What's the maintenance status? (last commit, open issues, contributor count)
5. Are there known CVEs?
6. What's the minimum viable permission set?

Rate: **SAFE** / **CAUTION** / **AVOID** with reasoning.

## New Plugin/Skill Install Audit

Run this checklist EVERY TIME a new plugin, MCP server, or skill is installed:

### Source Verification
- [ ] Verify GitHub owner/repo matches expected (not a typo-squat fork)
- [ ] Check repo stars, age, and maintenance activity
- [ ] Read the plugin metadata files

### Hook Audit
- [ ] What hooks does it register?
- [ ] Check matchers — does it hook `*` (all tools) or specific ones?
- [ ] Review every command for shell execution, auto-install scripts, file modifications, network calls

### MCP Server Audit
- [ ] Check transport type (stdio vs HTTP)
- [ ] For HTTP: verify URL is official (not a proxy)
- [ ] For stdio: review source for shell execution, file access scope, network access, env var access

### Permission Scope
- [ ] What tools/permissions does it declare?
- [ ] Does it request Bash access? With what patterns?
- [ ] Does it write to LaunchAgents/crontab? (persistence)
- [ ] Does it auto-install dependencies without consent?

### Data Flow
- [ ] Where does the plugin store data?
- [ ] Does it send data externally? (telemetry, analytics)
- [ ] Does it log tool output or conversation content?
- [ ] Could it capture secrets from files during the session?

### Verdict Format
```
## Plugin Security Audit: [name]

**Source:** github.com/owner/repo
**Version:** X.Y.Z
**Installed:** YYYY-MM-DD

### Hooks, MCP Servers, Permissions
[summary]

### Findings
| Severity | Finding | Remediation |
|----------|---------|-------------|

### Verdict: SAFE / CAUTION / BLOCK
```

## Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| **Critical** | Active exploit risk, exposed secrets | Fix immediately |
| **High** | Known CVE, excessive permissions | Fix this session |
| **Medium** | Outdated deps, broad permissions | Fix this week |
| **Low** | Best practice gaps | Note for future cleanup |

## Principles

- Cross-reference with OWASP Top 10 where applicable
- No false positives — verify each issue before reporting
- Provide remediation steps for every finding
- Minimal permissions by default — escalate only when justified

ARGUMENTS: target
