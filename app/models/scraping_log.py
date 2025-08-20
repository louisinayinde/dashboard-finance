"""
ScrapingLog model for Dashboard Finance
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class ScrapingStatus(enum.Enum):
    """Scraping status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"
    RATE_LIMITED = "rate_limited"

class ScrapingType(enum.Enum):
    """Scraping type enumeration"""
    STOCK_PRICE = "stock_price"
    COMPANY_INFO = "company_info"
    FINANCIAL_DATA = "financial_data"
    MARKET_DATA = "market_data"
    NEWS = "news"

class ScrapingLog(Base):
    """Scraping log model for monitoring scraping operations"""
    
    __tablename__ = "scraping_logs"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Scraping info
    source = Column(String(100), nullable=False, index=True)  # yahoo, alpha_vantage, marketwatch
    scraping_type = Column(Enum(ScrapingType), nullable=False, index=True)
    target_symbol = Column(String(20), nullable=True, index=True)  # Stock symbol if applicable
    
    # Status and timing
    status = Column(Enum(ScrapingStatus), default=ScrapingStatus.PENDING, nullable=False)
    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    duration = Column(Float, nullable=True)  # Duration in seconds
    
    # Results
    records_processed = Column(Integer, default=0, nullable=False)
    records_updated = Column(Integer, default=0, nullable=False)
    records_created = Column(Integer, default=0, nullable=False)
    
    # Error handling
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0, nullable=False)
    max_retries = Column(Integer, default=3, nullable=False)
    
    # Metadata
    user_agent = Column(String(255), nullable=True)
    ip_address = Column(String(45), nullable=True)  # IPv4 or IPv6
    request_headers = Column(Text, nullable=True)  # JSON string of headers
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<ScrapingLog(id={self.id}, source='{self.source}', type='{self.scraping_type}', status='{self.status}')>"
    
    @property
    def is_successful(self) -> bool:
        """Check if scraping was successful"""
        return self.status == ScrapingStatus.SUCCESS
    
    @property
    def is_failed(self) -> bool:
        """Check if scraping failed"""
        return self.status in [ScrapingStatus.FAILED, ScrapingStatus.TIMEOUT, ScrapingStatus.RATE_LIMITED]
    
    @property
    def can_retry(self) -> bool:
        """Check if scraping can be retried"""
        return self.retry_count < self.max_retries and self.is_failed
    
    @property
    def efficiency_rate(self) -> float:
        """Calculate efficiency rate (records_processed / duration)"""
        if self.duration and self.duration > 0:
            return self.records_processed / self.duration
        return 0.0
