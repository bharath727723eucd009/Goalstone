"""Structured logging configuration with loguru."""
import sys
from loguru import logger
from ..config import settings

def configure_logging():
    """Configure structured logging with loguru."""
    # Remove default handler
    logger.remove()
    
    # Add structured JSON logging
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {extra} | {message}",
        level=settings.log_level,
        serialize=True,
        enqueue=True
    )
    
    # Add file logging
    logger.add(
        "logs/app.log",
        rotation="100 MB",
        retention="30 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {extra} | {message}",
        level=settings.log_level,
        serialize=True,
        enqueue=True
    )

def get_logger(name: str = None):
    """Get logger instance with context."""
    if name:
        return logger.bind(module=name)
    return logger