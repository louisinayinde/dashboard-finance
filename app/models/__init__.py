"""
SQLAlchemy models for Dashboard Finance
"""

# Import base first
from .base import Base

# Import models in dependency order
from .user import User, UserRole
from .stock import Stock, MarketType
from .stock_price import StockPrice
from .user_portfolio import UserPortfolio
from .watchlist import Watchlist, WatchlistItem
from .scraping_log import ScrapingLog, ScrapingStatus, ScrapingType

# Export all models
__all__ = [
    # Base
    "Base",
    
    # User models
    "User",
    "UserRole",
    
    # Stock models
    "Stock", 
    "MarketType",
    "StockPrice",
    
    # Portfolio models
    "UserPortfolio",
    
    # Watchlist models
    "Watchlist",
    "WatchlistItem",
    
    # Scraping models
    "ScrapingLog",
    "ScrapingStatus", 
    "ScrapingType",
]
