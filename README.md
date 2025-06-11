# Sistema de Oposiciones Bots

## Estructura
```
├── bot_basico/          # Bot simple
├── bot_premium/         # Bot con IA
├── backend/             # API FastAPI
├── webpanel/            # Panel de control
└── core/                # Código compartido
```

## Requisitos
- Python 3.10+
- PostgreSQL (opcional)

## Instalación
```bash
pip install -r requirements.txt
cp .env.example .env  # Y configura tus variables
```

## Uso
```bash
# Bot básico
./scripts/start_basic.sh

# Bot premium
./scripts/start_premium.sh

# Panel web
./scripts/start_webpanel.sh
```

## Variables de Entorno Clave
| Variable | Descripción |
|----------|-------------|
| `TELEGRAM_*_TOKEN` | Tokens de bots de Telegram |
| `DATABASE_URL` | URL de conexión a la base de datos |
| `SECRET_KEY` | Para JWT y encriptación |

## Licencia
MIT