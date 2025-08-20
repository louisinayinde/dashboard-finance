"""
WebSocket API module.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/ws", tags=["websocket"])

# Placeholder endpoint
@router.get("/")
async def websocket_root():
    """WebSocket root endpoint."""
    return {"message": "WebSocket API"}

# TODO: Add WebSocket endpoints
# - GET /ws/stocks/{symbol} - WebSocket connection for real-time stock data
# - GET /ws/portfolio/{user_id} - WebSocket connection for portfolio updates
