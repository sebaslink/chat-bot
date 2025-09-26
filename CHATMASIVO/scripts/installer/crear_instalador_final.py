#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script final para crear instalador.exe del Chat Masivo
Versión optimizada y simplificada
"""

import os
import sys
import subprocess
import shutil
import time

def verificar_archivos():
    """Verificar que todos los archivos necesarios estén presentes"""
    print("🔍 Verificando archivos necesarios...")
    
    archivos_requeridos = [
        "main.py",
        "app/codchat.py",
        "templates/",
        "static/",
        "config/",
        "data/database/",
        "requirements.txt"
    ]
    
    faltantes = []
    for archivo in archivos_requeridos:
        if not os.path.exists(archivo):
            faltantes.append(archivo)
            print(f"  ❌ {archivo}")
        else:
            print(f"  ✅ {archivo}")
    
    if faltantes:
        print(f"\n⚠️  Archivos faltantes: {faltantes}")
        return False
    
    print("✅ Todos los archivos necesarios encontrados")
    return True

def instalar_dependencias():
    """Instalar dependencias necesarias"""
    print("\n📦 Verificando dependencias...")
    
    dependencias = ['pyinstaller']
    
    for dep in dependencias:
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'show', dep], 
                          check=True, capture_output=True)
            print(f"  ✅ {dep}")
        except subprocess.CalledProcessError:
            print(f"  📦 Instalando {dep}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', dep], 
                          check=True)
            print(f"  ✅ {dep} instalado")

def crear_ejecutable():
    """Crear ejecutable con PyInstaller"""
    print("\n🔨 Creando ejecutable...")
    
    # Usar main.py como archivo principal
    archivo_principal = "main.py"
    
    # Comando PyInstaller optimizado
    comando = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--windowed',
        '--name=ChatMasivo',
        '--clean',
        '--noconfirm',
        '--add-data=templates;templates',
        '--add-data=static;static',
        '--add-data=config;config',
        '--add-data=data;data',
        '--add-data=app;app',
        '--hidden-import=flask',
        '--hidden-import=twilio',
        '--hidden-import=pandas',
        '--hidden-import=openpyxl',
        '--hidden-import=sqlite3',
        '--hidden-import=werkzeug',
        '--hidden-import=dotenv',
        '--hidden-import=requests',
        '--hidden-import=beautifulsoup4',
        archivo_principal
    ]
    
    print(f"Ejecutando: {' '.join(comando)}")
    
    try:
        # Ejecutar con timeout
        resultado = subprocess.run(comando, timeout=600, check=True)
        print("✅ Ejecutable creado exitosamente")
        return True
    except subprocess.TimeoutExpired:
        print("❌ Timeout: El proceso tardó más de 10 minutos")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creando ejecutable: {e}")
        return False

def crear_carpeta_portable():
    """Crear carpeta portable con todos los archivos"""
    print("\n📁 Creando carpeta portable...")
    
    carpeta = "ChatMasivo_Portable"
    
    # Limpiar carpeta anterior
    if os.path.exists(carpeta):
        shutil.rmtree(carpeta)
    
    os.makedirs(carpeta)
    
    # Copiar ejecutable
    if os.path.exists("dist/ChatMasivo.exe"):
        shutil.copy2("dist/ChatMasivo.exe", carpeta)
        print("✅ Ejecutable copiado")
    else:
        print("❌ No se encontró el ejecutable")
        return False
    
    # Copiar archivos necesarios
    archivos_copiar = [
        ("templates/", "templates/"),
        ("static/", "static/"),
        ("config/", "config/"),
        ("data/", "data/"),
        ("app/", "app/"),
        ("requirements.txt", "requirements.txt")
    ]
    
    # Copiar archivos Twilio.env de diferentes ubicaciones
    twilio_files = [
        "Twilio.env",
        "config/twilio/Twilio.env",
        "config/twilio.env",
        "config/twilio/Twilio.env.example"
    ]
    
    twilio_copied = False
    for twilio_file in twilio_files:
        if os.path.exists(twilio_file):
            shutil.copy2(twilio_file, os.path.join(carpeta, "Twilio.env"))
            print(f"✅ {twilio_file} -> Twilio.env")
            twilio_copied = True
            break
    
    if not twilio_copied:
        # Crear Twilio.env de ejemplo si no existe
        crear_twilio_env_ejemplo(carpeta)
    
    for origen, destino in archivos_copiar:
        if os.path.exists(origen):
            destino_path = os.path.join(carpeta, destino)
            if origen.endswith('/'):
                shutil.copytree(origen, destino_path)
            else:
                shutil.copy2(origen, destino_path)
            print(f"✅ {origen} -> {destino}")
    
    # Crear archivos de configuración
    crear_archivos_configuracion(carpeta)
    
    print(f"✅ Carpeta portable creada: {carpeta}/")
    return True

def crear_archivos_configuracion(carpeta):
    """Crear archivos de configuración y documentación"""
    
    # Archivo de configuración inicial
    config_text = """# CONFIGURACIÓN INICIAL - CHAT MASIVO
# ===============================================

# IMPORTANTE: Edita este archivo con tus credenciales de Twilio
# antes de ejecutar ChatMasivo.exe

# Credenciales de Twilio (OBLIGATORIO)
TWILIO_ACCOUNT_SID=tu_account_sid_aqui
TWILIO_AUTH_TOKEN=tu_auth_token_aqui
TWILIO_WHATSAPP_FROM=+15005550009

