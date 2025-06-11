import os
import shutil
from pathlib import Path

def create_essential_dirs():
    """Crea solo los directorios esenciales que faltan"""
    essential_dirs = [
        "data/preguntas",
        "scripts"
    ]
    for dir_path in essential_dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"📂 Directorio creado: {dir_path}")

def secure_configs():
    """Crea o actualiza configuraciones de forma segura"""
    # Crear .env si no existe
    env_path = ".env"
    if not os.path.exists(env_path):
        with open(env_path, "w") as f:
            f.write("""# Configuración de entorno
TELEGRAM_TOKEN=tu_token_aqui
DATABASE_URL=sqlite:///data.db
OPENAI_API_KEY=tu_key_aqui
ADMIN_CHAT_ID=tu_id_aqui
""")
        print(f"🛡️ Archivo .env creado: {env_path}")
    
    # Actualizar config.py con backup
    config_path = "config.py"
    if os.path.exists(config_path):
        # Crear backup
        backup_path = f"{config_path}.bak"
        shutil.copy(config_path, backup_path)
        print(f"📦 Backup creado: {backup_path}")
        
        # Escribir nueva versión
        with open(config_path, "w") as f:
            f.write("""from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data.db")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
""")
        print(f"🔒 Configuración actualizada: {config_path}")

def setup_core_models():
    """Configura los modelos core solo si no existen"""
    core_dir = "core"
    os.makedirs(core_dir, exist_ok=True)
    
    # database.py
    db_path = os.path.join(core_dir, "database.py")
    if not os.path.exists(db_path):
        with open(db_path, "w") as f:
            f.write("""from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

def init_db():
    engine = create_engine(os.getenv("DATABASE_URL"))
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
""")
        print(f"💾 Módulo database creado: {db_path}")
    
    # models.py
    models_path = os.path.join(core_dir, "models.py")
    if not os.path.exists(models_path):
        with open(models_path, "w") as f:
            f.write("""from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Question(Base):
    __tablename__ = "questions"
    id = Column(String, primary_key=True)
    text = Column(String)
    category = Column(String)  # Formato: tema/subtema/artículo
    difficulty = Column(Integer)
    options = Column(String)  # JSON serializado

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True)
    question_id = Column(String, ForeignKey('questions.id'))
    reason = Column(String)
    comment = Column(String)
    status = Column(String, default='pending')  # pending/resolved/rejected
""")
        print(f"📝 Modelos creados: {models_path}")

def setup_example_yaml():
    """Crea un ejemplo de pregunta YAML"""
    yaml_path = "data/preguntas/ejemplo.yml"
    if not os.path.exists(yaml_path):
        os.makedirs(os.path.dirname(yaml_path), exist_ok=True)
        with open(yaml_path, "w") as f:
            f.write("""- tema: Derecho Civil
  subtema: Contratos
  articulo: 1454
  pregunta: "¿Qué es un contrato de compraventa?"
  opciones:
    - "A. Un acuerdo de voluntades"
    - "B. Un documento notarial"
    - "C. Un acto judicial"
  respuesta: "A"
  explicacion: "El contrato de compraventa se define como un acuerdo de voluntades..."
""")
        print(f"📄 Ejemplo YAML creado: {yaml_path}")

def main():
    print("\n⚙️ Configuración de proyecto para OpoBot\n")
    print("Este script realizará las siguientes acciones:")
    print("1. Creará carpetas esenciales faltantes")
    print("2. Configurará archivos de entorno (.env)")
    print("3. Actualizará config.py con seguridad mejorada")
    print("4. Creará modelos de base de datos básicos")
    print("5. Añadirá un ejemplo de pregunta YAML\n")
    
    confirm = input("¿Deseas continuar? (s/n): ").strip().lower()
    if confirm != 's':
        print("❌ Ejecución cancelada")
        return
    
    create_essential_dirs()
    secure_configs()
    setup_core_models()
    setup_example_yaml()
    
    print("\n✅ Configuración completada! Siguientes pasos:")
    print("1. Edita el archivo .env con tus credenciales reales")
    print("2. Revisa los modelos en core/models.py")
    print("3. Añade tus preguntas en data/preguntas/")
    print("4. Ejecuta tu aplicación normalmente")

if __name__ == "__main__":
    main()
