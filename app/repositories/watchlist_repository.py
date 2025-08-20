"""
Watchlist repository for user watchlist management
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_
import structlog

from .base import BaseRepository
from app.models.watchlist import Watchlist, WatchlistItem
from app.models.stock import Stock

logger = structlog.get_logger()


class WatchlistRepository(BaseRepository[Watchlist, dict, dict]):
    """Watchlist repository with watchlist-specific operations"""
    
    def __init__(self):
        super().__init__(Watchlist)
    
    def get_user_watchlists(self, db: Session, user_id: int) -> List[Watchlist]:
        """Get all watchlists for a user"""
        try:
            stmt = select(Watchlist).where(Watchlist.user_id == user_id).order_by(Watchlist.created_at.desc())
            result = db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error("Error getting user watchlists", user_id=user_id, error=str(e))
            raise
    
    def get_default_watchlist(self, db: Session, user_id: int) -> Optional[Watchlist]:
        """Get the default watchlist for a user"""
        try:
            stmt = select(Watchlist).where(
                and_(
                    Watchlist.user_id == user_id,
                    Watchlist.is_default == True
                )
            )
            result = db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error("Error getting default watchlist", user_id=user_id, error=str(e))
            raise
    
    def create_watchlist(
        self, 
        db: Session, 
        user_id: int, 
        name: str, 
        description: Optional[str] = None,
        is_default: bool = False
    ) -> Watchlist:
        """Create a new watchlist for a user"""
        try:
            # If this is the new default, unset other defaults
            if is_default:
                self._unset_other_defaults(db, user_id)
            
            watchlist_data = {
                "user_id": user_id,
                "name": name,
                "description": description,
                "is_default": is_default
            }
            
            new_watchlist = Watchlist(**watchlist_data)
            db.add(new_watchlist)
            db.commit()
            db.refresh(new_watchlist)
            
            logger.info("Watchlist created", user_id=user_id, watchlist_id=new_watchlist.id, name=name)
            return new_watchlist
        except Exception as e:
            db.rollback()
            logger.error("Error creating watchlist", user_id=user_id, name=name, error=str(e))
            raise
    
    def add_stock_to_watchlist(
        self, 
        db: Session, 
        watchlist_id: int, 
        stock_id: int, 
        notes: Optional[str] = None,
        target_price: Optional[str] = None
    ) -> WatchlistItem:
        """Add a stock to a watchlist"""
        try:
            # Check if stock is already in watchlist
            existing_item = self._get_watchlist_item(db, watchlist_id, stock_id)
            if existing_item:
                # Update existing item
                if notes is not None:
                    existing_item.notes = notes
                if target_price is not None:
                    existing_item.target_price = target_price
                
                db.add(existing_item)
                db.commit()
                db.refresh(existing_item)
                
                logger.info("Watchlist item updated", watchlist_id=watchlist_id, stock_id=stock_id)
                return existing_item
            
            # Create new item
            item_data = {
                "watchlist_id": watchlist_id,
                "stock_id": stock_id,
                "notes": notes,
                "target_price": target_price,
                "alert_enabled": True
            }
            
            new_item = WatchlistItem(**item_data)
            db.add(new_item)
            db.commit()
            db.refresh(new_item)
            
            logger.info("Stock added to watchlist", watchlist_id=watchlist_id, stock_id=stock_id)
            return new_item
        except Exception as e:
            db.rollback()
            logger.error("Error adding stock to watchlist", watchlist_id=watchlist_id, stock_id=stock_id, error=str(e))
            raise
    
    def remove_stock_from_watchlist(self, db: Session, watchlist_id: int, stock_id: int) -> bool:
        """Remove a stock from a watchlist"""
        try:
            item = self._get_watchlist_item(db, watchlist_id, stock_id)
            if not item:
                return False
            
            db.delete(item)
            db.commit()
            
            logger.info("Stock removed from watchlist", watchlist_id=watchlist_id, stock_id=stock_id)
            return True
        except Exception as e:
            db.rollback()
            logger.error("Error removing stock from watchlist", watchlist_id=watchlist_id, stock_id=stock_id, error=str(e))
            raise
    
    def get_watchlist_items(self, db: Session, watchlist_id: int) -> List[Dict[str, Any]]:
        """Get all items in a watchlist with stock details"""
        try:
            stmt = select(WatchlistItem).where(WatchlistItem.watchlist_id == watchlist_id)
            result = db.execute(stmt)
            items = result.scalars().all()
            
            # Get stock details for each item
            item_details = []
            for item in items:
                stock = db.get(Stock, item.stock_id)
                item_details.append({
                    "id": item.id,
                    "stock_symbol": stock.symbol if stock else "Unknown",
                    "stock_name": stock.name if stock else "Unknown",
                    "notes": item.notes,
                    "target_price": item.target_price,
                    "alert_enabled": item.alert_enabled,
                    "created_at": item.created_at.isoformat() if item.created_at else None
                })
            
            return item_details
        except Exception as e:
            logger.error("Error getting watchlist items", watchlist_id=watchlist_id, error=str(e))
            raise
    
    def search_watchlist_stocks(
        self, 
        db: Session, 
        watchlist_id: int, 
        query: str
    ) -> List[Dict[str, Any]]:
        """Search stocks in a watchlist by symbol or name"""
        try:
            # Get watchlist items
            stmt = select(WatchlistItem).where(WatchlistItem.watchlist_id == watchlist_id)
            result = db.execute(stmt)
            items = result.scalars().all()
            
            # Get stock details and filter by query
            matching_items = []
            for item in items:
                stock = db.get(Stock, item.stock_id)
                if stock and (
                    query.lower() in stock.symbol.lower() or 
                    query.lower() in stock.name.lower()
                ):
                    matching_items.append({
                        "id": item.id,
                        "stock_symbol": stock.symbol,
                        "stock_name": stock.name,
                        "notes": item.notes,
                        "target_price": item.target_price,
                        "alert_enabled": item.alert_enabled
                    })
            
            return matching_items
        except Exception as e:
            logger.error("Error searching watchlist stocks", watchlist_id=watchlist_id, query=query, error=str(e))
            raise
    
    def set_default_watchlist(self, db: Session, user_id: int, watchlist_id: int) -> bool:
        """Set a watchlist as the default for a user"""
        try:
            # Unset other defaults
            self._unset_other_defaults(db, user_id)
            
            # Set new default
            watchlist = db.get(Watchlist, watchlist_id)
            if not watchlist or watchlist.user_id != user_id:
                return False
            
            watchlist.is_default = True
            db.add(watchlist)
            db.commit()
            
            logger.info("Default watchlist set", user_id=user_id, watchlist_id=watchlist_id)
            return True
        except Exception as e:
            db.rollback()
            logger.error("Error setting default watchlist", user_id=user_id, watchlist_id=watchlist_id, error=str(e))
            raise
    
    def _unset_other_defaults(self, db: Session, user_id: int) -> None:
        """Unset other default watchlists for a user"""
        try:
            stmt = select(Watchlist).where(
                and_(
                    Watchlist.user_id == user_id,
                    Watchlist.is_default == True
                )
            )
            result = db.execute(stmt)
            defaults = result.scalars().all()
            
            for default in defaults:
                default.is_default = False
                db.add(default)
            
            db.commit()
        except Exception as e:
            logger.error("Error unsetting other defaults", user_id=user_id, error=str(e))
            raise
    
    def _get_watchlist_item(self, db: Session, watchlist_id: int, stock_id: int) -> Optional[WatchlistItem]:
        """Get a specific watchlist item"""
        try:
            stmt = select(WatchlistItem).where(
                and_(
                    WatchlistItem.watchlist_id == watchlist_id,
                    WatchlistItem.stock_id == stock_id
                )
            )
            result = db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error("Error getting watchlist item", watchlist_id=watchlist_id, stock_id=stock_id, error=str(e))
            raise
