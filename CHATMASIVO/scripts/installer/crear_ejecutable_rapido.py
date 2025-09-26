#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script rápido para crear ejecutable del Chat Masivo
Versión simplificada y optimizada
"""

import os
import sys
import subprocess
import shutil

def crear_ejecutable_rapido():
    """Crear ejecutable de forma rápida y simple"""
    print("🚀 CREANDO EJECUTABLE RÁPIDO - CHAT MASIVO")
    print("=" * 50)
    
    # Verificar archivo principal
    archivo_principal = "app/codchat.py"
    if not os.path.exists(archivo_principal):
        print("❌ No se encontró app/codchat.py")
        return False
    
    print(f"✅ Archivo principal encontrado: {archivo_principal}")
    
    # Comando PyInstaller simplificado
    comando = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--windowed',
        '--name=ChatMasivo',
        '--clean',
        '--noconfirm',
        archivo_principal
    ]
    
    print("\n🔨 Ejecutando PyInstaller...")
    print(f"Comando: {' '.join(comando)}")
    
    try:
        # Ejecutar PyInstaller
        resultado = subprocess.run(comando, check=True, capture_output=True, text=True)
        print("✅ PyInstaller ejecutado exitosamente")
        
        # Verificar que se creó el ejecutable
        ejecutable_path = "dist/ChatMasivo.exe"
        if os.path.exists(ejecutable_path):
            print(f"✅ Ejecutable creado: {ejecutable_path}")
            
            # Crear carpeta portable
            crear_carpeta_portable()
            return True
        else:
            print("❌ No se encontró el ejecutable en dist/")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando PyInstaller: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def crear_carpeta_portable():
    """Crear carpeta portable con el ejecutable"""
    print("\n📁 Creando carpeta portable...")
    
    carpeta_portable = "ChatMasivo_Portable"
    
    # Limpiar carpeta anterior si existe
    if os.path.exists(carpeta_portable):
        shutil.rmtree(carpeta_portable)
    
    os.makedirs(carpeta_portable)
    
    # Copiar ejecutable
    shutil.copy2("dist/ChatMasivo.exe", carpeta_portable)
    print("✅ Ejecutable copiado")
    
    # Copiar archivos necesarios
    archivos_copiar = [
        ("templates/", "templates/"),
        ("static/", "static/"),
        ("config/", "config/"),
        ("Twilio.env", "Twilio.env"),
        ("Twilio.env.example", "Twilio.env.example")
    ]
    
    for origen, destino in archivos_copiar:
        if os.path.exists(origen):
            destino_path = os.path.join(carpeta_portable, destino)
            if origen.endswith('/'):
                shutil.copytree(origen, destino_path)
            else:
                shutil.copy2(origen, destino_path)
            print(f"✅ {origen} -> {destino}")
    
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
    
    with open(os.path.join(carpeta_portable, "CONFIGURACION_INICIAL.txt"), 'w', encoding='utf-8') as f:
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
    
    with open(os.path.join(carpeta_portable, "README.txt"), 'w', encoding='utf-8') as f:
        f.write(readme_text)
    
    print(f"✅ Carpeta portable creada: {carpeta_portable}/")
    print(f"📁 Tamaño total: {obtener_tamaño_carpeta(carpeta_portable):.1f} MB")

def obtener_tamaño_carpeta(carpeta):
    """Obtener tamaño total de una carpeta en MB"""
    total = 0
    for dirpath, dirnames, filenames in os.walk(carpeta):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):
                total += os.path.getsize(filepath)
    return total / (1024 * 1024)  # Convertir a MB

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
    try:
        # Crear ejecutable
        if crear_ejecutable_rapido():
            print("\n🎉 ¡EJECUTABLE CREADO EXITOSAMENTE!")
            print("=" * 50)
            print("📁 Ubicación: ChatMasivo_Portable/")
            print("\n📋 INSTRUCCIONES:")
            print("1. Copia la carpeta 'ChatMasivo_Portable' a cualquier computadora")
            print("2. Configura 'Twilio.env' con tus credenciales")
            print("3. Ejecuta 'ChatMasivo.exe'")
            print("4. Abre http://localhost:5000 en tu navegador")
            
            # Preguntar si limpiar
            respuesta = input("\n¿Limpiar archivos temporales? (s/n): ").lower()
            if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
                limpiar_archivos_temporales()
        else:
            print("\n❌ Error creando ejecutable")
            
    except KeyboardInterrupt:
        print("\n\n❌ Proceso cancelado por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
