"""
Pytest configuration and fixtures for Dashboard Finance tests
"""

import asyncio
import pytest
from typing import Generator, AsyncGenerator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.core.config import settings
from main import app


# Test database configuration
TEST_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create test session factory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_db():
    """Create test database tables."""
    Base.metadata.create_all(bind=test_engine)
    yield test_engine
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session(test_db):
    """Create a fresh database session for a test."""
    connection = test_engine.connect()
    transaction = connection.begin()
    
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session) -> Generator[TestClient, None, None]:
    """Create a test client with database dependency override."""
    
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers():
    """Return authentication headers for testing."""
    return {"Authorization": "Bearer test-token"}


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
        "is_active": True
    }


@pytest.fixture
def sample_stock_data():
    """Sample stock data for testing."""
    return {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "exchange": "NASDAQ",
        "sector": "Technology",
        "industry": "Consumer Electronics"
    }


@pytest.fixture
def sample_stock_price_data():
    """Sample stock price data for testing."""
    return {
        "symbol": "AAPL",
        "price": 150.00,
        "change": 2.50,
        "change_percent": 1.69,
        "volume": 1000000,
        "market_cap": 2500000000000,
        "timestamp": "2024-01-01T00:00:00Z"
    }


# Async test fixtures
@pytest.fixture
async def async_client():
    """Create an async test client."""
    from httpx import AsyncClient
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


# Database fixtures for integration tests
@pytest.fixture(scope="function")
def clean_db():
    """Clean database before each test."""
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


# Mock fixtures
@pytest.fixture
def mock_redis():
    """Mock Redis client for testing."""
    class MockRedis:
        def __init__(self):
            self.data = {}
        
        def get(self, key):
            return self.data.get(key)
        
        def set(self, key, value, ex=None):
            self.data[key] = value
            return True
        
        def delete(self, key):
            if key in self.data:
                del self.data[key]
                return 1
            return 0
        
        def exists(self, key):
            return key in self.data
    
    return MockRedis()


@pytest.fixture
def mock_celery():
    """Mock Celery for testing."""
    class MockCelery:
        def __init__(self):
            self.tasks = {}
        
        def send_task(self, task_name, args=None, kwargs=None):
            task_id = f"mock-task-{len(self.tasks)}"
            self.tasks[task_id] = {
                "name": task_name,
                "args": args or [],
                "kwargs": kwargs or {}
            }
            return type("MockAsyncResult", (), {"id": task_id})()
    
    return MockCelery()


# Performance testing fixtures
@pytest.fixture
def performance_timer():
    """Timer fixture for performance testing."""
    import time
    
    class Timer:
        def __init__(self):
            self.start_time = None
            self.end_time = None
        
        def start(self):
            self.start_time = time.time()
        
        def stop(self):
            self.end_time = time.time()
        
        @property
        def duration(self):
            if self.start_time and self.end_time:
                return self.end_time - self.start_time
            return None
    
    return Timer()


# Environment fixtures
@pytest.fixture(autouse=True)
def test_environment(monkeypatch):
    """Set test environment variables."""
    monkeypatch.setenv("ENVIRONMENT", "testing")
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("DATABASE_URL", TEST_DATABASE_URL)
    monkeypatch.setenv("SECRET_KEY", "test-secret-key")
    monkeypatch.setenv("JWT_SECRET_KEY", "test-jwt-secret-key")


# Cleanup fixtures
@pytest.fixture(autouse=True)
def cleanup_test_files():
    """Clean up test files after tests."""
    yield
    import os
    import glob
    
    # Clean up test database
    if os.path.exists("./test.db"):
        os.remove("./test.db")
    
    # Clean up test log files
    for log_file in glob.glob("./test_*.log"):
        os.remove(log_file)
    
    # Clean up test uploads
    if os.path.exists("./test_uploads"):
        import shutil
        shutil.rmtree("./test_uploads")
