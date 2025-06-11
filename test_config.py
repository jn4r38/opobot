from pathlib import Path
from core.utils.config import settings

print("="*50)
print("🔍 Diagnóstico de configuración")
print(f"Archivo .env en: {Path('.env').absolute()}")
print(f"Token cargado: {'SÍ' if settings.TELEGRAM_TOKEN else 'NO'}")
print(f"Longitud token: {len(settings.TELEGRAM_TOKEN)}")
print(f"Contenido .env:\n{Path('.env').read_text()}")
print("="*50)
