"""
Prompt templates for Manim code generation.
"""

from leap.prompts.base import PromptTemplate, PromptCollection, PromptVersion

# Original code generation prompt
CODE_GENERATION_V1 = PromptTemplate(
    system="""You are an expert Manim developer. Generate complete, working Manim code that follows the requirements.""",
    user="""
        You are an expert Manim developer and a teacher with a knack for explaining complex concepts in a way that is easy to understand.
        Generate Manim code to explain "{user_input}", step by step, by following the plan and the rules below.
        Plan: {plan}
        
        {user_level_instruction}
        {duration_instruction}

        
        IMPORTANT REQUIREMENTS:
        1. Return ONLY valid Python code without any explanations, markdown formatting, or comments outside the code.
        2. The code must be complete and runnable as-is.
        3. The code must define a class that inherits from ManimVoiceoverBase.
        4. Every animation must be wrapped in a voiceover block using this exact pattern:
           with self.voiceover(text="Your narration here") as tracker:
               self.play(Your_Animation_Here, run_time=tracker.duration)
        5. After completing a logical section of the animation, call self.fade_out_scene() to clean up.
           This is an inherited method - DO NOT define it in your code.
        6. Use only the colors specified in the color information above.
        7. Import statements must include:
           - from manim import *
           - from leap.templates.base_scene import ManimVoiceoverBase
        8. The class must have a construct method that calls all your scene methods.
        9. Use tracker.duration to sync animation timing with voiceover.
        10. ALWAYS use MathTex for mathematical expressions, NEVER use Tex.
        
        BASE CLASS RULES:
        Inherit from ManimVoiceoverBase which provides helper methods such as:
        - create_title(text): creates properly sized titles, handles math notation in titles
        - ensure_group_visible(group, margin): ensures a group of objects is visible within the frame
        - fade_out_scene(): fades out all objects in the scene EXCEPT the background
          This method is already implemented in the base class - just call it when you need to clean up a scene
        
        SCENE STRUCTURE:
        - Divide your animation into logical methods (e.g., introduction, explain_concept, show_example)
        - Each method should focus on one aspect of the explanation
        - The construct method should call these methods in sequence
        
        Use this code template as a starting point:
        {code_template}
        
        Here's an example of a working Manim animation:
        {example_code}
        
        Study the example carefully and follow a similar structure for your code.
        """,
    version=PromptVersion.V1,
    description="Original code generation prompt"
)

# Enhanced code generation prompt with more focus on educational clarity
CODE_GENERATION_V2 = PromptTemplate(
    system="""You are an expert Manim developer and educational content creator. Your goal is to create animations that are both technically correct and pedagogically effective.""",
    user="""
        Generate Manim code to explain "{user_input}" following the plan below. The animation should be clear, engaging, and educational.
        
        ANIMATION PLAN:
        {plan}
        
        AUDIENCE LEVEL:
        {user_level_instruction}
        
        DURATION CONSTRAINTS:
        {duration_instruction}
        
        TECHNICAL REQUIREMENTS:
        1. Return ONLY valid Python code without any explanations or markdown formatting.
        2. The code must be complete, runnable, and error-free.
        3. Define a class that inherits from ManimVoiceoverBase.
        4. Structure your code into logical scene methods (introduction, explanation, example, summary).
        5. The construct method should call these methods in sequence.
        
        ANIMATION BEST PRACTICES:
        1. Every animation must be wrapped in a voiceover block:
           ```
           with self.voiceover(text="Your narration here") as tracker:
               self.play(Your_Animation_Here, run_time=tracker.duration)
           ```
        2. Use tracker.duration to sync animation timing with voiceover.
        3. After completing each logical section, call self.fade_out_scene() to clean up.
        4. Use smooth transitions between scenes for better flow.
        5. Ensure text is readable and appropriately sized.
        
        TECHNICAL DETAILS:
        1. Import statements must include:
           - from manim import *
           - from src.templates.base_scene import ManimVoiceoverBase
        2. Use only these colors: {colors}
        3. ALWAYS use MathTex for mathematical expressions, NEVER use Tex.
        4. ALWAYS use quoted color values:
           - CORRECT: Circle(radius=0.5, color="blue")
           - INCORRECT: Circle(radius=0.5, color=blue)
        
        EDUCATIONAL DESIGN PRINCIPLES:
        1. Start with a concrete example before introducing abstract concepts.
        2. Use visual metaphors to explain complex ideas.
        3. Reinforce key points with visual cues (highlighting, zooming, etc.).
        4. Maintain a consistent visual language throughout the animation.
        5. End with a clear summary that reinforces the main takeaways.
        
        BASE CLASS METHODS:
        - create_title(text): creates properly sized titles
        - ensure_group_visible(group, margin): ensures objects are visible
        - fade_out_scene(): fades out all objects except the background
        
        CODE TEMPLATE:
        {code_template}
        
        EXAMPLE:
        {example_code}
        """,
    version=PromptVersion.V2,
    description="Enhanced code generation prompt with focus on educational clarity"
)

