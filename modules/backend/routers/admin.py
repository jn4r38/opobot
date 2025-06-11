from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.models import User
from .dependencies import get_current_user

router = APIRouter()

# 👇 Personaliza estos endpoints según tus necesidades de administración
@router.get("/users")
async def list_users(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Lista todos los usuarios (solo admin)"""
    if not current_user.is_admin:  # Asegúrate de tener este campo en tu modelo User
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Implementa tu lógica de obtención de usuarios aquí
    return []