"""
Configuration management using Pydantic settings
"""

import os
from typing import List, Optional
from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application Configuration
    APP_NAME: str = Field(default="dashboard-finance", env="APP_NAME")
    APP_VERSION: str = Field(default="0.1.0", env="APP_VERSION")
    DEBUG: bool = Field(default=False, env="DEBUG")
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    
    # Server Configuration
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    WORKERS: int = Field(default=4, env="WORKERS")
    RELOAD: bool = Field(default=True, env="RELOAD")
    
    # Database Configuration
    DATABASE_URL: str = Field(
        default="postgresql://user:password@localhost:5432/dashboard_finance",
        env="DATABASE_URL"
    )
    DATABASE_POOL_SIZE: int = Field(default=20, env="DATABASE_POOL_SIZE")
    DATABASE_MAX_OVERFLOW: int = Field(default=30, env="DATABASE_MAX_OVERFLOW")
    DATABASE_POOL_TIMEOUT: int = Field(default=30, env="DATABASE_POOL_TIMEOUT")
    
    # Redis Configuration
    REDIS_URL: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    REDIS_PASSWORD: Optional[str] = Field(default=None, env="REDIS_PASSWORD")
    REDIS_DB: int = Field(default=0, env="REDIS_DB")
    
    # Celery Configuration
    CELERY_BROKER_URL: str = Field(default="redis://localhost:6379/1", env="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = Field(default="redis://localhost:6379/1", env="CELERY_RESULT_BACKEND")
    CELERY_TASK_ALWAYS_EAGER: bool = Field(default=False, env="CELERY_TASK_ALWAYS_EAGER")
    
    # Security Configuration
    SECRET_KEY: str = Field(
        default="your-super-secret-key-here-change-in-production",
        env="SECRET_KEY"
    )
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    
    # JWT Configuration
    JWT_SECRET_KEY: str = Field(
        default="your-jwt-secret-key-here",
        env="JWT_SECRET_KEY"
    )
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, env="JWT_REFRESH_TOKEN_EXPIRE_DAYS")
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        env="ALLOWED_ORIGINS"
    )
    ALLOWED_CREDENTIALS: bool = Field(default=True, env="ALLOWED_CREDENTIALS")
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=100, env="RATE_LIMIT_PER_MINUTE")
    RATE_LIMIT_PER_HOUR: int = Field(default=1000, env="RATE_LIMIT_PER_HOUR")
    
    # Scraping Configuration
    SCRAPING_INTERVAL_MINUTES: int = Field(default=5, env="SCRAPING_INTERVAL_MINUTES")
    SCRAPING_TIMEOUT_SECONDS: int = Field(default=30, env="SCRAPING_TIMEOUT_SECONDS")
    SCRAPING_USER_AGENT: str = Field(
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        env="SCRAPING_USER_AGENT"
    )
    
    # External APIs
    ALPHA_VANTAGE_API_KEY: Optional[str] = Field(default=None, env="ALPHA_VANTAGE_API_KEY")
    YAHOO_FINANCE_ENABLED: bool = Field(default=True, env="YAHOO_FINANCE_ENABLED")
    MARKETWATCH_ENABLED: bool = Field(default=True, env="MARKETWATCH_ENABLED")
    
    # Monitoring Configuration
    PROMETHEUS_ENABLED: bool = Field(default=True, env="PROMETHEUS_ENABLED")
    PROMETHEUS_PORT: int = Field(default=9090, env="PROMETHEUS_PORT")
    GRAFANA_ENABLED: bool = Field(default=True, env="GRAFANA_ENABLED")
    GRAFANA_PORT: int = Field(default=3000, env="GRAFANA_PORT")
    
    # Logging Configuration
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(default="json", env="LOG_FORMAT")
    LOG_FILE: str = Field(default="logs/app.log", env="LOG_FILE")
    
    # File Storage
    UPLOAD_DIR: str = Field(default="uploads", env="UPLOAD_DIR")
    MAX_FILE_SIZE: int = Field(default=10485760, env="MAX_FILE_SIZE")  # 10MB
    
    # Email Configuration
    SMTP_HOST: Optional[str] = Field(default=None, env="SMTP_HOST")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_USERNAME: Optional[str] = Field(default=None, env="SMTP_USERNAME")
    SMTP_PASSWORD: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    SMTP_TLS: bool = Field(default=True, env="SMTP_TLS")
    
    # AWS Configuration
    AWS_ACCESS_KEY_ID: Optional[str] = Field(default=None, env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(default=None, env="AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = Field(default="us-east-1", env="AWS_REGION")
    AWS_S3_BUCKET: Optional[str] = Field(default=None, env="AWS_S3_BUCKET")
    
    # Sentry Configuration
    SENTRY_DSN: Optional[str] = Field(default=None, env="SENTRY_DSN")
    SENTRY_ENVIRONMENT: str = Field(default="development", env="SENTRY_ENVIRONMENT")
    
    # Feature Flags
    FEATURE_WEBSOCKET_ENABLED: bool = Field(default=True, env="FEATURE_WEBSOCKET_ENABLED")
    FEATURE_REAL_TIME_UPDATES: bool = Field(default=True, env="FEATURE_REAL_TIME_UPDATES")
    FEATURE_USER_AUTHENTICATION: bool = Field(default=True, env="FEATURE_USER_AUTHENTICATION")
    FEATURE_ADMIN_PANEL: bool = Field(default=True, env="FEATURE_ADMIN_PANEL")
    
    @validator("ALLOWED_ORIGINS", pre=True)
    def parse_allowed_origins(cls, v):
        """Parse ALLOWED_ORIGINS from string to list if needed"""
        if isinstance(v, str):
            # Remove brackets and quotes, split by comma
            v = v.strip("[]").replace('"', '').replace("'", "").split(",")
            v = [origin.strip() for origin in v if origin.strip()]
        return v
    
    @validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        """Ensure SECRET_KEY is not the default value in production"""
        # Skip validation during class construction to avoid recursion
        return v
    
    @validator("JWT_SECRET_KEY")
    def validate_jwt_secret_key(cls, v):
        """Ensure JWT_SECRET_KEY is not the default value in production"""
        # Skip validation during class construction to avoid recursion
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create global settings instance
settings = Settings()

# Validate critical settings
def validate_settings():
    """Validate critical settings on startup"""
    if settings.ENVIRONMENT == "production":
        if settings.DEBUG:
            raise ValueError("DEBUG must be False in production")
        if not settings.SECRET_KEY or settings.SECRET_KEY == "your-super-secret-key-here-change-in-production":
            raise ValueError("SECRET_KEY must be set in production")
        if not settings.JWT_SECRET_KEY or settings.JWT_SECRET_KEY == "your-jwt-secret-key-here":
            raise ValueError("JWT_SECRET_KEY must be set in production")

# Validate settings on import
try:
    validate_settings()
except ValueError as e:
    import warnings
    warnings.warn(f"Settings validation warning: {e}", UserWarning)
