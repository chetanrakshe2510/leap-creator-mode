"""
Prompt templates for error correction in Manim code.
"""

from leap.prompts.base import PromptTemplate, PromptCollection, PromptVersion

# Original error correction prompt
ERROR_CORRECTION_V1 = PromptTemplate(
    system="""You are an expert Manim developer. Fix the code based on the error messags while maintaining the original animation intent.""",
    user="""
        Requirements:
        1. Code must define a Scene class that inherits from ManimVoiceoverBase
        2. Use only valid Manim methods and attributes from the following API documentation: {manim_api_context}
        3. Follow proper Python syntax
        4. Return valid Python code that fixes the identified issues
        5. The code must be complete and runnable as-is
        6. After completing a logical section of the animation, call self.fade_out_scene() to clean up
           This is an inherited method - DO NOT define it in your code
        7. Every animation must be wrapped in a voiceover block using this exact pattern:
           with self.voiceover(text="Your narration here") as tracker:
               self.play(Your_Animation_Here, run_time=tracker.duration)
        8. ALWAYS use MathTex for mathematical expressions, NEVER use Tex

        
        IMPORTANT ABOUT fade_out_scene():
        - This method is already implemented in the ManimVoiceoverBase class
        - It fades out all objects in the scene EXCEPT the background
        - You should NOT define this method in your code, just call it when you need to clean up a scene
        - Methods that create animations should generally end with self.fade_out_scene()
        
        COMMON ERRORS TO CHECK FOR:
        - Using Tex instead of MathTex for mathematical expressions
        - Using unquoted color values (e.g., color=blue instead of color="blue")
        - Missing or incorrect imports
        - Missing voiceover blocks around animations
        - Not calling fade_out_scene() after completing a logical section
        
        Error: {error}
        
        Original code:
        {generated_code}
        
        Original plan:
        {plan}
        
        IMPORTANT: Only use the following colors exactly as defined: {colors}
        
        In your response, include:
        1. The complete fixed code
        2. An explanation of what was fixed
        3. A list of specific errors that were addressed
        4. A list of validation checks you performed on the code
        """,
    version=PromptVersion.V1,
    description="Original error correction prompt"
)

# Enhanced error correction prompt with more structured approach
ERROR_CORRECTION_V2 = PromptTemplate(
    system="""You are an expert Manim developer and debugging specialist. Your task is to fix code errors while preserving the educational intent of the animation.""",
    user="""
        Fix the following Manim code that has encountered errors. Maintain the original educational intent while making it technically correct.
        
        ERROR DETAILS:
        {error}
        
        ORIGINAL ANIMATION PLAN:
        {plan}
        
        ORIGINAL CODE:
        {generated_code}
        
        DEBUGGING APPROACH:
        1. First identify the root cause of the error
        2. Fix the immediate issue
        3. Check for related issues that might cause problems
        4. Verify the fix doesn't break other parts of the code
        5. Ensure the educational intent is preserved
        
        TECHNICAL REQUIREMENTS:
        1. The code must define a class that inherits from ManimVoiceoverBase
        2. All animations must be wrapped in voiceover blocks:
           ```
           with self.voiceover(text="...") as tracker:
               self.play(..., run_time=tracker.duration)
           ```
        3. Call self.fade_out_scene() at the end of each logical section
        4. Use only these colors: {colors}
        5. Always use quoted color values (color="blue", not color=blue)
        6. Use MathTex for mathematical expressions, not Tex
        7. Include all necessary imports:
           - from manim import *
           - from src.templates.base_scene import ManimVoiceoverBase
        
        MANIM API CONTEXT:
        {manim_api_context}
        
        RESPONSE FORMAT:
        Return a structured response with:
        1. Complete fixed code (ready to run without modifications)
        2. Explanation of what was fixed
        3. List of specific errors addressed
        4. Validation checks performed
        """,
    version=PromptVersion.V2,
    description="Enhanced error correction prompt with structured debugging approach"
)

