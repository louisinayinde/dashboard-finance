"""
SQLAlchemy models for Dashboard Finance
"""

from .user import User, UserRole
from .stock import Stock, MarketType
from .stock_price import StockPrice
from .user_portfolio import UserPortfolio
from .watchlist import Watchlist, WatchlistItem
from .scraping_log import ScrapingLog, ScrapingStatus, ScrapingType

# Export all models
__all__ = [
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

# Base class for all models
from .user import Base
