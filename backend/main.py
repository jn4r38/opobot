from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import admin, reports, auth

# 👇 Cambia esto según tus necesidades de CORS
app = FastAPI(title="Oposiciones Bot API", version="1.0")

# Configuración CORS (Ajusta los orígenes permitidos)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica dominios reales
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluye los routers
app.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
app.include_router(admin.router, prefix="/admin", tags=["Administración"])
app.include_router(reports.router, prefix="/reports", tags=["Reportes"])

# 👇 Cambia este endpoint de prueba si lo necesitas
@app.get("/health")
async def health_check():
    return {"status": "ok"}