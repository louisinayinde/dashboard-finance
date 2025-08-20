"""
Database configuration and session management
"""

from typing import Generator
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool

from app.core.config import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_timeout=settings.DATABASE_POOL_TIMEOUT,
    pool_pre_ping=True,  # Enable connection health checks
    echo=settings.DEBUG,  # Log SQL queries in debug mode
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Create declarative base
Base = declarative_base()

# Metadata for migrations
metadata = MetaData()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session.
    Yields a database session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables() -> None:
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)


def drop_tables() -> None:
    """Drop all tables in the database (use with caution!)"""
    Base.metadata.drop_all(bind=engine)


def get_db_session() -> Session:
    """Get a database session (for use outside of FastAPI dependencies)"""
    return SessionLocal()


def close_db_session(session: Session) -> None:
    """Close a database session"""
    if session:
        session.close()


# Database health check
def check_database_health() -> bool:
    """Check if database is accessible"""
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        return True
    except Exception:
        return False


# Connection pool monitoring
def get_connection_pool_status() -> dict:
    """Get connection pool status information"""
    pool = engine.pool
    return {
        "pool_size": pool.size(),
        "checked_in": pool.checkedin(),
        "checked_out": pool.checkedout(),
        "overflow": pool.overflow(),
        "invalid": pool.invalid(),
    }


# Database initialization
def init_database() -> None:
    """Initialize database with tables and basic setup"""
    try:
        create_tables()
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        raise


# Database cleanup
def cleanup_database() -> None:
    """Clean up database connections and resources"""
    try:
        engine.dispose()
        print("Database connections cleaned up successfully")
    except Exception as e:
        print(f"Error cleaning up database: {e}")
        raise


# Context manager for database sessions
class DatabaseSession:
    """Context manager for database sessions"""
    
    def __init__(self):
        self.session = None
    
    def __enter__(self):
        self.session = get_db_session()
        return self.session
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            if exc_type is not None:
                self.session.rollback()
            else:
                self.session.commit()
            self.session.close()


# Transaction decorator
def transactional(func):
    """Decorator to handle database transactions automatically"""
    def wrapper(*args, **kwargs):
        with DatabaseSession() as session:
            # Inject session as first argument if function expects it
            if 'db' in func.__code__.co_varnames:
                kwargs['db'] = session
            return func(*args, **kwargs)
    return wrapper


# Database connection retry logic
def get_db_with_retry(max_retries: int = 3, retry_delay: float = 1.0) -> Generator[Session, None, None]:
    """
    Get database session with retry logic for connection issues
    """
    import time
    
    for attempt in range(max_retries):
        try:
            db = SessionLocal()
            # Test connection
            db.execute("SELECT 1")
            yield db
            break
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(retry_delay)
            continue
        finally:
            if 'db' in locals():
                db.close()
