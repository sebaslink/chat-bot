@echo off
title Chatbot Inteligente - SISTEMA UNIFICADO CON LOGIN
color 0A

echo.
echo ================================================================================
echo                    SISTEMA UNIFICADO FINAL - CHATBOT Y CHAT MASIVO
echo                    Sistema Completo con Login y Control de Acceso
echo ================================================================================
echo.

REM Detectar automáticamente la ruta de Python
echo [INFO] Detectando instalación de Python...

REM Intentar diferentes rutas de Python
set PYTHON_PATH=""

REM 1. Verificar si python está en PATH
python --version >nul 2>&1
if not errorlevel 1 (
    echo [OK] Python detectado en PATH
    set PYTHON_PATH=python
    goto :found_python
)

REM 2. Verificar ruta del entorno virtual local
if exist "chatbot_env\Scripts\python.exe" (
    echo [OK] Python detectado en entorno virtual local
    set PYTHON_PATH="chatbot_env\Scripts\python.exe"
    goto :found_python
)

REM 3. Verificar rutas comunes de Python
if exist "C:\Program Files\Python313\python.exe" (
    echo [OK] Python detectado en Program Files
    set PYTHON_PATH="C:\Program Files\Python313\python.exe"
    goto :found_python
)

if exist "C:\Program Files\Python312\python.exe" (
    echo [OK] Python detectado en Program Files (3.12)
    set PYTHON_PATH="C:\Program Files\Python312\python.exe"
    goto :found_python
)

if exist "C:\Program Files\Python311\python.exe" (
    echo [OK] Python detectado en Program Files (3.11)
    set PYTHON_PATH="C:\Program Files\Python311\python.exe"
    goto :found_python
)

if exist "C:\Python313\python.exe" (
    echo [OK] Python detectado en C:\Python313
    set PYTHON_PATH="C:\Python313\python.exe"
    goto :found_python
)

if exist "C:\Python312\python.exe" (
    echo [OK] Python detectado en C:\Python312
    set PYTHON_PATH="C:\Python312\python.exe"
    goto :found_python
)

REM 4. Buscar en AppData
for /d %%i in ("%USERPROFILE%\AppData\Local\Programs\Python\Python*") do (
    if exist "%%i\python.exe" (
        echo [OK] Python detectado en %%i
        set PYTHON_PATH="%%i\python.exe"
        goto :found_python
    )
)

REM Si no se encuentra Python
echo [ERROR] No se pudo detectar Python en el sistema
echo [INFO] Por favor instala Python desde https://python.org
echo [INFO] Asegúrate de marcar "Add Python to PATH" durante la instalación
pause
exit /b 1

:found_python
echo [OK] Usando Python: %PYTHON_PATH%
echo.

REM Verificar que el archivo principal existe
if not exist "SISTEMA_UNIFICADO_FINAL.py" (
    echo [ERROR] No se encontró SISTEMA_UNIFICADO_FINAL.py
    echo [INFO] Asegúrate de ejecutar este archivo desde el directorio correcto
    pause
    exit /b 1
)

echo [OK] Archivo principal encontrado
echo.

REM Instalar dependencias básicas
echo [INFO] Instalando dependencias necesarias...
%PYTHON_PATH% -m pip install Flask Werkzeug PyPDF2 python-docx requests beautifulsoup4 python-dotenv Pillow openpyxl --quiet --disable-pip-version-check

if errorlevel 1 (
    echo [WARNING] Error instalando algunas dependencias, continuando...
) else (
    echo [OK] Dependencias instaladas correctamente
)
echo.

REM Crear directorios necesarios
echo [INFO] Creando directorios necesarios...
if not exist "uploads" mkdir uploads
if not exist "data" mkdir data
if not exist "data\database" mkdir data\database
if not exist "templates" mkdir templates
if not exist "static" mkdir static
if not exist "static\uploads" mkdir static\uploads
if not exist "CHATMASIVO" mkdir CHATMASIVO

echo [OK] Directorios creados
echo.

REM Limpiar procesos Python anteriores
echo [INFO] Limpiando procesos anteriores...
taskkill /f /im python.exe >nul 2>&1

echo [OK] Procesos limpiados
echo.

REM Mostrar información del sistema
echo ================================================================================
echo                    INFORMACIÓN DEL SISTEMA
echo ================================================================================
echo.
echo [SISTEMA DE LOGIN IMPLEMENTADO]
echo [INFO] - Control de acceso por roles de usuario
echo [INFO] - Asesores: Acceso al Chat Masivo
echo [INFO] - Administradores/Programadores: Acceso completo al sistema
echo [INFO] - Redirección automática según rol
echo [INFO] - Gestión de sesiones segura
echo.
echo [FUNCIONALIDADES PRINCIPALES]
echo [INFO] - Chat Inteligente con IA
echo [INFO] - Carga de Documentos (PDF, Word, Excel, PowerPoint, Imágenes)
echo [INFO] - Extracción de contenido web
echo [INFO] - Chat Masivo por WhatsApp
echo [INFO] - Base de datos integrada
echo [INFO] - Gestión de usuarios
echo [INFO] - Interfaz web moderna y responsive
echo.
echo [URLS DEL SISTEMA]
echo [INFO] - URL Principal: http://localhost:5000
echo [INFO] - URL Login: http://localhost:5000/login
echo [INFO] - URL Chat Masivo: http://localhost:5001 (se abre automáticamente)
echo.
echo ================================================================================
echo                    INSTRUCCIONES DE USO
echo ================================================================================
echo.
echo [PASO 1] PRIMER USO:
echo [INFO] 1. El sistema se abrirá automáticamente en tu navegador
echo [INFO] 2. Serás redirigido a la página de login
echo [INFO] 3. Crea un usuario administrador desde la interfaz
echo [INFO] 4. Inicia sesión con tus credenciales
echo.
echo [PASO 2] GESTIÓN DE USUARIOS:
echo [INFO] 1. Como administrador, ve a la pestaña "Usuarios"
echo [INFO] 2. Crea usuarios con diferentes roles:
echo [INFO]    - Asesor: Solo acceso al Chat Masivo
echo [INFO]    - Administrador: Acceso completo al sistema
echo [INFO]    - Programador: Acceso completo al sistema
echo.
echo [PASO 3] USO DEL SISTEMA:
echo [INFO] 1. Sube documentos en la pestaña "Documentos"
echo [INFO] 2. Usa la pestaña "Chat" para conversar con la IA
echo [INFO] 3. Gestiona la base de datos en la pestaña "Base de Datos"
echo [INFO] 4. Accede al Chat Masivo desde el botón correspondiente
echo.
echo ================================================================================
echo                    INICIANDO SISTEMA
echo ================================================================================
echo.
echo [INFO] Iniciando Chatbot Inteligente...
echo [INFO] El sistema se abrirá automáticamente en tu navegador
echo [INFO] Presiona Ctrl+C para detener el servidor
echo.

REM Ejecutar el sistema
%PYTHON_PATH% SISTEMA_UNIFICADO_FINAL.py

echo.
echo [INFO] Sistema detenido!
echo [INFO] Gracias por usar el Chatbot Inteligente
pause
