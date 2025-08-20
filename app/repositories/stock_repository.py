"""
Stock repository for stock management operations
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_, desc, asc
import structlog

from .base import BaseRepository
from app.models.stock import Stock, MarketType

logger = structlog.get_logger()


class StockRepository(BaseRepository[Stock, dict, dict]):
    """Stock repository with stock-specific operations"""
    
    def __init__(self):
        super().__init__(Stock)
    
    def get_by_symbol(self, db: Session, symbol: str) -> Optional[Stock]:
        """Get stock by symbol"""
        try:
            stmt = select(Stock).where(Stock.symbol == symbol.upper())
            result = db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error("Error getting stock by symbol", symbol=symbol, error=str(e))
            raise
    
    def get_by_isin(self, db: Session, isin: str) -> Optional[Stock]:
        """Get stock by ISIN"""
        try:
            stmt = select(Stock).where(Stock.isin == isin.upper())
            result = db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error("Error getting stock by ISIN", isin=isin, error=str(e))
            raise
    
    def search_stocks(
        self, 
        db: Session, 
        query: str, 
        market_type: Optional[MarketType] = None,
        sector: Optional[str] = None,
        skip: int = 0, 
        limit: int = 50
    ) -> List[Stock]:
        """Search stocks by name, symbol, or description"""
        try:
            stmt = select(Stock).where(
                and_(
                    Stock.is_active == True,
                    or_(
                        Stock.symbol.ilike(f"%{query}%"),
                        Stock.name.ilike(f"%{query}%"),
                        Stock.company_description.ilike(f"%{query}%")
                    )
                )
            )
            
            # Apply additional filters
            if market_type:
                stmt = stmt.where(Stock.market_type == market_type)
            
            if sector:
                stmt = stmt.where(Stock.sector.ilike(f"%{sector}%"))
            
            stmt = stmt.order_by(Stock.symbol).offset(skip).limit(limit)
            result = db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error("Error searching stocks", query=query, error=str(e))
            raise
    
    def get_stocks_by_market(self, db: Session, market: str, skip: int = 0, limit: int = 100) -> List[Stock]:
        """Get stocks by market (NYSE, NASDAQ, etc.)"""
        try:
            stmt = select(Stock).where(
                and_(
                    Stock.market == market.upper(),
                    Stock.is_active == True
                )
            ).order_by(Stock.symbol).offset(skip).limit(limit)
            
            result = db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error("Error getting stocks by market", market=market, error=str(e))
            raise
    
    def get_stocks_by_sector(self, db: Session, sector: str, skip: int = 0, limit: int = 100) -> List[Stock]:
        """Get stocks by sector"""
        try:
            stmt = select(Stock).where(
                and_(
                    Stock.sector.ilike(f"%{sector}%"),
                    Stock.is_active == True
                )
            ).order_by(Stock.symbol).offset(skip).limit(limit)
            
            result = db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error("Error getting stocks by sector", sector=sector, error=str(e))
            raise
    
    def get_stocks_by_type(self, db: Session, market_type: MarketType, skip: int = 0, limit: int = 100) -> List[Stock]:
        """Get stocks by market type (STOCK, ETF, INDEX, etc.)"""
        try:
            stmt = select(Stock).where(
                and_(
                    Stock.market_type == market_type,
                    Stock.is_active == True
                )
            ).order_by(Stock.symbol).offset(skip).limit(limit)
            
            result = db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error("Error getting stocks by type", market_type=market_type.value, error=str(e))
            raise
    
    def get_tradable_stocks(self, db: Session, skip: int = 0, limit: int = 100) -> List[Stock]:
        """Get all tradable stocks"""
        try:
            stmt = select(Stock).where(
                and_(
                    Stock.is_tradable == True,
                    Stock.is_active == True
                )
            ).order_by(Stock.symbol).offset(skip).limit(limit)
            
            result = db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error("Error getting tradable stocks", error=str(e))
            raise
    
    def get_stocks_needing_price_update(self, db: Session, hours_old: int = 24, limit: int = 100) -> List[Stock]:
        """Get stocks that need price updates"""
        try:
            from datetime import datetime, timedelta
            cutoff_time = datetime.utcnow() - timedelta(hours=hours_old)
            
            stmt = select(Stock).where(
                and_(
                    Stock.is_active == True,
                    or_(
                        Stock.last_price_update.is_(None),
                        Stock.last_price_update < cutoff_time
                    )
                )
            ).order_by(Stock.last_price_update.asc().nullsfirst()).limit(limit)
            
            result = db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error("Error getting stocks needing price update", hours_old=hours_old, error=str(e))
            raise
    
    def update_stock_price_timestamp(self, db: Session, stock_id: int) -> bool:
        """Update the last_price_update timestamp for a stock"""
        try:
            stock = db.get(Stock, stock_id)
            if not stock:
                return False
            
            from datetime import datetime
            stock.last_price_update = datetime.utcnow()
            db.add(stock)
            db.commit()
            
            return True
        except Exception as e:
            db.rollback()
            logger.error("Error updating stock price timestamp", stock_id=stock_id, error=str(e))
            raise
    
    def get_market_summary(self, db: Session) -> Dict[str, Any]:
        """Get market summary statistics"""
        try:
            # Count stocks by market type
            type_counts = {}
            for market_type in MarketType:
                stmt = select(Stock).where(
                    and_(
                        Stock.market_type == market_type,
                        Stock.is_active == True
                    )
                )
                result = db.execute(stmt)
                type_counts[market_type.value] = len(result.scalars().all())
            
            # Count stocks by market
            market_counts = {}
            markets_stmt = select(Stock.market).distinct().where(Stock.is_active == True)
            markets_result = db.execute(markets_stmt)
            markets = [row[0] for row in markets_result if row[0]]
            
            for market in markets:
                stmt = select(Stock).where(
                    and_(
                        Stock.market == market,
                        Stock.is_active == True
                    )
                )
                result = db.execute(stmt)
                market_counts[market] = len(result.scalars().all())
            
            # Total active stocks
            total_stmt = select(Stock).where(Stock.is_active == True)
            total_result = db.execute(total_stmt)
            total_stocks = len(total_result.scalars().all())
            
            return {
                "total_stocks": total_stocks,
                "by_type": type_counts,
                "by_market": market_counts
            }
        except Exception as e:
            logger.error("Error getting market summary", error=str(e))
            raise
