"""
Celery application configuration for Dashboard Finance
"""

import os
from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

# Create Celery instance
celery_app = Celery(
    "dashboard-finance",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.scraping.stock_scraping",
        "app.tasks.maintenance.cleanup",
    ]
)

# Celery configuration
celery_app.conf.update(
    # Task routing
    task_routes={
        "app.tasks.scraping.*": {"queue": "scraping"},
        "app.tasks.maintenance.*": {"queue": "maintenance"},
        "app.tasks.*": {"queue": "default"},
    },
    
    # Task serialization
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    # Task execution
    task_always_eager=settings.CELERY_TASK_ALWAYS_EAGER,
    task_eager_propagates=True,
    task_ignore_result=False,
    task_store_errors_even_if_ignored=True,
    
    # Worker configuration
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    worker_disable_rate_limits=False,
    
    # Result backend
    result_expires=3600,  # 1 hour
    result_persistent=True,
    
    # Beat schedule (periodic tasks)
    beat_schedule={
        # Scrape stock data every 5 minutes during market hours
        "scrape-stock-data": {
            "task": "app.tasks.scraping.stock_scraping.scrape_all_stocks",
            "schedule": crontab(minute="*/5", hour="9-17"),  # 9 AM to 5 PM
            "options": {"queue": "scraping"},
        },
        
        # Clean up old data daily at 2 AM
        "cleanup-old-data": {
            "task": "app.tasks.maintenance.cleanup.cleanup_old_data",
            "schedule": crontab(hour=2, minute=0),
            "options": {"queue": "maintenance"},
        },
        
        # Health check every 10 minutes
        "health-check": {
            "task": "app.tasks.maintenance.health_check",
            "schedule": crontab(minute="*/10"),
            "options": {"queue": "maintenance"},
        },
        
        # Update market indices every hour
        "update-market-indices": {
            "task": "app.tasks.scraping.stock_scraping.update_market_indices",
            "schedule": crontab(minute=0),
            "options": {"queue": "scraping"},
        },
    },
    
    # Task time limits
    task_soft_time_limit=300,  # 5 minutes
    task_time_limit=600,       # 10 minutes
    
    # Retry configuration
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    
    # Monitoring
    worker_send_task_events=True,
    task_send_sent_event=True,
    
    # Security
    security_key=settings.SECRET_KEY,
    
    # Logging
    worker_log_format="[%(asctime)s: %(levelname)s/%(processName)s] %(message)s",
    worker_task_log_format="[%(asctime)s: %(levelname)s/%(processName)s] [%(task_name)s(%(task_id)s)] %(message)s",
)

# Task annotations for specific tasks
celery_app.conf.task_annotations = {
    "app.tasks.scraping.stock_scraping.scrape_all_stocks": {
        "rate_limit": "10/m",  # Max 10 tasks per minute
        "time_limit": 300,     # 5 minutes timeout
    },
    "app.tasks.scraping.stock_scraping.update_market_indices": {
        "rate_limit": "1/h",   # Max 1 task per hour
        "time_limit": 600,     # 10 minutes timeout
    },
    "app.tasks.maintenance.cleanup.cleanup_old_data": {
        "rate_limit": "1/d",   # Max 1 task per day
        "time_limit": 1800,    # 30 minutes timeout
    },
}

# Task routing for different environments
if settings.ENVIRONMENT == "development":
    # In development, route all tasks to default queue
    celery_app.conf.task_routes = {
        "app.tasks.*": {"queue": "default"},
    }
    
    # Disable rate limiting in development
    celery_app.conf.task_annotations = {}

# Optional: Configure result backend for different environments
if settings.ENVIRONMENT == "production":
    celery_app.conf.update(
        result_expires=7200,  # 2 hours in production
        worker_max_tasks_per_child=500,  # Lower in production
    )

# Task error handling
@celery_app.task(bind=True)
def debug_task(self):
    """Debug task for testing Celery setup"""
    print(f"Request: {self.request!r}")

# Health check task
@celery_app.task
def health_check():
    """Periodic health check task"""
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

if __name__ == "__main__":
    celery_app.start()
