@echo off
chcp 65001 >nul
title Chat Masivo WhatsApp - Crear Instalador

echo.
echo ========================================
echo   CHAT MASIVO - CREAR INSTALADOR
echo ========================================
echo.

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado o no está en el PATH
    echo.
    echo 📥 Descarga Python desde: https://www.python.org/downloads/
    echo    Asegúrate de marcar "Add Python to PATH" durante la instalación
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

:: Verificar archivos necesarios
if not exist "main.py" (
    echo ❌ No se encuentra el archivo main.py
    echo.
    echo 🔧 Solución: Ejecuta desde la carpeta raíz del proyecto
    echo.
    pause
    exit /b 1
)

if not exist "scripts\installer\crear_instalador_final.py" (
    echo ❌ No se encuentra el script del instalador
    echo.
    echo 🔧 Solución: Verifica que la estructura del proyecto esté completa
    echo.
    pause
    exit /b 1
)

echo ✅ Archivos necesarios encontrados
echo.

:: Instalar PyInstaller si no está instalado
echo 🔍 Verificando PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo 📦 Instalando PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ Error instalando PyInstaller
        pause
        exit /b 1
    )
    echo ✅ PyInstaller instalado
) else (
    echo ✅ PyInstaller ya está instalado
)

echo.
echo 🔨 Creando instalador...
echo.

:: Ejecutar script de creación de instalador
python scripts\installer\crear_instalador_final.py

if errorlevel 1 (
    echo.
    echo ❌ Error creando instalador
    echo.
    echo 💡 Posibles soluciones:
    echo    - Verifica que todos los archivos estén presentes
    echo    - Asegúrate de que no haya procesos usando archivos
    echo    - Ejecuta como administrador si es necesario
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ¡INSTALADOR CREADO EXITOSAMENTE!
echo ========================================
echo.
echo 📁 Ubicación: ChatMasivo_Portable\
echo.
echo 📋 INSTRUCCIONES:
echo 1. Copia la carpeta 'ChatMasivo_Portable' a cualquier computadora
echo 2. Configura 'Twilio.env' con tus credenciales
echo 3. Ejecuta 'ChatMasivo.exe'
echo 4. Abre http://localhost:5000 en tu navegador
echo.
echo 🎉 ¡Listo para distribuir!
echo.
pause
