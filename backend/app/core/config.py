from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "Financial Health Assessment Tool"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/financial_health"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ENCRYPTION_KEY: str = "your-encryption-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # AI Services - Perplexity SDK
    OPENAI_API_KEY: str = ""  # Perplexity API key
    AI_MODEL: str = "sonar-pro"  # Perplexity model (sonar-pro, sonar, sonar-reasoning)
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000"
    ]
    
    # Banking APIs (Examples - Replace with actual credentials)
    RAZORPAY_KEY_ID: str = ""
    RAZORPAY_KEY_SECRET: str = ""
    STRIPE_API_KEY: str = ""
    
    # GST API
    GST_API_URL: str = ""
    GST_API_KEY: str = ""
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".csv", ".xlsx", ".xls", ".pdf"]
    UPLOAD_DIR: str = "uploads"
    
    # Industry Benchmarks
    BENCHMARK_INDUSTRIES: List[str] = [
        "Manufacturing",
        "Retail",
        "Agriculture",
        "Services",
        "Logistics",
        "E-commerce",
        "Healthcare",
        "Technology"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
