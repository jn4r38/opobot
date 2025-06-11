# bot_basico/__init__.py

from .main import main as start_bot
from .handlers import setup_all_handlers

# Version del bot
__version__ = "1.0.0"

# Exporta la interfaz pública del módulo
__all__ = [
    'start_bot',
    'setup_all_handlers',
    '__version__'
]

# Inicialización opcional (si necesitas configurar algo al importar)
def _init():
    pass

_init()