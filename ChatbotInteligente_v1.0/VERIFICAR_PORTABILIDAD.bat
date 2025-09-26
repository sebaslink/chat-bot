@echo off
chcp 65001 >nul
title Chatbot Inteligente v1.0 - Verificador de Portabilidad

echo ================================================================================
echo                   CHATBOT INTELIGENTE v1.0 - VERIFICADOR DE PORTABILIDAD
echo                   Verificación automática del sistema
echo ================================================================================
echo.

echo [INFO] Verificando compatibilidad del sistema...
echo.

:: Verificar sistema operativo
echo [INFO] Verificando sistema operativo...
if "%OS%"=="Windows_NT" (
    echo [OK] Windows detectado: %OS%
    set "SISTEMA_OK=1"
) else (
    echo [ERROR] Este sistema no es compatible
    set "SISTEMA_OK=0"
)

:: Verificar arquitectura
echo [INFO] Verificando arquitectura...
if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
    echo [OK] Arquitectura 64-bit detectada
    set "ARQUITECTURA_OK=1"
) else if "%PROCESSOR_ARCHITECTURE%"=="x86" (
    echo [OK] Arquitectura 32-bit detectada
    set "ARQUITECTURA_OK=1"
) else (
    echo [WARNING] Arquitectura no reconocida: %PROCESSOR_ARCHITECTURE%
    set "ARQUITECTURA_OK=1"
)

:: Verificar Python
echo [INFO] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no está instalado o no está en el PATH
    set "PYTHON_OK=0"
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%i"
    echo [OK] Python %PYTHON_VERSION% detectado
    
    :: Verificar versión mínima (3.8)
    for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
        if %%a GTR 3 (
            set "PYTHON_OK=1"
        ) else if %%a EQU 3 (
            if %%b GEQ 8 (
                set "PYTHON_OK=1"
            ) else (
                echo [ERROR] Python 3.8 o superior requerido
                set "PYTHON_OK=0"
            )
        ) else (
            echo [ERROR] Python 3.8 o superior requerido
            set "PYTHON_OK=0"
        )
    )
)

:: Verificar ubicación de Python
if %PYTHON_OK% EQU 1 (
    echo [INFO] Verificando ubicación de Python...
    for /f "tokens=*" %%i in ('where python 2^>nul') do set "PYTHON_PATH=%%i"
    echo [OK] Python encontrado en: %PYTHON_PATH%
)

:: Verificar archivos críticos
echo [INFO] Verificando archivos críticos...
if exist "SISTEMA_UNIFICADO_FINAL.py" (
    echo [OK] Archivo principal encontrado
    set "ARCHIVO_PRINCIPAL_OK=1"
) else (
    echo [ERROR] Archivo principal SISTEMA_UNIFICADO_FINAL.py no encontrado
    set "ARCHIVO_PRINCIPAL_OK=0"
)

if exist "requirements_completo.txt" (
    echo [OK] Archivo de dependencias encontrado
    set "REQUIREMENTS_OK=1"
) else (
    echo [ERROR] Archivo requirements_completo.txt no encontrado
    set "REQUIREMENTS_OK=0"
)

if exist "templates" (
    echo [OK] Carpeta de templates encontrada
    set "TEMPLATES_OK=1"
) else (
    echo [ERROR] Carpeta templates no encontrada
    set "TEMPLATES_OK=0"
)

if exist "static" (
    echo [OK] Carpeta static encontrada
    set "STATIC_OK=1"
) else (
    echo [ERROR] Carpeta static no encontrada
    set "STATIC_OK=0"
)

:: Verificar dependencias instaladas
if %PYTHON_OK% EQU 1 (
    echo [INFO] Verificando dependencias instaladas...
    %PYTHON_PATH% -c "import flask" >nul 2>&1
    if %errorlevel% neq 0 (
        echo [WARNING] Flask no está instalado
        set "FLASK_OK=0"
    ) else (
        echo [OK] Flask instalado
        set "FLASK_OK=1"
    )
    
    %PYTHON_PATH% -c "import sqlite3" >nul 2>&1
    if %errorlevel% neq 0 (
        echo [WARNING] SQLite3 no está disponible
        set "SQLITE_OK=0"
    ) else (
        echo [OK] SQLite3 disponible
        set "SQLITE_OK=1"
    )
) else (
    set "FLASK_OK=0"
    set "SQLITE_OK=0"
)

:: Verificar puertos disponibles
echo [INFO] Verificando puertos disponibles...
netstat -an | findstr ":5000" >nul
if %errorlevel% equ 0 (
    echo [WARNING] Puerto 5000 está en uso
    set "PUERTO_5000_OK=0"
) else (
    echo [OK] Puerto 5000 disponible
    set "PUERTO_5000_OK=1"
)

netstat -an | findstr ":5001" >nul
if %errorlevel% equ 0 (
    echo [WARNING] Puerto 5001 está en uso
    set "PUERTO_5001_OK=0"
) else (
    echo [OK] Puerto 5001 disponible
    set "PUERTO_5001_OK=1"
)

