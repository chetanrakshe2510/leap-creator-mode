"""
Unit tests for the configuration module.
"""
import pytest
from pathlib import Path
from leap.core.config import (
    BASE_DIR, PACKAGE_DIR, GENERATED_DIR, LOGS_DIR,
    OPENAI_MODEL, MANIM_QUALITY, EXECUTION_TIMEOUT, MAX_ATTEMPTS
)

@pytest.fixture(autouse=True)
def setup_test_dirs():
    """Ensure test directories exist."""
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    yield

def test_critical_paths():
    """Test that critical directory paths are correctly set up."""
    # Test base directories
    assert BASE_DIR.exists()
    assert PACKAGE_DIR.exists()
    assert PACKAGE_DIR == BASE_DIR / "leap"
    
    # Test generated directories
    assert GENERATED_DIR.parent == BASE_DIR
    assert LOGS_DIR.parent == GENERATED_DIR
    assert LOGS_DIR.exists()

def test_core_settings():
    """Test critical configuration settings."""
    # Model settings
    assert isinstance(OPENAI_MODEL, str)
    assert OPENAI_MODEL in ["o3-mini"]
    
    # Manim settings
    assert MANIM_QUALITY == "-ql"  # Low quality for alpha
    
    # Execution settings
    assert isinstance(EXECUTION_TIMEOUT, int)
    assert EXECUTION_TIMEOUT > 0
    assert isinstance(MAX_ATTEMPTS, int)
    assert MAX_ATTEMPTS > 0
