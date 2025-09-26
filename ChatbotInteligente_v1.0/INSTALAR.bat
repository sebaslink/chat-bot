@echo off
title Chatbot Inteligente - Instalador
color 0A

echo ================================================================================
echo                    CHATBOT INTELIGENTE - INSTALADOR
echo                    Sistema Completo con Todas las Funcionalidades
echo ================================================================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no está instalado
    echo [INFO] Descarga Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python detectado
echo.

REM Ejecutar instalador automático
echo [INFO] Ejecutando instalación automática...
python instalar_chatbot.py

if errorlevel 1 (
    echo [ERROR] Error en la instalación
    pause
    exit /b 1
)

REM Crear ejecutable final
echo [INFO] Creando ejecutable final...
copy "EJECUTAR_CHATBOT_CORREGIDO.bat" "EJECUTAR_CHATBOT.bat"

echo [OK] Instalación completada
echo [INFO] Ejecuta 'EJECUTAR_CHATBOT.bat' para iniciar
pause
