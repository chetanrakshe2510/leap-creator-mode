#!/usr/bin/env python3
"""
Run all tests for the leap package.
"""
import sys
import argparse
import pytest
from pathlib import Path

# Add the project root to the Python path if needed
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run tests for the leap package")
    
    parser.add_argument(
        "--no-e2e", 
        action="store_true",
        help="Skip end-to-end tests that involve the entire workflow"
    )
    
    parser.add_argument(
        "--coverage", 
        action="store_true",
        help="Generate a coverage report"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    parser.add_argument(
        "--test-path",
        type=str,
        default="tests",
        help="Path to tests to run (default: run all tests)"
    )
    
    return parser.parse_args()

def main():
    """Run the tests."""
    args = parse_args()
    
    # Build pytest arguments
    pytest_args = []
    
    # Add test path
    pytest_args.append(args.test_path)
    
    # Skip e2e tests if requested
    if args.no_e2e:
        pytest_args.append("--ignore=tests/e2e")
    
    # Add verbose flag if requested
    if args.verbose:
        pytest_args.append("-v")
    
    # Add coverage reporting if requested
    if args.coverage:
        pytest_args.extend([
            "--cov=leap",
            "--cov-report=term",
            "--cov-report=html:coverage_html"
        ])
    
    # Run the tests
    print(f"Running tests with arguments: {' '.join(pytest_args)}")
    exit_code = pytest.main(pytest_args)
    
    # Print coverage report location if generated
    if args.coverage:
        print("\nCoverage report generated in coverage_html/index.html")
    
    # Exit with the pytest exit code
    sys.exit(exit_code)

if __name__ == "__main__":
    main() 