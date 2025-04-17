from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import structlog
from contextlib import asynccontextmanager

from app.core.logging_config import setup_logging, LoggingContextMiddleware
from app.core.config import settings
from app.api.v1.endpoints import shopify_auth

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

# Add Session Middleware - MUST be before routers that use sessions
# Requires SESSION_SECRET_KEY to be set in your environment/.env file
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET_KEY,
    https_only=False,  # Set to True in production if served over HTTPS
    max_age=14 * 24 * 60 * 60  # Session cookie expiry in seconds (e.g., 14 days)
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

# Include API routers
# Include the Shopify OAuth router
app.include_router(
    shopify_auth.router, 
    prefix=f"{settings.API_V1_STR}/auth/shopify", 
    tags=["Shopify Auth"]
)

# Example of including other routers:
# from app.api.v1.endpoints import other_endpoint
# app.include_router(other_endpoint.router, prefix=f"{settings.API_V1_STR}/other", tags=["Other"])

# TODO: Include API routers here
# Example:
# from app.api.v1.api import api_router
# app.include_router(api_router, prefix="/api/v1") 