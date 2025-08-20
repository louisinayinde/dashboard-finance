"""
Logging configuration using structlog
"""

import logging
import sys
from pathlib import Path
from typing import Any, Dict

import structlog
from structlog.stdlib import LoggerFactory

from app.core.config import settings


def setup_logging() -> None:
    """Setup structured logging configuration"""
    
    # Create logs directory if it doesn't exist
    log_file = Path(settings.LOG_FILE)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure structlog
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
            structlog.processors.JSONRenderer() if settings.LOG_FORMAT == "json" else structlog.dev.ConsoleRenderer(),
        ],
        context_class=dict,
        logger_factory=LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL.upper()),
    )
    
    # Configure file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    
    # Add file handler to root logger
    logging.getLogger().addHandler(file_handler)
    
    # Set specific log levels for external libraries
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("celery").setLevel(logging.INFO)
    logging.getLogger("redis").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("playwright").setLevel(logging.WARNING)


def get_logger(name: str = None) -> structlog.BoundLogger:
    """Get a structured logger instance"""
    return structlog.get_logger(name)


def log_request_info(request_data: Dict[str, Any]) -> None:
    """Log request information in a structured way"""
    logger = get_logger("request")
    logger.info("HTTP Request", **request_data)


def log_response_info(response_data: Dict[str, Any]) -> None:
    """Log response information in a structured way"""
    logger = get_logger("response")
    logger.info("HTTP Response", **response_data)


def log_error(error: Exception, context: Dict[str, Any] = None) -> None:
    """Log error information in a structured way"""
    logger = get_logger("error")
    error_data = {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "error_traceback": getattr(error, "__traceback__", None),
    }
    
    if context:
        error_data.update(context)
    
    logger.error("Application Error", **error_data)


def log_performance(operation: str, duration: float, **kwargs) -> None:
    """Log performance metrics in a structured way"""
    logger = get_logger("performance")
    logger.info(
        "Performance Metric",
        operation=operation,
        duration=duration,
        **kwargs
    )


def log_security_event(event_type: str, user_id: str = None, **kwargs) -> None:
    """Log security events in a structured way"""
    logger = get_logger("security")
    security_data = {
        "event_type": event_type,
        "user_id": user_id,
        "timestamp": structlog.processors.TimeStamper(fmt="iso"),
    }
    security_data.update(kwargs)
    
    logger.warning("Security Event", **security_data)


def log_business_event(event_type: str, **kwargs) -> None:
    """Log business events in a structured way"""
    logger = get_logger("business")
    logger.info("Business Event", event_type=event_type, **kwargs)


# Convenience functions for common logging patterns
def log_api_call(endpoint: str, method: str, user_id: str = None, **kwargs) -> None:
    """Log API call information"""
    logger = get_logger("api")
    logger.info(
        "API Call",
        endpoint=endpoint,
        method=method,
        user_id=user_id,
        **kwargs
    )


def log_database_operation(operation: str, table: str, duration: float, **kwargs) -> None:
    """Log database operation information"""
    logger = get_logger("database")
    logger.info(
        "Database Operation",
        operation=operation,
        table=table,
        duration=duration,
        **kwargs
    )


def log_scraping_event(source: str, status: str, **kwargs) -> None:
    """Log scraping operation information"""
    logger = get_logger("scraping")
    logger.info(
        "Scraping Event",
        source=source,
        status=status,
        **kwargs
    )


def log_celery_task(task_name: str, task_id: str, status: str, **kwargs) -> None:
    """Log Celery task information"""
    logger = get_logger("celery")
    logger.info(
        "Celery Task",
        task_name=task_name,
        task_id=task_id,
        status=status,
        **kwargs
    )
