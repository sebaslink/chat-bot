@echo off
chcp 65001 >nul
title Chatbot Inteligente v1.0 - Instalador Portátil

echo ================================================================================
echo                   CHATBOT INTELIGENTE v1.0 - INSTALADOR PORTÁTIL
echo                   Instalación automática en cualquier computadora
echo ================================================================================
echo.

echo [INFO] Este instalador detectará automáticamente la configuración de tu sistema
echo [INFO] y configurará el Chatbot Inteligente para funcionar correctamente.
echo.

:: Detectar sistema operativo
echo [INFO] Detectando sistema operativo...
if "%OS%"=="Windows_NT" (
    echo [OK] Windows detectado
    set "SISTEMA=windows"
) else (
    echo [ERROR] Este instalador es para Windows
    pause
    exit /b 1
)

:: Detectar arquitectura
echo [INFO] Detectando arquitectura del sistema...
if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
    echo [OK] Arquitectura 64-bit detectada
    set "ARQUITECTURA=64"
) else (
    echo [OK] Arquitectura 32-bit detectada
    set "ARQUITECTURA=32"
)

:: Detectar Python
echo [INFO] Detectando instalación de Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no está instalado o no está en el PATH
    echo [INFO] Por favor instala Python 3.8 o superior desde https://python.org
    echo [INFO] Asegúrate de marcar "Add Python to PATH" durante la instalación
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%i"
echo [OK] Python %PYTHON_VERSION% detectado

:: Detectar ubicación de Python
echo [INFO] Detectando ubicación de Python...
for /f "tokens=*" %%i in ('where python 2^>nul') do set "PYTHON_PATH=%%i"
echo [OK] Python encontrado en: %PYTHON_PATH%

:: Crear directorios necesarios
echo [INFO] Creando estructura de directorios...
if not exist "data" mkdir "data"
if not exist "data\database" mkdir "data\database"
if not exist "static" mkdir "static"
if not exist "static\uploads" mkdir "static\uploads"
if not exist "templates" mkdir "templates"
if not exist "logs" mkdir "logs"
if not exist "CHATMASIVO" mkdir "CHATMASIVO"
if not exist "CHATMASIVO\static" mkdir "CHATMASIVO\static"
if not exist "CHATMASIVO\static\uploads" mkdir "CHATMASIVO\static\uploads"
if not exist "CHATMASIVO\templates" mkdir "CHATMASIVO\templates"
if not exist "CHATMASIVO\data" mkdir "CHATMASIVO\data"
if not exist "CHATMASIVO\data\database" mkdir "CHATMASIVO\data\database"
echo [OK] Directorios creados correctamente

:: Instalar dependencias
echo [INFO] Instalando dependencias del sistema...
echo [INFO] Esto puede tomar unos minutos...
%PYTHON_PATH% -m pip install --upgrade pip
%PYTHON_PATH% -m pip install -r requirements_completo.txt
if %errorlevel% neq 0 (
    echo [ERROR] Error instalando dependencias
    echo [INFO] Intentando con pip3...
    %PYTHON_PATH% -m pip3 install -r requirements_completo.txt
    if %errorlevel% neq 0 (
        echo [ERROR] No se pudieron instalar las dependencias
        echo [INFO] Verifica que tengas conexión a internet
        pause
        exit /b 1
    )
)
echo [OK] Dependencias instaladas correctamente

:: Crear archivos de configuración
echo [INFO] Creando archivos de configuración...

