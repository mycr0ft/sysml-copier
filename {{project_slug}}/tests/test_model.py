"""Tests for the example SysML model."""

from pathlib import Path

import pytest

from sysmlpy import load_project, analyze


MODELS_DIR = Path(__file__).parent.parent / "sysml" / "models"


@pytest.fixture
def model():
    """Load the SysML model from sysml/models/."""
    return load_project(str(MODELS_DIR))


def test_model_parses(model):
    """The example model should parse without errors."""
    assert model is not None, "Model failed to parse"


def test_model_has_packages(model):
    """The model should contain at least one package."""
    assert len(model.packages) > 0, "No packages found in model"


def test_model_has_parts(model):
    """The model should contain part definitions."""
    parts = model.find(sysml_type="part def")
    assert len(parts) > 0, "No part definitions found in model"


def test_model_has_actions(model):
    """The model should contain action definitions."""
    actions = model.find(sysml_type="action def")
    assert len(actions) > 0, "No action definitions found in model"


def test_model_passes_semantic_analysis(model):
    """The model should pass semantic analysis with no errors."""
    result = analyze(model, style_checks=False)
    errors = result.errors if hasattr(result, "errors") else []
    assert not errors, [f"[{e.code}] {e.message}" for e in errors]
