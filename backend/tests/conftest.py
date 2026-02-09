"""
Shared pytest fixtures and configuration.
"""
import pytest
import os
from pathlib import Path
from leap.core.config import (
    GENERATED_DIR,
    LOGS_DIR,
    ASSETS_DIR,
    TEMPLATES_DIR
)

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up test environment with required directories."""
    # Create required directories
    dirs = [GENERATED_DIR, LOGS_DIR, ASSETS_DIR, TEMPLATES_DIR]
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # Set up test environment variables
    os.environ.setdefault("OPENAI_MODEL", "gpt-4-turbo-preview")
    os.environ.setdefault("MANIM_QUALITY", "-ql")
    
    yield

@pytest.fixture
def sample_manim_code():
    """Return sample Manim code for testing."""
    return """
from manim import *

class TestScene(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
    """

@pytest.fixture
def sample_state():
    """Provide a sample workflow state for testing."""
    return {
        "user_input": "Explain how gravity works",
        "rendering_quality": "low",
        "user_level": "normal",
        "voice_model": "nova",
        "duration_detail": "short",
        "correction_attempts": 0
    } 