:: Crear base de datos de usuarios
echo [INFO] Configurando base de datos de usuarios...
%PYTHON_PATH% -c "
import sqlite3
import os
os.makedirs('data/database', exist_ok=True)
conn = sqlite3.connect('data/database/users.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        lastname TEXT,
        dni TEXT,
        role TEXT,
        username TEXT,
        password TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()
conn.close()
print('Base de datos de usuarios creada')
"

:: Crear base de datos del chatbot
echo [INFO] Configurando base de datos del chatbot...
%PYTHON_PATH% -c "
import sqlite3
import os
os.makedirs('data/database', exist_ok=True)
conn = sqlite3.connect('data/database/chatbot.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY,
        filename TEXT,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()
conn.close()
print('Base de datos del chatbot creada')
"

:: Crear base de datos de contactos
echo [INFO] Configurando base de datos de contactos...
%PYTHON_PATH% -c "
import sqlite3
import os
os.makedirs('data/database', exist_ok=True)
conn = sqlite3.connect('data/database/contactos.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS contactos (
        id INTEGER PRIMARY KEY,
        nombre TEXT,
        telefono TEXT,
        grupo TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()
conn.close()
print('Base de datos de contactos creada')
"

:: Crear base de conocimientos
echo [INFO] Configurando base de conocimientos...
echo {} > "data\knowledge_base.json"

:: Crear usuarios por defecto
echo [INFO] Creando usuarios por defecto...
%PYTHON_PATH% -c "
import sqlite3
import os

# Crear base de datos de usuarios si no existe
os.makedirs('data/database', exist_ok=True)
conn = sqlite3.connect('data/database/users.db')
cursor = conn.cursor()

# Crear tabla de usuarios
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        lastname TEXT,
        dni TEXT,
        role TEXT,
        username TEXT,
        password TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Verificar si ya existen usuarios
cursor.execute('SELECT COUNT(*) FROM users')
count = cursor.fetchone()[0]

if count == 0:
    # Crear usuario administrador por defecto
    cursor.execute('''
        INSERT INTO users (name, lastname, dni, role, username, password)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        'Administrador',
        'Sistema',
        '00000000',
        'administrativo',
        'admin',
        'admin123'
    ))
    
    # Crear usuario asesor por defecto
    cursor.execute('''
        INSERT INTO users (name, lastname, dni, role, username, password)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        'Juan',
        'Pérez',
        '12345678',
        'asesor',
        'jperez',
        '123456'
    ))
    
    print('Usuarios por defecto creados:')
    print('- admin/admin123 (Administrador)')
    print('- jperez/123456 (Asesor)')
else:
    print('Usuarios ya existen en la base de datos')

conn.commit()
conn.close()
"

:: Crear ejecutable personalizado para esta computadora
echo [INFO] Creando ejecutable personalizado para esta computadora...
echo @echo off > "EJECUTAR_CHATBOT.bat"
echo chcp 65001 ^>nul >> "EJECUTAR_CHATBOT.bat"
echo title Chatbot Inteligente v1.0 >> "EJECUTAR_CHATBOT.bat"
echo. >> "EJECUTAR_CHATBOT.bat"
echo echo ================================================================================ >> "EJECUTAR_CHATBOT.bat"
echo echo                   CHATBOT INTELIGENTE v1.0 >> "EJECUTAR_CHATBOT.bat"
echo echo                   Sistema Unificado con Login y Control de Acceso >> "EJECUTAR_CHATBOT.bat"
echo echo ================================================================================ >> "EJECUTAR_CHATBOT.bat"
echo echo. >> "EJECUTAR_CHATBOT.bat"
echo echo [INFO] Iniciando sistema... >> "EJECUTAR_CHATBOT.bat"
echo echo [INFO] Python: %PYTHON_PATH% >> "EJECUTAR_CHATBOT.bat"
echo echo [INFO] Versión: %PYTHON_VERSION% >> "EJECUTAR_CHATBOT.bat"
echo echo. >> "EJECUTAR_CHATBOT.bat"
echo echo [INFO] Presiona Ctrl+C para detener el servidor >> "EJECUTAR_CHATBOT.bat"
echo echo ================================================================================ >> "EJECUTAR_CHATBOT.bat"
echo echo. >> "EJECUTAR_CHATBOT.bat"
echo "%PYTHON_PATH%" "SISTEMA_UNIFICADO_FINAL.py" >> "EJECUTAR_CHATBOT.bat"
echo pause >> "EJECUTAR_CHATBOT.bat"

:: Crear script de inicio rápido
echo [INFO] Creando script de inicio rápido...
echo @echo off > "INICIAR_SISTEMA.bat"
echo title Chatbot Inteligente v1.0 >> "INICIAR_SISTEMA.bat"
echo echo Iniciando Chatbot Inteligente v1.0... >> "INICIAR_SISTEMA.bat"
echo call "EJECUTAR_CHATBOT.bat" >> "INICIAR_SISTEMA.bat"
echo pause >> "INICIAR_SISTEMA.bat"

:: Crear archivo de información del sistema
echo [INFO] Creando archivo de información del sistema...
echo # INFORMACIÓN DEL SISTEMA - CHATBOT INTELIGENTE v1.0 > "INFO_SISTEMA_LOCAL.txt"
echo. >> "INFO_SISTEMA_LOCAL.txt"
echo **Fecha de instalación:** %DATE% %TIME% >> "INFO_SISTEMA_LOCAL.txt"
echo **Sistema operativo:** %OS% >> "INFO_SISTEMA_LOCAL.txt"
echo **Arquitectura:** %PROCESSOR_ARCHITECTURE% >> "INFO_SISTEMA_LOCAL.txt"
echo **Usuario:** %USERNAME% >> "INFO_SISTEMA_LOCAL.txt"
echo **Directorio:** %CD% >> "INFO_SISTEMA_LOCAL.txt"
echo **Python:** %PYTHON_PATH% >> "INFO_SISTEMA_LOCAL.txt"
echo **Versión Python:** %PYTHON_VERSION% >> "INFO_SISTEMA_LOCAL.txt"
echo. >> "INFO_SISTEMA_LOCAL.txt"
echo **Archivos de inicio:** >> "INFO_SISTEMA_LOCAL.txt"
echo - EJECUTAR_CHATBOT.bat (Ejecutable principal) >> "INFO_SISTEMA_LOCAL.txt"
echo - INICIAR_SISTEMA.bat (Script de inicio rápido) >> "INFO_SISTEMA_LOCAL.txt"
echo. >> "INFO_SISTEMA_LOCAL.txt"
echo **URLs del sistema:** >> "INFO_SISTEMA_LOCAL.txt"
echo - URL Principal: http://localhost:5000 >> "INFO_SISTEMA_LOCAL.txt"
echo - URL Chat Masivo: http://localhost:5001 >> "INFO_SISTEMA_LOCAL.txt"
echo. >> "INFO_SISTEMA_LOCAL.txt"
echo **Usuarios por defecto:** >> "INFO_SISTEMA_LOCAL.txt"
echo - Usuario: admin / Contraseña: admin123 / Rol: Administrativo >> "INFO_SISTEMA_LOCAL.txt"
echo - Usuario: jperez / Contraseña: 123456 / Rol: Asesor >> "INFO_SISTEMA_LOCAL.txt"

:: Mostrar información final
echo.
echo ================================================================================
echo                   INSTALACIÓN COMPLETADA EXITOSAMENTE
echo ================================================================================
echo.
echo [SISTEMA INSTALADO]
echo ✅ Chatbot Inteligente v1.0 instalado correctamente
echo ✅ Dependencias instaladas
echo ✅ Base de datos configurada
echo ✅ Usuarios por defecto creados
echo ✅ Ejecutable personalizado creado
echo ✅ Archivos de configuración creados
echo.
echo [INFORMACIÓN DEL SISTEMA]
echo 🖥️  Sistema operativo: %OS%
echo 🏗️  Arquitectura: %PROCESSOR_ARCHITECTURE%
echo 🐍 Python: %PYTHON_PATH%
echo 📊 Versión Python: %PYTHON_VERSION%
echo 📁 Directorio: %CD%
echo.
echo [USUARIOS POR DEFECTO]
echo 👤 Usuario: admin
echo    Contraseña: admin123
echo    Rol: Administrativo
echo    Acceso: Sistema completo
echo.
echo 👤 Usuario: jperez
echo    Contraseña: 123456
echo    Rol: Asesor
echo    Acceso: Chat Masivo
echo.
echo [ARCHIVOS DE INICIO]
echo 🚀 EJECUTAR_CHATBOT.bat - Ejecutable principal (personalizado para esta PC)
echo 🚀 INICIAR_SISTEMA.bat - Script de inicio rápido
echo 📋 INFO_SISTEMA_LOCAL.txt - Información de esta instalación
echo.
echo [URLS DEL SISTEMA]
echo 🌐 URL Principal: http://localhost:5000
echo 🌐 URL Chat Masivo: http://localhost:5001
echo.
echo [INSTRUCCIONES DE USO]
echo 1. Ejecutar EJECUTAR_CHATBOT.bat o INICIAR_SISTEMA.bat
echo 2. El sistema se abrirá automáticamente en tu navegador
echo 3. Iniciar sesión con las credenciales por defecto
echo 4. El sistema redirigirá automáticamente según tu rol
echo.
echo [NOTAS IMPORTANTES]
echo ⚠️  Este instalador detectó automáticamente tu configuración de Python
echo ⚠️  El ejecutable EJECUTAR_CHATBOT.bat está personalizado para esta computadora
echo ⚠️  Si cambias la ubicación de Python, ejecuta este instalador nuevamente
echo.
echo ================================================================================
echo                   INSTALACIÓN COMPLETADA
echo ================================================================================
echo.
echo [INFO] Presiona cualquier tecla para continuar...
pause >nul
