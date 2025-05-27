"""
Configuration settings for Swakopmund Municipality Public Safety Service
"""
import os
from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application
    app_name: str = "Swakopmund Municipality Public Safety Service"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8686
    
    # Database
    database_url: Optional[str] = None
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "public_safety_db"
    db_user: str = "postgres"
    db_password: str = "postgres"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def db_url(self) -> str:
        """Construct database URL"""
        if self.database_url:
            return self.database_url
        # For local testing, use SQLite if PostgreSQL is not available
        try:
            import psycopg2
            return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        except ImportError:
            return "sqlite:///./public_safety.db"


# Global settings instance
settings = Settings() 