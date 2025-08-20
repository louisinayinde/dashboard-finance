"""
Portfolio repository for user portfolio management
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, func, desc
import structlog

from .base import BaseRepository
from app.models.user_portfolio import UserPortfolio
from app.models.user import User
from app.models.stock import Stock

logger = structlog.get_logger()


class PortfolioRepository(BaseRepository[UserPortfolio, dict, dict]):
    """Portfolio repository with portfolio-specific operations"""
    
    def __init__(self):
        super().__init__(UserPortfolio)
    
    def get_user_portfolio(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[UserPortfolio]:
        """Get all portfolio positions for a user"""
        try:
            stmt = select(UserPortfolio).where(
                and_(
                    UserPortfolio.user_id == user_id,
                    UserPortfolio.is_active == "active"
                )
            ).order_by(UserPortfolio.created_at.desc()).offset(skip).limit(limit)
            
            result = db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error("Error getting user portfolio", user_id=user_id, error=str(e))
            raise
    
    def get_position_by_stock(self, db: Session, user_id: int, stock_id: int) -> Optional[UserPortfolio]:
        """Get a specific position for a user and stock"""
        try:
            stmt = select(UserPortfolio).where(
                and_(
                    UserPortfolio.user_id == user_id,
                    UserPortfolio.stock_id == stock_id,
                    UserPortfolio.is_active == "active"
                )
            )
            result = db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error("Error getting position by stock", user_id=user_id, stock_id=stock_id, error=str(e))
            raise
    
    def add_position(
        self, 
        db: Session, 
        user_id: int, 
        stock_id: int, 
        quantity: float, 
        price: float, 
        notes: Optional[str] = None
    ) -> UserPortfolio:
        """Add a new position to user portfolio"""
        try:
            # Check if position already exists
            existing_position = self.get_position_by_stock(db, user_id, stock_id)
            
            if existing_position:
                # Update existing position
                new_total_quantity = existing_position.quantity + quantity
                new_total_invested = existing_position.total_invested + (quantity * price)
                new_avg_price = new_total_invested / new_total_quantity
                
                existing_position.quantity = new_total_quantity
                existing_position.average_price = new_avg_price
                existing_position.total_invested = new_total_invested
                
                if notes:
                    existing_position.notes = notes
                
                db.add(existing_position)
                db.commit()
                db.refresh(existing_position)
                
                logger.info("Position updated", user_id=user_id, stock_id=stock_id, new_quantity=new_total_quantity)
                return existing_position
            else:
                # Create new position
                position_data = {
                    "user_id": user_id,
                    "stock_id": stock_id,
                    "quantity": quantity,
                    "average_price": price,
                    "total_invested": quantity * price,
                    "notes": notes,
                    "is_active": "active"
                }
                
                new_position = UserPortfolio(**position_data)
                db.add(new_position)
                db.commit()
                db.refresh(new_position)
                
                logger.info("New position created", user_id=user_id, stock_id=stock_id, quantity=quantity)
                return new_position
        except Exception as e:
            db.rollback()
            logger.error("Error adding position", user_id=user_id, stock_id=stock_id, error=str(e))
            raise
    
    def update_position(
        self, 
        db: Session, 
        user_id: int, 
        stock_id: int, 
        quantity: Optional[float] = None,
        price: Optional[float] = None,
        notes: Optional[str] = None
    ) -> Optional[UserPortfolio]:
        """Update an existing position"""
        try:
            position = self.get_position_by_stock(db, user_id, stock_id)
            if not position:
                return None
            
            if quantity is not None:
                position.quantity = quantity
                if price is not None:
                    position.average_price = price
                position.total_invested = quantity * position.average_price
            
            if notes is not None:
                position.notes = notes
            
            db.add(position)
            db.commit()
            db.refresh(position)
            
            logger.info("Position updated", user_id=user_id, stock_id=stock_id)
            return position
        except Exception as e:
            db.rollback()
            logger.error("Error updating position", user_id=user_id, stock_id=stock_id, error=str(e))
            raise
    
    def close_position(self, db: Session, user_id: int, stock_id: int) -> bool:
        """Close a position (mark as closed)"""
        try:
            position = self.get_position_by_stock(db, user_id, stock_id)
            if not position:
                return False
            
            position.is_active = "closed"
            db.add(position)
            db.commit()
            
            logger.info("Position closed", user_id=user_id, stock_id=stock_id)
            return True
        except Exception as e:
            db.rollback()
            logger.error("Error closing position", user_id=user_id, stock_id=stock_id, error=str(e))
            raise
    
    def get_portfolio_summary(self, db: Session, user_id: int) -> Dict[str, Any]:
        """Get portfolio summary for a user"""
        try:
            # Get all active positions
            positions = self.get_user_portfolio(db, user_id)
            
            if not positions:
                return {
                    "total_positions": 0,
                    "total_invested": 0.0,
                    "estimated_value": 0.0,
                    "unrealized_pnl": 0.0,
                    "positions": []
                }
            
            # Calculate totals
            total_positions = len(positions)
            total_invested = sum(pos.total_invested for pos in positions)
            
            # For now, estimated value is the same as invested (would need current prices)
            estimated_value = total_invested
            unrealized_pnl = estimated_value - total_invested
            
            # Get position details with stock info
            position_details = []
            for pos in positions:
                stock = db.get(Stock, pos.stock_id)
                position_details.append({
                    "id": pos.id,
                    "stock_symbol": stock.symbol if stock else "Unknown",
                    "stock_name": stock.name if stock else "Unknown",
                    "quantity": pos.quantity,
                    "average_price": pos.average_price,
                    "total_invested": pos.total_invested,
                    "notes": pos.notes,
                    "created_at": pos.created_at.isoformat() if pos.created_at else None
                })
            
            return {
                "total_positions": total_positions,
                "total_invested": total_invested,
                "estimated_value": estimated_value,
                "unrealized_pnl": unrealized_pnl,
                "positions": position_details
            }
        except Exception as e:
            logger.error("Error getting portfolio summary", user_id=user_id, error=str(e))
            raise
    
    def get_portfolio_by_sector(self, db: Session, user_id: int) -> Dict[str, Any]:
        """Get portfolio breakdown by sector"""
        try:
            # Join with stocks to get sector information
            stmt = select(
                Stock.sector,
                func.sum(UserPortfolio.total_invested).label("total_invested"),
                func.sum(UserPortfolio.quantity).label("total_quantity")
            ).join(
                UserPortfolio, Stock.id == UserPortfolio.stock_id
            ).where(
                and_(
                    UserPortfolio.user_id == user_id,
                    UserPortfolio.is_active == "active"
                )
            ).group_by(Stock.sector)
            
            result = db.execute(stmt)
            sector_breakdown = {}
            
            for row in result:
                sector = row.sector or "Unknown"
                sector_breakdown[sector] = {
                    "total_invested": float(row.total_invested),
                    "total_quantity": float(row.total_quantity)
                }
            
            return sector_breakdown
        except Exception as e:
            logger.error("Error getting portfolio by sector", user_id=user_id, error=str(e))
            raise
