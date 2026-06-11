"""
Centralised message constants.

Import these instead of writing raw strings anywhere in the project.
"""

# ── Success ──────────────────────────────────────────────────────────────────
SUCCESS: str = "Success"
CREATED: str = "Created successfully"
UPDATED: str = "Updated successfully"
DELETED: str = "Deleted successfully"

# ── Validation ────────────────────────────────────────────────────────────────
VALIDATION_ERROR: str = "Validation Error"

# ── Auth ──────────────────────────────────────────────────────────────────────
AUTHENTICATION_FAILED: str = "Authentication Failed"
NOT_AUTHENTICATED: str = "Authentication Credentials Missing"
PERMISSION_DENIED: str = "Permission Denied"

# ── Resource ──────────────────────────────────────────────────────────────────
RESOURCE_NOT_FOUND: str = "Resource Not Found"

# ── Server ────────────────────────────────────────────────────────────────────
INTERNAL_SERVER_ERROR: str = "Internal Server Error"