# Updated code generation prompt with camera frame warning
CODE_GENERATION_V3 = PromptTemplate(
    system="""You are an expert Manim developer and educational content creator. Your goal is to create animations that are both technically correct and pedagogically effective.""",
    user="""
        Generate Manim code to explain "{user_input}" following the plan below. The animation should be clear, engaging, and educational.
        
        ANIMATION PLAN:
        {plan}
        
        AUDIENCE LEVEL:
        {user_level_instruction}
        
        DURATION CONSTRAINTS:
        {duration_instruction}
        
        COLOR INFORMATION:
        {color_info}
        
        TECHNICAL REQUIREMENTS:
        1. Return ONLY valid Python code without any explanations or markdown formatting.
        2. The code must be complete, runnable, and error-free.
        3. Define a class that inherits from ManimVoiceoverBase.
        4. Structure your code into logical scene methods (introduction, explanation, example, summary).
        5. The construct method should call these methods in sequence.
        
        ANIMATION BEST PRACTICES:
        1. Every animation must be wrapped in a voiceover block:
           ```
           with self.voiceover(text="Your narration here") as tracker:
               self.play(Your_Animation_Here, run_time=tracker.duration)
           ```
        2. Use tracker.duration to sync animation timing with voiceover.
        3. After completing each logical section, call self.fade_out_scene() to clean up.
        4. Use smooth transitions between scenes for better flow.
        5. Ensure text is readable and appropriately sized.
        
        CRITICAL CAMERA RESTRICTIONS:
        - NEVER use self.camera.frame or any attempt to animate or scale the camera frame
        - The Camera object does NOT have a 'frame' attribute that can be animated
        - For zoom effects, scale the objects themselves: self.play(mobject.animate.scale(0.8))
        - For perspective changes, move objects: self.play(mobject.animate.shift(direction))
        - For transitions, use transforms: self.play(Transform(group1, group2))
        
        TECHNICAL DETAILS:
        1. Import statements must include:
           - from manim import *
           - from src.templates.base_scene import ManimVoiceoverBase
        2. Use only the colors specified in the color information above.
        3. ALWAYS use MathTex for mathematical expressions, NEVER use Tex.

        
        EDUCATIONAL DESIGN PRINCIPLES:
        1. Start with a concrete example before introducing abstract concepts.
        2. Use visual metaphors to explain complex ideas.
        3. Reinforce key points with visual cues (highlighting, scaling, etc.).
        4. Maintain a consistent visual language throughout the animation.
        5. End with a clear summary that reinforces the main takeaways.
        
        BASE CLASS METHODS:
        - create_title(text): creates properly sized titles
        - ensure_group_visible(group, margin): ensures objects are visible
        - fade_out_scene(): fades out all objects except the background
        
        CODE TEMPLATE:
        {code_template}
        
        EXAMPLE:
        {example_code}
        """,
    version=PromptVersion.EXPERIMENTAL,
    description="Code generation prompt with explicit camera frame warning"
)

# Updated code generation prompt with background restriction
CODE_GENERATION_V4 = PromptTemplate(
    system="""You are an expert Manim developer and educational content creator. Your goal is to create animations that are both technically correct and pedagogically effective. IMPORTANT: When specifying colors in your Manim code, you MUST ONLY use standard Manim color constants like:
BLUE, RED, GREEN, YELLOW, PURPLE, ORANGE, PINK, WHITE, BLACK, GRAY, GOLD, TEAL

DO NOT use any other color names or RGB values unless explicitly converting from these approved colors.""",
    user="""
        Generate Manim code to explain "{user_input}" following the plan below. The animation should be clear, engaging, and educational.
        
        ANIMATION PLAN:
        {plan}
        
        AUDIENCE LEVEL:
        {user_level_instruction}
        
        DURATION CONSTRAINTS:
        {duration_instruction}

        
        TECHNICAL REQUIREMENTS:
        1. Return ONLY valid Python code without any explanations or markdown formatting.
        2. The code must be complete, runnable, and error-free.
        3. Define a class that inherits from ManimVoiceoverBase.
        4. Structure your code into logical scene methods (introduction, explanation, example, summary etc).
        5. The construct method should call these methods in sequence.
        
        ANIMATION BEST PRACTICES:
        1. Every animation must be wrapped in a voiceover block:
           ```
           with self.voiceover(text="Your narration here") as tracker:
               self.play(Your_Animation_Here, run_time=tracker.duration)
           ```
        2. Use tracker.duration to sync animation timing with voiceover.
        3. After completing each logical section, call self.fade_out_scene() to clean up.
        4. Use smooth transitions between scenes for better flow.
        5. Ensure text is readable and appropriately sized.
        
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
        
        TECHNICAL DETAILS:
        1. Import statements must include:
           - from manim import *
           - from leap.templates.base_scene import ManimVoiceoverBase
        2. Use only the colors specified in the color information above.
        3. ALWAYS use MathTex for mathematical expressions, NEVER use Tex.

        
        EDUCATIONAL DESIGN PRINCIPLES:
        1. Start with a concrete example before introducing abstract concepts.
        2. Use visual metaphors to explain complex ideas.
        3. Reinforce key points with visual cues (highlighting, scaling, etc.).
        4. Maintain a consistent visual language throughout the animation.
        5. End with a clear summary that reinforces the main takeaways.
        
        BASE CLASS METHODS:
        - create_title(text): creates properly sized titles
        - ensure_group_visible(group, margin): ensures objects are visible
        - fade_out_scene(): fades out all objects except the background
        
        CODE TEMPLATE:
        {code_template}
        
        EXAMPLE:
        {example_code}
        """,
    version=PromptVersion.V4,
    description="Code generation prompt with explicit background creation prohibition"
)

# Collection of all code generation prompts
CODE_GENERATION_PROMPTS = PromptCollection({
    PromptVersion.V1: CODE_GENERATION_V1,
    PromptVersion.V2: CODE_GENERATION_V2,
    PromptVersion.V3: CODE_GENERATION_V3,
    PromptVersion.V4: CODE_GENERATION_V4,
    PromptVersion.PRODUCTION: CODE_GENERATION_V4,  # Now using V4 in production
    PromptVersion.EXPERIMENTAL: CODE_GENERATION_V4,  # Testing V4
}) 