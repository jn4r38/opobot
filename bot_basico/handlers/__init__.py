from typing import List, Callable
from telegram.ext import Application
from . import reports, questions  # Importa todos los módulos de handlers

def setup_all_handlers(application: Application) -> None:
    """
    Registra todos los handlers del bot básico en la aplicación.
    
    Args:
        application: Instancia de Application de python-telegram-bot
    
    Ejemplo de uso:
        from bot_basico.handlers import setup_all_handlers
        setup_all_handlers(application)
    """
    # Obtiene todos los módulos de handlers dinámicamente
    handler_modules: List[Callable[[Application], None]] = [
        reports.setup,
        questions.setup
        # Añade aquí nuevos módulos de handlers
    ]
    
    # Registra cada handler
    for setup_handler in handler_modules:
        setup_handler(application)

# Exporta solo la función principal para mantener limpio el namespace
__all__ = ['setup_all_handlers']