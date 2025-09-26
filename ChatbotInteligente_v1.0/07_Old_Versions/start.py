#!/usr/bin/env python3
"""
Script de inicio rápido para el chatbot
"""

import os
import sys
import subprocess

def check_requirements():
    """Verifica que las dependencias estén instaladas"""
    try:
        import streamlit
        import openai
        import chromadb
        import PyPDF2
        import requests
        from bs4 import BeautifulSoup
        from sentence_transformers import SentenceTransformer
        print("✅ Todas las dependencias están instaladas")
        return True
    except ImportError as e:
        print(f"❌ Faltan dependencias: {e}")
        print("Ejecuta: pip install -r requirements.txt")
        return False

def check_env_file():
    """Verifica que el archivo .env esté configurado"""
    if not os.path.exists('.env'):
        print("⚠️ Archivo .env no encontrado")
        print("Copia env_example.txt a .env y configura tu OPENAI_API_KEY")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
        if 'OPENAI_API_KEY=tu_clave_api_aqui' in content or 'OPENAI_API_KEY=' not in content:
            print("⚠️ OPENAI_API_KEY no configurada en .env")
            print("Añade tu clave de API de OpenAI al archivo .env")
            return False
    
    print("✅ Archivo .env configurado correctamente")
    return True

def main():
    """Función principal"""
    print("🤖 Iniciando Chatbot Personalizado")
    print("=" * 40)
    
    # Verificar dependencias
    if not check_requirements():
        sys.exit(1)
    
    # Verificar configuración
    if not check_env_file():
        print("\n📝 Pasos para configurar:")
        print("1. Copia env_example.txt a .env")
        print("2. Edita .env y añade tu OPENAI_API_KEY")
        print("3. Ejecuta este script nuevamente")
        sys.exit(1)
    
    print("\n🚀 Iniciando aplicación...")
    
    # Crear directorio para PDFs si no existe
    os.makedirs("pdfs", exist_ok=True)
    
    # Iniciar Streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 ¡Hasta luego!")
    except Exception as e:
        print(f"❌ Error al iniciar la aplicación: {e}")

if __name__ == "__main__":
    main()
