"""Logging utilities"""

import logging
from rich.logging import RichHandler
from src.core.config import settings


def setup_logger(name: str) -> logging.Logger:
    """Setup logger with rich handler"""
    
    logger = logging.getLogger(name)
    logger.setLevel(settings.log_level)
    
    if not logger.handlers:
        handler = RichHandler(rich_tracebacks=True, markup=True)
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)
    
    return logger
