from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings.
    
    Loads environment variables using Pydantic's BaseSettings.
    """
    PROJECT_NAME: str = "AI-Powered Forecasting Tool"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings() 