# Updated error correction prompt with camera frame warning
ERROR_CORRECTION_V3 = PromptTemplate(
    system="""You are an expert Manim developer and debugging specialist. Your task is to fix code errors while preserving the educational intent of the animation.""",
    user="""
        Fix the following Manim code that has encountered errors. Maintain the original educational intent while making it technically correct.
        
        ERROR DETAILS:
        {error}
        
        ORIGINAL ANIMATION PLAN:
        {plan}
        
        ORIGINAL CODE:
        {generated_code}
        
        DEBUGGING APPROACH:
        1. First identify the root cause of the error
        2. Fix the immediate issue
        3. Check for related issues that might cause problems
        4. Verify the fix doesn't break other parts of the code
        5. Ensure the educational intent is preserved
        
        TECHNICAL REQUIREMENTS:
        1. The code must define a class that inherits from ManimVoiceoverBase
        2. All animations must be wrapped in voiceover blocks:
           ```
           with self.voiceover(text="...") as tracker:
               self.play(..., run_time=tracker.duration)
           ```
        3. Call self.fade_out_scene() at the end of each logical section
        4. Use only these colors: {colors}
        5. Always use quoted color values (color="blue", not color=blue)
        6. Use MathTex for mathematical expressions, not Tex
        7. Include all necessary imports:
           - from manim import *
           - from src.templates.base_scene import ManimVoiceoverBase
        
        CRITICAL CAMERA RESTRICTIONS:
        - NEVER use self.camera.frame or any attempt to animate or scale the camera frame
        - The Camera object does NOT have a 'frame' attribute that can be animated
        - Instead of camera frame manipulation, use these alternatives:
          * Scale the objects themselves: self.play(mobject.animate.scale(0.8))
          * Move objects: self.play(mobject.animate.shift(direction))
          * Group and transform objects: self.play(Transform(group1, group2))
        
        MANIM API CONTEXT:
        {manim_api_context}
        
        RESPONSE FORMAT:
        Return a structured response with:
        1. Complete fixed code (ready to run without modifications)
        2. Explanation of what was fixed
        3. List of specific errors addressed
        4. Validation checks performed
        """,
    version=PromptVersion.EXPERIMENTAL,
    description="Error correction prompt with explicit camera frame warning"
)

# Updated error correction prompt with background restriction and removed manim api context
ERROR_CORRECTION_V4 = PromptTemplate(
    system="""You are an expert Manim developer and debugging specialist. Your task is to fix code errors while preserving the educational intent of the animation.""",
    user="""
        Fix the following Manim code that has encountered errors. Maintain the original educational intent while making it technically correct.
        
        ERROR DETAILS:
        {error}
        
        ORIGINAL ANIMATION PLAN:
        {plan}
        
        ORIGINAL CODE:
        {generated_code}
        
        DEBUGGING APPROACH:
        1. First identify the root cause of the error
        2. Fix the immediate issue
        3. Check for related issues that might cause problems
        4. Verify the fix doesn't break other parts of the code or recreate previous errors
        5. Ensure the educational intent is preserved
        6. See if the code is using deprecated or removed methods and update it accordingly, here are some of the breaking changes: {manim_api_context}
        
        
        CRITICAL RESTRICTIONS:
        - NEVER create any background rectangles, images, or shapes that cover the entire screen
        - The base class already provides a background image - do not create your own
        - NEVER use Rectangle, ImageMobject, or any other object as a full-screen background
        - NEVER use self.camera.background or try to modify the camera background
        - NEVER use self.camera.frame or any attempt to animate or scale the camera frame
        - The Camera object does NOT have a 'frame' attribute that can be animated
        - For zoom effects, scale the objects themselves: self.play(mobject.animate.scale(0.8))
        - For perspective changes, move objects: self.play(mobject.animate.shift(direction))
        - For transitions, use transforms: self.play(Transform(group1, group2))
        
        
        RESPONSE FORMAT:
        Return a structured response with:
        1. Complete fixed code (ready to run without modifications)
        2. Explanation of what was fixed
        3. List of specific errors addressed
        4. Validation checks performed
        """,
    version=PromptVersion.V4,
    description="Error correction prompt with explicit background creation prohibition"
)

# Collection of all error correction prompts
ERROR_CORRECTION_PROMPTS = PromptCollection({
    PromptVersion.V1: ERROR_CORRECTION_V1,
    PromptVersion.V2: ERROR_CORRECTION_V2,
    PromptVersion.V3: ERROR_CORRECTION_V3,
    PromptVersion.V4: ERROR_CORRECTION_V4,
    PromptVersion.PRODUCTION: ERROR_CORRECTION_V4,  # Now using V4 in production
    PromptVersion.EXPERIMENTAL: ERROR_CORRECTION_V4,  # Testing V4
}) 