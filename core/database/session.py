from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core.utils.config import settings  # Asegúrate de tener esta configuración

# 👇 Cambia esta URL según tu base de datos (ej: PostgreSQL, MySQL)
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    future=True,
    echo=False,  # Cambia a True para ver queries SQL en desarrollo
    pool_size=20,
    max_overflow=10
)

# Session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def get_db() -> AsyncSession:
    """Provee una sesión de base de datos para cada request"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Para inicializar