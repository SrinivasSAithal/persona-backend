"""
Standard API response builders.

Every view should return one of these helpers so that the response shape
is always consistent across the entire project.

Shape
-----
{
    "success": bool,
    "message": str,
    "data": any | null,
    "errors": any | null
}
"""

from typing import Any

from rest_framework.response import Response

from core.constants import messages


# ── Internal builder ─────────────────────────────────────────────────────────

def _build(
    *,
    success: bool,
    message: str,
    data: Any,
    errors: Any,
    status_code: int,
) -> Response:
    """Build the unified envelope and return a DRF Response."""
    return Response(
        {
            "success": success,
            "message": message,
            "data": data,
            "errors": errors,
        },
        status=status_code,
    )


# ── Public helpers ────────────────────────────────────────────────────────────

def success_response(
    data: Any = None,
    message: str = messages.SUCCESS,
    status_code: int = 200,
) -> Response:
    """
    Return a 200 OK (or custom) success envelope.

    Parameters
    ----------
    data:
        The payload to include in ``data``.  Defaults to ``None``.
    message:
        Human-readable success message.
    status_code:
        HTTP status code.  Defaults to 200.

    Example
    -------
    ::

        return success_response(
            data=serializer.data,
            message="User fetched successfully"
        )
    """
    return _build(
        success=True,
        message=message,
        data=data,
        errors=None,
        status_code=status_code,
    )


def error_response(
    message: str = messages.INTERNAL_SERVER_ERROR,
    errors: Any = None,
    status_code: int = 400,
) -> Response:
    """
    Return an error envelope.

    Parameters
    ----------
    message:
        Human-readable error message.
    errors:
        Serializer errors, field errors, or any additional detail.
    status_code:
        HTTP status code.  Defaults to 400.

    Example
    -------
    ::

        return error_response(
            message="Invalid input",
            errors=serializer.errors
        )
    """
    return _build(
        success=False,
        message=message,
        data=None,
        errors=errors,
        status_code=status_code,
    )
