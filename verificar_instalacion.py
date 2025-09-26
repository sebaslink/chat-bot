#!/usr/bin/env python3
"""
Script de verificación de instalación
Verifica que no haya archivos duplicados y que la configuración sea correcta
"""

import os
import sys
from pathlib import Path

def mostrar_banner():
    """Mostrar banner del script"""
    print("=" * 60)
    print("🔍 VERIFICADOR DE INSTALACIÓN")
    print("=" * 60)
    print("Este script verifica que la instalación sea correcta")
    print("y que no haya archivos duplicados que generen conflictos.")
    print("=" * 60)

def verificar_archivos_principales():
    """Verificar archivos principales del sistema"""
    print("\n📁 Verificando archivos principales...")
    
    archivos_requeridos = [
        "SISTEMA_UNIFICADO_FINAL.py",
        "requirements.txt",
        "configurar_credenciales.py",
        "instalar_en_nueva_computadora.py"
    ]
    
    archivos_faltantes = []
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ {archivo} - FALTANTE")
            archivos_faltantes.append(archivo)
    
    return len(archivos_faltantes) == 0

def verificar_directorios():
    """Verificar directorios principales"""
    print("\n📂 Verificando directorios...")
    
    directorios_requeridos = [
        "CHATMASIVO",
        "templates",
        "static",
        "data",
        "CHATMASIVO/config",
        "CHATMASIVO/config/twilio",
        "CHATMASIVO/config/app"
    ]
    
    directorios_faltantes = []
    for directorio in directorios_requeridos:
        if os.path.exists(directorio):
            print(f"   ✅ {directorio}")
        else:
            print(f"   ❌ {directorio} - FALTANTE")
            directorios_faltantes.append(directorio)
    
    return len(directorios_faltantes) == 0

def verificar_archivos_duplicados():
    """Verificar archivos duplicados que puedan generar conflictos"""
    print("\n🔍 Verificando archivos duplicados...")
    
    archivos_duplicados = [
        "CHATMASIVO/config/twilio.env",
        "ChatbotInteligente_v1.0/CHATMASIVO/config/twilio.env",
        "railway_deploy/CHATMASIVO/config/twilio.env"
    ]
    
    duplicados_encontrados = []
    for archivo in archivos_duplicados:
        if os.path.exists(archivo):
            print(f"   ⚠️  {archivo} - DUPLICADO (debería eliminarse)")
            duplicados_encontrados.append(archivo)
        else:
            print(f"   ✅ {archivo} - OK (no existe)")
    
    return len(duplicados_encontrados) == 0

def verificar_archivos_configuracion():
    """Verificar archivos de configuración"""
    print("\n⚙️  Verificando archivos de configuración...")
    
    archivos_config = [
        ".env",
        "CHATMASIVO/config/twilio/Twilio.env",
        "CHATMASIVO/config/app/Twilio.env",
        "CHATMASIVO/config/twilio/Twilio.env.example",
        "CHATMASIVO/config/app/Twilio.env.example"
    ]
    
    configs_encontrados = []
    for archivo in archivos_config:
        if os.path.exists(archivo):
            print(f"   ✅ {archivo}")
            configs_encontrados.append(archivo)
        else:
            print(f"   ⚠️  {archivo} - No encontrado")
    
    return len(configs_encontrados) > 0

def verificar_dependencias():
    """Verificar dependencias de Python"""
    print("\n📦 Verificando dependencias...")
    
    try:
        import flask
        print("   ✅ Flask")
    except ImportError:
        print("   ❌ Flask - NO INSTALADO")
        return False
    
    try:
        import sqlite3
        print("   ✅ SQLite3")
    except ImportError:
        print("   ❌ SQLite3 - NO INSTALADO")
        return False
    
    try:
        import pandas
        print("   ✅ Pandas")
    except ImportError:
        print("   ⚠️  Pandas - NO INSTALADO (opcional)")
    
    try:
        import openpyxl
        print("   ✅ OpenPyXL")
    except ImportError:
        print("   ⚠️  OpenPyXL - NO INSTALADO (opcional)")
    
    return True

def verificar_credenciales():
    """Verificar configuración de credenciales"""
    print("\n🔑 Verificando credenciales...")
    
    # Verificar archivo .env
    if os.path.exists('.env'):
        print("   ✅ Archivo .env encontrado")
        
        # Leer archivo .env
        try:
            with open('.env', 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Verificar credenciales
            if 'TU_ACCOUNT_SID_AQUI' in contenido:
                print("   ⚠️  Credenciales no configuradas (usando placeholders)")
                return False
            elif 'TWILIO_ACCOUNT_SID=' in contenido:
                print("   ✅ Credenciales configuradas")
                return True
            else:
                print("   ⚠️  Formato de credenciales desconocido")
                return False
        except Exception as e:
            print(f"   ❌ Error leyendo .env: {e}")
            return False
    else:
        print("   ⚠️  Archivo .env no encontrado (modo demo)")
        return False

def mostrar_resumen(archivos_ok, directorios_ok, duplicados_ok, config_ok, deps_ok, creds_ok):
    """Mostrar resumen de la verificación"""
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    
    print(f"\n📁 Archivos principales: {'✅ OK' if archivos_ok else '❌ ERROR'}")
    print(f"📂 Directorios: {'✅ OK' if directorios_ok else '❌ ERROR'}")
    print(f"🔍 Archivos duplicados: {'✅ OK' if duplicados_ok else '⚠️  DUPLICADOS ENCONTRADOS'}")
    print(f"⚙️  Configuración: {'✅ OK' if config_ok else '⚠️  INCOMPLETA'}")
    print(f"📦 Dependencias: {'✅ OK' if deps_ok else '❌ ERROR'}")
    print(f"🔑 Credenciales: {'✅ CONFIGURADAS' if creds_ok else '⚠️  NO CONFIGURADAS (modo demo)'}")
    
    # Estado general
    if archivos_ok and directorios_ok and deps_ok:
        if creds_ok:
            print("\n🎉 ¡INSTALACIÓN COMPLETA Y FUNCIONAL!")
            print("   El sistema está listo para usar con credenciales reales.")
        else:
            print("\n✅ ¡INSTALACIÓN COMPLETA!")
            print("   El sistema funcionará en modo demo.")
            print("   Para usar credenciales reales, ejecuta: python configurar_credenciales.py")
    else:
        print("\n❌ INSTALACIÓN INCOMPLETA")
        print("   Revisa los errores anteriores y ejecuta: python instalar_en_nueva_computadora.py")
    
    print("\n📋 Próximos pasos:")
    if archivos_ok and directorios_ok and deps_ok:
        print("   1. Ejecutar: python SISTEMA_UNIFICADO_FINAL.py")
        print("   2. Abrir navegador en: http://localhost:5000")
        if not creds_ok:
            print("   3. Configurar credenciales: python configurar_credenciales.py")
    else:
        print("   1. Ejecutar: python instalar_en_nueva_computadora.py")
        print("   2. Seguir las instrucciones del instalador")

def main():
    """Función principal"""
    mostrar_banner()
    
    # Verificaciones
    archivos_ok = verificar_archivos_principales()
    directorios_ok = verificar_directorios()
    duplicados_ok = verificar_archivos_duplicados()
    config_ok = verificar_archivos_configuracion()
    deps_ok = verificar_dependencias()
    creds_ok = verificar_credenciales()
    
    # Mostrar resumen
    mostrar_resumen(archivos_ok, directorios_ok, duplicados_ok, config_ok, deps_ok, creds_ok)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Verificación cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
