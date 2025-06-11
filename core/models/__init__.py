from .report import Report
from .user import User
from .question import Question
from .base import Base  # Importa la clase base para SQLAlchemy

# Exporta todos los modelos para fácil importación
__all__ = ['Base', 'Report', 'User', 'Question']