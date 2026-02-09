"""
Mock LLM Service for offline development.

This service simulates LLM responses by returning pre-written Manim code,
allowing the application to run without an OpenAI API key.
"""
from pathlib import Path


class MockLLMService:
    """Simulates LLM responses by returning pre-written Manim code."""
    
    def generate_code(self) -> str:
        """
        Returns the GCF (Greatest Common Factor) example code.
        
        This bypasses the actual LLM call and returns a working Manim
        animation script for testing purposes.
        
        Returns:
            str: The Manim code for the GCF example animation.
        """
        template_path = Path(__file__).parent.parent / "templates" / "examples" / "gcf.py"
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
