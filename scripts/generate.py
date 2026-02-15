#!/usr/bin/env python3
"""Generate all intelligence hub files from a config.json.

Reads config.json from the project root and renders:
- CLAUDE.md (project instructions for Claude Code)
- data/research/intake-log.md
- data/research/bookmarks.md
- data/research/intelligence-brief.md
- data/research/people-to-watch.md
- data/portfolio/projects.md
- data/portfolio/content-pipeline.md
- data/portfolio/implementation-backlog.md

Usage:
    python3 scripts/generate.py [--config path/to/config.json] [--output-dir path/to/output]
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def load_config(config_path: str) -> dict:
    """Load and validate config.json."""
    path = Path(config_path)
    if not path.exists():
        print(f"Error: Config file not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    with open(path) as f:
        config = json.load(f)

    required_fields = ["business_name", "industry", "categories", "voice"]
    missing = [f for f in required_fields if f not in config]
    if missing:
        print(f"Error: Missing required config fields: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    return config


def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def generate_claude_md(config: dict) -> str:
    """Generate the CLAUDE.md project instructions."""
    name = config["business_name"]
    description = config.get("description", f"A {config.get('industry_label', config['industry'])} business")
    categories = config["categories"]
    voice = config["voice"]
    audience = config.get("audience", "customers")
    bookmark_topics = config.get("bookmark_topics", categories)

    category_lines = "\n".join(f"- **{c}** — Evaluate through this lens" for c in categories)
    topic_list = ", ".join(bookmark_topics)

    return f"""# CLAUDE.md

This file provides guidance to Claude Code when working with this intelligence hub.

## What This Is

A business intelligence system for **{name}**. {description}.

This system processes research links into actionable intelligence, tracks projects and recommendations, and builds a knowledge base that gets smarter over time. It is NOT a chatbot — it's an agent that accumulates context, connects dots across research, and produces structured recommendations.

## Skills

| Skill | Purpose |
|-------|---------|
| `/research <URL>` | Process a link through the full research pipeline |
| `/status [project]` | Status report — project pulse, recommendations, stale items |
| `/prioritize <args>` | Move projects between tiers or vote on recommendations |

## The `/research` Pipeline

1. **Timestamp & log** — Add entry to `data/research/intake-log.md` with status `pending`
2. **Fetch & understand** — WebFetch the content; follow referenced links
3. **Analyze** — Evaluate through these lenses:
{category_lines}
4. **Update knowledge base** — Create/update files in `data/knowledge/` as appropriate
5. **Update docs** — Add to `data/research/bookmarks.md`, update `data/research/intelligence-brief.md`, update `data/research/people-to-watch.md` if new person
6. **Report** — Structured summary with business applicability and action items
7. **Mark processed** — Change intake log status from `pending` to `processed`
8. **Cross-project check** — Check findings against `data/portfolio/projects.md` and add recommendations
9. **Log ideas** — Add actionable ideas to `data/portfolio/implementation-backlog.md`

## File Conventions

### data/research/

**intake-log.md** — Newest first. Format: `[YYYY-MM-DD HH:MM] | STATUS | Title | URL`
Statuses: `pending`, `processed`, `actioned`

**bookmarks.md** — Organized by topic: {topic_list}. Each entry has Author, Date, URL, Content summary, Tags, Notes.

**intelligence-brief.md** — The "so what?" doc. Key signals, action items by category, knowledge gaps.

**people-to-watch.md** — People who produce high-value content for this industry.

### data/portfolio/

**projects.md** — Project registry organized by tier (ACTIVE > READY > INCUBATING > SUPPORTING > DORMANT). Each project has: What, Status, Lane, Next actions, Last touched.

**content-pipeline.md** — Content tracking by platform and stage.

**implementation-backlog.md** — Every actionable idea from research. Statuses: `idea` > `exploring` > `in-progress` > `done` / `rejected` / `deferred`.

### data/knowledge/

