import logging
from telegram.ext import Application
from core.utils.config import settings
from .handlers import setup_all_handlers
from .ai_services import TutorAI

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class PremiumBot:
    def __init__(self):
        self.tutor_ai = TutorAI()
        self.application = self._create_application()

    def _create_application(self):
        return Application.builder() \
            .token(settings.TELEGRAM_PREMIUM_TOKEN) \
            .post_init(self._post_init) \
            .build()

    async def _post_init(self, app):
        await app.bot.set_my_commands([
            ("start", "Inicia el bot premium"),
            ("tutor", "Consulta al tutor IA"),
            ("simulacro", "Examen completo con IA")
        ])
        logging.info("Bot Premium inicializado")

    def run(self):
        self.application.run_polling()

def main():
    bot = PremiumBot()
    setup_all_handlers(bot.application)
    bot.run()