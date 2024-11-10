"""Logging configuration for the application."""

import os
import json
import logging
from typing import Any, Dict
import structlog
from pygments import highlight
from pygments.lexers import JsonLexer  # pylint: disable=no-name-in-module
from pygments.formatters import TerminalFormatter  # pylint: disable=no-name-in-module
from vitagen.constants import CONFIG_LOG_LEVEL, ENV_LOG_PRETTY

__all__ = ["configure_logging", "get_logger"]


def order_fields(_, __, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Processor to order fields in the log output.
    Ensures timestamp, level, and msg appear first in that order.
    """
    # Create a new ordered dict with the fields in desired order
    ordered = {}

    # First add timestamp if it exists
    if "timestamp" in event_dict:
        ordered["timestamp"] = event_dict.pop("timestamp")

    # Then add level if it exists
    if "level" in event_dict:
        ordered["level"] = event_dict.pop("level")

    if "logger" in event_dict:
        ordered["logger"] = event_dict.pop("logger")

    # Then add msg if it exists
    if "msg" in event_dict:
        ordered["msg"] = event_dict.pop("msg")

    # Add all remaining fields
    ordered.update(event_dict)

    return ordered


def set_logger(_, __, event_dict):
    """Set the logger in the event dictionary."""

    event_dict["logger"] = "vitagen"
    return event_dict


def configure_logging():
    """Configure logging for the application."""

    processors = (
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        set_logger,
        structlog.processors.EventRenamer("msg"),
        order_fields,
    )

    # get the log level from the configuration
    level = os.environ.get(CONFIG_LOG_LEVEL, "INFO").upper()
    log_level = getattr(logging, level)

    # get pretty print is enabled or not
    pretty_print = os.environ.get(ENV_LOG_PRETTY, "False") == "True"

    # if pretty print is enabled, add JSONRenderer with colored_json_serializer
    if pretty_print:
        processors += (
            structlog.processors.JSONRenderer(serializer=colored_json_serializer),
        )
    else:
        processors += (structlog.processors.JSONRenderer(),)

    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        processors=processors,
    )


def colored_json_serializer(obj, **kwargs):
    """Serialize a JSON object with color.

    Args:
        obj (dict): The JSON object to serialize.

    Returns:
        str: The serialized JSON object with color.
    """
    level = obj.get("level").upper()

    json_str = json.dumps(obj, indent=2, **kwargs)
    colored_json = highlight(json_str, JsonLexer(), TerminalFormatter())
    colored_level = highlight(level, JsonLexer(), TerminalFormatter())

    # remove new line from colored_level
    colored_level = colored_level.replace("\n", "")

    # add 2 spaces to the colored_json at beginning of each line
    colored_json = colored_json.replace("\n", "\n  ")

    return f"[{colored_level}]: {colored_json}"


def get_logger(name: str = None):
    """
    Get a configured logger instance.
    Args:
        name: Optional name for the logger. If None, uses the default logger.
    Returns:
        A configured structlog logger instance
    """
    logger = structlog.get_logger(name or "default")
    return logger
