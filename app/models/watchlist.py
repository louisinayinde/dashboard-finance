"""
Watchlist models for Dashboard Finance
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship

from .base import Base

class Watchlist(Base):
    """Watchlist model for user stock watchlists"""
    
    __tablename__ = "watchlists"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Watchlist info
    name = Column(String(100), nullable=False)  # Watchlist name
    description = Column(Text, nullable=True)  # Optional description
    is_default = Column(Boolean, default=False, nullable=False)  # Is this the default watchlist?
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="watchlists")
    items = relationship("WatchlistItem", back_populates="watchlist", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Watchlist(id={self.id}, user_id={self.user_id}, name='{self.name}')>"

class WatchlistItem(Base):
    """Individual stock item in a watchlist"""
    
    __tablename__ = "watchlist_items"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    watchlist_id = Column(Integer, ForeignKey("watchlists.id"), nullable=False, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False, index=True)
    
    # Item info
    notes = Column(Text, nullable=True)  # User notes about this stock
    target_price = Column(String(20), nullable=True)  # Target price for alerts
    alert_enabled = Column(Boolean, default=True, nullable=False)  # Enable price alerts
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    watchlist = relationship("Watchlist", back_populates="items")
    stock = relationship("Stock", back_populates="watchlists")
    
    def __repr__(self):
        return f"<WatchlistItem(id={self.id}, watchlist_id={self.watchlist_id}, stock_id={self.stock_id})>"
