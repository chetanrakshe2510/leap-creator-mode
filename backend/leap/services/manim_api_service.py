# import inspect
# import importlib
# import re
# from typing import Dict, List, Optional, Any, Set
# import logging

# import manim

# class ManimAPIService:
#     """Service for accessing Manim API information to assist with code generation and error correction."""
    
#     def __init__(self):
#         """Initialize the ManimAPIService."""
#         self.api_cache = {}
#         self.logger = logging.getLogger(__name__)
#         # Common Manim classes that are frequently used
#         self.common_classes = {
#             "Circle", "Square", "Rectangle", "Triangle", "Line", "Arrow", 
#             "Dot", "Text", "MathTex", "Tex", "VGroup", "Scene", "Mobject",
#             "Animation", "Transform", "Create", "FadeIn", "FadeOut", "Write",
#             "Arc", "ArcBetweenPoints", "CubicBezier", "DashedLine", "Polygon"
#         }
    
#     def get_class_info(self, class_name: str) -> Optional[Dict[str, Any]]:
#         """Get information about a Manim class.
        
#         Args:
#             class_name: The name of the class to look up
            
#         Returns:
#             Dictionary with class information or None if not found
#         """
#         if class_name in self.api_cache:
#             return self.api_cache[class_name]
        
#         try:
#             # Try to import the class from manim
#             manim = importlib.import_module("manim")
#             if hasattr(manim, class_name):
#                 cls = getattr(manim, class_name)
                
#                 # Get method signatures
#                 methods = {}
#                 for name, method in inspect.getmembers(cls, inspect.isfunction):
#                     if not name.startswith("_") or name == "__init__":
#                         try:
#                             signature = inspect.signature(method)
#                             methods[name] = {
#                                 "signature": str(signature),
#                                 "parameters": [param for param in signature.parameters],
#                                 "docstring": inspect.getdoc(method) or ""
#                             }
#                         except (ValueError, TypeError):
#                             # Some methods might not be inspectable
#                             pass
                
#                 # Get class docstring
#                 docstring = inspect.getdoc(cls) or ""
                
#                 # Store in cache
#                 self.api_cache[class_name] = {
#                     "docstring": docstring,
#                     "methods": methods
#                 }
                
#                 return self.api_cache[class_name]
            
#         except (ImportError, AttributeError) as e:
#             self.logger.warning(f"Could not find Manim class {class_name}: {str(e)}")
        
#         return None
    
#     def get_method_signature(self, class_name: str, method_name: str) -> Optional[str]:
#         """Get the signature of a specific method.
        
#         Args:
#             class_name: The name of the class
#             method_name: The name of the method
            
#         Returns:
#             Method signature as a string or None if not found
#         """
#         class_info = self.get_class_info(class_name)
#         if class_info and method_name in class_info["methods"]:
#             return class_info["methods"][method_name]["signature"]
#         return None
    
#     def extract_error_context(self, error_message):
#         """Extract context from error messages to identify relevant classes and methods."""
#         context = {}
        
#         # Extract class names from error messages
#         class_pattern = r"'([A-Za-z0-9_]+)' object"
#         class_matches = re.findall(class_pattern, error_message)
#         if class_matches:
#             context['class_name'] = class_matches[0]
        
#         # Extract method names from error messages
#         method_pattern = r"has no attribute '([A-Za-z0-9_]+)'"
#         method_matches = re.findall(method_pattern, error_message)
#         if method_matches:
#             context['missing_method'] = method_matches[0]
        
#         # Extract method names from error messages about wrong number of arguments
#         wrong_args_pattern = r"([A-Za-z0-9_]+)\(\) takes (\d+) positional arguments? but (\d+) (?:was|were) given"
#         wrong_args_matches = re.findall(wrong_args_pattern, error_message)
#         if wrong_args_matches:
#             method_name, expected, actual = wrong_args_matches[0]
#             context['method_name'] = method_name
#             context['expected_args'] = expected
#             context['actual_args'] = actual
        
#         # Extract method names from error messages about unexpected keyword arguments
#         unexpected_kwarg_pattern = r"([A-Za-z0-9_]+)\(\) got an unexpected keyword argument '([A-Za-z0-9_]+)'"
#         unexpected_kwarg_matches = re.findall(unexpected_kwarg_pattern, error_message)
#         if unexpected_kwarg_matches:
#             method_name, kwarg = unexpected_kwarg_matches[0]
#             context['method_name'] = method_name
#             context['invalid_kwarg'] = kwarg
            
