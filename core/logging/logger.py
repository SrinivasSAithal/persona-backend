"""
Centralised logging utility.

Thin wrappers around the standard ``logging`` module so that every part
of the project uses a consistent logger name (``"core"``) and log format.

Usage
-----
::

    from core.logging.logger import log_info, log_warning, log_error, log_exception

    log_info("User created successfully")
    log_warning("Profile image missing")
    log_error("Database connection failed")

    try:
        ...
    except Exception as exc:
        log_exception(exc)

Log format (configured in settings.py)
---------------------------------------
::

    2026-06-11 22:30:15 | INFO | User created successfully
"""

import logging
import traceback

# Single named logger – all wrappers write to this logger.
# The Django LOGGING config in settings.py routes it to console + files.
_logger = logging.getLogger("core")


# ── Public wrappers ───────────────────────────────────────────────────────────

def log_info(message: str) -> None:
    """
    Log an informational message.

    Parameters
    ----------
    message:
        Human-readable description of the event.

    Example
    -------
    ::

        log_info("User created successfully")
    """
    _logger.info(message)


def log_warning(message: str) -> None:
    """
    Log a warning message.

    Parameters
    ----------
    message:
        Description of a potentially problematic situation.

    Example
    -------
    ::

        log_warning("Profile image missing")
    """
    _logger.warning(message)


def log_error(message: str) -> None:
    """
    Log an error message (non-exception).

    Parameters
    ----------
    message:
        Description of the error.

    Example
    -------
    ::

        log_error("Database connection failed")
    """
    _logger.error(message)


def log_exception(exc: Exception) -> None:
    """
    Log an exception together with its full traceback.

    Parameters
    ----------
    exc:
        The caught exception object.

    Example
    -------
    ::

        try:
            ...
        except Exception as e:
            log_exception(e)
    """
    _logger.exception(
        "%s: %s\n%s",
        type(exc).__name__,
        exc,
        traceback.format_exc(),
    )
