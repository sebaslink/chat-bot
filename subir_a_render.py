#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para preparar la aplicación para subir directamente a Render
Sin necesidad de GitHub
"""

import os
import shutil
import zipfile
from datetime import datetime

def crear_zip_para_render():
    """Crear un archivo ZIP listo para subir a Render"""
    
    print("🚀 PREPARANDO APLICACIÓN PARA RENDER")
    print("=" * 50)
    
    # Archivos y carpetas a incluir
    archivos_incluir = [
        "SISTEMA_UNIFICADO_FINAL.py",
        "requirements.txt",
        "Procfile",
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
    temp_dir = "render_deploy"
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
    zip_filename = f"chatbot_render_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    
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

def mostrar_instrucciones_render():
    """Mostrar instrucciones para subir a Render"""
    
    print("\n" + "=" * 60)
    print("📋 INSTRUCCIONES PARA SUBIR A RENDER")
    print("=" * 60)
    
    print("""
🌐 PASO 1: CREAR CUENTA EN RENDER
   1. Ve a: https://render.com
   2. Regístrate con tu email
   3. Confirma tu cuenta

🚀 PASO 2: CREAR NUEVO SERVICIO
   1. Haz clic en "New +"
   2. Selecciona "Web Service"
   3. Haz clic en "Build and deploy from a Git repository"
   4. Luego selecciona "Deploy without Git"

📁 PASO 3: SUBIR ARCHIVO ZIP
   1. Arrastra el archivo ZIP creado
   2. O haz clic en "Choose File" y selecciona el ZIP

⚙️ PASO 4: CONFIGURAR SERVICIO
   - Name: chatbot-inteligente
   - Environment: Python 3
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn SISTEMA_UNIFICADO_FINAL:app --bind 0.0.0.0:$PORT

🔧 PASO 5: VARIABLES DE ENTORNO
   Agregar estas variables en la sección "Environment Variables":
   - PORT: 10000
   - PYTHON_VERSION: 3.11.0
   - FLASK_ENV: production

🚀 PASO 6: DESPLEGAR
   1. Haz clic en "Create Web Service"
   2. Espera a que termine el despliegue
   3. Tu app estará disponible en: https://tu-app.onrender.com

💰 COSTO: GRATIS (con limitaciones)
   - 750 horas gratis por mes
   - Se duerme después de 15 minutos de inactividad
   - Se despierta automáticamente al recibir tráfico
""")

def main():
    """Función principal"""
    
    print("🎯 PREPARADOR DE DESPLIEGUE PARA RENDER")
    print("   Sin necesidad de GitHub")
    print("=" * 50)
    
    # Verificar archivos necesarios
    archivos_requeridos = [
        "SISTEMA_UNIFICADO_FINAL.py",
        "requirements.txt",
        "Procfile"
    ]
    
    faltantes = []
    for archivo in archivos_requeridos:
        if not os.path.exists(archivo):
            faltantes.append(archivo)
    
    if faltantes:
        print("❌ FALTAN ARCHIVOS NECESARIOS:")
        for archivo in faltantes:
            print(f"   - {archivo}")
        print("\n💡 Ejecuta primero: python preparar_render.py")
        return
    
    # Crear archivo ZIP
    zip_file = crear_zip_para_render()
    
    # Mostrar instrucciones
    mostrar_instrucciones_render()
    
    print(f"\n🎉 ¡LISTO! Archivo creado: {zip_file}")
    print("📤 Ahora puedes subirlo directamente a Render")

if __name__ == "__main__":
    main()
