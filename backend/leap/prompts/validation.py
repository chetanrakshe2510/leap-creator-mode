"""
Prompt templates for code validation.
"""

from leap.prompts.base import PromptTemplate, PromptCollection, PromptVersion

# Basic validation prompt
VALIDATION_V1 = PromptTemplate(
    system="""You are an expert Manim developer and code validator. Your task is to validate Manim code for correctness and adherence to best practices.""",
    user="""
        Validate the following Manim code for correctness and adherence to best practices.
        
        CODE TO VALIDATE:
        {code}
        
        VALIDATION CRITERIA:
        1. The code must define a class that inherits from ManimVoiceoverBase
        2. The class must have a construct method
        3. All animations must be wrapped in voiceover blocks
        4. Each logical section should end with self.fade_out_scene()
        5. Color values must be quoted (e.g., color="blue", not color=blue)
        6. Mathematical expressions must use MathTex, not Tex
        7. Required imports must be present
        
        RESPONSE FORMAT:
        Return a structured validation result with:
        1. Whether the code is valid (true/false)
        2. A list of issues found (if any)
        3. Suggestions for fixing each issue
        """,
    version=PromptVersion.V1,
    description="Basic code validation prompt"
)

# Enhanced validation prompt with more detailed checks
VALIDATION_V2 = PromptTemplate(
    system="""You are an expert Manim developer, code validator, and educational content specialist. Your task is to perform a comprehensive validation of Manim code for technical correctness, educational effectiveness, and adherence to best practices.""",
    user="""
        Perform a comprehensive validation of the following Manim code, checking for technical correctness, educational effectiveness, and adherence to best practices.
        
        CODE TO VALIDATE:
        {code}
        
        TECHNICAL VALIDATION:
        1. Syntax correctness and Python best practices
        2. Proper inheritance from ManimVoiceoverBase
        3. Required imports (manim, ManimVoiceoverBase)
        4. Use of MathTex for mathematical expressions
        
        STRUCTURAL VALIDATION:
        1. Presence of construct method
        2. Logical organization into scene methods
        3. Proper method calls in construct
        4. Appropriate use of self.fade_out_scene() at the end of sections
        
        EDUCATIONAL VALIDATION:
        1. All animations wrapped in voiceover blocks for narration
        2. Appropriate pacing and timing
        3. Clear visual hierarchy and readability
        4. Logical flow of concepts
        5. Effective use of visual elements to support learning
        
        RESPONSE FORMAT:
        Return a structured validation result with:
        1. Overall validity assessment (valid/invalid)
        2. Categorized list of issues (technical, structural, educational)
        3. Severity level for each issue (error, warning, suggestion)
        4. Specific recommendations for addressing each issue
        5. General suggestions for improving the animation
        """,
    version=PromptVersion.V2,
    description="Enhanced code validation prompt with educational effectiveness checks"
)

# Collection of all validation prompts
VALIDATION_PROMPTS = PromptCollection({
    PromptVersion.V1: VALIDATION_V1,
    PromptVersion.V2: VALIDATION_V2,
    PromptVersion.PRODUCTION: VALIDATION_V2,  # Currently using V2 in production
    PromptVersion.EXPERIMENTAL: VALIDATION_V1,  # Testing V1
}) 