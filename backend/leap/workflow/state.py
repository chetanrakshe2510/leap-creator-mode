from typing import Dict, Any, Optional, TypedDict, List
from pydantic import  Field
class GraphState(TypedDict, total=False):
    """State for the workflow graph."""
    user_input: str = Field(description="Original user prompt")
    reformulated_input: Optional[str] = Field(None, description="Reformulated version of the user input that's clearer and more specific")
    plan: Optional[str] = Field(None, description="Plan for the animation")
    generated_code: Optional[str] = Field(None, description="Generated code")
    execution_result: Optional[Dict[str, Any]] = Field(None, description="Result of the execution")
    error: Optional[str] = Field(None, description="Error message")
    correction_attempts: int = Field(0, description="Number of correction attempts")
    rendering_quality: str = Field("low", description="Rendering quality")
    duration_detail: str = Field("short", description="Duration of the animation")
    user_level: str = Field("normal", description="Explanation level")
    voice_model: str = Field("nova", description="Voice model")
    email: Optional[str] = Field(None, description="User email")
    validation_status: Optional[str] = Field(None, description="Status of input validation (valid, invalid, needs_clarification)")
    suggestion: Optional[str] = Field(None, description="Suggestion for improving the input")
    prompts: Optional[Dict[str, Dict[str, str]]] = Field(None, description="Prompts used in each step")

