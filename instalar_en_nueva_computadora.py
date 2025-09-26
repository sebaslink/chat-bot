#!/usr/bin/env python3
"""
Script de instalación completa para nueva computadora
Incluye configuración automática de credenciales
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def verificar_python():
    """Verificar versión de Python"""
    print("🐍 Verificando Python...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def instalar_dependencias():
    """Instalar dependencias de Python"""
    print("\n📦 Instalando dependencias...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def crear_directorios():
    """Crear directorios necesarios"""
    print("\n📁 Creando directorios...")
    directorios = [
        "data/database",
        "static/uploads",
        "uploads",
        "logs",
        "CHATMASIVO/config/twilio",
        "CHATMASIVO/config/app"
    ]
    
    for directorio in directorios:
        os.makedirs(directorio, exist_ok=True)
        print(f"   ✅ {directorio}")
    
    return True

def configurar_credenciales():
    """Configurar credenciales de Twilio"""
    print("\n🔧 Configuración de Credenciales de Twilio")
    print("=" * 50)
    
    print("\n📋 Necesitarás las siguientes credenciales de Twilio:")
    print("   1. Account SID (comienza con 'AC...')")
    print("   2. Auth Token (32 caracteres)")
    print("   3. Número de WhatsApp (formato: +1234567890)")
    print("\n   Puedes obtenerlas en: https://console.twilio.com/")
    print("   Ve a: Account > API keys & tokens")
    
    respuesta = input("\n¿Tienes las credenciales listas? (s/n): ").lower()
    if respuesta != 's':
        print("⚠️  Puedes configurar las credenciales más tarde ejecutando:")
        print("   python configurar_credenciales.py")
        print("\n💡 El sistema funcionará en modo DEMO sin credenciales")
        return True
    
    # Ejecutar script de configuración
    try:
        print("\n🚀 Ejecutando configurador de credenciales...")
        result = subprocess.run([sys.executable, "configurar_credenciales.py"], 
                              capture_output=False, text=True)
        if result.returncode == 0:
            print("✅ Credenciales configuradas correctamente")
            return True
        else:
            print("❌ Error en configuración de credenciales")
            return False
    except Exception as e:
        print(f"❌ Error ejecutando configurador: {e}")
        print("💡 Puedes configurar las credenciales manualmente más tarde")
        return True

def crear_script_ejecucion():
    """Crear script de ejecución para la nueva computadora"""
    print("\n🚀 Creando script de ejecución...")
    
    if platform.system() == "Windows":
        script_content = """@echo off
echo ========================================
echo   CHAT MASIVO WHATSAPP - SISTEMA UNIFICADO
echo ========================================
echo.
echo Iniciando sistema...
python SISTEMA_UNIFICADO_FINAL.py
pause
"""
        with open("EJECUTAR_CHATBOT.bat", "w", encoding="utf-8") as f:
            f.write(script_content)
        print("   ✅ EJECUTAR_CHATBOT.bat creado")
    else:
        script_content = """#!/bin/bash
