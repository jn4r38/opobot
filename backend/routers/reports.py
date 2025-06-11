from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.models import QuestionReport
from .dependencies import get_current_user

router = APIRouter()

# 👇 Personaliza estos endpoints según tu modelo de reportes
@router.get("")
async def get_reports(
    status: str = "pending",
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """Obtiene reportes filtrados por estado"""
    # Implementa tu lógica de consulta a la base de datos
    return []

@router.post("/{report_id}/resolve")
async def resolve_report(
    report_id: int,
    action: str,  # "approve" o "reject"
    db: AsyncSession = Depends(get_db)
):
    """Cambia el estado de un reporte"""
    # Implementa tu lógica de actualización
    return {"status": "success"}