# Número de prueba (opcional)
NUMERO_PRUEBA=+15005550009

# Clave secreta de Flask (opcional)
FLASK_SECRET_KEY=tu_clave_secreta_aqui

# INSTRUCCIONES:
# 1. Renombra este archivo a "Twilio.env"
# 2. Reemplaza los valores de ejemplo con tus credenciales reales
# 3. Ejecuta ChatMasivo.exe
# 4. Abre tu navegador en http://localhost:5000
"""
    
    with open(os.path.join(carpeta, "CONFIGURACION_INICIAL.txt"), 'w', encoding='utf-8') as f:
        f.write(config_text)
    
    # README
    readme_text = """# CHAT MASIVO - VERSIÓN PORTABLE
=====================================

## INSTRUCCIONES DE USO

1. **Configuración inicial:**
   - Edita el archivo "CONFIGURACION_INICIAL.txt"
   - Renómbralo a "Twilio.env"
   - Agrega tus credenciales de Twilio

2. **Ejecutar la aplicación:**
   - Haz doble clic en "ChatMasivo.exe"
   - Espera a que se abra la ventana del navegador
   - Si no se abre automáticamente, ve a: http://localhost:5000

3. **Funcionalidades:**
   - Agregar contactos manualmente
   - Importar contactos desde Excel
   - Enviar mensajes masivos por WhatsApp
   - Gestionar grupos de contactos
   - Ver estadísticas de envíos

## REQUISITOS DEL SISTEMA

- Windows 7 o superior
- Conexión a internet
- Cuenta de Twilio activa

## VERSIÓN

Versión 1.0 - Chat Masivo WhatsApp
"""
    
    with open(os.path.join(carpeta, "README.txt"), 'w', encoding='utf-8') as f:
        f.write(readme_text)
    
    # Archivo de inicio rápido
    inicio_text = """@echo off
title Chat Masivo WhatsApp
echo Iniciando Chat Masivo...
echo.
echo Si no se abre automáticamente, ve a: http://localhost:5000
echo.
ChatMasivo.exe
pause
"""
    
    with open(os.path.join(carpeta, "INICIAR_CHAT_MASIVO.bat"), 'w', encoding='utf-8') as f:
        f.write(inicio_text)
    
    print("✅ Archivos de configuración creados")

def crear_twilio_env_ejemplo(carpeta):
    """Crear archivo Twilio.env de ejemplo"""
    twilio_content = """# CONFIGURACIÓN TWILIO - CHAT MASIVO
# ===============================================

# IMPORTANTE: Edita este archivo con tus credenciales de Twilio
# antes de ejecutar ChatMasivo.exe

# Credenciales de Twilio (OBLIGATORIO)
TWILIO_ACCOUNT_SID=tu_account_sid_aqui
TWILIO_AUTH_TOKEN=tu_auth_token_aqui
TWILIO_WHATSAPP_FROM=+15005550009

# Número de prueba (opcional)
NUMERO_PRUEBA=+15005550009

# Clave secreta de Flask (opcional)
FLASK_SECRET_KEY=tu_clave_secreta_aqui

# INSTRUCCIONES:
# 1. Reemplaza los valores de ejemplo con tus credenciales reales
# 2. Ejecuta ChatMasivo.exe
# 3. Abre tu navegador en http://localhost:5000
"""
    
    twilio_path = os.path.join(carpeta, "Twilio.env")
    with open(twilio_path, 'w', encoding='utf-8') as f:
        f.write(twilio_content)
    
    print("✅ Twilio.env de ejemplo creado")

def limpiar_archivos_temporales():
    """Limpiar archivos temporales"""
    print("\n🧹 Limpiando archivos temporales...")
    
    directorios = ["build", "dist", "__pycache__"]
    archivos = ["ChatMasivo.spec"]
    
    for directorio in directorios:
        if os.path.exists(directorio):
            shutil.rmtree(directorio)
            print(f"✅ Eliminado: {directorio}")
    
    for archivo in archivos:
        if os.path.exists(archivo):
            os.remove(archivo)
            print(f"✅ Eliminado: {archivo}")

def main():
    """Función principal"""
    print("CREADOR DE INSTALADOR FINAL - CHAT MASIVO")
    print("=" * 55)
    
    try:
        # Verificar archivos
        if not verificar_archivos():
            print("\n❌ Faltan archivos necesarios. Revisa los errores arriba.")
            return False
        
        # Instalar dependencias
        instalar_dependencias()
        
        # Crear ejecutable
        if not crear_ejecutable():
            print("\n❌ Error creando ejecutable")
            return False
        
        # Crear carpeta portable
        if not crear_carpeta_portable():
            print("\n❌ Error creando carpeta portable")
            return False
        
        print("\n🎉 ¡INSTALADOR CREADO EXITOSAMENTE!")
        print("=" * 55)
        print("📁 Ubicación: ChatMasivo_Portable/")
        print("\n📋 INSTRUCCIONES:")
        print("1. Copia la carpeta 'ChatMasivo_Portable' a cualquier computadora")
        print("2. Configura 'Twilio.env' con tus credenciales")
        print("3. Ejecuta 'ChatMasivo.exe' o 'INICIAR_CHAT_MASIVO.bat'")
        print("4. Abre http://localhost:5000 en tu navegador")
        
        # Preguntar si limpiar
        respuesta = input("\n¿Limpiar archivos temporales? (s/n): ").lower()
        if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
            limpiar_archivos_temporales()
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n❌ Proceso cancelado por el usuario")
        return False
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
