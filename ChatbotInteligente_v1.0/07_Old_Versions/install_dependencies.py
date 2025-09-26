#!/usr/bin/env python3
"""
Script para instalar todas las dependencias del chatbot
"""

import subprocess
import sys
import os

def install_package(package):
    """Instala un paquete usando pip"""
    try:
        print(f"Instalando {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} instalado correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando {package}: {e}")
        return False

def test_import(package, import_name=None):
    """Prueba si un paquete se puede importar"""
    if import_name is None:
        import_name = package
    
    try:
        __import__(import_name)
        print(f"✅ {package} se puede importar correctamente")
        return True
    except ImportError as e:
        print(f"❌ Error importando {package}: {e}")
        return False

def main():
    """Función principal"""
    print("🤖 Instalando dependencias del Chatbot")
    print("=" * 50)
    
    # Lista de paquetes a instalar
    packages = [
        "streamlit",
        "openai", 
        "chromadb",
        "pypdf2",
        "beautifulsoup4",
        "requests",
        "python-dotenv",
        "sentence-transformers",
        "numpy",
        "pandas",
        "tiktoken"
    ]
    
    # Instalar paquetes
    installed = []
    failed = []
    
    for package in packages:
        if install_package(package):
            installed.append(package)
        else:
            failed.append(package)
    
    print("\n" + "=" * 50)
    print("📊 Resumen de instalación:")
    print(f"✅ Instalados correctamente: {len(installed)}")
    print(f"❌ Fallaron: {len(failed)}")
    
    if installed:
        print("\nPaquetes instalados:")
        for pkg in installed:
            print(f"  - {pkg}")
    
    if failed:
        print("\nPaquetes que fallaron:")
        for pkg in failed:
            print(f"  - {pkg}")
    
    # Probar imports
    print("\n🧪 Probando imports...")
    test_packages = [
        ("streamlit", "streamlit"),
        ("openai", "openai"),
        ("chromadb", "chromadb"),
        ("pypdf2", "PyPDF2"),
        ("beautifulsoup4", "bs4"),
        ("requests", "requests"),
        ("python-dotenv", "dotenv"),
        ("sentence-transformers", "sentence_transformers"),
        ("numpy", "numpy"),
        ("pandas", "pandas"),
        ("tiktoken", "tiktoken")
    ]
    
    working_imports = 0
    for package, import_name in test_packages:
        if test_import(package, import_name):
            working_imports += 1
    
    print(f"\n📈 Imports exitosos: {working_imports}/{len(test_packages)}")
    
    if working_imports == len(test_packages):
        print("\n🎉 ¡Todas las dependencias están funcionando correctamente!")
        print("Puedes ejecutar el chatbot con: python app.py")
    else:
        print("\n⚠️ Algunas dependencias no están funcionando correctamente.")
        print("Revisa los errores anteriores e intenta reinstalar los paquetes fallidos.")

if __name__ == "__main__":
    main()
