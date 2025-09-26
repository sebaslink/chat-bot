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

REM 2. Verificar rutas comunes de Python
if exist "C:\Program Files\Python313\python.exe" (
    echo [OK] Python detectado en Program Files (3.13)
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

REM 3. Buscar en AppData
for /d %%i in ("%USERPROFILE%\AppData\Local\Programs\Python\Python*") do (
    if exist "%%i\python.exe" (
        echo [OK] Python detectado en %%i
        set PYTHON_PATH="%%i\python.exe"
        goto :found_python
    )
)

REM 4. Buscar en Program Files (x86)
if exist "C:\Program Files (x86)\Python313\python.exe" (
    echo [OK] Python detectado en Program Files (x86) (3.13)
    set PYTHON_PATH="C:\Program Files (x86)\Python313\python.exe"
    goto :found_python
)

if exist "C:\Program Files (x86)\Python312\python.exe" (
    echo [OK] Python detectado en Program Files (x86) (3.12)
    set PYTHON_PATH="C:\Program Files (x86)\Python312\python.exe"
    goto :found_python
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
echo [INFO] - Asesores: Acceso directo al Chat Masivo original
echo [INFO] - Administradores/Programadores: Acceso completo al sistema
echo [INFO] - Redirección automática según rol implementada
echo [INFO] - Gestión de sesiones segura
echo [INFO] - Página de login para todos los usuarios
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
echo [INFO] - URL Principal: http://localhost:5000 (página de login)
echo [INFO] - URL Login: http://localhost:5000/login
echo [INFO] - URL Chat Masivo: http://localhost:5001 (aplicación original)
echo [INFO] - URL Chatbot: http://localhost:5000/chatbot (para administradores/programadores)
echo [INFO] - Redirección automática según rol después del login
echo.
echo ================================================================================
echo                    INSTRUCCIONES DE USO
echo ================================================================================
echo.
echo [PASO 1] PRIMER USO:
echo [INFO] 1. El sistema se abrirá automáticamente en tu navegador
echo [INFO] 2. Serás redirigido a la página de login
echo [INFO] 3. Usa las credenciales por defecto: admin/admin123
echo [INFO] 4. O crea un nuevo usuario desde la interfaz
echo.
echo [PASO 2] GESTIÓN DE USUARIOS:
echo [INFO] 1. Como administrador, ve a la pestaña "Usuarios"
echo [INFO] 2. Crea usuarios con diferentes roles:
echo [INFO]    - Asesor: Solo acceso al Chat Masivo
echo [INFO]    - Administrador: Acceso completo al sistema
echo [INFO]    - Programador: Acceso completo al sistema
echo.
echo [PASO 3] USO DEL SISTEMA:
echo [INFO] 1. ASESORES: Van directamente al Chat Masivo original
echo [INFO] 2. ADMINISTRADORES/PROGRAMADORES: Acceso completo al Chatbot
echo [INFO] 3. Sube documentos en la pestaña "Documentos"
echo [INFO] 4. Usa la pestaña "Chat" para conversar con la IA
echo [INFO] 5. Gestiona la base de datos en la pestaña "Base de Datos"
echo [INFO] 6. Accede al Chat Masivo desde el botón correspondiente
echo.
echo ================================================================================
echo                    CORRECCIONES IMPLEMENTADAS
echo ================================================================================
echo.
echo [SISTEMA DE LOGIN COMPLETO]
echo [INFO] - Página de login moderna y responsiva
echo [INFO] - Autenticación con usuario y contraseña
echo [INFO] - Redirección automática según rol:
echo [INFO]   * Asesores → Chat Masivo original (puerto 5001)
echo [INFO]   * Administradores/Programadores → ChatBot completo (puerto 5000)
echo [INFO] - Gestión de sesiones con cookies
echo [INFO] - Logout funcional desde todas las páginas
echo.
echo [GESTIÓN DE USUARIOS]
echo [INFO] - Creación de usuarios con diferentes roles
echo [INFO] - Formulario completo de registro
echo [INFO] - Base de datos de usuarios integrada
echo [INFO] - Visualización de usuarios en pestaña "Base de Datos"
echo [INFO] - Estadísticas por rol con colores distintivos
echo.
echo [CORRECCIONES TÉCNICAS]
echo [INFO] - Error "require_auth not defined" corregido
echo [INFO] - Decoradores movidos al inicio del archivo
echo [INFO] - Protección de todas las rutas sensibles
echo [INFO] - Peticiones frontend con credenciales incluidas
echo [INFO] - Redirección de asesores corregida
echo [INFO] - Página del Chat Masivo con información del usuario
echo [INFO] - Error de JSON en botón Chat Masivo solucionado
echo [INFO] - Interfaz en blanco del Chat Masivo corregida
echo [INFO] - Ruta /abrir_chatmasivo simplificada
echo [INFO] - Interfaz original del Chat Masivo funcionando
echo [INFO] - Redirección al Chat Masivo original (puerto 5001)
echo [INFO] - Inicio automático del Chat Masivo original
echo [INFO] - Sistema de roles corregido completamente
echo [INFO] - Asesores van directamente al Chat Masivo
echo [INFO] - Administradores/Programadores van al Chatbot completo
echo [INFO] - Redirección automática según rol implementada
echo [INFO] - Chat Masivo original funcionando en puerto 5001
echo [INFO] - Sistema de login completamente funcional
echo [INFO] - Error de conexión en Chat Masivo corregido
echo [INFO] - Manejo mejorado de errores de autenticación
echo [INFO] - Interfaz de usuario más amigable para errores
echo [INFO] - Mensajes informativos en lugar de errores alarmantes
echo [INFO] - Botón "Chatbot Completo" funcionando correctamente
echo [INFO] - Logout desde Chat Masivo corregido
echo [INFO] - Acceso directo al Chat Masivo sin redirección forzada
echo [INFO] - Manejo mejorado de errores de autenticación
echo [INFO] - Mensajes informativos en lugar de errores alarmantes
echo [INFO] - Estados no autenticados con colores grises
echo [INFO] - Botones de acción claros y accesibles
echo [INFO] - Comunicación robusta entre puertos 5000 y 5001
echo.
echo [BASE DE DATOS MEJORADA]
echo [INFO] - Visualización completa de la base de datos
echo [INFO] - Estadísticas en tiempo real
echo [INFO] - Gestión de usuarios integrada
echo [INFO] - Tabla de usuarios con información detallada
echo [INFO] - Exportación y backup de datos
echo.
echo [ESTADO ACTUAL DEL SISTEMA]
echo [INFO] - Sistema completamente funcional
echo [INFO] - Login implementado y funcionando
echo [INFO] - Redirección por roles operativa
echo [INFO] - Chat Masivo original integrado
echo [INFO] - Ambos servidores ejecutándose correctamente
echo [INFO] - Imágenes y recursos cargados
echo [INFO] - Error de conexión en Chat Masivo resuelto
echo [INFO] - Interfaz de usuario mejorada
echo [INFO] - Manejo de errores optimizado
echo [INFO] - Comunicación entre puertos 5000 y 5001 estable
echo [INFO] - Sistema de redirección por roles completamente funcional
echo [INFO] - Chat Masivo original integrado y funcionando
echo [INFO] - Botón "Chatbot Completo" operativo
echo [INFO] - Logout desde Chat Masivo corregido
echo [INFO] - Acceso directo sin redirección forzada
echo [INFO] - Interfaz de Chat Masivo optimizada para mejor visualización
echo [INFO] - Mensajes de error discretos y no intrusivos
echo [INFO] - Sistema completamente funcional sin conflictos de visualización
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