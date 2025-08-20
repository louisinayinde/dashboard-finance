"""
UserPortfolio model for Dashboard Finance
"""

from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from .base import Base

class UserPortfolio(Base):
    """User portfolio model for managing user stock positions"""
    
    __tablename__ = "user_portfolios"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False, index=True)
    
    # Position data
    quantity = Column(Float, nullable=False)  # Number of shares
    average_price = Column(Float, nullable=False)  # Average purchase price
    total_invested = Column(Float, nullable=False)  # Total amount invested
    
    # Additional position info
    notes = Column(Text, nullable=True)  # User notes about this position
    purchase_date = Column(DateTime, nullable=True)  # First purchase date
    
    # Status
    is_active = Column(String(20), default="active", nullable=False)  # active, sold, closed
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="portfolios")
    stock = relationship("Stock", back_populates="portfolios")
    
    def __repr__(self):
        return f"<UserPortfolio(id={self.id}, user_id={self.user_id}, stock_id={self.stock_id}, quantity={self.quantity})>"
    
    @property
    def current_value(self) -> float:
        """Calculate current position value (quantity * current_price)"""
        # This would need to be calculated dynamically with current stock price
        return self.quantity * self.average_price
    
    @property
    def unrealized_pnl(self) -> float:
        """Calculate unrealized profit/loss"""
        # This would need current stock price to calculate
        return 0.0  # Placeholder
    
    @property
    def position_size(self) -> str:
        """Get position size category"""
        if self.total_invested < 1000:
            return "small"
        elif self.total_invested < 10000:
            return "medium"
        else:
            return "large"
