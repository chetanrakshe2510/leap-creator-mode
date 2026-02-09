#!/usr/bin/env python3
"""
Prompt Management CLI Tool

This tool helps manage prompts in the AskLeap system, allowing users to:
- List available prompts
- View prompt details
- Export prompts to JSON
- Import prompts from JSON
- Create new prompt versions
- Compare different prompt versions
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
import importlib
import difflib
from tabulate import tabulate

# Add the project root to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from leap.prompts.base import PromptTemplate, PromptCollection, PromptVersion
from leap.prompts import (
    SCENE_PLANNING_PROMPTS,
    CODE_GENERATION_PROMPTS,
    ERROR_CORRECTION_PROMPTS,
    VALIDATION_PROMPTS
)

# Map of prompt collection names to their objects
PROMPT_COLLECTIONS = {
    "scene_planning": SCENE_PLANNING_PROMPTS,
    "code_generation": CODE_GENERATION_PROMPTS,
    "error_correction": ERROR_CORRECTION_PROMPTS,
    "validation": VALIDATION_PROMPTS
}


def list_prompts(args):
    """List all available prompts."""
    rows = []
    for name, collection in PROMPT_COLLECTIONS.items():
        for version in collection.list_versions():
            template = collection.get(version)
            rows.append([
                name,
                version.value,
                template.description or "No description",
                ", ".join(template.tags)
            ])
    
    print(tabulate(
        rows,
        headers=["Collection", "Version", "Description", "Tags"],
        tablefmt="grid"
    ))


def view_prompt(args):
    """View details of a specific prompt."""
    collection_name = args.collection
    version = PromptVersion(args.version)
    
    if collection_name not in PROMPT_COLLECTIONS:
        print(f"Error: Collection '{collection_name}' not found")
        return
    
    collection = PROMPT_COLLECTIONS[collection_name]
    
    try:
        template = collection.get(version)
    except KeyError:
        print(f"Error: Version '{version.value}' not found in collection '{collection_name}'")
        return
    
    print(f"Collection: {collection_name}")
    print(f"Version: {version.value}")
    print(f"Description: {template.description or 'No description'}")
    print(f"Tags: {', '.join(template.tags)}")
    print("\nSystem Message:")
    print("=" * 80)
    print(template.system)
    print("\nUser Message Template:")
    print("=" * 80)
    print(template.user)


def export_prompts(args):
    """Export prompts to JSON files."""
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # By default, only export the prompts that are actually used in the code (production)
    # If --all-versions is specified, export all versions
    export_all = args.all_versions
    
    for name, collection in PROMPT_COLLECTIONS.items():
        output_file = output_dir / f"{name}_prompts.json"
        
        if not export_all:
            # Export only the production version (the one used in code)
            try:
                production_template = collection.get(PromptVersion.PRODUCTION)
                export_data = {
                    "production": production_template.to_dict()
                }
                with open(output_file, 'w') as f:
                    f.write(json.dumps(export_data, indent=2))
                print(f"Exported {name} prompt (production version) to {output_file}")
            except KeyError:
                print(f"Warning: No production version found for {name}")
        else:
            # Export all versions
            with open(output_file, 'w') as f:
                f.write(collection.to_json())
            print(f"Exported all versions of {name} prompts to {output_file}")


def import_prompts(args):
    """Import prompts from JSON files."""
    input_file = Path(args.input_file)
    collection_name = args.collection
    
    if not input_file.exists():
        print(f"Error: Input file '{input_file}' not found")
        return
    
    if collection_name not in PROMPT_COLLECTIONS:
        print(f"Error: Collection '{collection_name}' not found")
        return
    
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        collection = PromptCollection.from_dict(data)
        
        # Print summary of imported prompts
        print(f"Successfully imported prompts for '{collection_name}':")
        for version in collection.list_versions():
            template = collection.get(version)
            print(f"  - {version.value}: {template.description or 'No description'}")
        
        print("\nNote: This tool only displays the imported prompts but doesn't modify the codebase.")
        print("To use these prompts, you need to update the appropriate files in src/prompts/")
        
    except Exception as e:
        print(f"Error importing prompts: {str(e)}")


def compare_prompts(args):
    """Compare different versions of a prompt."""
    collection_name = args.collection
    version1 = PromptVersion(args.version1)
    version2 = PromptVersion(args.version2)
    
    if collection_name not in PROMPT_COLLECTIONS:
        print(f"Error: Collection '{collection_name}' not found")
        return
    
    collection = PROMPT_COLLECTIONS[collection_name]
    
    try:
        template1 = collection.get(version1)
        template2 = collection.get(version2)
    except KeyError as e:
        print(f"Error: Version not found - {str(e)}")
        return
    
    print(f"Comparing {collection_name} prompts: {version1.value} vs {version2.value}")
    
    # Compare system messages
    print("\nSystem Message Diff:")
    print("=" * 80)
    sys_diff = difflib.unified_diff(
        template1.system.splitlines(),
        template2.system.splitlines(),
        fromfile=f"{version1.value} system",
        tofile=f"{version2.value} system",
        lineterm=''
    )
    print('\n'.join(sys_diff))
    
    # Compare user messages
    print("\nUser Message Diff:")
    print("=" * 80)
    user_diff = difflib.unified_diff(
        template1.user.splitlines(),
        template2.user.splitlines(),
        fromfile=f"{version1.value} user",
        tofile=f"{version2.value} user",
        lineterm=''
    )
    print('\n'.join(user_diff))


def create_prompt_version(args):
    """Create a new prompt version based on an existing one."""
    collection_name = args.collection
    base_version = PromptVersion(args.base_version)
    new_version = args.new_version
    
    if collection_name not in PROMPT_COLLECTIONS:
        print(f"Error: Collection '{collection_name}' not found")
        return
    
    collection = PROMPT_COLLECTIONS[collection_name]
    
    try:
        base_template = collection.get(base_version)
    except KeyError:
        print(f"Error: Base version '{base_version.value}' not found in collection '{collection_name}'")
        return
    
    # Create a new template based on the existing one
    new_template_dict = base_template.to_dict()
    new_template_dict["version"] = new_version
    new_template_dict["description"] = f"New version based on {base_version.value}"
    
    # Print the template as Python code
    print(f"# Add this to src/prompts/{collection_name}.py:")
    print(f"{new_version.upper()} = PromptTemplate(")
    print(f"    system=\"\"\"{new_template_dict['system']}\"\"\",")
    print(f"    user=\"\"\"{new_template_dict['user']}\"\"\",")
    print(f"    version=PromptVersion.{new_version.upper()},")
    print(f"    description=\"{new_template_dict['description']}\",")
    print(f"    tags={new_template_dict['tags']}")
    print(")")
    
    print("\n# Then update the collection:")
    print(f"{collection_name.upper()}_PROMPTS = PromptCollection({{")
    print("    # ... existing versions ...")
    print(f"    PromptVersion.{new_version.upper()}: {new_version.upper()},")
    print("})")


def main():
    parser = argparse.ArgumentParser(description="Prompt Management CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # List prompts
    list_parser = subparsers.add_parser("list", help="List all available prompts")
    
    # View prompt
    view_parser = subparsers.add_parser("view", help="View details of a specific prompt")
    view_parser.add_argument("collection", help="Prompt collection name")
    view_parser.add_argument("version", help="Prompt version")
    
    # Export prompts
    export_parser = subparsers.add_parser("export", help="Export prompts to JSON files")
    export_parser.add_argument("--output-dir", default="./prompt_exports", help="Output directory for JSON files")
    export_parser.add_argument("--all-versions", action="store_true", help="Export all prompt versions instead of just the production version")
    
    # Import prompts
    import_parser = subparsers.add_parser("import", help="Import prompts from JSON files")
    import_parser.add_argument("collection", help="Prompt collection name")
    import_parser.add_argument("input_file", help="Input JSON file")
    
    # Compare prompts
    compare_parser = subparsers.add_parser("compare", help="Compare different versions of a prompt")
    compare_parser.add_argument("collection", help="Prompt collection name")
    compare_parser.add_argument("version1", help="First prompt version")
    compare_parser.add_argument("version2", help="Second prompt version")
    
    # Create new prompt version
    create_parser = subparsers.add_parser("create", help="Create a new prompt version based on an existing one")
    create_parser.add_argument("collection", help="Prompt collection name")
    create_parser.add_argument("base_version", help="Base prompt version")
    create_parser.add_argument("new_version", help="New version name")
    
    args = parser.parse_args()
    
    if args.command == "list":
        list_prompts(args)
    elif args.command == "view":
        view_prompt(args)
    elif args.command == "export":
        export_prompts(args)
    elif args.command == "import":
        import_prompts(args)
    elif args.command == "compare":
        compare_prompts(args)
    elif args.command == "create":
        create_prompt_version(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main() 