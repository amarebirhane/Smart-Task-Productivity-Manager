import os
from typing import Optional, Any
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Smart Task & Productivity Manager"
    API_V1_STR: str = "/api/v1"
    
    # Authentications
    SECRET_KEY: str = "super-secret-key-please-change-in-production-12345"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # SMTP Configuration
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = 587
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = settings_name if (settings_name := os.getenv("PROJECT_NAME")) else "Smart Task Manager"
    
    # First Superuser
    FIRST_SUPERUSER: str = "admin@example.com"
    FIRST_SUPERUSER_USERNAME: str = "admin"
    FIRST_SUPERUSER_PASSWORD: str = "adminpassword123"
    
    # Database
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "changeme"
    POSTGRES_SERVER: str = "db"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DBS: str = "task_manager"
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        # Use postgresql+psycopg2 for sync or postgresql+asyncpg for async
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DBS}"

    class Config:
        env_file = ".env"

settings = Settings()
