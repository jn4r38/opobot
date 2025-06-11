#!/bin/bash

# Inicia el bot premium con configuración especial
PYTHONPATH=$PWD \
BOT_MODE="premium" \
python -m bot_premium.main \
--log-level=debug \
--reload