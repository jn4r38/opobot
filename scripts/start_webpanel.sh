#!/bin/bash

# Inicia el panel web con Uvicorn
PYTHONPATH=$PWD \
uvicorn backend.main:app \
--host 0.0.0.0 \
--port 8000 \
--reload \
--log-level debug