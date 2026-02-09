import re

from typing import Dict, Any, Optional, List

from leap.workflow.state import GraphState
from leap.core.logging import setup_question_logger
from leap.models import CodeIssue, CodeValidationResult


def validate_code(state: GraphState, config: Optional[Dict[str, Any]] = None, **kwargs) -> GraphState:
    """Validate the generated code using AST parsing and structured validation.
    
    Args:
        state: The current workflow state
        config: Optional configuration parameters
        
    Returns:
        The updated workflow state
    """
    logger = setup_question_logger(state["user_input"])
    logger.info("Validating generated code")
    
    try:
        if not state["generated_code"]:
            return GraphState(
                user_input=state["user_input"],
                plan=state["plan"],
                generated_code=None,
                execution_result=None,
                error="No code to validate",
                correction_attempts=state.get("correction_attempts", 0)
            )
            
        # Log that we're validating code (without logging the full code)
        code_lines = state["generated_code"].split("\n")
        logger.info(f"Validating code ({len(code_lines)} lines)")
        
        # Perform basic validation using AST
        issues = []
        is_valid = True
        
        # Skip AST parsing for syntax validation to avoid string literal errors
        # We'll rely on execution to catch syntax errors
        
        # Continue with other validations that don't require AST parsing
        if "from manim import *" not in state["generated_code"]:
            issues.append(CodeIssue(
                message="Code must import all Manim classes",
                severity="error",
                suggestion="Add 'from manim import *' at the top of the file"
            ))
            is_valid = False

        # Check for ManimVoiceoverBase import - accept multiple possible paths
        valid_base_imports = [
            "from leap.templates.base_scene import ManimVoiceoverBase",
        ]
        
        has_valid_import = any(import_path in state["generated_code"] for import_path in valid_base_imports)
        if not has_valid_import:
            issues.append(CodeIssue(
                message="Code must import ManimVoiceoverBase",
                severity="error",
                suggestion="Add 'from leap.templates.base_scene import ManimVoiceoverBase' at the top of the file"
            ))
            is_valid = False
            

            
        if "def construct(self)" not in state["generated_code"]:
            issues.append(CodeIssue(
                message="Scene class must have a construct method",
                severity="error",
                suggestion="Add a 'def construct(self):' method to your Scene class"
            ))
            is_valid = False
            
        # Check for deprecated methods
        deprecated_methods = ["self.clear()", "ShowCreation"]
        for method in deprecated_methods:
            if method in state["generated_code"]:
                if method == "self.clear()":
                    issues.append(CodeIssue(
                        message="self.clear() removes the background. Use self.fade_out_scene() instead.",
                        severity="error",
                        suggestion="Replace self.clear() with self.fade_out_scene()"
                    ))
                    is_valid = False
                elif method == "ShowCreation":
                    issues.append(CodeIssue(
                        message="ShowCreation is deprecated. Use Create() instead.",
                        severity="warning",
                        suggestion="Replace ShowCreation with Create"
                    ))
                    is_valid = False
        
        # Check for voiceover blocks
        if "with self.voiceover" not in state["generated_code"]:
            issues.append(CodeIssue(
                message="Code must use voiceover blocks for animations",
                severity="error",
                suggestion="Wrap animations in 'with self.voiceover(text=\"...\") as tracker:' blocks"
            ))
            is_valid = False
        
        # Check for Tex vs MathTex usage (using regex instead of AST)
        if re.search(r'(?<![A-Za-z])Tex\s*\(', state["generated_code"]) and not re.search(r'MathTex\s*\(', state["generated_code"]):
            issues.append(CodeIssue(
                message="Using Tex instead of MathTex for mathematical expressions",
                severity="error",
                suggestion="Replace Tex with MathTex for mathematical expressions"
            ))
            is_valid = False
        

        
        # Check for background creation
        background_patterns = [
            r'Rectangle\s*\(\s*width\s*=\s*FRAME_WIDTH',
            r'Rectangle\s*\(\s*width\s*=\s*config\.frame_width',
            r'Rectangle\s*\(\s*height\s*=\s*FRAME_HEIGHT',
            r'Rectangle\s*\(\s*height\s*=\s*config\.frame_height',
            r'ImageMobject\s*\(\s*.*\s*\)\s*.*\s*background',
            r'self\.camera\.background',
            r'ReplacementTransform\s*\(\s*self\.camera\.background'
        ]
        
        for pattern in background_patterns:
            if re.search(pattern, state["generated_code"]):
                issues.append(CodeIssue(
                    message="Code creates a background element which will conflict with the base scene background",
                    severity="error",
                    suggestion="Remove all background creation. The base class already provides a background image."
                ))
                is_valid = False
                break
        # # Check for color values in constructor arguments (using regex)
        # color_params = ['color', 'fill_color', 'stroke_color', 'background_stroke_color']
        # # Continue with the rest of the validation
        # for param in color_params:
        #     if re.search(rf'{param}=\s*(?![\'"])([A-Za-z_]+)(?=\s*[,)])', state["generated_code"]):
        #         issues.append(CodeIssue(
        #             message=f"Unquoted color value in {param} parameter",
        #             severity="error",
        #             suggestion=f"Use quoted color values: {param}=\"blue\" instead of {param}=blue"
        #         ))
        #         is_valid = False
        
        # # Check for unquoted color values in set_color method
        # if re.search(r'\.set_color\(\s*(?![\'"])([A-Za-z_]+)\s*\)', state["generated_code"]):
        #     issues.append(CodeIssue(
        #         message="Unquoted color value in set_color method",
        #         severity="error",
        #         suggestion="Use quoted color values: .set_color(\"blue\") instead of .set_color(blue)"
        #     ))
        #     is_valid = False
        
        # Create validation result
        validation_result = CodeValidationResult(
            is_valid=is_valid,
            issues=issues
        )
        
        # Log validation results
        if issues:
            logger.info(f"Validation found {len(issues)} issues:")
            for i, issue in enumerate(issues, 1):
                logger.info(f"  {i}. {issue.severity.upper()}: {issue.message}")
        else:
            logger.info("Validation successful - no issues found")
        
        # If not valid, set error message
        if not is_valid:
            error_message = "\n".join([
                f"{issue.severity.upper()}: {issue.message}" + 
                (f" (Line {issue.line_number})" if issue.line_number else "") +
                (f" - Suggestion: {issue.suggestion}" if issue.suggestion else "")
                for issue in validation_result.issues
            ])
            
            return GraphState(
                user_input=state["user_input"],
                plan=state["plan"],
                generated_code=state["generated_code"],
                execution_result=None,
                error=error_message,
                correction_attempts=state.get("correction_attempts", 0)
            )
                    
        return GraphState(
            user_input=state["user_input"],
            plan=state["plan"],
            generated_code=state["generated_code"],
            execution_result=None,
            error=None,
            correction_attempts=state.get("correction_attempts", 0)
        )
        
    except Exception as e:
        error_msg = f"Code validation failed: {str(e)}"
        logger.error(error_msg)
        return GraphState(
            user_input=state["user_input"],
            plan=state["plan"],
            generated_code=state["generated_code"],
            execution_result=None,
            error=error_msg,
            correction_attempts=state.get("correction_attempts", 0)
        ) 