"""
Centralized prompt management system for AskLeap.
This module provides access to all prompts used in the application.
"""

from leap.prompts.planning import SCENE_PLANNING_PROMPTS
from leap.prompts.generation import CODE_GENERATION_PROMPTS
from leap.prompts.correction import ERROR_CORRECTION_PROMPTS
from leap.prompts.validation import VALIDATION_PROMPTS

__all__ = [
    "SCENE_PLANNING_PROMPTS",
    "CODE_GENERATION_PROMPTS", 
    "ERROR_CORRECTION_PROMPTS",
    "VALIDATION_PROMPTS"
] 