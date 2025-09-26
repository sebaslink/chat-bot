#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple para crear solo el ejecutable .exe del Chat Masivo
Sin instalador, solo el archivo ejecutable
"""

import os
import sys
import subprocess
import shutil

def instalar_pyinstaller():
    """Instalar PyInstaller si no está disponible"""
    print("🔍 Verificando PyInstaller...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'show', 'pyinstaller'], 
                      check=True, capture_output=True)
        print("✅ PyInstaller ya está instalado")
        return True
    except subprocess.CalledProcessError:
        print("📦 Instalando PyInstaller...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], 
                          check=True)
            print("✅ PyInstaller instalado exitosamente")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando PyInstaller: {e}")
            return False

def crear_ejecutable():
    """Crear ejecutable con PyInstaller"""
    print("\n🔨 Creando ejecutable...")
    
    # Buscar archivo principal
    archivo_principal = None
    posibles_rutas = [
        "app/codchat.py",
        "codigo/codchat.py",
        "codchat.py"
    ]
    
    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            archivo_principal = ruta
            break
    
    if not archivo_principal:
        print("❌ No se encontró el archivo principal codchat.py")
        return False
    
    print(f"📄 Usando archivo principal: {archivo_principal}")
    
    # Comando PyInstaller
    comando = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',  # Un solo archivo
        '--windowed',  # Sin consola
        '--name=ChatMasivo',
        '--clean',  # Limpiar cache
    ]
    
    # Agregar icono si existe
    if os.path.exists('imagen/icono.jpg'):
        comando.extend(['--icon=imagen/icono.jpg'])
        print("🎨 Icono encontrado y agregado")
    
    # Agregar archivos de datos
    if os.path.exists('templates'):
        comando.extend(['--add-data=templates;templates'])
        print("📁 Templates agregados")
    
    if os.path.exists('static'):
        comando.extend(['--add-data=static;static'])
        print("📁 Static agregado")
    
    if os.path.exists('config'):
        comando.extend(['--add-data=config;config'])
        print("📁 Config agregado")
    
    # Archivos de configuración
    if os.path.exists('Twilio.env'):
        comando.extend(['--add-data=Twilio.env;.'])
        print("📄 Twilio.env agregado")
    
    if os.path.exists('Twilio.env.example'):
        comando.extend(['--add-data=Twilio.env.example;.'])
        print("📄 Twilio.env.example agregado")
    
    # Imports ocultos
    imports_ocultos = [
        'flask', 'twilio', 'pandas', 'openpyxl', 'sqlite3',
        'werkzeug', 'dotenv', 'csv', 'io', 'base64', 'random',
        'datetime', 'logging', 'os', 'sys'
    ]
    
    for imp in imports_ocultos:
        comando.extend([f'--hidden-import={imp}'])
    
    # Archivo principal
    comando.append(archivo_principal)
    
    print(f"\n🚀 Ejecutando: {' '.join(comando)}")
    
    try:
        subprocess.run(comando, check=True)
        print("\n✅ Ejecutable creado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error creando ejecutable: {e}")
        return False

def crear_estructura_portable():
    """Crear estructura portable para el ejecutable"""
    print("\n📁 Creando estructura portable...")
    
    dir_portable = "ChatMasivo_Portable"
    if os.path.exists(dir_portable):
        shutil.rmtree(dir_portable)
    os.makedirs(dir_portable)
    
    # Copiar ejecutable
    if os.path.exists("dist/ChatMasivo.exe"):
        shutil.copy2("dist/ChatMasivo.exe", dir_portable)
        print("✅ Ejecutable copiado")
    else:
        print("❌ No se encontró el ejecutable")
        return False
    
    # Copiar archivos necesarios
    archivos_copiar = [
        ("templates/", "templates/"),
        ("static/", "static/"),
        ("config/", "config/"),
        ("Twilio.env", "Twilio.env"),
        ("Twilio.env.example", "Twilio.env.example"),
        ("requirements.txt", "requirements.txt")
    ]
    
    for origen, destino in archivos_copiar:
        if os.path.exists(origen):
            destino_path = os.path.join(dir_portable, destino)
            if origen.endswith('/'):
                shutil.copytree(origen, destino_path)
            else:
                shutil.copy2(origen, destino_path)
            print(f"  ✓ {origen} -> {destino}")
    
    # Crear archivo de configuración
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
    
    with open(os.path.join(dir_portable, "CONFIGURACION_INICIAL.txt"), 'w', encoding='utf-8') as f:
        f.write(config_text)
    
    # Crear README
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

## SOPORTE

Para soporte técnico, contacta al desarrollador.

## VERSIÓN

Versión 1.0 - Chat Masivo WhatsApp
"""
    
    with open(os.path.join(dir_portable, "README.txt"), 'w', encoding='utf-8') as f:
        f.write(readme_text)
    
    print(f"✅ Estructura portable creada en: {dir_portable}")
    return dir_portable

def limpiar_archivos():
    """Limpiar archivos temporales"""
    print("\n🧹 Limpiando archivos temporales...")
    
    directorios = ["build", "dist", "__pycache__"]
    archivos = ["ChatMasivo.spec"]
    
    for directorio in directorios:
        if os.path.exists(directorio):
            shutil.rmtree(directorio)
            print(f"  ✓ Eliminado: {directorio}")
    
    for archivo in archivos:
        if os.path.exists(archivo):
            os.remove(archivo)
            print(f"  ✓ Eliminado: {archivo}")

def main():
    """Función principal"""
    print("🚀 CREADOR DE EJECUTABLE - CHAT MASIVO")
    print("=" * 45)
    
    # Instalar PyInstaller
    if not instalar_pyinstaller():
        return False
    
    # Crear ejecutable
    if not crear_ejecutable():
        return False
    
    # Crear estructura portable
    dir_portable = crear_estructura_portable()
    if not dir_portable:
        return False
    
    print("\n🎉 ¡EJECUTABLE CREADO EXITOSAMENTE!")
    print("=" * 45)
    print(f"📁 Ubicación: {dir_portable}/")
    print("\n📋 INSTRUCCIONES:")
    print("1. Copia la carpeta completa a cualquier computadora")
    print("2. Configura Twilio.env con tus credenciales")
    print("3. Ejecuta ChatMasivo.exe")
    print("4. Abre http://localhost:5000 en tu navegador")
    
    # Preguntar si limpiar
    respuesta = input("\n¿Limpiar archivos temporales? (s/n): ").lower()
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        limpiar_archivos()
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Proceso cancelado por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
