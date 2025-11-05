import os
from typing import List, Union
from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "Bazar Universal API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./bazar_universal.db")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # CORS - Accept both string and list
    CORS_ORIGINS: Union[str, List[str]] = [
        "http://localhost:3000",
        "http://localhost:5173", 
        "http://localhost:5174",
        "https://bazar-universal.netlify.app",
        "https://*.netlify.app",
        "https://*.render.com",
        "https://*.railway.app",
        "https://*.vercel.app"
    ]
    
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            # Handle comma-separated string from environment variables
            if v.strip():
                return [i.strip() for i in v.split(",")]
            return []
        elif isinstance(v, list):
            return v
        return []

    model_config = {
        "env_file": ".env",
        "case_sensitive": True
    }

settings = Settings()
