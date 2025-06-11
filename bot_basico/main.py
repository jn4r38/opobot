import logging
from telegram.ext import Application, CommandHandler
from core.utils.config import settings
from .handlers import reports, questions

# Configuración básica de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def post_init(application: Application) -> None:
    """Tareas después de inicializar el bot"""
    await application.bot.set_my_commands([
        ("start", "Inicia el bot"),
        ("test", "Realiza un test"),
        ("report", "Reporta un problema")
    ])

def main() -> None:
    """Punto de entrada del bot básico"""
    application = Application.builder() \
        .token(settings.TELEGRAM_BOT_TOKEN) \
        .post_init(post_init) \
        .build()

    # Registra los handlers
    reports.setup(application)
    questions.setup(application)

    # Inicia el bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()