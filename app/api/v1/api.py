"""
Main API router that includes all sub-routers
"""

from fastapi import APIRouter

from app.api.v1 import auth, stocks, users, websocket, test_metrics, simple_test

# Create main API router
api_router = APIRouter()

# Include all sub-routers
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)

api_router.include_router(
    stocks.router,
    prefix="/stocks",
    tags=["Stocks"]
)

api_router.include_router(
    websocket.router,
    prefix="/ws",
    tags=["WebSocket"]
)

api_router.include_router(
    test_metrics.router,
    prefix="/test",
    tags=["Test Metrics"]
)

api_router.include_router(
    simple_test.router,
    prefix="/debug",
    tags=["Debug"]
)

# Health check endpoint for API
@api_router.get("/health")
async def api_health_check():
    """API health check endpoint"""
    return {
        "status": "healthy",
        "api_version": "v1",
        "endpoints": [
            "/auth",
            "/users", 
            "/stocks",
            "/ws"
        ]
    }
