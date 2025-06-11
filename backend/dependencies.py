from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from core.database.session import get_db
from core.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# 👇 Cambia la lógica de verificación según tu modelo de usuario
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Dependencia para obtener usuario autenticado"""
    # Implementa tu lógica de verificación de token aquí
    # Ejemplo básico:
    user = await db.get(User, user_id)  # Esto es solo un ejemplo
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return user