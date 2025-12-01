"""Configuration settings for the multi-agent system."""
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database
    mongodb_url: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    postgres_url: str = os.getenv("POSTGRES_URL", "postgresql://user:pass@localhost/db")
    
    # Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # API
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    
    # External APIs
    job_api_key: str = os.getenv("JOB_API_KEY", "mock_key")
    finance_api_key: str = os.getenv("FINANCE_API_KEY", "mock_key")
    wellness_api_key: str = os.getenv("WELLNESS_API_KEY", "mock_key")
    learning_api_key: str = os.getenv("LEARNING_API_KEY", "mock_key")
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # JWT
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")

settings = Settings()