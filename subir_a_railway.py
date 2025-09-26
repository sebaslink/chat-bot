#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para preparar la aplicación para subir directamente a Railway
Sin necesidad de GitHub
"""

import os
import shutil
import zipfile
from datetime import datetime

def crear_zip_para_railway():
    """Crear un archivo ZIP listo para subir a Railway"""
    
    print("🚀 PREPARANDO APLICACIÓN PARA RAILWAY")
    print("=" * 50)
    
    # Archivos y carpetas a incluir
    archivos_incluir = [
        "SISTEMA_UNIFICADO_FINAL.py",
        "requirements.txt",
        "railway.json",
        "runtime.txt",
        ".gitignore",
        "README_FINAL.md",
        "static/",
        "templates/",
        "uploads/",
        "data/",
        "logs/",
        "CHATMASIVO/",
        "ChatbotInteligente_v1.0/"
    ]
    
    # Crear directorio temporal
    temp_dir = "railway_deploy"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    print("📁 Copiando archivos necesarios...")
    
    # Copiar archivos
    for item in archivos_incluir:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.copytree(item, os.path.join(temp_dir, item))
                print(f"✅ Carpeta copiada: {item}")
            else:
                shutil.copy2(item, temp_dir)
                print(f"✅ Archivo copiado: {item}")
        else:
            print(f"⚠️  No encontrado: {item}")
    
    # Crear archivo ZIP
    zip_filename = f"chatbot_railway_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    
    print(f"\n📦 Creando archivo ZIP: {zip_filename}")
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname)
    
    # Limpiar directorio temporal
    shutil.rmtree(temp_dir)
    
    print(f"\n✅ ARCHIVO LISTO: {zip_filename}")
    print(f"📏 Tamaño: {os.path.getsize(zip_filename) / (1024*1024):.2f} MB")
    
    return zip_filename

def mostrar_instrucciones_railway():
    """Mostrar instrucciones para subir a Railway"""
    
    print("\n" + "=" * 60)
    print("📋 INSTRUCCIONES PARA SUBIR A RAILWAY")
    print("=" * 60)
    
    print("""
🌐 PASO 1: CREAR CUENTA EN RAILWAY
   1. Ve a: https://railway.app
   2. Regístrate con GitHub o email
   3. Confirma tu cuenta

🚀 PASO 2: CREAR NUEVO PROYECTO
   1. Haz clic en "New Project"
   2. Selecciona "Deploy from GitHub repo"
   3. Luego selecciona "Deploy from template"
   4. Busca "Python" y selecciona

📁 PASO 3: SUBIR ARCHIVO ZIP
   1. En el proyecto, haz clic en "Settings"
   2. Ve a "Source" y selecciona "Upload ZIP"
   3. Sube el archivo ZIP creado

⚙️ PASO 4: CONFIGURAR VARIABLES
   En la sección "Variables":
   - PORT: 5000
   - PYTHON_VERSION: 3.11.0
   - FLASK_ENV: production

🚀 PASO 5: DESPLEGAR
   1. Railway detectará automáticamente el archivo principal
   2. Instalará las dependencias
   3. Tu app estará disponible en: https://tu-app.railway.app

💰 COSTO: GRATIS (con limitaciones)
   - $5 de crédito gratis por mes
   - Se duerme después de 5 minutos de inactividad
   - Se despierta automáticamente al recibir tráfico
""")

def main():
    """Función principal"""
    
    print("🎯 PREPARADOR DE DESPLIEGUE PARA RAILWAY")
    print("   Sin necesidad de GitHub")
    print("=" * 50)
    
    # Verificar archivos necesarios
    archivos_requeridos = [
        "SISTEMA_UNIFICADO_FINAL.py",
        "requirements.txt",
        "railway.json"
    ]
    
    faltantes = []
    for archivo in archivos_requeridos:
        if not os.path.exists(archivo):
            faltantes.append(archivo)
    
    if faltantes:
        print("❌ FALTAN ARCHIVOS NECESARIOS:")
        for archivo in faltantes:
            print(f"   - {archivo}")
        print("\n💡 Ejecuta primero: python preparar_despliegue_simple.py")
        return
    
    # Crear archivo ZIP
    zip_file = crear_zip_para_railway()
    
    # Mostrar instrucciones
    mostrar_instrucciones_railway()
    
    print(f"\n🎉 ¡LISTO! Archivo creado: {zip_file}")
    print("📤 Ahora puedes subirlo directamente a Railway")

if __name__ == "__main__":
    main()
