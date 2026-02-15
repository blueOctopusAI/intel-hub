"""Test that all industry presets are valid and complete."""

import json
from pathlib import Path

import pytest

REQUIRED_FIELDS = [
    "industry",
    "industry_label",
    "description",
    "categories",
    "project_lanes",
    "bookmark_topics",
    "default_voice",
    "audience",
    "example_projects",
]

VALID_VOICES = ["casual", "friendly", "professional", "technical"]


def get_preset_files():
    presets_dir = Path(__file__).parent.parent / "presets"
    return sorted(presets_dir.glob("*.json"))


def get_preset_ids():
    return [f.stem for f in get_preset_files()]


@pytest.fixture(params=get_preset_files(), ids=get_preset_ids())
def preset(request):
    path = request.param
    with open(path) as f:
        return json.load(f), path.stem


class TestPresetStructure:
    def test_has_required_fields(self, preset):
        data, name = preset
        for field in REQUIRED_FIELDS:
            assert field in data, f"Preset '{name}' missing required field: {field}"

    def test_categories_not_empty(self, preset):
        data, name = preset
        assert len(data["categories"]) >= 2, f"Preset '{name}' needs at least 2 categories"

    def test_bookmark_topics_not_empty(self, preset):
        data, name = preset
        assert len(data["bookmark_topics"]) >= 2, f"Preset '{name}' needs at least 2 bookmark topics"

    def test_project_lanes_not_empty(self, preset):
        data, name = preset
        assert len(data["project_lanes"]) >= 2, f"Preset '{name}' needs at least 2 project lanes"

    def test_valid_voice(self, preset):
        data, name = preset
        assert data["default_voice"] in VALID_VOICES, (
            f"Preset '{name}' has invalid voice: {data['default_voice']}. Must be one of {VALID_VOICES}"
        )

    def test_example_projects_provided(self, preset):
        data, name = preset
        assert len(data["example_projects"]) >= 1, f"Preset '{name}' needs at least 1 example project"

    def test_industry_is_snake_case(self, preset):
        data, name = preset
        assert "_" in data["industry"] or data["industry"].islower(), (
            f"Preset '{name}' industry should be snake_case: {data['industry']}"
        )

    def test_no_empty_strings(self, preset):
        data, name = preset
        for field in ["industry", "industry_label", "description", "default_voice", "audience"]:
            assert data[field].strip(), f"Preset '{name}' has empty string for: {field}"


class TestPresetConsistency:
    def test_all_presets_valid_json(self, presets_dir):
        for f in presets_dir.glob("*.json"):
            with open(f) as fh:
                data = json.load(fh)  # Should not raise
            assert isinstance(data, dict), f"{f.name} is not a JSON object"

    def test_no_duplicate_industries(self, presets_dir):
        industries = []
        for f in presets_dir.glob("*.json"):
            with open(f) as fh:
                data = json.load(fh)
            industries.append(data["industry"])
        assert len(industries) == len(set(industries)), "Duplicate industry values across presets"

    def test_minimum_preset_count(self, presets_dir):
        count = len(list(presets_dir.glob("*.json")))
        assert count >= 3, f"Expected at least 3 presets, found {count}"
