import logging
import hashlib
from datetime import datetime
from pathlib import Path
from leap.core.config import LOGS_DIR
from pythonjsonlogger.json import JsonFormatter

# Dictionary to store loggers by their hash
_loggers = {}

def setup_question_logger(question: str) -> logging.Logger:
    """Setup a logger for a specific question."""
    # Create a hash of the question to use as a unique identifier
    question_hash = hashlib.md5(question.encode()).hexdigest()
    
    # Check if we already have a logger for this question
    if question_hash in _loggers:
        return _loggers[question_hash]
    
    # Create a new logger
    logger = logging.getLogger(f"question_{question_hash}")
    
    # Only add handler if none exists
    if not logger.handlers:
        # Create a sanitized filename from the question
        safe_name = question.lower()
        safe_name = "".join(c if c.isalnum() else "_" for c in safe_name[:30])
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = LOGS_DIR / f"{safe_name}_{timestamp}.log"
        
        # Set the logger level
        logger.setLevel(logging.INFO)
        
        # Remove any existing handlers
        logger.handlers = []
        
        # Create a json formatter for structured logging
        formatter = JsonFormatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # Add file handler
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
        # Add console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    
    # Store the logger for future use
    _loggers[question_hash] = logger
    
    return logger

# Setup root logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
) 