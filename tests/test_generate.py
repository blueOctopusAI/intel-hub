"""Test the file generation logic."""

import json
import sys
from pathlib import Path

import pytest

# Add scripts dir to path so we can import generate
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from generate import (
    generate_all,
    generate_bookmarks,
    generate_claude_md,
    generate_content_pipeline,
    generate_implementation_backlog,
    generate_intake_log,
    generate_intelligence_brief,
    generate_people_to_watch,
    generate_projects,
    load_config,
)


class TestLoadConfig:
    def test_loads_valid_config(self, config_file):
        config = load_config(str(config_file))
        assert config["business_name"] == "Asheville Pool Pros"

    def test_rejects_missing_file(self, tmp_path):
        with pytest.raises(SystemExit):
            load_config(str(tmp_path / "nonexistent.json"))

    def test_rejects_missing_required_fields(self, tmp_path):
        bad_config = tmp_path / "bad.json"
        bad_config.write_text(json.dumps({"business_name": "Test"}))
        with pytest.raises(SystemExit):
            load_config(str(bad_config))

    def test_accepts_minimal_config(self, tmp_path, minimal_config):
        path = tmp_path / "config.json"
        path.write_text(json.dumps(minimal_config))
        config = load_config(str(path))
        assert config["business_name"] == "Test Business"


class TestGenerateClaudeMd:
    def test_contains_business_name(self, sample_config):
        result = generate_claude_md(sample_config)
        assert "Asheville Pool Pros" in result

    def test_contains_all_categories(self, sample_config):
        result = generate_claude_md(sample_config)
        for cat in sample_config["categories"]:
            assert cat in result, f"Missing category: {cat}"

    def test_contains_voice(self, sample_config):
        result = generate_claude_md(sample_config)
        assert "casual" in result

    def test_contains_audience(self, sample_config):
        result = generate_claude_md(sample_config)
        assert "homeowners" in result

    def test_contains_research_pipeline(self, sample_config):
        result = generate_claude_md(sample_config)
        assert "/research" in result
        assert "Pipeline" in result

    def test_contains_skills_table(self, sample_config):
        result = generate_claude_md(sample_config)
        assert "/research" in result
        assert "/status" in result
        assert "/prioritize" in result


class TestGenerateIntakeLog:
    def test_contains_business_name(self, sample_config):
        result = generate_intake_log(sample_config)
        assert "Asheville Pool Pros" in result

    def test_has_format_instructions(self, sample_config):
        result = generate_intake_log(sample_config)
        assert "YYYY-MM-DD" in result
        assert "pending" in result
        assert "processed" in result


class TestGenerateBookmarks:
    def test_has_topic_sections(self, sample_config):
        result = generate_bookmarks(sample_config)
        for topic in sample_config["bookmark_topics"]:
            assert f"## {topic}" in result

    def test_uses_categories_as_fallback(self, minimal_config):
        result = generate_bookmarks(minimal_config)
        assert "## Implement" in result
        assert "## Monitor" in result


class TestGenerateIntelligenceBrief:
    def test_contains_business_name(self, sample_config):
        result = generate_intelligence_brief(sample_config)
        assert "Asheville Pool Pros" in result

    def test_has_category_action_tables(self, sample_config):
        result = generate_intelligence_brief(sample_config)
        for cat in sample_config["categories"]:
            assert f"### {cat}" in result

    def test_has_key_signals_section(self, sample_config):
        result = generate_intelligence_brief(sample_config)
        assert "Key Signals" in result

    def test_has_thesis_section(self, sample_config):
        result = generate_intelligence_brief(sample_config)
        assert "Thesis" in result


class TestGeneratePeopleToWatch:
    def test_contains_business_name(self, sample_config):
        result = generate_people_to_watch(sample_config)
        assert "Asheville Pool Pros" in result


class TestGenerateProjects:
    def test_contains_project_names(self, sample_config):
        result = generate_projects(sample_config)
        assert "Spring marketing push" in result
        assert "Hire second technician" in result

    def test_has_tier_sections(self, sample_config):
        result = generate_projects(sample_config)
        assert "## ACTIVE" in result
        assert "## READY" in result
        assert "## DORMANT" in result

    def test_has_recommendations_table(self, sample_config):
        result = generate_projects(sample_config)
        assert "Recommendations" in result

    def test_handles_no_projects(self, minimal_config):
        result = generate_projects(minimal_config)
        assert "ACTIVE" in result  # Structure still there


class TestGenerateContentPipeline:
    def test_has_platform_sections(self, sample_config):
        result = generate_content_pipeline(sample_config)
        assert "Facebook" in result
        assert "Google Business Profile" in result

    def test_handles_no_platforms(self, minimal_config):
        result = generate_content_pipeline(minimal_config)
        assert "No platforms configured" in result


class TestGenerateBacklog:
    def test_has_category_sections(self, sample_config):
        result = generate_implementation_backlog(sample_config)
        assert "## BUILD" in result
        assert "## ADOPT" in result
        assert "## OFFER" in result


class TestGenerateAll:
    def test_creates_all_files(self, tmp_path, sample_config):
        config_path = tmp_path / "config.json"
        config_path.write_text(json.dumps(sample_config))

        created = generate_all(sample_config, tmp_path)

        assert len(created) == 8
        assert "CLAUDE.md" in created
        assert "data/research/intake-log.md" in created
        assert "data/research/bookmarks.md" in created
        assert "data/research/intelligence-brief.md" in created
        assert "data/research/people-to-watch.md" in created
        assert "data/portfolio/projects.md" in created
        assert "data/portfolio/content-pipeline.md" in created
        assert "data/portfolio/implementation-backlog.md" in created

    def test_files_actually_exist(self, tmp_path, sample_config):
        generate_all(sample_config, tmp_path)

        for rel_path in [
            "CLAUDE.md",
            "data/research/intake-log.md",
            "data/research/bookmarks.md",
            "data/research/intelligence-brief.md",
            "data/research/people-to-watch.md",
            "data/portfolio/projects.md",
            "data/portfolio/content-pipeline.md",
            "data/portfolio/implementation-backlog.md",
        ]:
            full_path = tmp_path / rel_path
            assert full_path.exists(), f"Expected file not created: {rel_path}"
            assert full_path.stat().st_size > 0, f"File is empty: {rel_path}"

    def test_files_contain_business_name(self, tmp_path, sample_config):
        generate_all(sample_config, tmp_path)

        # Most files should mention the business
        for rel_path in [
            "CLAUDE.md",
            "data/research/intake-log.md",
            "data/research/bookmarks.md",
            "data/research/intelligence-brief.md",
        ]:
            content = (tmp_path / rel_path).read_text()
            assert "Asheville Pool Pros" in content, f"Business name not in {rel_path}"

    def test_creates_directory_structure(self, tmp_path, sample_config):
        generate_all(sample_config, tmp_path)

        assert (tmp_path / "data" / "research").is_dir()
        assert (tmp_path / "data" / "portfolio").is_dir()

    def test_idempotent(self, tmp_path, sample_config):
        """Running generate twice should not fail or corrupt files."""
        generate_all(sample_config, tmp_path)
        first_content = (tmp_path / "CLAUDE.md").read_text()

        generate_all(sample_config, tmp_path)
        second_content = (tmp_path / "CLAUDE.md").read_text()

        assert first_content == second_content
