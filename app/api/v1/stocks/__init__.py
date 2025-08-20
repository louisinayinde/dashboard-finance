"""
Stocks API module.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/stocks", tags=["stocks"])

# Placeholder endpoint
@router.get("/")
async def stocks_root():
    """Stocks root endpoint."""
    return {"message": "Stocks API"}

# TODO: Add stock data endpoints
# - GET /stocks/search
# - GET /stocks/{symbol}
# - GET /stocks/{symbol}/history
# - GET /stocks/{symbol}/price
