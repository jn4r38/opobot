import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data.db")

# Instancia única accesible
settings = Settings()