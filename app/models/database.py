"""
Database models for the application.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

# TODO: Add actual models
# - User
# - Stock
# - Price
# - Portfolio
# - Transaction
# etc.

class PlaceholderModel(Base):
    """Placeholder model to ensure Base is properly initialized."""
    __tablename__ = "placeholder"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
