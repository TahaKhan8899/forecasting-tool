from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog
from contextlib import asynccontextmanager

from app.core.logging_config import setup_logging, LoggingContextMiddleware

# Set up structured logging
setup_logging()
logger = structlog.get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Log when application starts
    logger.info("FastAPI application startup complete")
    yield
    # Shutdown: Log when application shuts down
    logger.info("FastAPI application shutdown complete")

app = FastAPI(
    title="AI-Powered Forecasting Tool",
    description="Backend API for automated forecasting of e-commerce metrics",
    version="0.1.0",
    lifespan=lifespan,
)

# Add logging middleware
app.add_middleware(LoggingContextMiddleware)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "AI-Powered Forecasting Tool API",
        "version": "0.1.0",
        "status": "active"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    logger.debug("Health check endpoint called")
    return {"status": "healthy"}

# TODO: Include API routers here
# Example:
# from app.api.v1.api import api_router
# app.include_router(api_router, prefix="/api/v1") 