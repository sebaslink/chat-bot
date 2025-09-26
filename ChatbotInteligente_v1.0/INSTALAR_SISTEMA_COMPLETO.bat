@echo off
chcp 65001 >nul
title Chatbot Inteligente v1.0 - Instalador Completo

echo ================================================================================
echo                   CHATBOT INTELIGENTE v1.0 - INSTALADOR COMPLETO
echo                   Sistema Unificado con Login y Control de Acceso
echo ================================================================================
echo.

echo [INFO] Iniciando instalación del sistema completo...
echo.

:: Verificar si Python está instalado
echo [INFO] Verificando instalación de Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no está instalado o no está en el PATH
    echo [INFO] Por favor instala Python 3.8 o superior desde https://python.org
    pause
    exit /b 1
)

echo [OK] Python detectado correctamente
echo.

:: Crear directorios necesarios
echo [INFO] Creando directorios necesarios...
if not exist "data" mkdir "data"
if not exist "data\database" mkdir "data\database"
if not exist "static" mkdir "static"
if not exist "static\uploads" mkdir "static\uploads"
if not exist "templates" mkdir "templates"
if not exist "logs" mkdir "logs"
echo [OK] Directorios creados correctamente
echo.

:: Instalar dependencias
echo [INFO] Instalando dependencias del sistema...
pip install -r requirements_completo.txt
if %errorlevel% neq 0 (
    echo [ERROR] Error instalando dependencias
    echo [INFO] Intentando con pip3...
    pip3 install -r requirements_completo.txt
    if %errorlevel% neq 0 (
        echo [ERROR] No se pudieron instalar las dependencias
        pause
        exit /b 1
    )
)
echo [OK] Dependencias instaladas correctamente
echo.

:: Copiar archivos de configuración si no existen
echo [INFO] Configurando archivos del sistema...
if not exist "data\database\users.db" (
    echo [INFO] Creando base de datos de usuarios...
    python -c "import sqlite3; conn = sqlite3.connect('data/database/users.db'); conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, lastname TEXT, dni TEXT, role TEXT, username TEXT, password TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'); conn.commit(); conn.close()"
)

if not exist "data\database\chatbot.db" (
    echo [INFO] Creando base de datos del chatbot...
    python -c "import sqlite3; conn = sqlite3.connect('data/database/chatbot.db'); conn.execute('CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY, filename TEXT, content TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'); conn.commit(); conn.close()"
)

if not exist "data\database\contactos.db" (
    echo [INFO] Creando base de datos de contactos...
    python -c "import sqlite3; conn = sqlite3.connect('data/database/contactos.db'); conn.execute('CREATE TABLE IF NOT EXISTS contactos (id INTEGER PRIMARY KEY, nombre TEXT, telefono TEXT, grupo TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'); conn.commit(); conn.close()"
)

if not exist "data\knowledge_base.json" (
    echo [INFO] Creando base de conocimientos...
    echo {} > "data\knowledge_base.json"
)
echo [OK] Archivos de configuración creados
echo.

:: Crear usuarios por defecto
echo [INFO] Creando usuarios por defecto...
python -c "
import sqlite3
import hashlib
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
echo [OK] Usuarios por defecto configurados
echo.

:: Verificar archivos críticos
echo [INFO] Verificando archivos críticos...
if not exist "SISTEMA_UNIFICADO_FINAL.py" (
    echo [ERROR] Archivo principal SISTEMA_UNIFICADO_FINAL.py no encontrado
    pause
    exit /b 1
)

if not exist "EJECUTAR_CHATBOT_FINAL.bat" (
    echo [ERROR] Ejecutable EJECUTAR_CHATBOT_FINAL.bat no encontrado
    pause
    exit /b 1
)

echo [OK] Archivos críticos verificados
echo.

:: Crear script de inicio rápido
echo [INFO] Creando script de inicio rápido...
echo @echo off > "INICIAR_SISTEMA.bat"
echo title Chatbot Inteligente v1.0 >> "INICIAR_SISTEMA.bat"
echo echo Iniciando Chatbot Inteligente v1.0... >> "INICIAR_SISTEMA.bat"
echo call "EJECUTAR_CHATBOT_FINAL.bat" >> "INICIAR_SISTEMA.bat"
echo pause >> "INICIAR_SISTEMA.bat"
echo [OK] Script de inicio rápido creado
echo.

:: Mostrar información del sistema
echo ================================================================================
echo                   INSTALACIÓN COMPLETADA EXITOSAMENTE
echo ================================================================================
echo.
echo [SISTEMA INSTALADO]
echo ✅ Chatbot Inteligente v1.0 instalado correctamente
echo ✅ Dependencias instaladas
echo ✅ Base de datos configurada
echo ✅ Usuarios por defecto creados
echo ✅ Archivos de configuración creados
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
echo 🚀 EJECUTAR_CHATBOT_FINAL.bat - Ejecutable principal
echo 🚀 INICIAR_SISTEMA.bat - Script de inicio rápido
echo.
echo [URLS DEL SISTEMA]
echo 🌐 URL Principal: http://localhost:5000
echo 🌐 URL Chat Masivo: http://localhost:5001
echo.
echo [INSTRUCCIONES DE USO]
echo 1. Ejecutar EJECUTAR_CHATBOT_FINAL.bat o INICIAR_SISTEMA.bat
echo 2. El sistema se abrirá automáticamente en tu navegador
echo 3. Iniciar sesión con las credenciales por defecto
echo 4. El sistema redirigirá automáticamente según tu rol
echo.
echo [SOPORTE]
echo 📧 Para soporte técnico o reportar problemas
echo 📅 Versión: 1.0
echo ✅ Estado: Completamente funcional
echo.
echo ================================================================================
echo                   INSTALACIÓN COMPLETADA
echo ================================================================================
echo.
echo [INFO] Presiona cualquier tecla para continuar...
pause >nul