**strategies/** — Deep methodology breakdowns
**tools/** — Tool evaluations
**transcripts/** — Video/audio transcripts

## Key Principles

1. **Depth over speed** — Better to deeply understand one link than to skim five
2. **Business lens** — Every analysis must answer "what does {name} DO with this?"
3. **Honest assessment** — Don't hype things that aren't ready
4. **Connect the dots** — Link new intel to existing knowledge
5. **Timestamp everything** — The user should always be able to ask "what was the last link?"
6. **Follow the thread** — If a post references an article/repo/video, fetch that too
7. **Track people, not just content** — Add high-value producers to people-to-watch.md

## Voice

Write in a **{voice}** tone. The audience is **{audience}**.

## Division of Labor

**Claude does:** Fetch, read, analyze, document, maintain all research files, create action items.
**User does:** Install/test tools, engage on social, create published content, make final decisions.

## Action Categories

{category_lines}
"""


def generate_intake_log(config: dict) -> str:
    name = config["business_name"]
    return f"""# Research Intake Log

Timestamped record of every link researched for {name}. Newest first.

**Format:** `[YYYY-MM-DD HH:MM] | STATUS | Title | URL`

**Statuses:**
- `pending` — Logged, not yet started
- `processed` — Fully analyzed and documented
- `actioned` — Implementation ideas logged to backlog

---

*(No entries yet — run `/research <URL>` to get started)*
"""


def generate_bookmarks(config: dict) -> str:
    name = config["business_name"]
    topics = config.get("bookmark_topics", config["categories"])
    sections = "\n\n".join(f"## {topic}\n\n*(No bookmarks yet)*" for topic in topics)

    return f"""# Bookmarks

Curated research collection for {name}. Organized by topic.

Each entry: Author, Date, URL, Content summary, Tags, Notes.

---

{sections}
"""


def generate_intelligence_brief(config: dict) -> str:
    name = config["business_name"]
    categories = config["categories"]

    action_tables = []
    for cat in categories:
        action_tables.append(f"""### {cat}

| Action | Source | Priority | Status |
|--------|--------|----------|--------|
| *(none yet)* | — | — | — |""")

    action_section = "\n\n".join(action_tables)

    return f"""# Intelligence Brief

*Last updated: {today()}*

Synthesized intelligence for **{name}**. This is the "so what?" document — what matters for the business right now.

---

## Key Signals

*(No signals yet — signals emerge as you process research links with `/research`)*

---

## Action Items

{action_section}

---

## Knowledge Gaps

*(Gaps will be identified as research accumulates)*

---

## Thesis

*(Your business thesis will develop as the intelligence system learns your industry)*
"""


def generate_people_to_watch(config: dict) -> str:
    name = config["business_name"]
    return f"""# People to Watch

Ranked by follow priority for {name}. Track people who consistently produce valuable content.

**Format:** Name | Platform | Why | Follow Priority

---

*(No people tracked yet — they'll be added as you process research with `/research`)*
"""


def generate_projects(config: dict) -> str:
    name = config["business_name"]
    lanes = config.get("project_lanes", ["Revenue", "Operations", "Growth"])
    projects = config.get("projects", [])

    lane_desc = ", ".join(f"**{l}**" for l in lanes)

    project_entries = []
    for p in projects:
        proj_name = p if isinstance(p, str) else p.get("name", "Unnamed")
        project_entries.append(f"""### {proj_name}

- **What:** *(describe this project)*
- **Status:** Not started
- **Lane:** *(pick: {', '.join(lanes)})*
- **Next actions:**
  - [ ] *(add first action)*
- **Last touched:** {today()}""")

    if not project_entries:
        project_entries.append("*(No projects yet — add them here or use `/prioritize`)*")

    projects_section = "\n\n".join(project_entries)

    return f"""# Project Registry

*Last updated: {today()}*

{name} project portfolio. Every project sits in at least one lane: {lane_desc}.

---

## ACTIVE

{projects_section}

---

## READY

*(Could start this week with minimal setup)*

---

## INCUBATING

*(Designed but not yet built)*

---

## SUPPORTING

*(Tools and systems that serve active projects)*

---

## DORMANT

*(Paused — could be revived with new context)*

---

## Recommendations

| # | Suggestion | Source | Votes | Status |
|---|-----------|--------|-------|--------|
| *(none yet)* | — | — | — | — |
"""


def generate_content_pipeline(config: dict) -> str:
    name = config["business_name"]
    platforms = config.get("platforms", [])

    if not platforms:
        platform_sections = "*(No platforms configured — add them during setup)*"
    else:
        sections = []
        for p in platforms:
            sections.append(f"""### {p}

| Title | Stage | Priority | Due | Notes |
|-------|-------|----------|-----|-------|
| *(none yet)* | — | — | — | — |""")
        platform_sections = "\n\n".join(sections)

    return f"""# Content Pipeline

*Last updated: {today()}*

Content tracking for {name}. Stages: Idea > Research > Outline > Draft > Review > Scheduled > Published.

---

{platform_sections}
"""


def generate_implementation_backlog(config: dict) -> str:
    name = config["business_name"]
    return f"""# Implementation Backlog

Every actionable idea from research for {name}. If it's worth doing, it goes here.

**Statuses:** `idea` > `exploring` > `in-progress` > `done` / `rejected` / `deferred`

---

## BUILD

| ID | Idea | Source | Status | Notes |
|----|------|--------|--------|-------|
| *(none yet)* | — | — | — | — |

## ADOPT

| ID | Tool/Practice | Source | Status | Notes |
|----|--------------|--------|--------|-------|
| *(none yet)* | — | — | — | — |

## OFFER

| ID | Service/Product | Source | Status | Notes |
|----|----------------|--------|--------|-------|
| *(none yet)* | — | — | — | — |
"""


def generate_all(config: dict, output_dir: Path) -> list[str]:
    """Generate all files. Returns list of created file paths."""
    generators = {
        "CLAUDE.md": generate_claude_md,
        "data/research/intake-log.md": generate_intake_log,
        "data/research/bookmarks.md": generate_bookmarks,
        "data/research/intelligence-brief.md": generate_intelligence_brief,
        "data/research/people-to-watch.md": generate_people_to_watch,
        "data/portfolio/projects.md": generate_projects,
        "data/portfolio/content-pipeline.md": generate_content_pipeline,
        "data/portfolio/implementation-backlog.md": generate_implementation_backlog,
    }

    created = []
    for rel_path, generator in generators.items():
        full_path = output_dir / rel_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        content = generator(config)
        full_path.write_text(content)
        created.append(str(rel_path))

    return created


def main():
    parser = argparse.ArgumentParser(description="Generate intelligence hub files from config")
    parser.add_argument("--config", default="config.json", help="Path to config.json")
    parser.add_argument("--output-dir", default=".", help="Output directory (project root)")
    args = parser.parse_args()

    config = load_config(args.config)
    output_dir = Path(args.output_dir)

    created = generate_all(config, output_dir)

    print(f"Generated {len(created)} files:")
    for f in created:
        print(f"  {f}")


if __name__ == "__main__":
    main()
