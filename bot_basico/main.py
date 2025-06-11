#!/usr/bin/env python3
"""
OpoBot - Bot de oposiciones con funcionalidades básicas y premium
Versión definitiva con configuración .env
"""

import asyncio
import logging
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field, ValidationError
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, 
    CommandHandler, 
    ContextTypes, 
    MessageHandler, 
    CallbackQueryHandler,
    filters
)

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    """Configuración del bot usando pydantic-settings"""
    
    # Token del bot (compatible con ambos nombres)
    TELEGRAM_TOKEN: str = Field(..., description="Token del bot de Telegram")
    
    # Admin
    ADMIN_USER_ID: int = Field(..., description="ID del usuario administrador")
    
    # Base de datos
    DATABASE_URL: str = Field(
        default="sqlite:///./data/opobot.db", 
        description="URL de la base de datos"
    )
    
    # IA APIs (opcionales)
    DEEPSEEK_API_KEY: str = Field(default="", description="API Key de DeepSeek")
    OPENAI_API_KEY: str = Field(default="", description="API Key de OpenAI")
    
    # JWT para autenticación web
    JWT_SECRET: str = Field(default="change-this-secret-key", description="Clave secreta JWT")
    
    # Rutas de archivos
    DATA_DIR: str = Field(default="./data", description="Directorio de datos")
    QUESTIONS_DIR: str = Field(default="./data/preguntas", description="Directorio de preguntas YAML")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Cargar configuración
try:
    settings = Settings()
    logger.info("✅ Configuración cargada correctamente")
except ValidationError as e:
    logger.error("❌ Error en la configuración del .env:")
    for error in e.errors():
        field = error['loc'][0]
        msg = error['msg']
        logger.error(f"   • {field}: {msg}")
    exit(1)

