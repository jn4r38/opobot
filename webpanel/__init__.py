from fastapi.templating import Jinja2Templates
from pathlib import Path

# Configuración de templates
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

# Exporta solo lo esencial
__all__ = ['templates']