"""
Prometheus metrics configuration for Dashboard Finance
"""

from prometheus_client import Counter, Histogram, Gauge, Summary

# HTTP Request Metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"]
)

# Database Metrics
DB_CONNECTION_ACTIVE = Gauge(
    "db_connections_active",
    "Number of active database connections"
)

DB_QUERY_DURATION = Histogram(
    "db_query_duration_seconds",
    "Database query duration in seconds",
    ["operation", "table"]
)

# Celery Task Metrics
CELERY_TASK_COUNT = Counter(
    "celery_tasks_total",
    "Total Celery tasks processed",
    ["task_name", "status"]
)

CELERY_TASK_DURATION = Histogram(
    "celery_task_duration_seconds",
    "Celery task duration in seconds",
    ["task_name"]
)

CELERY_WORKER_ACTIVE = Gauge(
    "celery_workers_active",
    "Number of active Celery workers"
)

# Scraping Metrics
SCRAPING_SUCCESS_COUNT = Counter(
    "scraping_success_total",
    "Total successful scraping operations",
    ["source", "data_type"]
)

SCRAPING_ERROR_COUNT = Counter(
    "scraping_errors_total",
    "Total scraping errors",
    ["source", "error_type"]
)

SCRAPING_DURATION = Histogram(
    "scraping_duration_seconds",
    "Scraping operation duration in seconds",
    ["source", "data_type"]
)

# WebSocket Metrics
WEBSOCKET_CONNECTIONS = Gauge(
    "websocket_connections_active",
    "Number of active WebSocket connections"
)

WEBSOCKET_MESSAGES = Counter(
    "websocket_messages_total",
    "Total WebSocket messages sent",
    ["message_type"]
)

# Business Logic Metrics
STOCK_DATA_UPDATES = Counter(
    "stock_data_updates_total",
    "Total stock data updates",
    ["symbol", "source"]
)

USER_AUTH_ATTEMPTS = Counter(
    "user_auth_attempts_total",
    "Total user authentication attempts",
    ["status", "method"]
)

# System Metrics
MEMORY_USAGE = Gauge(
    "memory_usage_bytes",
    "Memory usage in bytes",
    ["type"]
)

CPU_USAGE = Gauge(
    "cpu_usage_percent",
    "CPU usage percentage"
)

# Custom Business Metrics
ACTIVE_USERS = Gauge(
    "active_users_total",
    "Number of active users"
)

STOCKS_MONITORED = Gauge(
    "stocks_monitored_total",
    "Number of stocks being monitored"
)

DATA_FRESHNESS = Gauge(
    "data_freshness_seconds",
    "Age of the most recent data in seconds",
    ["data_type"]
)