class OpoBot:
    """Clase principal del bot de oposiciones"""
    
    def __init__(self):
        self.application = None
        self.setup_directories()
        logger.info(f"🤖 OpoBot inicializado - Admin ID: {settings.ADMIN_USER_ID}")
    
    def setup_directories(self):
        """Crear directorios necesarios"""
        data_path = Path(settings.DATA_DIR)
        questions_path = Path(settings.QUESTIONS_DIR)
        
        data_path.mkdir(exist_ok=True)
        questions_path.mkdir(exist_ok=True)
        
        logger.info(f"📁 Directorios configurados:")
        logger.info(f"   • Datos: {data_path.absolute()}")
        logger.info(f"   • Preguntas: {questions_path.absolute()}")
    
    def is_admin(self, user_id: int) -> bool:
        """Verificar si el usuario es administrador"""
        return user_id == settings.ADMIN_USER_ID
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        user = update.effective_user
        
        # Keyboard con opciones principales
        keyboard = [
            [InlineKeyboardButton("🎯 Hacer Test", callback_data="test_menu")],
            [InlineKeyboardButton("📊 Mi Progreso", callback_data="progreso")],
            [InlineKeyboardButton("⚙️ Configuración", callback_data="config")],
        ]
        
        # Opciones adicionales para admin
        if self.is_admin(user.id):
            keyboard.append([InlineKeyboardButton("🔧 Panel Admin", callback_data="admin_panel")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_message = f"""
🎯 **¡Bienvenido a OpoBot, {user.first_name}!**

Tu asistente personal para preparar oposiciones.

🤖 **Funciones disponibles:**
• Tests de preguntas por temas
• Seguimiento de progreso
• Recordatorios de estudio
• Sistema de reportes

💎 **Premium (próximamente):**
• Tutor IA personalizado
• Simulacros cronometrados  
• Análisis avanzado

¿Qué quieres hacer hoy?
        """
        
        await update.message.reply_text(
            welcome_message, 
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help"""
        help_text = """
📋 **Comandos disponibles:**

**🎯 Estudio:**
• `/test` - Hacer test de preguntas
• `/test [tema]` - Test de tema específico
• `/progreso` - Ver estadísticas
• `/temas` - Lista de temas disponibles

**⚙️ Configuración:**
• `/recordatorio [hora]` - Configurar recordatorios
• `/config` - Configuración personal

**🛠️ Utilidades:**
• `/report` - Reportar problema con pregunta
• `/about` - Información del bot
• `/help` - Mostrar esta ayuda

**💎 Premium (próximamente):**
• `/tutor [pregunta]` - Consultar tutor IA
• `/simulacro` - Examen cronometrado

**👨‍💼 Admin** (solo administradores):
• `/admin` - Panel de administración
• `/stats` - Estadísticas globales
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def test_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /test - Iniciar test de preguntas"""
        tema = " ".join(context.args) if context.args else None
        
        keyboard = [
            [InlineKeyboardButton("🎲 Test Aleatorio", callback_data="test_random")],
            [InlineKeyboardButton("📚 Por Tema", callback_data="test_by_theme")],
            [InlineKeyboardButton("🔄 Continuar Último", callback_data="test_continue")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = "🎯 **Test de Preguntas**\n\n"
        if tema:
            message += f"Tema seleccionado: **{tema}**\n\n"
        
        message += "¿Cómo quieres estudiar hoy?"
        
        await update.message.reply_text(
            message,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def progreso_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /progreso - Mostrar progreso del usuario"""
        user = update.effective_user
        
        # TODO: Conectar con base de datos real
        progress_message = f"""
📊 **Progreso de {user.first_name}**

📈 **Estadísticas generales:**
• Preguntas respondidas: 156
• Respuestas correctas: 89 (57%)
• Respuestas incorrectas: 67 (43%)
• Tiempo estudiado: 12h 30m

🎯 **Por temas:**
• 📜 Constitución: 78% (23/30)
• ⚖️ Derecho Administrativo: 45% (18/40)
• 🔍 Derecho Penal: 62% (15/24)
• 💼 Derecho Civil: 33% (8/24)

🔥 **Racha actual:** 5 días consecutivos
📅 **Último estudio:** Hace 2 horas

💡 **Recomendación:** 
Practicar más Derecho Administrativo para mejorar la puntuación general.
        """
        
        keyboard = [
            [InlineKeyboardButton("📊 Gráfico Detallado", callback_data="detailed_progress")],
            [InlineKeyboardButton("🎯 Test Recomendado", callback_data="recommended_test")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            progress_message,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def admin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /admin - Panel de administración"""
        if not self.is_admin(update.effective_user.id):
            await update.message.reply_text("❌ No tienes permisos de administrador.")
            return
        
        keyboard = [
            [InlineKeyboardButton("📊 Estadísticas", callback_data="admin_stats")],
            [InlineKeyboardButton("🚩 Reportes", callback_data="admin_reports")],
            [InlineKeyboardButton("👥 Usuarios", callback_data="admin_users")],
            [InlineKeyboardButton("📝 Preguntas", callback_data="admin_questions")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        admin_message = """
🔧 **Panel de Administración**

Selecciona una opción para gestionar el bot:

📊 **Estadísticas** - Ver métricas de uso
🚩 **Reportes** - Gestionar reportes de usuarios  
👥 **Usuarios** - Administrar usuarios y premium
📝 **Preguntas** - Gestionar base de preguntas
        """
        
        await update.message.reply_text(
            admin_message,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def tutor_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /tutor - Asistente IA (Próximamente)"""
        if not context.args:
            await update.message.reply_text(
                "🤖 **Tutor IA - Próximamente**\n\n"
                "El tutor IA personalizado estará disponible pronto.\n\n"
                "Podrás hacer preguntas como:\n"
                "• `/tutor explica el artículo 14`\n"
                "• `/tutor diferencia entre ley y decreto`\n"
                "• `/tutor casos prácticos`\n\n"
                "💎 *Funcionalidad Premium en desarrollo*"
            )
            return
        
        question = " ".join(context.args)
        await update.message.reply_text(
            f"🤖 **Tutor IA - En desarrollo**\n\n"
            f"❓ **Tu pregunta:** {question}\n\n"
            f"Esta funcionalidad estará disponible próximamente.\n"
            f"Mientras tanto, puedes usar `/test` para practicar."
        )
    
    async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /about - Información del bot"""
        about_text = """
🤖 **OpoBot v1.0**

Bot especializado en preparación de oposiciones.

**🛠️ Características:**
• Tests interactivos por temas
• Seguimiento de progreso personal
• Sistema de reportes de calidad
• Recordatorios de estudio

**💎 Premium (en desarrollo):**
• Tutor IA personalizado
• Simulacros cronometrados
• Análisis avanzado con gráficos

**👨‍💻 Desarrollado por:** @tu_usuario
**📧 Soporte:** tu_email@ejemplo.com
**🌐 Web:** https://tu-web.com

**📊 Estado del sistema:**
• ✅ Bot operativo
• ✅ Base de datos conectada
• 🔄 IA en desarrollo
        """
        
        keyboard = [
            [InlineKeyboardButton("🚀 Hacer Test", callback_data="test_menu")],
            [InlineKeyboardButton("📊 Mi Progreso", callback_data="progreso")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            about_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar callbacks de botones inline"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "test_menu":
            await query.edit_message_text(
                "🎯 **Selecciona tipo de test:**\n\n"
                "🎲 **Aleatorio** - Preguntas variadas\n"
                "📚 **Por tema** - Elige tema específico\n"
                "🔄 **Continuar** - Donde lo dejaste",
                parse_mode='Markdown'
            )
        
        elif data == "progreso":
            await query.edit_message_text(
                "📊 **Tu progreso se está cargando...**\n\n"
                "Usa `/progreso` para ver estadísticas detalladas.",
                parse_mode='Markdown'
            )
        
        elif data == "config":
            keyboard = [
                [InlineKeyboardButton("🔔 Recordatorios", callback_data="config_reminders")],
                [InlineKeyboardButton("🎯 Preferencias", callback_data="config_preferences")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                "⚙️ **Configuración**\n\n"
                "¿Qué quieres configurar?",
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
        
        elif data.startswith("admin_"):
            if not self.is_admin(query.from_user.id):
                await query.edit_message_text("❌ Sin permisos de administrador.")
                return
            
            if data == "admin_stats":
                await query.edit_message_text(
                    "📊 **Estadísticas del Bot**\n\n"
                    "• Usuarios totales: 1,234\n"
                    "• Usuarios activos (7d): 456\n"
                    "• Preguntas respondidas: 12,345\n"
                    "• Reportes pendientes: 3\n"
                    "• Uptime: 99.9%",
                    parse_mode='Markdown'
                )
        
        else:
            await query.edit_message_text(
                f"🔄 **Función en desarrollo**\n\n"
                f"La opción '{data}' estará disponible pronto."
            )
    
    async def unknown_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar comandos desconocidos"""
        await update.message.reply_text(
            "❓ **Comando no reconocido**\n\n"
            "Usa `/help` para ver todos los comandos disponibles.\n"
            "O `/start` para volver al menú principal."
        )
    
    def setup_handlers(self):
        """Configurar manejadores de comandos"""
        # Comandos principales
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("test", self.test_command))
        self.application.add_handler(CommandHandler("progreso", self.progreso_command))
        self.application.add_handler(CommandHandler("tutor", self.tutor_command))
        self.application.add_handler(CommandHandler("about", self.about_command))
        
        # Comandos de admin
        self.application.add_handler(CommandHandler("admin", self.admin_command))
        
        # Callbacks de botones
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
        
        # Manejar comandos desconocidos
        self.application.add_handler(
            MessageHandler(filters.COMMAND, self.unknown_command)
        )
        
        logger.info("✅ Todos los handlers configurados")
    
    async def run(self):
        """Ejecutar el bot"""
        logger.info("🚀 Inicializando OpoBot...")
        
        # Crear aplicación
        self.application = Application.builder().token(settings.TELEGRAM_TOKEN).build()
        
        # Configurar handlers
        self.setup_handlers()
        
        # Información de inicio
        logger.info("📋 Configuración activa:")
        logger.info(f"   🤖 Token: {settings.TELEGRAM_TOKEN[:10]}...")
        logger.info(f"   👤 Admin ID: {settings.ADMIN_USER_ID}")
        logger.info(f"   💾 Base de datos: {settings.DATABASE_URL}")
        logger.info(f"   📁 Directorio datos: {settings.DATA_DIR}")
        
        # Ejecutar bot
        logger.info("🎯 Bot iniciado correctamente. Presiona Ctrl+C para detener.")
        await self.application.run_polling(
            drop_pending_updates=True,
            close_loop=False
        )

async def main():
    """Función principal"""
    try:
        bot = OpoBot()
        await bot.run()
    except KeyboardInterrupt:
        logger.info("👋 Bot detenido por el usuario")
    except Exception as e:
        logger.error(f"❌ Error fatal: {e}")
        raise

if __name__ == "__main__":
    print("🤖 OpoBot - Bot de Preparación de Oposiciones")
    print("=" * 50)
    asyncio.run(main())