echo "========================================"
echo "  CHAT MASIVO WHATSAPP - SISTEMA UNIFICADO"
echo "========================================"
echo ""
echo "Iniciando sistema..."
python3 SISTEMA_UNIFICADO_FINAL.py
"""
        with open("ejecutar_chatbot.sh", "w", encoding="utf-8") as f:
            f.write(script_content)
        os.chmod("ejecutar_chatbot.sh", 0o755)
        print("   ✅ ejecutar_chatbot.sh creado")

def limpiar_archivos_duplicados():
    """Limpiar archivos duplicados que puedan generar conflictos"""
    print("\n🧹 Limpiando archivos duplicados...")
    
    archivos_duplicados = [
        "CHATMASIVO/config/twilio.env",
        "ChatbotInteligente_v1.0/CHATMASIVO/config/twilio.env",
        "railway_deploy/CHATMASIVO/config/twilio.env"
    ]
    
    for archivo in archivos_duplicados:
        if os.path.exists(archivo):
            try:
                os.remove(archivo)
                print(f"   🗑️  Eliminado: {archivo}")
            except Exception as e:
                print(f"   ⚠️  No se pudo eliminar {archivo}: {e}")
    
    print("   ✅ Limpieza completada")

def verificar_instalacion():
    """Verificar que la instalación sea correcta"""
    print("\n🔍 Verificando instalación...")
    
    # Verificar archivos principales
    archivos_requeridos = [
        "SISTEMA_UNIFICADO_FINAL.py",
        "requirements.txt",
        "configurar_credenciales.py"
    ]
    
    for archivo in archivos_requeridos:
        if not os.path.exists(archivo):
            print(f"❌ Archivo requerido no encontrado: {archivo}")
            return False
        print(f"   ✅ {archivo}")
    
    # Verificar directorios
    directorios_requeridos = [
        "CHATMASIVO",
        "templates",
        "static"
    ]
    
    for directorio in directorios_requeridos:
        if not os.path.exists(directorio):
            print(f"❌ Directorio requerido no encontrado: {directorio}")
            return False
        print(f"   ✅ {directorio}")
    
    # Verificar archivos de configuración
    archivos_config = [
        "CHATMASIVO/config/twilio/Twilio.env.example",
        "CHATMASIVO/config/app/Twilio.env.example"
    ]
    
    for archivo in archivos_config:
        if os.path.exists(archivo):
            print(f"   ✅ {archivo}")
        else:
            print(f"   ⚠️  {archivo} - No encontrado (opcional)")
    
    print("✅ Instalación verificada correctamente")
    return True

def mostrar_instrucciones_finales():
    """Mostrar instrucciones finales"""
    print("\n" + "=" * 60)
    print("🎉 ¡INSTALACIÓN COMPLETADA!")
    print("=" * 60)
    
    print("\n📋 Para usar el sistema:")
    if platform.system() == "Windows":
        print("   1. Doble clic en: EJECUTAR_CHATBOT.bat")
        print("   2. O ejecuta: python SISTEMA_UNIFICADO_FINAL.py")
    else:
        print("   1. Ejecuta: ./ejecutar_chatbot.sh")
        print("   2. O ejecuta: python3 SISTEMA_UNIFICADO_FINAL.py")
    
    print("   3. Abre tu navegador en: http://localhost:5000")
    
    print("\n🔧 Si necesitas configurar credenciales:")
    print("   python configurar_credenciales.py")
    
    print("\n📚 Documentación disponible en:")
    print("   - README_GITLAB.md")
    print("   - CHATMASIVO/docs/")
    
    print("\n🆘 Soporte:")
    print("   - Revisa los logs en: chatmasivo.log")
    print("   - Consulta la documentación")
    
    print("\n⚠️  IMPORTANTE:")
    print("   - Mantén las credenciales de Twilio seguras")
    print("   - No compartas archivos .env")
    print("   - El sistema funciona en modo demo sin credenciales")

def main():
    """Función principal de instalación"""
    print("🤖 Chat Masivo WhatsApp - Instalador Automático")
    print("=" * 60)
    print(f"🖥️  Sistema: {platform.system()} {platform.release()}")
    print(f"🐍 Python: {sys.version}")
    print("=" * 60)
    
    # Verificar Python
    if not verificar_python():
        sys.exit(1)
    
    # Instalar dependencias
    if not instalar_dependencias():
        print("\n❌ Error en la instalación de dependencias")
        sys.exit(1)
    
    # Crear directorios
    if not crear_directorios():
        print("\n❌ Error creando directorios")
        sys.exit(1)
    
    # Limpiar archivos duplicados
    limpiar_archivos_duplicados()
    
    # Configurar credenciales
    configurar_credenciales()
    
    # Crear script de ejecución
    crear_script_ejecucion()
    
    # Verificar instalación
    if not verificar_instalacion():
        print("\n❌ Error en la verificación de instalación")
        sys.exit(1)
    
    # Mostrar instrucciones finales
    mostrar_instrucciones_finales()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Instalación cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado durante la instalación: {e}")
        sys.exit(1)
