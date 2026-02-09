import re
from typing import Dict, Any, Optional

# from leap.workflow.state import GraphState
from leap.core.logging import setup_question_logger
from leap.models import ManimCodeResponse
from leap.services import LLMService
from leap.workflow.utils import log_state_transition, get_manim_api_context
from leap.prompts import CODE_GENERATION_PROMPTS
from leap.prompts.base import PromptVersion

def read_gcf_example() -> str:
    """Read the GCF example from templates."""
    from pathlib import Path
    
    # Get the path to the GCF example file
    template_path = Path(__file__).parent.parent.parent / "templates" / "examples" / "gcf.py"
    
    # Read the file content
    with open(template_path, "r") as f:
        content = f.read()
    
    return content

def _sanitize_generated_code(code: str) -> str:
    """
    Clean and validate the generated code.
    Replace Tex with MathTex and ensure proper color usage.
    """
    # Replace quoted color strings with color constants
    # This regex looks for color parameters in constructors that are quoted strings
    color_params = ['color', 'fill_color', 'stroke_color', 'background_stroke_color']
    for param in color_params:
        code = re.sub(
            rf'{param}=\s*[\'"]([A-Za-z_]+)[\'"](?=\s*[,)])',
            lambda m: f'{param}={m.group(1).upper()}',  # Convert to uppercase to match Manim constants
            code
        )
    
    # Replace .set_color("blue") with .set_color(BLUE)
    # This regex looks for a set_color call with a quoted string
    code = re.sub(
        r'\.set_color\(\s*[\'"]([A-Za-z_]+)[\'"]\s*\)',
        lambda m: f'.set_color({m.group(1).upper()})',  # Convert to uppercase to match Manim constants
        code
    )
    
    # Replace Tex with MathTex for mathematical expressions
    # This regex looks for Tex constructor calls that are not part of a larger name (like MathTex)
    code = re.sub(
        r'(?<![A-Za-z])Tex\s*\(',
        'MathTex(',
        code
    )
    
    return code

