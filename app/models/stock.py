"""
Stock model for Dashboard Finance
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean, Enum
from sqlalchemy.orm import relationship
import enum

from .base import Base

class MarketType(enum.Enum):
    """Market type enumeration"""
    STOCK = "stock"
    ETF = "etf"
    INDEX = "index"
    CRYPTO = "crypto"
    FOREX = "forex"

class Stock(Base):
    """Stock model for financial instruments"""
    
    __tablename__ = "stocks"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic identification
    symbol = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    isin = Column(String(12), unique=True, nullable=True)  # International Securities Identification Number
    
    # Market information
    market = Column(String(100), nullable=True)  # NYSE, NASDAQ, etc.
    market_type = Column(Enum(MarketType), default=MarketType.STOCK, nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    
    # Company information
    sector = Column(String(100), nullable=True)
    industry = Column(String(100), nullable=True)
    company_description = Column(Text, nullable=True)
    website = Column(String(255), nullable=True)
    
    # Financial metrics
    market_cap = Column(Float, nullable=True)  # Market capitalization in currency
    pe_ratio = Column(Float, nullable=True)  # Price-to-Earnings ratio
    dividend_yield = Column(Float, nullable=True)  # Dividend yield percentage
    beta = Column(Float, nullable=True)  # Beta coefficient
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_tradable = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_price_update = Column(DateTime, nullable=True)
    
    # Relationships
    prices = relationship("StockPrice", back_populates="stock", cascade="all, delete-orphan")
    portfolios = relationship("UserPortfolio", back_populates="stock", cascade="all, delete-orphan")
    watchlists = relationship("WatchlistItem", back_populates="stock", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Stock(id={self.id}, symbol='{self.symbol}', name='{self.name}')>"
    
    @property
    def display_name(self) -> str:
        """Get display name for the stock"""
        return f"{self.symbol} - {self.name}"
    
    @property
    def is_index(self) -> bool:
        """Check if stock is an index"""
        return self.market_type == MarketType.INDEX
    
    @property
    def is_crypto(self) -> bool:
        """Check if stock is a cryptocurrency"""
        return self.market_type == MarketType.CRYPTO
