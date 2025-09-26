#!/usr/bin/env python3
"""
Instalador Automático del Chatbot Inteligente
Descarga e instala todas las dependencias necesarias
"""

import os
import sys
import subprocess
import platform
import urllib.request
import zipfile
import shutil
from pathlib import Path

def print_banner():
    """Muestra el banner del instalador"""
    print("=" * 80)
    print("                    CHATBOT INTELIGENTE - INSTALADOR AUTOMÁTICO")
    print("                    Sistema Completo con Todas las Funcionalidades")
    print("=" * 80)
    print()

def check_python():
    """Verifica que Python esté instalado"""
    print("[INFO] Verificando instalación de Python...")
    
    try:
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print(f"[ERROR] Se requiere Python 3.8 o superior. Versión actual: {version.major}.{version.minor}")
            print("[INFO] Descarga Python desde: https://www.python.org/downloads/")
            return False
        
        print(f"[OK] Python {version.major}.{version.minor}.{version.micro} detectado")
        return True
        
    except Exception as e:
        print(f"[ERROR] No se pudo verificar la versión de Python: {e}")
        return False

def check_pip():
    """Verifica que pip esté disponible"""
    print("[INFO] Verificando pip...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print("[OK] pip está disponible")
        return True
        
    except subprocess.CalledProcessError:
        print("[ERROR] pip no está disponible")
        print("[INFO] Instalando pip...")
        try:
            subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], 
                          check=True)
            print("[OK] pip instalado correctamente")
            return True
        except subprocess.CalledProcessError:
            print("[ERROR] No se pudo instalar pip")
            return False

def upgrade_pip():
    """Actualiza pip a la última versión"""
    print("[INFO] Actualizando pip...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        print("[OK] pip actualizado")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"[WARNING] No se pudo actualizar pip: {e}")
        return False

def install_requirements():
    """Instala las dependencias desde requirements.txt"""
    print("[INFO] Instalando dependencias del chatbot...")
    
    requirements_file = "requirements_completo.txt"
    
    if not os.path.exists(requirements_file):
        print(f"[ERROR] No se encontró el archivo {requirements_file}")
        return False
    
    try:
        # Instalar dependencias una por una para mejor control de errores
        with open(requirements_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                print(f"[INFO] Instalando {line}...")
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", line], 
                                  check=True, capture_output=True)
                    print(f"[OK] {line} instalado")
                except subprocess.CalledProcessError as e:
                    print(f"[WARNING] No se pudo instalar {line}: {e}")
                    # Continuar con las siguientes dependencias
        
        print("[OK] Dependencias instaladas")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error al instalar dependencias: {e}")
        return False

def create_directories():
    """Crea los directorios necesarios"""
    print("[INFO] Creando directorios necesarios...")
    
    directories = [
        "uploads",
        "data",
        "data/database", 
        "templates",
        "static",
        "static/uploads",
        "logs",
        "CHATMASIVO",
        "CHATMASIVO/data",
        "CHATMASIVO/data/csv",
        "CHATMASIVO/data/excel",
        "CHATMASIVO/data/database",
        "CHATMASIVO/logs",
        "CHATMASIVO/static",
        "CHATMASIVO/static/uploads",
        "CHATMASIVO/templates",
        "CHATMASIVO/config",
        "CHATMASIVO/config/twilio",
        "CHATMASIVO/scripts",
        "CHATMASIVO/scripts/installer",
        "CHATMASIVO/scripts/tests",
        "CHATMASIVO/scripts/utilities"
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"[OK] Directorio creado: {directory}")
        except Exception as e:
            print(f"[WARNING] No se pudo crear {directory}: {e}")
    
    print("[OK] Directorios creados")

def create_config_files():
    """Crea archivos de configuración básicos"""
    print("[INFO] Creando archivos de configuración...")
    
    # Archivo .env básico
    env_content = """# Configuración del Chatbot Inteligente
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=sistema_unificado_secret_key_2024

# Configuración de base de datos
DATABASE_URL=sqlite:///data/database/chatbot.db

# Configuración de Twilio (opcional)
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=your_phone_number_here

# Configuración de OpenAI (opcional)
OPENAI_API_KEY=your_openai_api_key_here
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("[OK] Archivo .env creado")
    except Exception as e:
        print(f"[WARNING] No se pudo crear .env: {e}")
    
    # Archivo de configuración de la aplicación
    config_content = """# Configuración de la aplicación
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 16777216  # 16MB
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'pptx', 'xlsx', 'xls', 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'}

# Configuración de logging
LOG_LEVEL = 'INFO'
LOG_FILE = 'sistema_unificado.log'

# Configuración de puertos
CHATBOT_PORT = 5000
CHAT_MASIVO_PORT = 5001
"""
    
    try:
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(config_content)
        print("[OK] Archivo config.py creado")
    except Exception as e:
        print(f"[WARNING] No se pudo crear config.py: {e}")

def test_installation():
    """Prueba que la instalación funcione correctamente"""
    print("[INFO] Probando instalación...")
    
    try:
        # Probar importaciones principales
        import flask
        import PyPDF2
        import requests
        import sqlite3
        print("[OK] Importaciones principales funcionando")
        
        # Probar creación de base de datos
        conn = sqlite3.connect('data/database/test.db')
        conn.close()
        print("[OK] Base de datos SQLite funcionando")
        
        # Limpiar archivo de prueba
        os.remove('data/database/test.db')
        
        print("[OK] Instalación verificada correctamente")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error en la verificación: {e}")
        return False

def main():
    """Función principal del instalador"""
    print_banner()
    
    print("[INFO] Iniciando instalación del Chatbot Inteligente...")
    print()
    
    # Verificar Python
    if not check_python():
        print("[ERROR] Instalación cancelada - Python no compatible")
        input("Presiona Enter para salir...")
        return False
    
    # Verificar pip
    if not check_pip():
        print("[ERROR] Instalación cancelada - pip no disponible")
        input("Presiona Enter para salir...")
        return False
    
    # Actualizar pip
    upgrade_pip()
    
    # Crear directorios
    create_directories()
    
    # Crear archivos de configuración
    create_config_files()
    
    # Instalar dependencias
    if not install_requirements():
        print("[WARNING] Algunas dependencias no se pudieron instalar")
        print("[INFO] Puedes instalarlas manualmente más tarde")
    
    # Probar instalación
    if test_installation():
        print()
        print("=" * 80)
        print("                    ¡INSTALACIÓN COMPLETADA EXITOSAMENTE!")
        print("=" * 80)
        print()
        print("[INFO] El Chatbot Inteligente está listo para usar")
        print("[INFO] Ejecuta 'EJECUTAR_CHATBOT_FINAL.bat' para iniciar")
        print("[INFO] O ejecuta 'python SISTEMA_UNIFICADO_FINAL.py' directamente")
        print()
        print("[FUNCIONALIDADES DISPONIBLES:]")
        print("- Chat inteligente con IA")
        print("- Carga de documentos (PDF, Word, Excel, PowerPoint)")
        print("- Extracción de contenido web")
        print("- Chat masivo por WhatsApp")
        print("- Interfaz web moderna y responsive")
        print()
    else:
        print()
        print("=" * 80)
        print("                    INSTALACIÓN COMPLETADA CON ADVERTENCIAS")
        print("=" * 80)
        print()
        print("[WARNING] Algunos componentes pueden no funcionar correctamente")
        print("[INFO] Revisa los mensajes de error anteriores")
        print()
    
    input("Presiona Enter para continuar...")
    return True

if __name__ == "__main__":
    main()
