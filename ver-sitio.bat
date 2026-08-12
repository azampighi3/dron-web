@echo off
title Sitio web RCKT
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
  echo.
  echo   No se encontro Python en este computador.
  echo   Instalalo desde https://www.python.org/downloads/
  echo   IMPORTANTE: marca la casilla "Add Python to PATH" al instalar.
  echo.
  pause
  exit /b 1
)

python ver-sitio.py
pause
