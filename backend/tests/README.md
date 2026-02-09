# Leap Tests

This directory contains the test suite for the Leap project, an AI-powered educational animation generator using Manim.

## Quick Start

```bash
# From the backend directory
# 1. Install the package in development mode with dev dependencies
pip install -e ".[dev]"

# 2. Run all tests except end-to-end tests (recommended for development)
python -m tests.run_tests --no-e2e

# 3. Run with verbose output
python -m tests.run_tests --no-e2e -v

# 4. Run with coverage report
python -m tests.run_tests --no-e2e --coverage
```

## Directory Structure

```
tests/
├── __init__.py          # Package initialization
├── conftest.py          # Pytest configuration and shared fixtures
├── run_tests.py         # Test runner script
├── unit/               # Unit tests for individual components
│   ├── test_config.py
│   ├── test_workflow_utils.py
│   ├── test_state.py
│   └── ...
├── integration/        # Integration tests
├── api/               # API endpoint tests
├── e2e/              # End-to-end tests (skipped by default)
│   ├── __init__.py
│   ├── test_basic_workflow.py
```

## Running Tests

### Recommended for Development
```bash
# Run all tests except e2e tests with the custom test runner
python -m tests.run_tests --no-e2e -v

# Run specific test categories using pytest directly
pytest tests/unit -v
pytest tests/integration -v

# Run specific test file
pytest tests/unit/test_graph.py -v
```

### Test Runner Options
The `run_tests.py` script provides several options:

```bash
# Show all options
python -m tests.run_tests --help

# Available options:
--no-e2e     # Skip end-to-end tests
--coverage   # Generate coverage report
--verbose    # Show detailed output
--test-path  # Specify a path to test (default: all tests)
```

### Test Configuration
- Tests use pytest fixtures defined in `conftest.py`
- Integration tests mock external services
- Unit tests focus on core logic

## Test Categories

### Unit Tests
- Focus on individual components and functions
- Fast execution, no external dependencies
- Run these frequently during development

### Integration Tests
- Test workflow steps and component interactions
- Mock external services where needed
- Run these before committing changes

### API Tests
- Test API endpoints using FastAPI TestClient
- Most tests mock the actual animation generation
- Verify API response structure and error handling

### End-to-End Tests (Skipped by Default)
The `e2e` directory contains comprehensive end-to-end tests that verify the entire workflow from input to video generation. These tests:
- Take longer to run (5-10 minutes)
- Require full system setup (Manim, ffmpeg, etc.)
- Generate actual videos
- Test various input scenarios

To run E2E tests when needed:
```bash
# Run all tests including e2e
python -m tests.run_tests

# Run only e2e tests
pytest tests/e2e/test_basic_workflow.py -v
```

## Writing Tests

### Test File Template

```python
"""
Unit tests for [component].
"""
import pytest
from leap.[module] import [component]

def test_feature():
    """Test specific feature."""
    # Arrange
    # Act
    # Assert
    assert True

class TestComponent:
    """Test suite for component."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures."""
        yield
        # Cleanup code here
    
    def test_specific_feature(self):
        """Test specific feature."""
        assert True
```

### Using Fixtures

```python
# In conftest.py
@pytest.fixture
def sample_state():
    """Provide a sample workflow state."""
    return {
        "user_input": "Explain gravity",
        "rendering_quality": "low",
        "user_level": "normal"
    }

# In your test file
def test_workflow(sample_state):
    """Test workflow with sample state."""
    assert sample_state["user_level"] == "normal"
```

## Environment Setup

### Required Environment Variables

Create a `.env` file in the backend directory:

```bash
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o
MANIM_QUALITY=-ql
```

### Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Unix
venv\Scripts\activate     # Windows

# Install dependencies
pip install -e ".[dev]"
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'leap'**
   ```bash
   # Solution: Install package in development mode
   pip install -e ".[dev]"
   ```

2. **pytest command not found**
   ```bash
   # Solution: Ensure dev dependencies are installed
   pip install -e ".[dev]"
   ```

3. **Missing environment variables**
   ```bash
   # Solution: Copy and edit .env file
   cp .env.example .env
   ```

4. **Tests taking too long to run**
   ```bash
   # Solution: Skip e2e tests
   python -m tests.run_tests --no-e2e
   ```

### Getting Help

If you encounter issues:
1. Check the error message and traceback
2. Review this README
3. Check existing GitHub issues
4. Create a new issue with:
   - Error message
   - Steps to reproduce
   - Expected vs actual behavior

## Contributing

1. Write tests for new features
2. Update existing tests when changing functionality
3. Ensure all tests pass before submitting PR
4. Include coverage report in PR

## Continuous Integration

Tests are automatically run on:
- Pull requests to main branch
- Push to main branch
- Nightly builds

Check `.github/workflows/tests.yml` for CI configuration. 