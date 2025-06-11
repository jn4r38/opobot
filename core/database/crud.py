from typing import Type, TypeVar, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.models import Report, User, Question  # Importa tus modelos

ModelType = TypeVar('ModelType')

class CRUDBase:
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        result = await db.execute(select(self.model).filter(self.model.id == id))
        return result.scalars().first()

    async def create(self, db: AsyncSession, obj_in) -> ModelType:
        db_obj = self.model(**obj_in.dict())  # Ajusta según tus schemas Pydantic
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    # 👇 Personaliza estos métodos según tus necesidades
    async def update(self, db: AsyncSession, db_obj: ModelType, obj_in) -> ModelType:
        update_data = obj_in.dict(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, id: int) -> bool:
        obj = await self.get(db, id)
        if obj:
            await db.delete(obj)
            await db.commit()
            return True
        return False

# Instancias específicas para cada modelo
crud_report = CRUDBase(Report)
crud_user = CRUDBase(User)
crud_question = CRUDBase(Question)

# 👇 Añade operaciones personalizadas para cada modelo aquí
async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def get_reports_by_status(db: AsyncSession, status: str, limit: int = 100):
    result = await db.execute(
        select(Report)
        .filter(Report.status == status)
        .limit(limit)
        .order_by(Report.created_at.desc())
    )
    return result.scalars().all()