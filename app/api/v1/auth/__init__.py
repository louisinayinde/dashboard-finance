"""
Authentication API module.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["authentication"])

# Placeholder endpoint
@router.get("/")
async def auth_root():
    """Authentication root endpoint."""
    return {"message": "Authentication API"}

# TODO: Add authentication endpoints
# - POST /auth/login
# - POST /auth/register
# - POST /auth/refresh
# - POST /auth/logout
