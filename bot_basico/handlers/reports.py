from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, ConversationHandler
from core.database import crud
from core.utils.telegram_utils import build_report_keyboard

# Estados para el flujo de reportes
SELECTING_REASON, WRITING_COMMENT = range(2)

async def start_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia el proceso de reporte"""
    # Implementa lógica para obtener question_id según tu flujo
    question_id = context.user_data.get('current_question')
    
    if not question_id:
        await update.message.reply_text("ℹ️ Usa este comando mientras respondes una pregunta")
        return

    context.user_data['report'] = {'question_id': question_id}
    
    await update.message.reply_text(
        "📝 Selecciona el motivo del reporte:\n\n"
        "1️⃣ - Error en la pregunta\n"
        "2️⃣ - Opciones incorrectas\n"
        "3️⃣ - Explicación confusa"
    )
    
    return SELECTING_REASON

async def receive_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Procesa el comentario del usuario"""
    comment = update.message.text
    report_data = context.user_data['report']
    
    # Guarda el reporte en la base de datos
    await crud.create_report(
        question_id=report_data['question_id'],
        user_id=update.effective_user.id,
        reason=report_data['reason'],
        comment=comment
    )
    
    await update.message.reply_text("✅ Reporte enviado. ¡Gracias por tu ayuda!")
    return ConversationHandler.END

def setup(application):
    """Configura los handlers de reportes"""
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('report', start_report)],
        states={
            SELECTING_REASON: [MessageHandler(filters.TEXT, select_reason)],
            WRITING_COMMENT: [MessageHandler(filters.TEXT, receive_comment)]
        },
        fallbacks=[CommandHandler('cancel', cancel_report)]
    )
    
    application.add_handler(conv_handler)