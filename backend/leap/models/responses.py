from typing import Dict, Optional, List, Literal
from pydantic import BaseModel, Field

class ManimCodeResponse(BaseModel):
    code: str = Field(..., description="The complete, valid Python code for the Manim animation")
    explanation: Optional[str] = Field(None, description="Explanation of the code or changes made")
    error_fixes: Optional[List[str]] = Field(None, description="List of errors fixed in the code")
    fixed_issues: Optional[List[Dict[str, str]]] = Field(None, description="Detailed information about each fixed issue")
    validation_checks: Optional[List[str]] = Field(None, description="List of validation checks performed on the code")

class ScenePlanResponse(BaseModel):
    """Model for scene planning response."""
    plan: str = Field(..., description="The detailed plan for the animation scenes")
    reasoning: Optional[str] = Field(None, description="Reasoning behind the scene planning decisions")

class CodeIssue(BaseModel):
    """Model for a code issue found during validation."""
    message: str = Field(..., description="Description of the issue")
    severity: str = Field(..., description="Severity of the issue: 'error', 'warning', or 'info'")
    line_number: Optional[int] = Field(None, description="Line number where the issue was found")
    suggestion: Optional[str] = Field(None, description="Suggestion for fixing the issue")

class CodeValidationResult(BaseModel):
    """Model for code validation results."""
    is_valid: bool = Field(..., description="Whether the code is valid")
    issues: List[CodeIssue] = Field(default_factory=list, description="List of issues found in the code")

class ValidationResult(BaseModel):
    """Model for input validation results."""
    classification: Literal["VALID", "NEEDS_CLARIFICATION", "INVALID"] = Field(
        ..., description="The classification of the input validation"
    )
    explanation: str = Field(
        ..., description="Explanation for why the input was classified this way"
    )
    suggestion: Optional[str] = Field(
        None, description="Suggestion for improving the input if needed"
    )
    reformulated_question: Optional[str] = Field(
        None, description="A clearer, reformulated version of the user's question that could be used internally"
    ) 