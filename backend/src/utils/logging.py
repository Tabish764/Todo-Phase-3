"""Logging utilities for the Todo AI Chatbot application."""
import logging
from typing import Any
from datetime import datetime


class StructuredLogger:
    """Structured logging for the application."""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Create handler if not exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def info(self, message: str, **kwargs: Any):
        """Log info level message with structured data."""
        structured_msg = self._format_message(message, **kwargs)
        self.logger.info(structured_msg)

    def error(self, message: str, **kwargs: Any):
        """Log error level message with structured data."""
        structured_msg = self._format_message(message, **kwargs)
        self.logger.error(structured_msg)

    def warning(self, message: str, **kwargs: Any):
        """Log warning level message with structured data."""
        structured_msg = self._format_message(message, **kwargs)
        self.logger.warning(structured_msg)

    def debug(self, message: str, **kwargs: Any):
        """Log debug level message with structured data."""
        structured_msg = self._format_message(message, **kwargs)
        self.logger.debug(structured_msg)

    def _format_message(self, message: str, **kwargs: Any) -> str:
        """Format message with structured data."""
        if kwargs:
            data_str = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
            return f"{message} | {data_str}"
        return message


# Create a global logger instance
app_logger = StructuredLogger("chatbot")
