"""
StockPrice model for Dashboard Finance
"""

from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class StockPrice(Base):
    """Stock price model for historical price data"""
    
    __tablename__ = "stock_prices"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False, index=True)
    
    # Price data
    open_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    adjusted_close = Column(Float, nullable=True)  # Adjusted for splits/dividends
    
    # Volume and trading data
    volume = Column(Integer, nullable=False)
    average_volume = Column(Integer, nullable=True)
    
    # Additional metrics
    change_amount = Column(Float, nullable=True)  # Price change from previous day
    change_percent = Column(Float, nullable=True)  # Percentage change
    
    # Data source and quality
    source = Column(String(100), nullable=False)  # yahoo, alpha_vantage, etc.
    data_quality = Column(String(20), default="high", nullable=False)  # high, medium, low
    
    # Timestamps
    timestamp = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    stock = relationship("Stock", back_populates="prices")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_stock_timestamp', 'stock_id', 'timestamp'),
        Index('idx_timestamp_source', 'timestamp', 'source'),
    )
    
    def __repr__(self):
        return f"<StockPrice(id={self.id}, stock_id={self.stock_id}, close={self.close_price}, timestamp='{self.timestamp}')>"
    
    @property
    def price_range(self) -> float:
        """Get the price range (high - low)"""
        return self.high_price - self.low_price
    
    @property
    def is_up_day(self) -> bool:
        """Check if it's an up day (close > open)"""
        return self.close_price > self.open_price
    
    @property
    def is_down_day(self) -> bool:
        """Check if it's a down day (close < open)"""
        return self.close_price < self.open_price
