from .main import main as start_premium_bot
from .handlers import setup_all_handlers
from core.utils.config import settings

__version__ = "1.0.0-premium"
__all__ = ['start_premium_bot', 'setup_all_handlers']

def _init():
    if not settings.TELEGRAM_PREMIUM_TOKEN:
        raise ValueError("Token premium no configurado")

_init()