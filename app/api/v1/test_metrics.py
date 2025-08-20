"""
Test endpoints for generating metrics
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/summary")
async def metrics_summary():
    """Get a summary of current metrics values"""
    return {
        "message": "Current metrics summary",
        "endpoints": {
            "health": "/health",
            "metrics": "/metrics",
            "docs": "/docs"
        },
        "test_endpoints": {
            "summary": "/api/v1/test/summary",
            "simple": "/api/v1/debug/simple"
        }
    }

@router.get("/ping")
async def ping():
    """Simple ping endpoint"""
    return {"message": "pong", "status": "ok"}
