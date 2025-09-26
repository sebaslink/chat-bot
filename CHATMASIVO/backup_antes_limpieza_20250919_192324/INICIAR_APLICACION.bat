@echo off
chcp 65001 >nul
title Chat Masivo WhatsApp - Iniciar Aplicación

echo.
echo ========================================
echo   CHAT MASIVO WHATSAPP - INICIAR APP
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

:: Verificar archivo principal
if not exist "main.py" (
    echo ❌ No se encuentra el archivo main.py
    echo.
    echo 🔧 Solución: Ejecuta desde la carpeta raíz del proyecto
    echo.
    pause
    exit /b 1
)

echo ✅ Archivo principal encontrado
echo.

:: Verificar dependencias
echo 🔍 Verificando dependencias...
python -c "import flask, twilio, pandas, openpyxl" >nul 2>&1
if errorlevel 1 (
    echo 📦 Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Error instalando dependencias
        pause
        exit /b 1
    )
    echo ✅ Dependencias instaladas
) else (
    echo ✅ Dependencias OK
)

echo.
echo 🚀 Iniciando Chat Masivo...
echo.
echo 📱 La aplicación se abrirá en: http://localhost:5000
echo.
echo ⚠️  Para detener la aplicación presiona Ctrl+C
echo.

:: Iniciar aplicación en segundo plano
echo 🚀 Iniciando aplicación...
start /b python main.py

:: Esperar a que la aplicación inicie
echo ⏳ Esperando que la aplicación inicie...
timeout /t 5 /nobreak >nul

:: Verificar que esté funcionando
echo 🔍 Verificando aplicación...
python -c "import requests; r = requests.get('http://localhost:5000', timeout=5); print('✅ Aplicación funcionando' if r.status_code == 200 else '❌ Error en aplicación')" 2>nul

if errorlevel 1 (
    echo ❌ No se puede conectar a la aplicación
    echo.
    echo 💡 Posibles soluciones:
    echo    - Verifica que el puerto 5000 esté libre
    echo    - Ejecuta como administrador
    echo    - Revisa los logs de error
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ¡APLICACIÓN FUNCIONANDO CORRECTAMENTE!
echo ========================================
echo.
echo 🌐 Abriendo navegador automáticamente...
echo.

:: Abrir navegador automáticamente
start http://localhost:5000

echo ✅ Navegador abierto en http://localhost:5000
echo.
echo 📋 FUNCIONALIDADES DISPONIBLES:
echo   ✅ Agregar contactos
echo   ✅ Crear grupos
echo   ✅ Plantillas de mensajes
echo   ✅ Envío masivo
echo   ✅ Importar/Exportar Excel
echo   ✅ Estadísticas
echo   ✅ Eliminar contactos
echo.
echo ⚠️  Para detener la aplicación presiona Ctrl+C en esta ventana
echo.
echo 👋 Mantén esta ventana abierta mientras uses la aplicación
pause