:: Calcular puntuación de compatibilidad
set /a PUNTUACION=0
if %SISTEMA_OK% EQU 1 set /a PUNTUACION+=20
if %ARQUITECTURA_OK% EQU 1 set /a PUNTUACION+=10
if %PYTHON_OK% EQU 1 set /a PUNTUACION+=30
if %ARCHIVO_PRINCIPAL_OK% EQU 1 set /a PUNTUACION+=10
if %REQUIREMENTS_OK% EQU 1 set /a PUNTUACION+=5
if %TEMPLATES_OK% EQU 1 set /a PUNTUACION+=5
if %STATIC_OK% EQU 1 set /a PUNTUACION+=5
if %FLASK_OK% EQU 1 set /a PUNTUACION+=10
if %SQLITE_OK% EQU 1 set /a PUNTUACION+=5

:: Mostrar resultados
echo.
echo ================================================================================
echo                   RESULTADOS DE LA VERIFICACIÓN
echo ================================================================================
echo.

if %PUNTUACION% GEQ 90 (
    echo [✅ EXCELENTE] Sistema completamente compatible (%PUNTUACION%%%)
    echo [INFO] El sistema debería funcionar perfectamente
    set "ESTADO=EXCELENTE"
) else if %PUNTUACION% GEQ 70 (
    echo [⚠️  BUENO] Sistema mayormente compatible (%PUNTUACION%%%)
    echo [INFO] El sistema debería funcionar con algunas advertencias
    set "ESTADO=BUENO"
) else if %PUNTUACION% GEQ 50 (
    echo [⚠️  REGULAR] Sistema parcialmente compatible (%PUNTUACION%%%)
    echo [INFO] El sistema puede funcionar pero necesita correcciones
    set "ESTADO=REGULAR"
) else (
    echo [❌ MALO] Sistema no compatible (%PUNTUACION%%%)
    echo [INFO] El sistema no funcionará correctamente
    set "ESTADO=MALO"
)

echo.
echo [DETALLES DE LA VERIFICACIÓN]
echo.

if %SISTEMA_OK% EQU 1 (
    echo ✅ Sistema operativo: Compatible
) else (
    echo ❌ Sistema operativo: No compatible
)

if %ARQUITECTURA_OK% EQU 1 (
    echo ✅ Arquitectura: Compatible
) else (
    echo ❌ Arquitectura: No compatible
)

if %PYTHON_OK% EQU 1 (
    echo ✅ Python: Instalado y compatible
) else (
    echo ❌ Python: No instalado o no compatible
)

if %ARCHIVO_PRINCIPAL_OK% EQU 1 (
    echo ✅ Archivo principal: Encontrado
) else (
    echo ❌ Archivo principal: No encontrado
)

if %REQUIREMENTS_OK% EQU 1 (
    echo ✅ Dependencias: Archivo encontrado
) else (
    echo ❌ Dependencias: Archivo no encontrado
)

if %TEMPLATES_OK% EQU 1 (
    echo ✅ Templates: Carpeta encontrada
) else (
    echo ❌ Templates: Carpeta no encontrada
)

if %STATIC_OK% EQU 1 (
    echo ✅ Recursos estáticos: Carpeta encontrada
) else (
    echo ❌ Recursos estáticos: Carpeta no encontrada
)

if %FLASK_OK% EQU 1 (
    echo ✅ Flask: Instalado
) else (
    echo ❌ Flask: No instalado
)

if %SQLITE_OK% EQU 1 (
    echo ✅ SQLite3: Disponible
) else (
    echo ❌ SQLite3: No disponible
)

if %PUERTO_5000_OK% EQU 1 (
    echo ✅ Puerto 5000: Disponible
) else (
    echo ⚠️  Puerto 5000: En uso
)

if %PUERTO_5001_OK% EQU 1 (
    echo ✅ Puerto 5001: Disponible
) else (
    echo ⚠️  Puerto 5001: En uso
)

echo.
echo [RECOMENDACIONES]

if %PYTHON_OK% EQU 0 (
    echo 🔧 Instala Python 3.8 o superior desde https://python.org
    echo 🔧 Asegúrate de marcar "Add Python to PATH" durante la instalación
)

if %FLASK_OK% EQU 0 (
    echo 🔧 Ejecuta: pip install -r requirements_completo.txt
)

if %PUERTO_5000_OK% EQU 0 (
    echo 🔧 Cierra otras aplicaciones que usen el puerto 5000
)

if %PUERTO_5001_OK% EQU 0 (
    echo 🔧 Cierra otras aplicaciones que usen el puerto 5001
)

if %ESTADO% EQU "EXCELENTE" (
    echo 🚀 El sistema está listo para funcionar
    echo 🚀 Ejecuta INSTALAR_EN_OTRA_COMPUTADORA.bat para configurar
) else if %ESTADO% EQU "BUENO" (
    echo ⚠️  El sistema debería funcionar con algunas advertencias
    echo ⚠️  Ejecuta INSTALAR_EN_OTRA_COMPUTADORA.bat para configurar
) else if %ESTADO% EQU "REGULAR" (
    echo 🔧 El sistema necesita correcciones antes de funcionar
    echo 🔧 Sigue las recomendaciones anteriores
) else (
    echo ❌ El sistema no es compatible con esta computadora
    echo ❌ Instala los requisitos necesarios
)

echo.
echo ================================================================================
echo                   VERIFICACIÓN COMPLETADA
echo ================================================================================
echo.
echo [INFO] Puntuación de compatibilidad: %PUNTUACION%%%
echo [INFO] Estado: %ESTADO%
echo.
echo [INFO] Presiona cualquier tecla para continuar...
pause >nul
