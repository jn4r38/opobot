from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from core.database import crud
from core.utils.telegram_utils import build_report_keyboard

async def premium_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler de reportes premium con análisis IA"""
    question_id = context.user_data.get('current_question')
    
    if not question_id:
        await update.message.reply_text("Use este comando mientras responde una pregunta")
        return

    # Análisis IA adicional para reportes premium
    analysis = await context.bot_data['tutor_ai'].analyze_question(question_id)
    
    await update.message.reply_text(
        f"🚨 Reporte Premium\n\n"
        f"Análisis IA:\n{analysis}\n\n"
        f"Describa el problema:",
        reply_markup=build_report_keyboard(question_id, premium=True)
    )

def setup(application):
    application.add_handler(CommandHandler("report", premium_report))