# backend/routers/__init__.py

from fastapi import APIRouter
from .admin import router as admin_router
from .reports import router as reports_router
from .auth import router as auth_router

# Lista de todos los routers disponibles
routers = [
    admin_router,
    reports_router,
    auth_router
]

# Opcional: Router principal que podrías usar para agruparlos
main_router = APIRouter()
main_router.include_router(auth_router, prefix="/auth", tags=["Autenticación"])
main_router.include_router(admin_router, prefix="/admin", tags=["Administración"])
main_router.include_router(reports_router, prefix="/reports", tags=["Reportes"])

__all__ = ['routers', 'main_router']  # Controla qué se exporta