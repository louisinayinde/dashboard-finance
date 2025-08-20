"""
Simple test endpoint for debugging
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/simple")
async def simple_test():
    """Simple test endpoint"""
    return {"message": "Simple test endpoint works!"}
