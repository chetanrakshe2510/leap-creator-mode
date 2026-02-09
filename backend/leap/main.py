#!/usr/bin/env python3
"""
Main script to run the Leap workflow with a sample prompt.
This script demonstrates how to use the workflow to generate Manim animations.
"""

import os
import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, Any

# Add the backend directory to the Python path if needed
backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Now we can import from src
from leap.workflow.graph import workflow
from leap.workflow.state import GraphState
from leap.core.logging import setup_question_logger
from leap.core.config import GENERATED_DIR

# Setup logger - will be replaced with question-specific logger later
logger = logging.getLogger("leap")

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="AskLeap AI command-line interface")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    subparsers.required = True
    
    # Run command - the default behavior
    run_parser = subparsers.add_parser("run", help="Run the workflow with a prompt")
    run_parser.add_argument(
        "prompt", 
        type=str, 
        nargs="?",
        default="Explain the concept of derivatives in calculus with visual examples",
        help="The prompt to use for generating the animation"
    )
    run_parser.add_argument(
        "--quality", 
        type=str, 
        choices=["low", "medium", "high"], 
        default="low",
        help="Rendering quality for the animation"
    )
    run_parser.add_argument(
        "--level", 
        type=str, 
        choices=["ELI5", "normal", "advanced"],
        default="normal",
        help="Explanation level"
    )
    run_parser.add_argument(
        "--voice", 
        type=str, 
        choices=["nova", "alloy", "echo", "fable", "onyx", "shimmer"], 
        default="nova",
        help="Voice model to use"
    )
    run_parser.add_argument(
        "--email", 
        type=str, 
        default=None,
        help="User email for notifications"
    )
    
    # Visualize workflow command - for developers
    vis_parser = subparsers.add_parser("visualize-workflow", help="Generate a visualization of the workflow graph")
    vis_parser.add_argument(
        "--output", 
        type=str, 
        default="workflow_graph.png",
        help="Path to save the visualization image (.png format)"
    )
    
    return parser.parse_args()

def create_initial_state(args) -> GraphState:
    """Create the initial state from args."""
    return GraphState(
        user_input=args.prompt,
        quality=args.quality,
        level=args.level,
        voice=args.voice,
        email=args.email
    )

def run_workflow(state: GraphState) -> Dict[str, Any]:
    """Run the workflow with the given initial state."""
    # Create a logger specific to this question
    logger = setup_question_logger(state["user_input"])
    logger.info(f"Starting workflow with prompt: {state['user_input']}")
    
    # Run the workflow
    result = workflow.invoke(state)
    
    # Return the final state
    return result

def visualize_workflow(output_path):
    """Generate a PNG visualization of the workflow graph.
    
    Args:
        output_path: Path to save the visualization
    """
    try:
        print(f"Generating workflow visualization to {output_path}...")
        
        # Make sure the workflow is compiled before accessing get_graph()
        from leap.workflow.graph import workflow
        
        # Generate the PNG visualization
        workflow.get_graph().draw_mermaid_png(output_file_path=output_path)
        print(f"Workflow visualization saved to {output_path}")
        return True
        
    except Exception as e:
        print(f"Error generating workflow visualization: {str(e)}")
        if "graphviz" in str(e).lower():
            print("This feature requires graphviz to be installed.")
            print("Install with: pip install graphviz")
            print("(You may also need to install the graphviz system package)")
        return False

def main():
    """Main function to run the workflow."""
    args = parse_arguments()
    
    if args.command == "visualize-workflow":
        # Generate workflow visualization
        output_path = args.output
        if not output_path.lower().endswith(".png"):
            output_path += ".png"
        visualize_workflow(output_path)
        return
    
    # Default command: run
    # Create initial state
    initial_state = create_initial_state(args)
    
    # Run the workflow
    result = run_workflow(initial_state)
    
    # Print the result summary
    print("\n" + "="*50)
    print("WORKFLOW EXECUTION SUMMARY")
    print("="*50)
    print(f"Prompt: {result['user_input']}")
    
    if result.get('error'):
        print(f"\nError encountered: {result['error']}")
    else:
        print("\nWorkflow completed successfully!")
        
    if result.get('execution_result'):
        if result['execution_result'].get('success'):
            output_file = result['execution_result'].get('output_file')
            print(f"\nGenerated animation: {output_file}")
        else:
            print(f"\nError executing Manim code: {result['execution_result'].get('error')}")
    
    # Print the location of the generated code directory
    code_dir = GENERATED_DIR / "code"
    print(f"\nGenerated code saved in: {code_dir}")
        
    print("="*50)

if __name__ == "__main__":
    main() 