def generate_code(
    state: Dict[str, Any],
    llm_service: Optional[LLMService] = None
) -> Dict[str, Any]:
    """Generate Manim code based on the plan using structured output.
    
    Args:
        state: The current workflow state
        llm_service: Optional LLM service for dependency injection
        
    Returns:
        The updated workflow state
    """
    logger = setup_question_logger(state["user_input"])
    logger.info("Generating Manim code from plan")
    
    # Check for Mock Mode - bypass LLM generation
    from leap.core.config import MOCK_MODE
    if MOCK_MODE:
        from leap.services.mock_llm_service import MockLLMService
        logger.info("MOCK MODE ENABLED: Skipping LLM generation.")
        mock_code = MockLLMService().generate_code()
        return {
            **state, 
            "generated_code": mock_code,
            "correction_attempts": 0
        }
    
    api_context = get_manim_api_context()
    
    # Use provided service or create a new one
    llm_service = llm_service or LLMService()
    
    try:
        # Get user level from state
        user_level = state.get("user_level", "normal")
        
        # Create a user level instruction
        user_level_instruction = ""
        if user_level == "ELI5":
            user_level_instruction = "The explanation should be suitable for a 5-year-old. Use very simple words, fun stories, colorful examples, and pictures that a small child would understand. Avoid any complicated words. Compare ideas to things children experience in daily life like toys, animals, or family activities."
        elif user_level == "advanced":
            user_level_instruction = "The explanation should be suitable for an advanced student. You can use appropriate terminology and go into technical details."
        else:  # normal
            user_level_instruction = "The explanation should be suitable for a high school/early college student. You can use appropriate terminology but still make it accessible."
        
        # Add duration instruction
        duration_instruction = "The animation should be 1-2 minutes long, so keep it concise and focused."
        
        # Get example code for one-shot learning
        example_code = read_gcf_example()
        # TODO: It should search and fetch the most relevant example code for the topic
        logger.info("Using GCF example for one-shot learning")
        
        # Create a code template with proper color usage
        code_template = f"""
from manim import *
from leap.templates.base_scene import ManimVoiceoverBase

class SCENE_NAME(ManimVoiceoverBase):
    # IMPORTANT: NEVER create backgrounds - the base class already provides one
    # DO NOT use Rectangle or any shape that covers the entire screen as a background
    # IMPORTANT: Always use color constants (e.g., BLUE) from manim, never use strings (e.g., "blue").
    # IMPORTANT: Use MathTex for mathematical expressions, NEVER use Tex
    def construct(self):
        # Call each scene method in sequence
        self.introduction()
        self.explain_concept()
        self.show_example()
        self.summarize()
        
    def introduction(self):
        # Create a title with standard text colors
        title = self.create_title("Your Title Here")  # title introducing the topic
        subtitle = self.create_subtitle("Your Subtitle Here")  # subtitle describing what the topic means
        subtitle.next_to(title, DOWN)
        group = VGroup(title, subtitle)
        self.ensure_group_visible(group, margin=0.5)
        
        with self.voiceover(text="Your narration here") as tracker:
            self.play(Write(title), Write(subtitle), run_time=tracker.duration)
        
        # Clean up the scene when done
        self.fade_out_scene()
        
    def explain_concept(self):
        # Your concept explanation here
        # Create mathematical expressions using MathTex, not Tex
        equation = MathTex(r"E = mc^2")
        
        # Example of proper color usage:
        # 1. Using standard color combinations
        highlight_box = Rectangle(
            color=YELLOW,  # Use color constants, not strings
            fill_opacity=0.3,
            stroke_width=2
        )
        highlight_box.surround(equation)
        
        # 2. Using named colors for emphasis
        circle = Circle(radius=0.5, color=BLUE)  # Use color constants, not strings
        square = Square(side_length=1, color=RED)  # Use color constants, not strings
        
        # 3. Setting colors after creation
        circle.set_fill(color=BLUE, opacity=0.5)  # Use color constants, not strings
        square.set_stroke(color=RED, width=2)  # Use color constants, not strings
        
        with self.voiceover(text="Your narration here") as tracker:
            self.play(Write(equation), run_time=tracker.duration)
        
        # Clean up the scene when done
        self.fade_out_scene()
        
    def show_example(self):
        # Your example here
        pass
        
        # Clean up the scene when done
        self.fade_out_scene()
        
    def summarize(self):
        # Your summary here
        pass
        
        # Clean up the scene when done
        self.fade_out_scene()
"""
        
        # Format the prompt with our parameters
        formatted_prompt = CODE_GENERATION_PROMPTS.get(PromptVersion.PRODUCTION).format(
            user_input=state["user_input"],
            plan=state["plan"],
            user_level_instruction=user_level_instruction,
            duration_instruction=duration_instruction,
            code_template=code_template,
            example_code=example_code
        )
        
        # Store the prompts in the state for tracing
        if "prompts" not in state:
            state["prompts"] = {}
        state["prompts"]["generation"] = {
            "system": formatted_prompt["system"],
            "user": formatted_prompt["user"]
        }
        
        # Generate the code with structured output
        logger.info("Generating code with Instructor...")
        response = llm_service.generate_structured_response(
            system_content=formatted_prompt["system"],
            user_content=formatted_prompt["user"],
            response_model=ManimCodeResponse
        )
        
        # Sanitize the generated code
        sanitized_code = _sanitize_generated_code(response.code)
        
        # Log code generation success
        code_lines = sanitized_code.split("\n")
        logger.info(f"Code generation successful: {len(code_lines)} lines of code")
        
        # Process the response
        output_state = {
            **state, 
            "generated_code": sanitized_code,
            "correction_attempts": 0
        }
        
        # Log explanation if provided
        if response.explanation:
            explanation = response.explanation
            if len(explanation) > 200:
                explanation = explanation[:197] + "..."
            logger.info(f"Code generation explanation: {explanation}")
        
        return log_state_transition("generate_code", state, output_state)
    
    except Exception as e:
        error_msg = f"Code generation failed: {str(e)}"
        logger.error(error_msg)
        return {
            **state,
            "error": error_msg,
            "generated_code": state.get("generated_code")
        } 