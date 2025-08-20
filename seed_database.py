#!/usr/bin/env python3
"""
Database seeding script for Dashboard Finance
"""

import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.seeders.main_seeder import MainSeeder
import structlog

# Setup logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


def main():
    """Main seeding function"""
    logger.info("Starting database seeding process...")
    
    # Get database session
    db: Session = SessionLocal()
    
    try:
        # Create seeder instance
        seeder = MainSeeder(db)
        
        # Check if data already exists
        from app.models.user import User
        existing_users = db.query(User).count()
        
        if existing_users > 0:
            logger.warning(f"Database already contains {existing_users} users. Skipping seeding.")
            choice = input("Do you want to clear existing data and reseed? (y/N): ").strip().lower()
            
            if choice == 'y':
                logger.info("Clearing existing data...")
                seeder.clear_all_data()
            else:
                logger.info("Seeding cancelled.")
                return
        
        # Seed the database
        seeder.seed_all()
        
        logger.info("Database seeding completed successfully!")
        
        # Display summary
        display_summary(db)
        
    except Exception as e:
        logger.error("Error during seeding", error=str(e))
        sys.exit(1)
    finally:
        db.close()


def display_summary(db: Session):
    """Display a summary of the seeded data"""
    try:
        from app.models.user import User
        from app.models.stock import Stock
        from app.models.stock_price import StockPrice
        from app.models.user_portfolio import UserPortfolio
        from app.models.watchlist import Watchlist, WatchlistItem
        
        user_count = db.query(User).count()
        stock_count = db.query(Stock).count()
        price_count = db.query(StockPrice).count()
        portfolio_count = db.query(UserPortfolio).count()
        watchlist_count = db.query(Watchlist).count()
        watchlist_item_count = db.query(WatchlistItem).count()
        
        print("\n" + "="*60)
        print("🎉 DATABASE SEEDING SUMMARY")
        print("="*60)
        print(f"👥 Users created: {user_count}")
        print(f"📈 Stocks created: {stock_count}")
        print(f"💰 Stock prices created: {price_count}")
        print(f"💼 Portfolio positions: {portfolio_count}")
        print(f"👀 Watchlists created: {watchlist_count}")
        print(f"📋 Watchlist items: {watchlist_item_count}")
        print("="*60)
        
        # Display user credentials
        print("\n🔑 TEST USER CREDENTIALS:")
        print("-" * 40)
        users = db.query(User).all()
        for user in users:
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Password: password123")
            print(f"Role: {user.role.value}")
            print("-" * 40)
        
        print("\n🚀 You can now test the application with these credentials!")
        
    except Exception as e:
        logger.error("Error displaying summary", error=str(e))


if __name__ == "__main__":
    main()
