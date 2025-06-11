#!/bin/bash

# Inicia el bot básico con auto-reload en desarrollo
PYTHONPATH=$PWD \
BOT_MODE="basic" \
python -m bot_basico.main \
--log-level=info \
--reload