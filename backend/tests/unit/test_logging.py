"""
Unit tests for the logging module.
"""
import pytest
import logging
from pathlib import Path
from leap.core.logging import setup_question_logger, _loggers
from leap.core.config import LOGS_DIR
from pythonjsonlogger.json import JsonFormatter

@pytest.fixture
def test_question():
    """Test question fixture."""
    return "How does gravity work?"

@pytest.fixture(autouse=True)
def cleanup_loggers():
    """Clean up loggers after each test."""
    # Store original loggers
    original_loggers = logging.Logger.manager.loggerDict.copy()
    original_cache = _loggers.copy()
    
    yield
    
    # Restore original loggers
    logging.Logger.manager.loggerDict = original_loggers
    _loggers.clear()
    _loggers.update(original_cache)

def test_setup_question_logger_basic(test_question):
    """Test basic logger setup functionality."""
    logger = setup_question_logger(test_question)
    
    # Check logger instance and name
    assert isinstance(logger, logging.Logger)
    assert logger.name.startswith("question_")
    
    # Check handlers
    assert len(logger.handlers) == 2  # File and console handlers
    
    # Check file handler
    file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
    assert len(file_handlers) == 1
    
    # Check log file location
    log_file_path = Path(file_handlers[0].baseFilename)
    assert log_file_path.parent == LOGS_DIR
    assert "how_does_gravity_work" in log_file_path.name

def test_logger_caching(test_question):
    """Test that loggers are cached for the same question."""
    logger1 = setup_question_logger(test_question)
    logger2 = setup_question_logger(test_question)
    
    assert logger1 is logger2
    assert len(logger1.handlers) == len(logger2.handlers) == 2

def test_json_formatting(test_question):
    """Test that loggers use JSON formatting."""
    logger = setup_question_logger(test_question)
    
    # Check that handlers use JsonFormatter
    for handler in logger.handlers:
        assert isinstance(handler.formatter, JsonFormatter) 