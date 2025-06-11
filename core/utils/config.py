from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Configuración general
    ENV: str = "dev"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./oposiciones.db"
    
    # Telegram
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_ADMIN_IDS: list[int] = []
    
    # Auth
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 horas
    
    # Web Panel
    WEBAPP_URL: str = "http://localhost:3000"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# 👇 Cambia esto según tus necesidades:
# - Añade más variables de configuración
# - Modifica valores por defecto
# - Ajusta la configuración de entorno