#         # Extract undefined variables
#         undefined_var_pattern = r"NameError: name '([A-Za-z0-9_]+)' is not defined"
#         undefined_var_matches = re.findall(undefined_var_pattern, error_message)
#         if undefined_var_matches:
#             context['undefined_variable'] = undefined_var_matches[0]
            
#         # Extract module import errors
#         import_error_pattern = r"ImportError: No module named '([A-Za-z0-9_.]+)'"
#         import_error_matches = re.findall(import_error_pattern, error_message)
#         if import_error_matches:
#             context['missing_module'] = import_error_matches[0]
            
#         # Extract syntax errors
#         syntax_error_pattern = r"SyntaxError: (.*?) \(line (\d+)\)"
#         syntax_error_matches = re.findall(syntax_error_pattern, error_message)
#         if syntax_error_matches:
#             error_msg, line_num = syntax_error_matches[0]
#             context['syntax_error'] = error_msg
#             context['error_line'] = line_num
        
#         return context

#     def suggest_fix(self, error_message):
#         """Suggest a fix based on the error message."""
#         context = self.extract_error_context(error_message)
#         if not context:
#             return None
        
#         # Handle undefined variable errors
#         if 'undefined_variable' in context:
#             var_name = context['undefined_variable']
            
#             # Check for common Manim constants
#             if var_name in ['FRAME_WIDTH', 'FRAME_HEIGHT']:
#                 return (
#                     f"The constant '{var_name}' is not defined in current Manim versions. "
#                     f"Instead of using {var_name}, use specific values like 14 for width and 8 for height, "
#                     f"or use the FullScreenRectangle() class for a background that covers the entire screen. "
#                     f"Example: background = Rectangle(width=14, height=8, fill_opacity=1) or background = FullScreenRectangle()"
#                 )
#             elif var_name in ['UP', 'DOWN', 'LEFT', 'RIGHT', 'ORIGIN', 'OUT', 'IN']:
#                 return (
#                     f"The direction constant '{var_name}' needs to be imported from manim. "
#                     f"Make sure you have 'from manim import *' at the top of your file."
#                 )
#             elif var_name in ['PI', 'TAU', 'DEGREES', 'RADIANS']:
#                 return (
#                     f"The mathematical constant '{var_name}' needs to be imported from manim. "
#                     f"Make sure you have 'from manim import *' at the top of your file."
#                 )
#             elif var_name in ['RED', 'GREEN', 'BLUE', 'YELLOW', 'PURPLE', 'ORANGE', 'WHITE', 'BLACK']:
#                 return (
#                     f"The color constant '{var_name}' needs to be imported from manim. "
#                     f"Make sure you have 'from manim import *' at the top of your file. "
#                     f"Alternatively, use quoted color strings like \"red\", \"green\", etc."
#                 )
#             else:
#                 return f"The variable '{var_name}' is not defined. Check for typos or make sure it's defined before use."
        
#         # Handle missing method errors
#         elif 'class_name' in context and 'missing_method' in context:
#             class_name = context['class_name']
#             missing_method = context['missing_method']
            
#             # Check if the method name is similar to any existing method
#             if class_name in self.common_classes:
#                 try:
#                     class_obj = getattr(manim, class_name)
#                     methods = [method for method in dir(class_obj) if callable(getattr(class_obj, method)) and not method.startswith('_')]
                    
#                     # Find similar method names
#                     similar_methods = []
#                     for method in methods:
#                         if missing_method in method or method in missing_method:
#                             similar_methods.append(method)
                    
#                     # For dash-related methods, suggest specific styling methods
#                     if 'dash' in missing_method.lower():
#                         dash_alternatives = [m for m in methods if 'stroke' in m or 'style' in m or 'color' in m]
#                         if dash_alternatives:
#                             similar_methods.extend(dash_alternatives)
#                             # Add a note about DashedLine
#                             suggestion = f"The method '{missing_method}' does not exist for {class_name}. For dashed lines, use the DashedLine class instead of {class_name}. Alternatively, you can use these styling methods: {', '.join(set(similar_methods))}."
#                             return suggestion
                    
#                     if similar_methods:
#                         suggestion = f"The method '{missing_method}' does not exist for {class_name}. Did you mean one of these: {', '.join(set(similar_methods))}?"
#                         return suggestion
#                     else:
#                         # Get common methods that might be useful
#                         common_methods = ['set_color', 'set_fill', 'set_stroke', 'move_to', 'shift', 'scale', 'rotate']
#                         available_methods = [m for m in common_methods if m in methods]
                        
