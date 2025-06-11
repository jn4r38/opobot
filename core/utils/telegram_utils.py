from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from typing import Optional, Dict, Any
from core.utils.config import settings

async def send_question_with_options(
    update: Update,
    question_text: str,
    options: list[str],
    correct_idx: int,
    explanation: Optional[str] = None
) -> None:
    """Envía una pregunta con opciones como botones inline"""
    keyboard = [
        [InlineKeyboardButton(opt, callback_data=f"ans_{i}")]
        for i, opt in enumerate(options)
    ]
    
    await update.message.reply_text(
        text=question_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def notify_admins(
    context: ContextTypes.DEFAULT_TYPE,
    message: str,
    exclude_ids: list[int] = []
) -> None:
    """Envía notificaciones a los administradores"""
    for admin_id in settings.TELEGRAM_ADMIN_IDS:
        if admin_id not in exclude_ids:
            try:
                await context.bot.send_message(
                    chat_id=admin_id,
                    text=message
                )
            except Exception as e:
                print(f"Error notifying admin {admin_id}: {e}")

def build_report_keyboard(question_id: str) -> InlineKeyboardMarkup:
    """Construye teclado inline para reportar preguntas"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚩 Reportar", callback_data=f"report_{question_id}")]
    ])

# 👇 Personaliza:
# - Tipos de teclados (inline, reply, etc.)
# - Lógica de notificaciones
# - Manejo de errores específicos