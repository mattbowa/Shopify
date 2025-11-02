"""Configuration settings for the application."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Shopify API credentials
    shopify_api_key: str
    shopify_api_secret: str
    app_url: str
    
    # Database
    database_url: str = "sessions.db"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

