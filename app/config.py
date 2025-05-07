from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any, List
import secrets


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 Minuten * 24 Stunden * 8 Tage = 8 Tage
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    
    # CORS-Einstellungen
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:8000", "http://localhost:3000"]
    
    # Datenbankeinstellungen
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./test.db"
    
    # Erste Superuser-Einstellungen
    FIRST_SUPERUSER: str = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin"
    
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()