"""
Logging format and context filter
"""

import logging
import os
import sys
from contextvars import ContextVar
from typing import Optional

import colorlog

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
LOG_FORMAT = "%(log_color)s %(asctime)s - [%(levelname)s] - %(name)s - "\
    "(%(filename)s).%(funcName)s(%(lineno)d) - C: %(ctx)s - U: %(user)s - M: %(message)s"

correlation_id: ContextVar[Optional[str]] = ContextVar('correlation_id', default='N/A')
correlation_user: ContextVar[Optional[str]] = ContextVar('correlation_user', default='Anonymous')

_configured_loggers = set()
_root_handler_configured = False


def set_context(context: Optional[str]) -> Optional[str]:
    """
    Set correlation context
    :param context: Correlation ID
    :return: Token for resetting context
    """
    if context is None:
        context = 'N/A'
    return correlation_id.set(context)


def set_usercontext(context: Optional[str]) -> Optional[str]:
    """
    Set user context
    :param context: User identifier
    :return: Token for resetting context
    """
    if context is None:
        context = 'Anonymous'
    return correlation_user.set(context)


def get_context() -> str:
    """
    Get correlation context
    :return: Current correlation ID
    """
    return correlation_id.get()


def get_usercontext() -> str:
    """
    Get user context
    :return: Current user identifier
    """
    return correlation_user.get()


def clear_context() -> None:
    """
    Clear all context variables
    """
    correlation_id.set('N/A')
    correlation_user.set('Anonymous')


class ContextFilter(logging.Filter):
    """
    Filter to add context information to log records
    """

    def filter(self, record) -> bool:
        """
        Add context information to log record
        :param record: Log record
        :return: True to keep the record
        """
        record.user = correlation_user.get()
        record.ctx = correlation_id.get()
        return True


def _get_log_level() -> int:
    """
    Get log level from environment or default to INFO
    :return: Log level
    """
    levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    return levels.get(LOG_LEVEL, logging.INFO)


def _configure_root_handler() -> None:
    """
    Configure root handler only once to prevent duplicates
    """
    global _root_handler_configured

    if _root_handler_configured:
        return

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(_get_log_level())

    # Clear any existing handlers
    root_logger.handlers.clear()

    # Create and add stream handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(_get_log_level())

    # Use colorlog if available, fallback to standard formatter
    try:
        formatter = colorlog.ColoredFormatter(LOG_FORMAT)
    except Exception:
        # Fallback format without colors
        fallback_format = "%(asctime)s - [%(levelname)s] - %(name)s - "\
            "(%(filename)s).%(funcName)s(%(lineno)d) - C: %(ctx)s - U: %(user)s - M: %(message)s"
        formatter = logging.Formatter(fallback_format)

    stream_handler.setFormatter(formatter)
    stream_handler.addFilter(ContextFilter())

    root_logger.addHandler(stream_handler)
    _root_handler_configured = True


def get_logger(name: str) -> logging.Logger:
    """
    Get a properly configured logger instance
    :param name: Logger name (usually __name__)
    :return: Configured logger
    """
    # Configure root handler once
    _configure_root_handler()

    # Get logger instance
    logger = logging.getLogger(name)

    # Only configure if not already configured
    if name not in _configured_loggers:
        logger.setLevel(_get_log_level())
        # Don't add handlers here - use root logger handlers
        logger.propagate = True
        _configured_loggers.add(name)

    return logger


def reset_logging_config() -> None:
    """
    Reset logging configuration - useful for testing
    """
    global _configured_loggers, _root_handler_configured

    _configured_loggers.clear()
    _root_handler_configured = False

    # Clear root logger handlers
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
