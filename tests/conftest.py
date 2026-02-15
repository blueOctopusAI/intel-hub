"""Shared fixtures for intel-hub tests."""

import json
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).parent.parent
PRESETS_DIR = ROOT_DIR / "presets"
SCRIPTS_DIR = ROOT_DIR / "scripts"


@pytest.fixture
def root_dir():
    return ROOT_DIR


@pytest.fixture
def presets_dir():
    return PRESETS_DIR


@pytest.fixture
def sample_config():
    """A minimal valid config for testing."""
    return {
        "business_name": "Asheville Pool Pros",
        "description": "Residential pool maintenance and repair in Western NC",
        "role": "Owner",
        "industry": "home_services",
        "industry_label": "Home Services",
        "categories": ["Implement", "Marketing", "Monitor", "Competitors", "Equipment & Suppliers"],
        "bookmark_topics": ["Industry Trends", "Equipment & Tech", "Marketing Ideas", "Competitor Intel"],
        "project_lanes": ["Revenue", "Operations", "Growth"],
        "projects": ["Spring marketing push", "Hire second technician"],
        "platforms": ["Facebook", "Google Business Profile"],
        "voice": "casual",
        "audience": "homeowners",
    }


@pytest.fixture
def minimal_config():
    """The absolute minimum config that should be accepted."""
    return {
        "business_name": "Test Business",
        "industry": "custom",
        "categories": ["Implement", "Monitor"],
        "voice": "professional",
    }


@pytest.fixture
def config_file(tmp_path, sample_config):
    """Write sample config to a temp file and return the path."""
    path = tmp_path / "config.json"
    path.write_text(json.dumps(sample_config, indent=2))
    return path
