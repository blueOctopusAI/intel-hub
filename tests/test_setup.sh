#!/usr/bin/env bash
# Integration test: run setup.sh non-interactively and verify output.
# Usage: bash tests/test_setup.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
TEST_DIR=$(mktemp -d)

echo "=== Intel Hub Setup Integration Test ==="
echo "Test directory: $TEST_DIR"
echo ""

# Copy project files to test directory
cp -r "$PROJECT_DIR/presets" "$TEST_DIR/"
cp -r "$PROJECT_DIR/scripts" "$TEST_DIR/"
cp "$PROJECT_DIR/setup.sh" "$TEST_DIR/"
mkdir -p "$TEST_DIR/.claude/skills"
mkdir -p "$TEST_DIR/data"

# Create a test config
cat > "$TEST_DIR/config.json" <<'EOF'
{
  "business_name": "Test Pool Company",
  "description": "Pool maintenance and repair",
  "role": "Owner",
  "industry": "home_services",
  "industry_label": "Home Services",
  "categories": ["Implement", "Marketing", "Monitor"],
  "bookmark_topics": ["Industry Trends", "Marketing Ideas"],
  "project_lanes": ["Revenue", "Operations"],
  "projects": ["Spring campaign", "New truck"],
  "platforms": ["Facebook", "Instagram"],
  "voice": "casual",
  "audience": "homeowners"
}
EOF

# Run generation (non-interactive mode)
echo "[TEST] Running setup --non-interactive..."
cd "$TEST_DIR"
bash setup.sh --non-interactive
echo ""

# --- Assertions ---
PASS=0
FAIL=0

assert_file_exists() {
    if [ -f "$TEST_DIR/$1" ]; then
        echo "  PASS: $1 exists"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $1 missing"
        FAIL=$((FAIL + 1))
    fi
}

assert_file_contains() {
    if grep -q "$2" "$TEST_DIR/$1" 2>/dev/null; then
        echo "  PASS: $1 contains '$2'"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $1 does not contain '$2'"
        FAIL=$((FAIL + 1))
    fi
}

assert_file_not_empty() {
    if [ -s "$TEST_DIR/$1" ]; then
        echo "  PASS: $1 is not empty"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $1 is empty"
        FAIL=$((FAIL + 1))
    fi
}

echo "[TEST] Checking generated files..."

# File existence
assert_file_exists "CLAUDE.md"
assert_file_exists "config.json"
assert_file_exists "data/research/intake-log.md"
assert_file_exists "data/research/bookmarks.md"
assert_file_exists "data/research/intelligence-brief.md"
assert_file_exists "data/research/people-to-watch.md"
assert_file_exists "data/portfolio/projects.md"
assert_file_exists "data/portfolio/content-pipeline.md"
assert_file_exists "data/portfolio/implementation-backlog.md"

# Content checks
assert_file_contains "CLAUDE.md" "Test Pool Company"
assert_file_contains "CLAUDE.md" "Implement"
assert_file_contains "CLAUDE.md" "Marketing"
assert_file_contains "CLAUDE.md" "casual"
assert_file_contains "CLAUDE.md" "/research"
assert_file_contains "data/research/bookmarks.md" "Industry Trends"
assert_file_contains "data/research/bookmarks.md" "Marketing Ideas"
assert_file_contains "data/research/intelligence-brief.md" "Test Pool Company"
assert_file_contains "data/portfolio/projects.md" "Spring campaign"
assert_file_contains "data/portfolio/projects.md" "New truck"
assert_file_contains "data/portfolio/projects.md" "Recommendations"
assert_file_contains "data/portfolio/content-pipeline.md" "Facebook"
assert_file_contains "data/portfolio/content-pipeline.md" "Instagram"

# Non-empty checks
assert_file_not_empty "CLAUDE.md"
assert_file_not_empty "data/research/intelligence-brief.md"
assert_file_not_empty "data/portfolio/projects.md"

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="

# Cleanup
rm -rf "$TEST_DIR"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
echo "All tests passed!"
