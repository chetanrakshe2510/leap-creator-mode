"""
Tracing utilities for the workflow.

This module provides utilities for tracing the workflow with LangSmith.
"""
import os
import functools
from typing import Any, Callable, Dict, Optional, TypeVar, cast

# Try to import langsmith, but don't fail if it's not available
try:
    from langsmith import traceable as langsmith_traceable
    LANGSMITH_AVAILABLE = True
except ImportError:
    LANGSMITH_AVAILABLE = False
    # Create a dummy decorator that does nothing
    def langsmith_traceable(func=None, **kwargs):
        if func is None:
            return lambda f: f
        return func

# Type variable for the function
F = TypeVar('F', bound=Callable[..., Any])

def traceable(
    func: Optional[F] = None,
    name: Optional[str] = None,
    run_type: str = "chain",
    tags: Optional[list] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> F:
    """
    Decorator to trace a function with LangSmith.
    
    This decorator wraps the langsmith traceable decorator and adds some additional
    functionality specific to our workflow.
    
    Args:
        func: The function to trace
        name: The name of the run
        run_type: The type of run (chain, llm, tool, etc.)
        tags: Tags to add to the run
        metadata: Metadata to add to the run
        
    Returns:
        The decorated function
    """
    # If langsmith is not available or tracing is disabled, return the original function
    if not LANGSMITH_AVAILABLE or os.environ.get("LANGSMITH_TRACING", "").lower() != "true":
        if func is None:
            return lambda f: f
        return func
    
    # If func is None, we're being called with arguments
    if func is None:
        return lambda f: traceable(f, name=name, run_type=run_type, tags=tags, metadata=metadata)
    
    # Get the function name if not provided
    if name is None:
        name = func.__name__
    
    # Add workflow tag if not provided
    if tags is None:
        tags = []
    if "workflow" not in tags:
        tags.append("workflow")
    
    # Add node tag if not provided
    if "node" not in tags:
        tags.append("node")
    
    # Create metadata if not provided
    if metadata is None:
        metadata = {}
    
    # Add function name to metadata
    metadata["function_name"] = func.__name__
    
    # Apply the langsmith traceable decorator
    traced_func = langsmith_traceable(
        name=name,
        run_type=run_type,
        tags=tags,
        metadata=metadata,
    )(func)
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return traced_func(*args, **kwargs)
    
    return cast(F, wrapper) 