from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path

class Settings(BaseSettings):
    TELEGRAM_TOKEN: str = Field(..., min_length=46, max_length=46)
    ADMIN_USER_ID: int = Field(...)
    DATABASE_URL: str = "sqlite:///./data/opobot.db"
    
    class Config:
        env_file = ".env"  # Asegúrate que apunta al archivo correcto
        env_file_encoding = "utf-8"

settings = Settings()