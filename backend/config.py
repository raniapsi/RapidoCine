from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configuration de l'application"""
    
    # Application
    APP_NAME: str = "RapidoCine API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database (SQLite pour développement local)
    DATABASE_URL: str = "sqlite:///./rapidocine.db"
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost", "http://localhost:8000", "http://localhost:80", "http://127.0.0.1", "*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