#                         if available_methods:
#                             suggestion = f"The method '{missing_method}' does not exist for {class_name}. Common methods you can use include: {', '.join(available_methods)}."
#                             return suggestion
#                         else:
#                             return f"The method '{missing_method}' does not exist for {class_name}. Check the documentation for available methods."
#                 except (AttributeError, ImportError):
#                     pass
        
#         # Handle wrong number of arguments errors
#         elif 'method_name' in context and 'expected_args' in context and 'actual_args' in context:
#             method_name = context['method_name']
#             expected = context['expected_args']
#             actual = context['actual_args']
            
#             # Try to find the method signature
#             for class_name in self.common_classes:
#                 try:
#                     class_obj = getattr(manim, class_name)
#                     if hasattr(class_obj, method_name) or class_name == method_name:
#                         # Handle constructor case
#                         if class_name == method_name:
#                             signature = str(inspect.signature(class_obj.__init__))
#                             return f"The {class_name} constructor takes {expected} positional arguments, but you provided {actual}. The correct signature is: {class_name}{signature}. Use keyword arguments for optional parameters."
#                         else:
#                             method = getattr(class_obj, method_name)
#                             signature = str(inspect.signature(method))
#                             return f"The method {class_name}.{method_name}{signature} takes {expected} arguments, but you provided {actual}."
#                 except (AttributeError, ImportError):
#                     continue
            
#             return f"The method {method_name}() takes {expected} arguments, but you provided {actual}. Check the documentation for the correct signature."
        
#         # Handle unexpected keyword argument errors
#         elif 'method_name' in context and 'invalid_kwarg' in context:
#             method_name = context['method_name']
#             invalid_kwarg = context['invalid_kwarg']
            
#             # Try to find the method signature
#             for class_name in self.common_classes:
#                 try:
#                     class_obj = getattr(manim, class_name)
#                     if hasattr(class_obj, method_name):
#                         method = getattr(class_obj, method_name)
#                         signature = str(inspect.signature(method))
#                         return f"The parameter '{invalid_kwarg}' is not valid for {class_name}.{method_name}{signature}. Check the documentation:"
#                 except (AttributeError, ImportError):
#                     continue
            
#             return f"The parameter '{invalid_kwarg}' is not valid for {method_name}(). Check the documentation for valid parameters."
        
#         return None
    
#     def extract_classes_from_code(self, code: str) -> Set[str]:
#         """Extract Manim class names from a code snippet.
        
#         Args:
#             code: The code to analyze
            
#         Returns:
#             Set of class names found in the code
#         """
#         # Pattern to match class instantiations: ClassName(
#         class_pattern = r'([A-Z][A-Za-z0-9_]*)\('
#         # Pattern to match method calls: .method_name(
#         method_pattern = r'\.([a-z][A-Za-z0-9_]*)\('
        
#         classes = set()
        
#         # Find all class instantiations
#         for match in re.finditer(class_pattern, code):
#             class_name = match.group(1)
#             # Only include if it's likely a Manim class (starts with capital letter)
#             # and is in our common classes list or we can find it in the manim module
#             if class_name in self.common_classes or self.get_class_info(class_name) is not None:
#                 classes.add(class_name)
        
#         return classes
    
#     def extract_classes_from_error(self, error_msg: str) -> Set[str]:
#         """Extract Manim class names from an error message.
        
#         Args:
#             error_msg: The error message to analyze
            
#         Returns:
#             Set of class names found in the error
#         """
#         # Pattern to match class names in errors
#         patterns = [
#             r'([A-Z][A-Za-z0-9_]*) object has no attribute',  # AttributeError
#             r'Cannot call ([A-Z][A-Za-z0-9_]*)\.', # Method call on object with no points
#             r'([A-Z][A-Za-z0-9_]*)\.__init__\(\) takes', # Wrong number of arguments
#             r'module \'manim\' has no attribute \'([A-Z][A-Za-z0-9_]*)\'', # Missing import
#             r'\'([A-Z][A-Za-z0-9_]*)\' object is not', # Type error
#         ]
        
#         classes = set()
        
#         for pattern in patterns:
#             for match in re.finditer(pattern, error_msg):
#                 class_name = match.group(1)
#                 if class_name in self.common_classes or self.get_class_info(class_name) is not None:
#                     classes.add(class_name)
        
