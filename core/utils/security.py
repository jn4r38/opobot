from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from typing import Optional
from core.utils.config import settings

# Configuración de seguridad
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica contraseña contra hash almacenado"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Genera hash de contraseña"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Genera JWT token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

def decode_token(token: str) -> Optional[dict]:
    """Decodifica y verifica JWT"""
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
    except jwt.JWTError:
        return None

# 👇 Personaliza:
# - Esquema de encriptación (bcrypt, argon2)
# - Manejo de errores específicos
# - Claims adicionales en el token