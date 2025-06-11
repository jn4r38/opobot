import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from core.utils.config import Config

# Configura logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    """Manejador del comando /start"""
    update.message.reply_text('¡Bot de oposiciones activado! Usa /test para empezar.')

def main() -> None:
    """Inicia el bot"""
    updater = Updater(Config.TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    # Registra los comandos
    dispatcher.add_handler(CommandHandler("start", start))

    # Inicia el bot
    updater.start_polling()
    logger.info("Bot escuchando...")
    updater.idle()

if __name__ == '__main__':
    main()