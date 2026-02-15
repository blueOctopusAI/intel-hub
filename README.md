# Intel Hub

An AI-powered business intelligence system that runs on your machine. Paste links, get structured analysis through your business lens, build a knowledge base that compounds over time.

**This is not a chatbot.** It's an agent that accumulates context, connects new information to everything it already knows, tracks your projects, and produces actionable recommendations.

## How It Works

```
You paste a link
        |
Claude Code fetches, reads, analyzes
        |
Updates your knowledge base:
  - Intake log (what you researched)
  - Bookmarks (organized by your topics)
  - Intelligence brief (key signals + actions)
  - Project recommendations (what to do next)
        |
You check /status for your dashboard
```

Every research input connects to your existing knowledge. Patterns emerge. The system gets smarter.

## Quick Start

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and authenticated
- Python 3.10+
- Git

### Setup

```bash
git clone https://github.com/blueOctopusAI/intel-hub.git
cd intel-hub
bash setup.sh
```

The setup wizard asks about your business (name, industry, what you track) and generates all configuration files. Takes about 2 minutes.

### Usage

```bash
claude
```

Then in Claude Code:

```
/research https://example.com/industry-article
```

Watch it analyze the article through your business categories, update your knowledge base, and create action items.

```
/status
```

See your project pulse, recommended focus, stale items, and new recommendations.

```
/prioritize rec 1 up
```

Vote on recommendations. Manage your project tiers.

## Skills

| Skill | Purpose |
|-------|---------|
| `/research <URL>` | Process a link through the 9-step intelligence pipeline |
| `/status [project]` | Project pulse, recommended focus, stale items, new recommendations |
| `/prioritize <args>` | Move projects between tiers or vote on recommendations |
| `/atomize <source>` | Turn a blog post or article into social media variations |
| `/add-project <name>` | Scan a project directory, detect stack, add to registry |
| `/security [target]` | Security audit — exposed secrets, deps, tool evaluations |

## Industry Presets

The setup wizard includes presets that pre-fill sensible defaults:

| Preset | For | Categories |
|--------|-----|-----------|
| Home Services | Contractor, plumber, HVAC, pool | Implement, Marketing, Monitor, Competitors, Equipment |
| Restaurant | Restaurant, cafe, food truck | Implement, Menu & Sourcing, Marketing, Monitor, Competitors |
| Professional Services | Consulting, legal, accounting | Implement, Offer, Tools, Monitor, Content |
| Retail | Shop, online store, boutique | Implement, Product & Inventory, Marketing, Monitor, Competitors |
| Healthcare | Dental, medical, wellness | Implement, Patient Experience, Compliance, Monitor, Marketing |
| Real Estate | Brokerage, property mgmt | Implement, Market Intel, Marketing, Monitor, Competitors |

You can customize any preset during setup or start from scratch.

## What Gets Generated

After setup, your project looks like this:

```
intel-hub/
├── CLAUDE.md                          # Claude Code instructions (auto-generated)
├── config.json                        # Your business config
├── data/
│   ├── research/
│   │   ├── intake-log.md              # Every link you've researched
│   │   ├── bookmarks.md               # Organized by your topics
│   │   ├── intelligence-brief.md      # Key signals + action items
│   │   └── people-to-watch.md         # Valuable content producers
│   ├── knowledge/
│   │   ├── strategies/                # Deep methodology breakdowns
│   │   ├── tools/                     # Tool evaluations
│   │   └── transcripts/              # Video/audio transcripts
│   └── portfolio/
│       ├── projects.md                # Your project registry
│       ├── content-pipeline.md        # Content by platform
│       └── implementation-backlog.md  # Ideas to build/adopt/offer
├── logs/                              # Setup and operation logs
└── .claude/skills/                    # All 6 skills above
```

All data is markdown files. Human-readable, git-trackable, no database required.

## Advanced

### Non-Interactive Setup

If you already have a `config.json`:

```bash
bash setup.sh --non-interactive
```

Or load a preset directly:

```bash
bash setup.sh --preset home-services
```

### Regenerating Config

If you change `config.json` and want to regenerate `CLAUDE.md` without overwriting your research data:

```bash
python3 scripts/generate.py
```

To force-overwrite all files (deletes existing research data):

```bash
python3 scripts/generate.py --force
```

### Troubleshooting

Setup and generation logs are saved to `logs/` with timestamps. Each run captures:
- Platform, OS, shell, Python version
- Claude Code installation status
- WSL detection (for Windows users)
- Config choices and file generation results

Check the latest log:

```bash
ls -lt logs/ | head -5
cat logs/setup-*.log
```

## Testing

```bash
pip install -r requirements.txt
pytest tests/ -v
bash tests/test_setup.sh
```

## License

MIT — see [LICENSE](LICENSE)
