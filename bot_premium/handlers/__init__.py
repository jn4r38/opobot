from .premium_reports import setup as setup_reports
from .tutor_ai import setup as setup_tutor

def setup_all_handlers(application):
    """Registra todos los handlers premium"""
    setup_reports(application)
    setup_tutor(application)
    # Añade aquí nuevos handlers premium