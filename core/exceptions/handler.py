"""
Global DRF exception handler.

Configure in settings.py:

    REST_FRAMEWORK = {
        "EXCEPTION_HANDLER": "core.exceptions.handler.custom_exception_handler"
    }

Every exception is converted to the standard envelope:

    {
        "success": false,
        "message": "<human-readable>",
        "data":    null,
        "errors":  <detail or null>
    }

Unhandled exceptions are also logged with a full traceback.
"""

import logging
from typing import Any

from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
    ValidationError,
)
from rest_framework.request import Request
from rest_framework.response import Response

from core.constants import messages
from core.responses.response import error_response

logger = logging.getLogger("core")


# ── Helpers ───────────────────────────────────────────────────────────────────

def _extract_errors(exc: ValidationError) -> Any:
    """
    Pull the raw validation detail out of a ValidationError.

    DRF stores errors as nested dicts/lists of ``ErrorDetail`` objects;
    we just pass them straight through — DRF's renderer will serialise them.
    """
    return exc.detail


# ── Handler ───────────────────────────────────────────────────────────────────

def custom_exception_handler(exc: Exception, context: dict) -> Response:
    """
    Convert any exception raised inside a DRF view into the standard envelope.

    Parameters
    ----------
    exc:
        The exception that was raised.
    context:
        DRF context dict (contains ``view``, ``request``, etc.).

    Returns
    -------
    Response
        A DRF ``Response`` using the standard error envelope.
    """
    request: Request = context.get("request")  # type: ignore[assignment]

    # ── ValidationError ───────────────────────────────────────────────────────
    if isinstance(exc, ValidationError):
        return error_response(
            message=messages.VALIDATION_ERROR,
            errors=_extract_errors(exc),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # ── AuthenticationFailed ──────────────────────────────────────────────────
    if isinstance(exc, AuthenticationFailed):
        return error_response(
            message=messages.AUTHENTICATION_FAILED,
            errors=None,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    # ── NotAuthenticated ──────────────────────────────────────────────────────
    if isinstance(exc, NotAuthenticated):
        return error_response(
            message=messages.NOT_AUTHENTICATED,
            errors=None,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    # ── PermissionDenied ──────────────────────────────────────────────────────
    if isinstance(exc, PermissionDenied):
        return error_response(
            message=messages.PERMISSION_DENIED,
            errors=None,
            status_code=status.HTTP_403_FORBIDDEN,
        )

    # ── Http404 ───────────────────────────────────────────────────────────────
    if isinstance(exc, Http404):
        return error_response(
            message=messages.RESOURCE_NOT_FOUND,
            errors=None,
            status_code=status.HTTP_404_NOT_FOUND,
        )

    # ── Generic APIException ──────────────────────────────────────────────────
    if isinstance(exc, APIException):
        return error_response(
            message=str(exc.detail) if exc.detail else messages.INTERNAL_SERVER_ERROR,
            errors=None,
            status_code=exc.status_code,
        )

    # ── Unhandled / unexpected exceptions ────────────────────────────────────
    logger.exception(
        "Unhandled exception | path=%s | method=%s",
        getattr(request, "path", "unknown"),
        getattr(request, "method", "unknown"),
        exc_info=exc,
    )
    return error_response(
        message=messages.INTERNAL_SERVER_ERROR,
        errors=None,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
