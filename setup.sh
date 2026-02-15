#!/usr/bin/env bash
# setup.sh — Interactive setup wizard for Intel Hub
# Asks questions about your business and generates all configuration files.
#
# Usage:
#   bash setup.sh                    # Interactive mode
#   bash setup.sh --preset <name>    # Load a preset (home-services, restaurant, etc.)
#   bash setup.sh --non-interactive  # Use config.json that already exists

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PRESETS_DIR="$SCRIPT_DIR/presets"
CONFIG_FILE="$SCRIPT_DIR/config.json"

# Colors (if terminal supports them)
if [ -t 1 ]; then
    BOLD='\033[1m'
    DIM='\033[2m'
    GREEN='\033[0;32m'
    CYAN='\033[0;36m'
    YELLOW='\033[0;33m'
    RESET='\033[0m'
else
    BOLD='' DIM='' GREEN='' CYAN='' YELLOW='' RESET=''
fi

# --- Parse arguments ---
PRESET_NAME=""
NON_INTERACTIVE=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --preset)
            PRESET_NAME="$2"
            shift 2
            ;;
        --non-interactive)
            NON_INTERACTIVE=true
            shift
            ;;
        --help|-h)
            echo "Usage: bash setup.sh [--preset <name>] [--non-interactive]"
            echo ""
            echo "Presets:"
            for f in "$PRESETS_DIR"/*.json; do
                name=$(basename "$f" .json)
                label=$(python3 -c "import json; print(json.load(open('$f'))['industry_label'])" 2>/dev/null || echo "$name")
                echo "  $name — $label"
            done
            exit 0
            ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done

# --- Non-interactive mode ---
if $NON_INTERACTIVE; then
    if [ ! -f "$CONFIG_FILE" ]; then
        echo "Error: --non-interactive requires config.json to exist"
        exit 1
    fi
    echo "Generating files from existing config.json..."
    python3 "$SCRIPT_DIR/scripts/generate.py" --config "$CONFIG_FILE" --output-dir "$SCRIPT_DIR"
    echo ""
    echo -e "${GREEN}Done!${RESET} Run ${CYAN}claude${RESET} to start using your intelligence hub."
    exit 0
fi

# --- Welcome ---
echo ""
echo -e "${BOLD}================================================${RESET}"
echo -e "${BOLD}  Intel Hub — Business Intelligence Setup${RESET}"
echo -e "${BOLD}================================================${RESET}"
echo ""
echo "This wizard will configure an AI-powered intelligence"
echo "system for your business. Takes about 2 minutes."
echo ""

# --- Helper: prompt with default ---
ask() {
    local prompt="$1"
    local default="$2"
    local result

    if [ -n "$default" ]; then
        echo -en "${CYAN}$prompt${RESET} ${DIM}[$default]${RESET}: "
    else
        echo -en "${CYAN}$prompt${RESET}: "
    fi
    read -r result
    echo "${result:-$default}"
}

# --- Helper: multi-select from list ---
ask_multi() {
    local prompt="$1"
    shift
    local defaults=("$@")

    echo -e "${CYAN}$prompt${RESET}"
    echo -e "${DIM}(comma-separated, or press Enter to accept defaults)${RESET}"
    echo -e "${DIM}Defaults: ${defaults[*]}${RESET}"
    echo -n "> "
    read -r input

    if [ -z "$input" ]; then
        printf '%s\n' "${defaults[@]}"
    else
        IFS=',' read -ra items <<< "$input"
        for item in "${items[@]}"; do
            echo "$(echo "$item" | xargs)"  # trim whitespace
        done
    fi
}

# --- Step 1: Industry preset ---
echo -e "${BOLD}Step 1: Your Industry${RESET}"
echo ""

if [ -n "$PRESET_NAME" ]; then
    PRESET_FILE="$PRESETS_DIR/$PRESET_NAME.json"
    if [ ! -f "$PRESET_FILE" ]; then
        echo "Error: Preset '$PRESET_NAME' not found"
        exit 1
    fi
    echo "Using preset: $PRESET_NAME"
else
    echo "Available presets:"
    i=1
    declare -a preset_files=()
    for f in "$PRESETS_DIR"/*.json; do
        name=$(basename "$f" .json)
        label=$(python3 -c "import json; print(json.load(open('$f'))['industry_label'])" 2>/dev/null || echo "$name")
        echo "  $i) $label"
        preset_files+=("$f")
        ((i++))
    done
    echo "  $i) Custom (no preset)"
    echo ""

    echo -n "Choose [1-$i]: "
    read -r choice

    if [ "$choice" -lt "$i" ] 2>/dev/null; then
        PRESET_FILE="${preset_files[$((choice-1))]}"
        PRESET_NAME=$(basename "$PRESET_FILE" .json)
        echo ""
        echo "Loaded: $PRESET_NAME"
    else
        PRESET_FILE=""
        PRESET_NAME="custom"
    fi
fi

echo ""

# --- Load preset defaults ---
if [ -n "$PRESET_FILE" ] && [ -f "$PRESET_FILE" ]; then
    DEFAULT_CATEGORIES=$(python3 -c "import json; print(','.join(json.load(open('$PRESET_FILE'))['categories']))")
    DEFAULT_VOICE=$(python3 -c "import json; print(json.load(open('$PRESET_FILE'))['default_voice'])")
    DEFAULT_AUDIENCE=$(python3 -c "import json; print(json.load(open('$PRESET_FILE'))['audience'])")
    DEFAULT_BOOKMARK_TOPICS=$(python3 -c "import json; print(','.join(json.load(open('$PRESET_FILE'))['bookmark_topics']))")
    DEFAULT_LANES=$(python3 -c "import json; print(','.join(json.load(open('$PRESET_FILE'))['project_lanes']))")
    INDUSTRY_LABEL=$(python3 -c "import json; print(json.load(open('$PRESET_FILE'))['industry_label'])")
else
    DEFAULT_CATEGORIES="Implement,Monitor,Content"
    DEFAULT_VOICE="professional"
    DEFAULT_AUDIENCE="customers"
    DEFAULT_BOOKMARK_TOPICS="Industry Trends,Tools & Tech,Competitor Intel"
    DEFAULT_LANES="Revenue,Operations,Growth"
    INDUSTRY_LABEL="Custom"
fi

# --- Step 2: Business info ---
echo -e "${BOLD}Step 2: Your Business${RESET}"
echo ""
BUSINESS_NAME=$(ask "Business name" "")
if [ -z "$BUSINESS_NAME" ]; then
    echo "Error: Business name is required"
    exit 1
fi

BUSINESS_DESC=$(ask "One-line description" "A $INDUSTRY_LABEL business")
YOUR_ROLE=$(ask "Your role" "Owner")
echo ""

# --- Step 3: Categories ---
echo -e "${BOLD}Step 3: Analysis Categories${RESET}"
echo "When you research a link, Claude will analyze it through these lenses."
echo ""

IFS=',' read -ra CAT_ARRAY <<< "$DEFAULT_CATEGORIES"
mapfile -t CATEGORIES < <(ask_multi "Categories" "${CAT_ARRAY[@]}")
echo ""

# --- Step 4: Projects ---
echo -e "${BOLD}Step 4: Current Projects${RESET}"
echo "What are you working on right now? (1 per line, blank line to finish)"
echo -e "${DIM}These don't have to be software — 'Spring marketing push' is fine.${RESET}"
echo ""

PROJECTS=()
while true; do
    echo -n "> "
    read -r project
    if [ -z "$project" ]; then
        break
    fi
    PROJECTS+=("$project")
done
echo ""

# --- Step 5: Platforms ---
echo -e "${BOLD}Step 5: Content Platforms${RESET}"
echo "Where do you publish content? (comma-separated, or Enter to skip)"
echo -e "${DIM}Examples: Facebook, Instagram, X, Google Business Profile, YouTube, Blog, Email${RESET}"
echo ""
echo -n "> "
read -r platforms_input

PLATFORMS=()
if [ -n "$platforms_input" ]; then
    IFS=',' read -ra PLATFORMS <<< "$platforms_input"
    # Trim whitespace
    PLATFORMS=("${PLATFORMS[@]// /}")
fi
echo ""

# --- Step 6: Voice ---
echo -e "${BOLD}Step 6: Communication Style${RESET}"
echo ""
VOICE=$(ask "Voice (casual / friendly / professional / technical)" "$DEFAULT_VOICE")
AUDIENCE=$(ask "Who is your audience?" "$DEFAULT_AUDIENCE")
echo ""

# --- Build config.json ---
echo -e "${BOLD}Generating your intelligence hub...${RESET}"
echo ""

# Build JSON with Python (handles escaping properly)
python3 - "$CONFIG_FILE" "$BUSINESS_NAME" "$BUSINESS_DESC" "$YOUR_ROLE" \
    "$PRESET_NAME" "$INDUSTRY_LABEL" "$VOICE" "$AUDIENCE" <<'PYTHON_SCRIPT'
import json
import sys

config_path = sys.argv[1]
business_name = sys.argv[2]
description = sys.argv[3]
role = sys.argv[4]
industry = sys.argv[5]
industry_label = sys.argv[6]
voice = sys.argv[7]
audience = sys.argv[8]

# Read categories, projects, platforms from environment
import os
categories = [c.strip() for c in os.environ.get("CATEGORIES", "").split("\n") if c.strip()]
projects = [p.strip() for p in os.environ.get("PROJECTS", "").split("\n") if p.strip()]
platforms = [p.strip() for p in os.environ.get("PLATFORMS", "").split("\n") if p.strip()]
bookmark_topics = [t.strip() for t in os.environ.get("BOOKMARK_TOPICS", "").split(",") if t.strip()]
project_lanes = [l.strip() for l in os.environ.get("PROJECT_LANES", "").split(",") if l.strip()]

config = {
    "business_name": business_name,
    "description": description,
    "role": role,
    "industry": industry,
    "industry_label": industry_label,
    "categories": categories,
    "bookmark_topics": bookmark_topics or categories,
    "project_lanes": project_lanes or ["Revenue", "Operations", "Growth"],
    "projects": projects,
    "platforms": platforms,
    "voice": voice,
    "audience": audience,
}

with open(config_path, "w") as f:
    json.dump(config, f, indent=2)

print(f"  config.json written")
PYTHON_SCRIPT

# Export arrays as newline-separated env vars for Python
export CATEGORIES
CATEGORIES=$(printf '%s\n' "${CATEGORIES[@]}")
export PROJECTS
PROJECTS=$(printf '%s\n' "${PROJECTS[@]}")
export PLATFORMS
PLATFORMS=$(printf '%s\n' "${PLATFORMS[@]}")
export BOOKMARK_TOPICS="$DEFAULT_BOOKMARK_TOPICS"
export PROJECT_LANES="$DEFAULT_LANES"

# Re-run the Python to actually write (env vars are set now)
python3 - "$CONFIG_FILE" "$BUSINESS_NAME" "$BUSINESS_DESC" "$YOUR_ROLE" \
    "$PRESET_NAME" "$INDUSTRY_LABEL" "$VOICE" "$AUDIENCE" <<'PYTHON_SCRIPT'
import json
import sys
import os

config_path = sys.argv[1]
config = {
    "business_name": sys.argv[2],
    "description": sys.argv[3],
    "role": sys.argv[4],
    "industry": sys.argv[5],
    "industry_label": sys.argv[6],
    "categories": [c.strip() for c in os.environ.get("CATEGORIES", "").split("\n") if c.strip()],
    "bookmark_topics": [t.strip() for t in os.environ.get("BOOKMARK_TOPICS", "").split(",") if t.strip()],
    "project_lanes": [l.strip() for l in os.environ.get("PROJECT_LANES", "").split(",") if l.strip()],
    "projects": [p.strip() for p in os.environ.get("PROJECTS", "").split("\n") if p.strip()],
    "platforms": [p.strip() for p in os.environ.get("PLATFORMS", "").split(",") if p.strip()],
    "voice": sys.argv[7],
    "audience": sys.argv[8],
}

# Fill defaults
if not config["bookmark_topics"]:
    config["bookmark_topics"] = config["categories"]
if not config["project_lanes"]:
    config["project_lanes"] = ["Revenue", "Operations", "Growth"]

with open(config_path, "w") as f:
    json.dump(config, f, indent=2)
PYTHON_SCRIPT

# --- Generate all files ---
python3 "$SCRIPT_DIR/scripts/generate.py" --config "$CONFIG_FILE" --output-dir "$SCRIPT_DIR"

# --- Done ---
echo ""
echo -e "${GREEN}================================================${RESET}"
echo -e "${GREEN}  Your intelligence hub is ready!${RESET}"
echo -e "${GREEN}================================================${RESET}"
echo ""
echo -e "  Business: ${BOLD}$BUSINESS_NAME${RESET}"
echo -e "  Industry: $INDUSTRY_LABEL"
echo -e "  Categories: ${CATEGORIES[*]}"
echo ""
echo -e "  ${BOLD}Next steps:${RESET}"
echo -e "  1. Run ${CYAN}claude${RESET} to start Claude Code"
echo -e "  2. Type ${CYAN}/research <URL>${RESET} to analyze your first link"
echo -e "  3. Type ${CYAN}/status${RESET} to see your dashboard"
echo ""
echo -e "  Your data lives in ${DIM}data/${RESET}"
echo -e "  Your config is in ${DIM}config.json${RESET}"
echo ""
