@echo off
title ORGANIZAR PROYECTO - VERSION SIMPLE
color 0A

echo.
echo ========================================
echo   ORGANIZANDO PROYECTO SIMPLE
echo   Chat Masivo WhatsApp
echo ========================================
echo.

REM Verificar si ya está organizado
if exist "codigo" (
    echo [INFO] El proyecto ya esta organizado
    echo [INFO] Verificando estructura...
    echo.
    
    REM Verificar archivos principales
    if exist "codigo\codchat_simple.py" (
        echo ✓ Archivo principal encontrado
    ) else (
        echo ✗ Archivo principal NO encontrado
    )
    
    if exist "configuracion\Twilio.env" (
        echo ✓ Configuracion encontrada
    ) else (
        echo ✗ Configuracion NO encontrada
    )
    
    if exist "templates\interface_simple.html" (
        echo ✓ Templates encontrados
    ) else (
        echo ✗ Templates NO encontrados
    )
    
    echo.
    echo ========================================
    echo   PROYECTO YA ORGANIZADO
    echo ========================================
    echo.
    echo Para ejecutar el programa:
    echo   Doble clic en: EJECUTAR_CHAT_MASIVO.bat
    echo.
    echo O desde la carpeta ejecutables:
    echo   ejecutables\ABRIR_APLICACION.bat
    echo.
    pause
    exit /b 0
)

REM Si no está organizado, organizar
echo [INFO] Organizando proyecto...

REM Crear carpetas si no existen
if not exist "codigo" mkdir codigo
if not exist "ejecutables" mkdir ejecutables
if not exist "documentacion" mkdir documentacion
if not exist "configuracion" mkdir configuracion
if not exist "templates" mkdir templates
if not exist "static" mkdir static
if not exist "logs" mkdir logs

echo ✓ Carpetas creadas

REM Mover archivos Python (solo si están en la raíz)
for %%f in (*.py) do (
    if exist "%%f" (
        move "%%f" "codigo\" >nul 2>&1
        echo   ✓ Movido: %%f
    )
)

REM Mover archivos .bat (solo si están en la raíz)
for %%f in (*.bat) do (
    if exist "%%f" (
        if not "%%f"=="ORGANIZAR_SIMPLE.bat" (
            move "%%f" "ejecutables\" >nul 2>&1
            echo   ✓ Movido: %%f
        )
    )
)

REM Mover archivos .md
for %%f in (*.md) do (
    if exist "%%f" (
        move "%%f" "documentacion\" >nul 2>&1
        echo   ✓ Movido: %%f
    )
)

REM Mover archivos .env y .txt
for %%f in (*.env) do (
    if exist "%%f" (
        move "%%f" "configuracion\" >nul 2>&1
        echo   ✓ Movido: %%f
    )
)

for %%f in (*.txt) do (
    if exist "%%f" (
        move "%%f" "configuracion\" >nul 2>&1
        echo   ✓ Movido: %%f
    )
)

REM Mover archivos de datos
for %%f in (*.db) do (
    if exist "%%f" (
        move "%%f" "logs\" >nul 2>&1
        echo   ✓ Movido: %%f
    )
)

for %%f in (*.log) do (
    if exist "%%f" (
        move "%%f" "logs\" >nul 2>&1
        echo   ✓ Movido: %%f
    )
)

REM Crear ejecutable principal
echo [INFO] Creando ejecutable principal...
(
echo @echo off
echo title Chat Masivo WhatsApp - Ejecutar
echo color 0A
echo.
echo echo.
echo echo ========================================
echo echo   CHAT MASIVO WHATSAPP
echo echo   Ejecutando desde carpeta organizada
echo echo ========================================
echo echo.
echo.
echo REM Cambiar al directorio de codigo
echo cd codigo
echo.
echo REM Verificar Python
echo python --version ^>nul 2^>^&1
echo if errorlevel 1 ^(
echo     echo [ERROR] Python no encontrado
echo     echo.
echo     echo Solucion:
echo     echo 1. Instala Python desde https://python.org
echo     echo 2. Marca "Add Python to PATH"
echo     echo 3. Reinicia esta ventana
echo     echo.
echo     pause
echo     exit /b 1
echo ^)
echo.
echo REM Instalar dependencias
echo echo [INFO] Instalando dependencias...
echo pip install -r ../configuracion/requirements.txt --quiet --disable-pip-version-check
echo.
echo REM Crear script para abrir navegador
echo echo [INFO] Preparando apertura automatica...
echo echo @echo off ^> abrir.bat
echo echo timeout /t 3 /nobreak ^^>nul ^^>^> abrir.bat
echo echo start http://localhost:5000 ^^>^> abrir.bat
echo echo del abrir.bat ^^>^> abrir.bat
echo start /B abrir.bat
echo.
echo echo.
echo echo ========================================
echo echo   INICIANDO APLICACION
echo echo ========================================
echo echo.
echo echo URL: http://localhost:5000
echo echo Puerto: 5000
echo echo Modo: Produccion ^(Twilio configurado^)
echo echo.
echo echo La aplicacion se abrira automaticamente
echo echo en tu navegador en unos segundos...
echo echo.
echo echo Para detener el servidor presiona Ctrl+C
echo echo.
echo.
echo REM Iniciar servidor
echo python codchat_simple.py
echo.
echo REM Limpiar
echo if exist abrir.bat del abrir.bat
echo.
echo echo.
echo echo Aplicacion cerrada.
echo pause
) > EJECUTAR_CHAT_MASIVO.bat

echo ✓ Ejecutable principal creado

echo.
echo ========================================
echo   ORGANIZACION COMPLETADA
echo ========================================
echo.
echo Estructura creada:
echo   codigo\          - Archivos Python
echo   ejecutables\     - Archivos .bat
echo   documentacion\   - Archivos .md
echo   configuracion\   - Archivos .env y .txt
echo   templates\       - Plantillas HTML
echo   static\          - Archivos estaticos
echo   logs\            - Base de datos y logs
echo.
echo Para ejecutar el programa:
echo   Doble clic en: EJECUTAR_CHAT_MASIVO.bat
echo.
echo ¡Proyecto organizado exitosamente!
echo.
pause