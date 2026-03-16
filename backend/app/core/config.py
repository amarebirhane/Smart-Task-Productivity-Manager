import os
from typing import Optional, Any
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

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
    EMAILS_FROM_NAME: Optional[str] = os.getenv("PROJECT_NAME", "Smart Task Manager")
    
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
    
    # S3 / MinIO
    S3_BUCKET: str = "task-attachments"
    S3_ENDPOINT_URL: Optional[str] = None
    S3_ACCESS_KEY: Optional[str] = None
    S3_SECRET_KEY: Optional[str] = None
    
    # Environment
    ENVIRONMENT: str = "development" # development, production
    BACKUP_DIR: str = "backups"

    # Redis
    REDIS_URL: Optional[str] = None

    # MinIO Root (used for setup/admin)
    MINIO_ROOT_USER: Optional[str] = None
    MINIO_ROOT_PASSWORD: Optional[str] = None

    @field_validator("SMTP_PASSWORD", "S3_SECRET_KEY", "SECRET_KEY", mode="after")
    @classmethod
    def check_secrets_in_production(cls, v: Optional[str], info: Any) -> Optional[str]:
        if info.data.get("ENVIRONMENT") == "production" and not v:
            raise ValueError(f"CRITICAL: {info.field_name} must be set in production environment!")
        return v

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        # Use postgresql+psycopg2 for sync or postgresql+asyncpg for async
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DBS}"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
