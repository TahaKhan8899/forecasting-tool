import logging
import sys
import structlog
import time
import uuid
from typing import Optional, Callable
from pythonjsonlogger import json as jsonlogger
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

from app.core.config import settings


class LoggingContextMiddleware(BaseHTTPMiddleware):
    """Middleware for adding request context to logs using structlog."""
    
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Generate a unique request ID
        request_id = str(uuid.uuid4())
        
        # Bind request data to the logger context
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            client_host=request.client.host if request.client else None,
        )
        
        # Add timing information
        start_time = time.time()
        
        try:
            # Process the request
            response = await call_next(request)
            
            # Add response data to context
            process_time = time.time() - start_time
            structlog.contextvars.bind_contextvars(
                status_code=response.status_code,
                duration=f"{process_time:.4f}s",
            )
            
            return response
        except Exception as e:
            # Log any unhandled exceptions
            process_time = time.time() - start_time
            structlog.contextvars.bind_contextvars(
                status_code=500,
                duration=f"{process_time:.4f}s",
                error=str(e),
            )
            raise


def setup_logging(log_level: Optional[str] = None) -> None:
    """
    Configure structured logging for the application.
    
    Args:
        log_level: Optional log level override (defaults to settings.LOG_LEVEL if not provided)
    """
    # Determine log level (use argument, settings, or INFO as fallback)
    level = getattr(logging, log_level or settings.LOG_LEVEL or "INFO")
    
    # Define shared processors for structlog
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]
    
    # Configure standard logging
    pre_chain = [
        # Pre-processing for non-structlog logs (e.g., from libraries)
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
    ]
    
    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Remove existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create a console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Create a JSON formatter
    formatter = structlog.stdlib.ProcessorFormatter(
        processor=structlog.processors.JSONRenderer(),
        foreign_pre_chain=pre_chain,
    )
    
    # Add the formatter to the handler
    console_handler.setFormatter(formatter)
    
    # Add the handler to the root logger
    root_logger.addHandler(console_handler)
    
    # Configure Uvicorn loggers to use the same format
    for logger_name in ("uvicorn", "uvicorn.access", "uvicorn.error"):
        logger = logging.getLogger(logger_name)
        logger.handlers = []  # Remove default handlers
        logger.propagate = True  # Use the root logger's handlers
    
    # Configure structlog
    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    ) 