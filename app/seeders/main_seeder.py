"""
Main seeder for populating database with test data
"""

from datetime import datetime
from sqlalchemy.orm import Session
import structlog

from app.models.user import User, UserRole
from app.models.stock import Stock, MarketType
from app.models.stock_price import StockPrice
from app.models.user_portfolio import UserPortfolio
from app.models.watchlist import Watchlist, WatchlistItem
from app.repositories.user_repository import UserRepository
from app.repositories.stock_repository import StockRepository
from app.repositories.portfolio_repository import PortfolioRepository
from app.repositories.watchlist_repository import WatchlistRepository

logger = structlog.get_logger()


class MainSeeder:
    """Main seeder class for populating database with test data"""
    
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository()
        self.stock_repo = StockRepository()
        self.portfolio_repo = PortfolioRepository()
        self.watchlist_repo = WatchlistRepository()
    
    def seed_all(self) -> None:
        """Seed all data"""
        logger.info("Starting database seeding...")
        
        try:
            # Seed users first
            users = self._seed_users()
            
            # Seed stocks
            stocks = self._seed_stocks()
            
            # Seed stock prices
            self._seed_stock_prices(stocks)
            
            # Seed portfolios
            self._seed_portfolios(users, stocks)
            
            # Seed watchlists
            self._seed_watchlists(users, stocks)
            
            logger.info("Database seeding completed successfully!")
            
        except Exception as e:
            logger.error("Error during seeding", error=str(e))
            raise
    
    def _seed_users(self) -> list:
        """Seed users with test data"""
        logger.info("Seeding users...")
        
        users_data = [
            {
                "email": "admin@dashboard.com",
                "username": "admin",
                "password": "admin123",
                "first_name": "Admin",
                "last_name": "User",
                "role": UserRole.ADMIN,
                "is_verified": True
            },
            {
                "email": "john.doe@example.com",
                "username": "john_doe",
                "password": "password123",
                "first_name": "John",
                "last_name": "Doe",
                "role": UserRole.PREMIUM,
                "is_verified": True
            },
            {
                "email": "jane.smith@example.com",
                "username": "jane_smith",
                "password": "password123",
                "first_name": "Jane",
                "last_name": "Smith",
                "role": UserRole.USER,
                "is_verified": True
            },
            {
                "email": "bob.wilson@example.com",
                "username": "bob_wilson",
                "password": "password123",
                "first_name": "Bob",
                "last_name": "Wilson",
                "role": UserRole.USER,
                "is_verified": False
            }
        ]
        
        users = []
        for user_data in users_data:
            user = self.user_repo.create_user(self.db, user_data)
            users.append(user)
            logger.info(f"Created user: {user.username}")
        
        return users
    
    def _seed_stocks(self) -> list:
        """Seed stocks with test data"""
        logger.info("Seeding stocks...")
        
        stocks_data = [
            # Tech Stocks
            {
                "symbol": "AAPL",
                "name": "Apple Inc.",
                "market": "NASDAQ",
                "market_type": MarketType.STOCK,
                "currency": "USD",
                "sector": "Technology",
                "industry": "Consumer Electronics",
                "company_description": "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide.",
                "website": "https://www.apple.com",
                "market_cap": 3000000000000,  # 3 trillion
                "pe_ratio": 25.5,
                "dividend_yield": 0.5,
                "beta": 1.2
            },
            {
                "symbol": "MSFT",
                "name": "Microsoft Corporation",
                "market": "NASDAQ",
                "market_type": MarketType.STOCK,
                "currency": "USD",
                "sector": "Technology",
                "industry": "Software",
                "company_description": "Microsoft Corporation develops, licenses, and supports software, services, devices, and solutions worldwide.",
                "website": "https://www.microsoft.com",
                "market_cap": 2800000000000,  # 2.8 trillion
                "pe_ratio": 30.2,
                "dividend_yield": 0.8,
                "beta": 0.9
            },
            {
                "symbol": "GOOGL",
                "name": "Alphabet Inc.",
                "market": "NASDAQ",
                "market_type": MarketType.STOCK,
                "currency": "USD",
                "sector": "Technology",
                "industry": "Internet Services",
                "company_description": "Alphabet Inc. provides online advertising services in the United States, Europe, the Middle East, Africa, the Asia-Pacific, Canada, and Latin America.",
                "website": "https://www.google.com",
                "market_cap": 1800000000000,  # 1.8 trillion
                "pe_ratio": 28.5,
                "dividend_yield": 0.0,
                "beta": 1.1
            },
            # Financial Stocks
            {
                "symbol": "JPM",
                "name": "JPMorgan Chase & Co.",
                "market": "NYSE",
                "market_type": MarketType.STOCK,
                "currency": "USD",
                "sector": "Financial Services",
                "industry": "Banks",
                "company_description": "JPMorgan Chase & Co. operates as a financial services company worldwide.",
                "website": "https://www.jpmorganchase.com",
                "market_cap": 450000000000,  # 450 billion
                "pe_ratio": 12.8,
                "dividend_yield": 2.8,
                "beta": 1.3
            },
            # ETFs
            {
                "symbol": "SPY",
                "name": "SPDR S&P 500 ETF Trust",
                "market": "NYSE",
                "market_type": MarketType.ETF,
                "currency": "USD",
                "sector": "ETF",
                "industry": "Broad Market",
                "company_description": "The SPDR S&P 500 ETF Trust tracks the S&P 500 Index, which comprises 500 large-cap U.S. stocks.",
                "website": "https://www.spdrs.com",
                "market_cap": 400000000000,  # 400 billion
                "pe_ratio": 22.5,
                "dividend_yield": 1.5,
                "beta": 1.0
            },
            {
                "symbol": "QQQ",
                "name": "Invesco QQQ Trust",
                "market": "NASDAQ",
                "market_type": MarketType.ETF,
                "currency": "USD",
                "sector": "ETF",
                "industry": "Technology",
                "company_description": "The Invesco QQQ Trust tracks the NASDAQ-100 Index, which includes 100 of the largest non-financial companies listed on the NASDAQ.",
                "website": "https://www.invesco.com",
                "market_cap": 200000000000,  # 200 billion
                "pe_ratio": 28.5,
                "dividend_yield": 0.6,
                "beta": 1.2
            },
            # Indices
            {
                "symbol": "^GSPC",
                "name": "S&P 500 Index",
                "market": "INDEX",
                "market_type": MarketType.INDEX,
                "currency": "USD",
                "sector": "Index",
                "industry": "Broad Market",
                "company_description": "The S&P 500 is a stock market index that tracks 500 large companies listed on stock exchanges in the United States.",
                "website": "https://www.spglobal.com",
                "market_cap": None,
                "pe_ratio": 22.5,
                "dividend_yield": 1.5,
                "beta": 1.0
            }
        ]
        
        stocks = []
        for stock_data in stocks_data:
            stock = self.stock_repo.create(self.db, stock_data)
            stocks.append(stock)
            logger.info(f"Created stock: {stock.symbol} - {stock.name}")
        
        return stocks
    
    def _seed_stock_prices(self, stocks: list) -> None:
        """Seed stock prices with historical data"""
        logger.info("Seeding stock prices...")
        
        from datetime import datetime, timedelta
        
        # Generate 30 days of historical data
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        
        for stock in stocks:
            if stock.market_type == MarketType.INDEX:
                continue  # Skip indices for now
            
            current_date = start_date
            base_price = 100.0  # Base price for simulation
            
            while current_date <= end_date:
                # Simulate daily price movement
                import random
                change_percent = random.uniform(-0.05, 0.05)  # -5% to +5%
                new_price = base_price * (1 + change_percent)
                
                # Generate OHLC data
                open_price = base_price
                high_price = max(open_price, new_price) * random.uniform(1.0, 1.02)
                low_price = min(open_price, new_price) * random.uniform(0.98, 1.0)
                close_price = new_price
                
                # Volume
                volume = random.randint(1000000, 10000000)
                
                price_data = {
                    "stock_id": stock.id,
                    "open_price": round(open_price, 2),
                    "high_price": round(high_price, 2),
                    "low_price": round(low_price, 2),
                    "close_price": round(close_price, 2),
                    "adjusted_close": round(close_price, 2),
                    "volume": volume,
                    "average_volume": volume,
                    "change_amount": round(close_price - open_price, 2),
                    "change_percent": round(((close_price - open_price) / open_price) * 100, 2),
                    "source": "seeder",
                    "data_quality": "high",
                    "timestamp": current_date
                }
                
                price = StockPrice(**price_data)
                self.db.add(price)
                
                # Update base price for next day
                base_price = close_price
                current_date += timedelta(days=1)
            
            # Update stock's last price update
            stock.last_price_update = end_date
            self.db.add(stock)
        
        self.db.commit()
        logger.info("Stock prices seeded successfully")
    
    def _seed_portfolios(self, users: list, stocks: list) -> None:
        """Seed user portfolios with test positions"""
        logger.info("Seeding portfolios...")
        
        # Give John Doe some positions
        john = next(u for u in users if u.username == "john_doe")
        
        # Add AAPL position
        aapl = next(s for s in stocks if s.symbol == "AAPL")
        self.portfolio_repo.add_position(
            self.db, 
            john.id, 
            aapl.id, 
            quantity=100, 
            price=150.0,
            notes="Long-term investment in Apple"
        )
        
        # Add MSFT position
        msft = next(s for s in stocks if s.symbol == "MSFT")
        self.portfolio_repo.add_position(
            self.db, 
            john.id, 
            msft.id, 
            quantity=50, 
            price=300.0,
            notes="Microsoft position for tech exposure"
        )
        
        # Give Jane Smith some positions
        jane = next(u for u in users if u.username == "jane_smith")
        
        # Add SPY position
        spy = next(s for s in stocks if s.symbol == "SPY")
        self.portfolio_repo.add_position(
            self.db, 
            jane.id, 
            spy.id, 
            quantity=200, 
            price=400.0,
            notes="Core portfolio holding"
        )
        
        logger.info("Portfolios seeded successfully")
    
    def _seed_watchlists(self, users: list, stocks: list) -> None:
        """Seed user watchlists with test data"""
        logger.info("Seeding watchlists...")
        
        # Create watchlist for John Doe
        john = next(u for u in users if u.username == "john_doe")
        tech_watchlist = self.watchlist_repo.create_watchlist(
            self.db, 
            john.id, 
            "Tech Watchlist", 
            "Technology stocks to monitor",
            is_default=True
        )
        
        # Add stocks to watchlist
        googl = next(s for s in stocks if s.symbol == "GOOGL")
        self.watchlist_repo.add_stock_to_watchlist(
            self.db, 
            tech_watchlist.id, 
            googl.id, 
            notes="Monitor for entry point",
            target_price="120.00"
        )
        
        # Create watchlist for Jane Smith
        jane = next(u for u in users if u.username == "jane_smith")
        etf_watchlist = self.watchlist_repo.create_watchlist(
            self.db, 
            jane.id, 
            "ETF Watchlist", 
            "ETFs to consider for portfolio",
            is_default=True
        )
        
        # Add QQQ to watchlist
        qqq = next(s for s in stocks if s.symbol == "QQQ")
        self.watchlist_repo.add_stock_to_watchlist(
            self.db, 
            etf_watchlist.id, 
            qqq.id, 
            notes="Tech-heavy ETF for growth",
            target_price="350.00"
        )
        
        logger.info("Watchlists seeded successfully")
    
    def clear_all_data(self) -> None:
        """Clear all seeded data (use with caution!)"""
        logger.warning("Clearing all seeded data...")
        
        try:
            # Clear in reverse order due to foreign key constraints
            self.db.query(WatchlistItem).delete()
            self.db.query(Watchlist).delete()
            self.db.query(UserPortfolio).delete()
            self.db.query(StockPrice).delete()
            self.db.query(Stock).delete()
            self.db.query(User).delete()
            
            self.db.commit()
            logger.info("All data cleared successfully")
            
        except Exception as e:
            self.db.rollback()
            logger.error("Error clearing data", error=str(e))
            raise
