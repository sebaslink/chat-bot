#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar el instalador creado
Verifica que todos los archivos necesarios estén presentes
"""

import os
import sys
import subprocess
from pathlib import Path

def verificar_archivos_requeridos():
    """Verificar que todos los archivos necesarios estén presentes"""
    print("🔍 Verificando archivos requeridos...")
    
    archivos_requeridos = [
        "app/codchat.py",
        "codigo/codchat.py", 
        "templates/",
        "static/",
        "requirements.txt"
    ]
    
    archivos_encontrados = []
    archivos_faltantes = []
    
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            archivos_encontrados.append(archivo)
            print(f"  ✅ {archivo}")
        else:
            archivos_faltantes.append(archivo)
            print(f"  ❌ {archivo}")
    
    if archivos_faltantes:
        print(f"\n⚠️  Archivos faltantes: {len(archivos_faltantes)}")
        return False
    else:
        print(f"\n✅ Todos los archivos requeridos encontrados: {len(archivos_encontrados)}")
        return True

def verificar_dependencias():
    """Verificar que las dependencias estén instaladas"""
    print("\n🔍 Verificando dependencias...")
    
    dependencias = [
        "flask",
        "twilio", 
        "pandas",
        "openpyxl",
        "python-dotenv",
        "werkzeug"
    ]
    
    dependencias_ok = []
    dependencias_faltantes = []
    
    for dep in dependencias:
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'show', dep], 
                          check=True, capture_output=True)
            dependencias_ok.append(dep)
            print(f"  ✅ {dep}")
        except subprocess.CalledProcessError:
            dependencias_faltantes.append(dep)
            print(f"  ❌ {dep}")
    
    if dependencias_faltantes:
        print(f"\n⚠️  Dependencias faltantes: {len(dependencias_faltantes)}")
        print("💡 Instala con: pip install -r requirements.txt")
        return False
    else:
        print(f"\n✅ Todas las dependencias instaladas: {len(dependencias_ok)}")
        return True

def verificar_pyinstaller():
    """Verificar que PyInstaller esté instalado"""
    print("\n🔍 Verificando PyInstaller...")
    
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'show', 'pyinstaller'], 
                      check=True, capture_output=True)
        print("  ✅ PyInstaller instalado")
        return True
    except subprocess.CalledProcessError:
        print("  ❌ PyInstaller no instalado")
        print("  💡 Instala con: pip install pyinstaller")
        return False

def verificar_inno_setup():
    """Verificar que Inno Setup esté instalado"""
    print("\n🔍 Verificando Inno Setup...")
    
    ubicaciones = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
        r"C:\Program Files\Inno Setup 5\ISCC.exe"
    ]
    
    for ubicacion in ubicaciones:
        if os.path.exists(ubicacion):
            print(f"  ✅ Inno Setup encontrado: {ubicacion}")
            return True
    
    print("  ❌ Inno Setup no encontrado")
    print("  💡 Descarga desde: https://jrsoftware.org/isinfo.php")
    return False

def probar_creacion_ejecutable():
    """Probar la creación del ejecutable"""
    print("\n🧪 Probando creación de ejecutable...")
    
    try:
        # Ejecutar script de creación
        resultado = subprocess.run([sys.executable, 'crear_ejecutable_simple.py'], 
                                 capture_output=True, text=True, timeout=300)
        
        if resultado.returncode == 0:
            print("  ✅ Ejecutable creado exitosamente")
            
            # Verificar que el ejecutable existe
            if os.path.exists("ChatMasivo_Portable/ChatMasivo.exe"):
                print("  ✅ Archivo ejecutable encontrado")
                return True
            else:
                print("  ❌ Archivo ejecutable no encontrado")
                return False
        else:
            print(f"  ❌ Error creando ejecutable: {resultado.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("  ❌ Timeout creando ejecutable (más de 5 minutos)")
        return False
    except Exception as e:
        print(f"  ❌ Error inesperado: {e}")
        return False

def generar_reporte():
    """Generar reporte de verificación"""
    print("\n📊 GENERANDO REPORTE DE VERIFICACIÓN")
    print("=" * 50)
    
    # Verificaciones
    archivos_ok = verificar_archivos_requeridos()
    dependencias_ok = verificar_dependencias()
    pyinstaller_ok = verificar_pyinstaller()
    inno_ok = verificar_inno_setup()
    
    # Resumen
    print("\n📋 RESUMEN:")
    print(f"  Archivos requeridos: {'✅ OK' if archivos_ok else '❌ FALTANTES'}")
    print(f"  Dependencias Python: {'✅ OK' if dependencias_ok else '❌ FALTANTES'}")
    print(f"  PyInstaller: {'✅ OK' if pyinstaller_ok else '❌ FALTANTE'}")
    print(f"  Inno Setup: {'✅ OK' if inno_ok else '❌ FALTANTE'}")
    
    # Recomendaciones
    print("\n💡 RECOMENDACIONES:")
    
    if not archivos_ok:
        print("  - Verifica que todos los archivos del proyecto estén presentes")
    
    if not dependencias_ok:
        print("  - Ejecuta: pip install -r requirements.txt")
    
    if not pyinstaller_ok:
        print("  - Ejecuta: pip install pyinstaller")
    
    if not inno_ok:
        print("  - Descarga e instala Inno Setup para crear instalador completo")
    
    # Estado general
    if archivos_ok and dependencias_ok and pyinstaller_ok:
        print("\n🎉 ¡SISTEMA LISTO PARA CREAR INSTALADOR!")
        print("  Puedes ejecutar: python crear_ejecutable_simple.py")
        
        if inno_ok:
            print("  O para instalador completo: python crear_instalador.py")
    else:
        print("\n⚠️  SISTEMA NO LISTO")
        print("  Resuelve los problemas indicados arriba")
    
    return archivos_ok and dependencias_ok and pyinstaller_ok

def main():
    """Función principal"""
    print("🧪 PROBADOR DE INSTALADOR - CHAT MASIVO")
    print("=" * 45)
    
    try:
        generar_reporte()
        
        # Preguntar si probar creación
        respuesta = input("\n¿Probar creación de ejecutable? (s/n): ").lower()
        if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
            probar_creacion_ejecutable()
        
    except KeyboardInterrupt:
        print("\n\n❌ Prueba cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
