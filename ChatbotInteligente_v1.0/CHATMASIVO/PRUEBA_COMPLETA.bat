@echo off
chcp 65001 >nul
title Chat Masivo WhatsApp - Prueba Completa

echo.
echo ========================================
echo   CHAT MASIVO - PRUEBA COMPLETA
echo ========================================
echo.

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

:: Verificar archivos principales
if not exist "main.py" (
    echo ❌ No se encuentra main.py
    pause
    exit /b 1
)

if not exist "templates\interface_simple.html" (
    echo ❌ No se encuentra la interfaz
    pause
    exit /b 1
)

echo ✅ Archivos principales encontrados
echo.

:: Reparar base de datos si es necesario
echo 🔧 Verificando base de datos...
python reparar_base_datos.py
if errorlevel 1 (
    echo ❌ Error reparando base de datos
    pause
    exit /b 1
)

echo ✅ Base de datos OK
echo.

:: Iniciar aplicación en segundo plano
echo 🚀 Iniciando aplicación...
start /b python main.py

:: Esperar a que inicie
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
echo 🌐 Accede a: http://localhost:5000
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
echo 🎉 ¡Prueba completada exitosamente!
echo.
echo 💡 Para crear instalador ejecuta: CREAR_INSTALADOR_FINAL.bat
echo.
pause