#         # Extract method names and try to find their classes
#         method_patterns = [
#             r'([a-z][a-z_]+)\(\) got an unexpected keyword argument',  # Unexpected keyword
#             r'([a-z][a-z_]+)\(\) missing \d+ required positional argument',  # Missing argument
#         ]
        
#         for pattern in method_patterns:
#             for match in re.finditer(pattern, error_msg):
#                 method_name = match.group(1)
#                 # Try to find which classes have this method
#                 for class_name in self.common_classes:
#                     class_info = self.get_class_info(class_name)
#                     if class_info and method_name in class_info["methods"]:
#                         classes.add(class_name)
        
#         return classes
    
#     def get_targeted_api_docs(self, code: str = "", error_msg: str = "") -> str:
#         """Get targeted API documentation for classes mentioned in code or error message.
        
#         Args:
#             code: The code to analyze (optional)
#             error_msg: The error message to analyze (optional)
            
#         Returns:
#             A string containing relevant API documentation
#         """
#         classes = set()
        
#         # Extract classes from both code and error message
#         if code:
#             classes.update(self.extract_classes_from_code(code))
        
#         if error_msg:
#             classes.update(self.extract_classes_from_error(error_msg))
        
#         # If no classes found, include a few common ones
#         if not classes:
#             classes = {"Circle", "Square", "Line", "MathTex", "VGroup"}
        
#         # Build documentation string
#         docs = []
#         docs.append("# Manim API Documentation\n")
        
#         for class_name in sorted(classes):
#             class_info = self.get_class_info(class_name)
#             if class_info:
#                 docs.append(f"## {class_name}\n")
#                 docs.append(f"{class_info['docstring']}\n")
                
#                 # Add constructor info
#                 if "__init__" in class_info["methods"]:
#                     init_info = class_info["methods"]["__init__"]
#                     docs.append(f"### Constructor\n")
#                     docs.append(f"```python\n{class_name}{init_info['signature']}\n```\n")
#                     if init_info["docstring"]:
#                         docs.append(f"{init_info['docstring']}\n")
                
#                 # Add a few key methods (limit to 5 to avoid too much information)
#                 methods = [m for m in class_info["methods"] if m != "__init__"]
#                 if methods:
#                     docs.append(f"### Key Methods\n")
#                     for method_name in methods[:5]:
#                         method_info = class_info["methods"][method_name]
#                         docs.append(f"#### {method_name}\n")
#                         docs.append(f"```python\n{method_name}{method_info['signature']}\n```\n")
#                         if method_info["docstring"]:
#                             docs.append(f"{method_info['docstring']}\n")
        
#         # Add common best practices
#         docs.append(self.get_common_best_practices())
        
#         return "\n".join(docs)
    
#     def get_common_best_practices(self) -> str:
#         """Get common best practices and error solutions for Manim.
        
#         Returns:
#             A string containing common best practices
#         """
#         return """
# ## Common Manim Best Practices and Error Solutions

# ### Working with Paths and Points
# - Always initialize path objects (Line, Arc, etc.) with explicit coordinates
# - For a Line, use: `Line(start=ORIGIN, end=RIGHT)`
# - For an Arc, use: `Arc(radius=1, start_angle=0, angle=PI)`
# - When using MoveAlongPath, ensure the path has points

# ### Camera Frame Issues
# - Never use `camera.frame` directly - it doesn't exist in current Manim versions
# - Instead of camera manipulation, scale or move the objects themselves
# - Use `self.play(mobject.animate.scale(0.8))` instead of camera zooming

# ### Background and Branding
# - NEVER create or modify the background - it's already set in the base class with product branding
# - Do not use `FullScreenRectangle`, `Rectangle`, or any other object as a background
# - The background is automatically added in the ManimVoiceoverBase class constructor

# ### Color Handling
# - Always use quoted color values: `color="blue"` not `color=blue`
# - Use predefined colors like RED, GREEN, BLUE, or hex values like "#FF0000"

# ### Text and Math
# - Use MathTex for mathematical expressions, not Tex
# - For regular text, use Text("Your text here")

# ### Constants and Dimensions
# - FRAME_WIDTH and FRAME_HEIGHT are not defined in current Manim versions
# - For specific dimensions, use explicit values: `Rectangle(width=14, height=8)`
# - Common constants that need to be imported: UP, DOWN, LEFT, RIGHT, ORIGIN
# - Mathematical constants: PI, TAU, DEGREES, RADIANS

# ### Animation Performance
# - Avoid creating too many objects (>100)
# - Use VGroup to manage collections of objects
# - Avoid infinite loops or loops without clear exit conditions
# """ 