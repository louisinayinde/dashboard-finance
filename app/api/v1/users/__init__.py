"""
Users API module.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

# Placeholder endpoint
@router.get("/")
async def users_root():
    """Users root endpoint."""
    return {"message": "Users API"}

# TODO: Add user management endpoints
# - GET /users/me
# - PUT /users/me
# - GET /users/{user_id}
# - DELETE /users/{user_id}
