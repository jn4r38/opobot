from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from core.utils.telegram_utils import send_question_with_options
from core.database import crud

async def start_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia un test con preguntas aleatorias"""
    # Obtiene preguntas de la base de datos
    questions = await crud.get_random_questions(limit=5)
    
    if not questions:
        await update.message.reply_text("⚠️ No hay preguntas disponibles")
        return

    # Guarda el estado del test en context.user_data
    context.user_data['test'] = {
        'questions': questions,
        'current': 0,
        'score': 0
    }

    # Envía la primera pregunta
    await send_next_question(update, context)

async def send_next_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envía la siguiente pregunta del test"""
    test_data = context.user_data['test']
    question = test_data['questions'][test_data['current']]
    
    await send_question_with_options(
        update=update,
        question_text=question.text,
        options=question.options,
        correct_idx=question.correct_answer,
        explanation=question.explanation
    )

def setup(application):
    """Registra los handlers de preguntas"""
    application.add_handler(CommandHandler("test", start_test))
    application.add_handler(CallbackQueryHandler(handle_answer, pattern="^ans_"))