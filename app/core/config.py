from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, ConfigDict
from typing import Optional

class Settings(BaseSettings):
    """Application settings.
    
    Loads environment variables using Pydantic's BaseSettings.
    """
    PROJECT_NAME: str = "AI-Powered Forecasting Tool"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str
    
    # Logging configuration
    LOG_LEVEL: str = "INFO"

    # Base URL for the application
    APP_URL: Optional[AnyHttpUrl] = None # e.g., "http://localhost:8000" or "https://myapp.com"

    # Secret key for signing cookies (e.g., session, state nonce)
    # Generate using: openssl rand -hex 32
    SESSION_SECRET_KEY: str

    # Shopify App Configuration
    SHOPIFY_API_KEY: str
    SHOPIFY_API_SECRET: str
    SHOPIFY_APP_SCOPES: str # Comma-separated scopes, e.g., "read_products,write_orders"
    SHOPIFY_REDIRECT_PATH: str = "/api/v1/auth/shopify/callback" # Relative path for the redirect

    @property
    def SHOPIFY_REDIRECT_URI(self) -> Optional[str]:
        """Constructs the full Shopify redirect URI from APP_URL and SHOPIFY_REDIRECT_PATH."""
        if self.APP_URL:
            # Ensure APP_URL doesn't have a trailing slash and path starts with one
            base = str(self.APP_URL).rstrip('/')
            path = self.SHOPIFY_REDIRECT_PATH if self.SHOPIFY_REDIRECT_PATH.startswith('/') else f"/{self.SHOPIFY_REDIRECT_PATH}"
            return f"{base}{path}"
        return None

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True
    )


settings = Settings() 