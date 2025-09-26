#!/usr/bin/env python3
"""
Script de inicio para el chatbot con opciones de carga de datos
"""

import os
import sys

def show_welcome():
    """Muestra el mensaje de bienvenida"""
    print("🤖" + "=" * 58 + "🤖")
    print("🤖" + " " * 20 + "CHATBOT PERSONALIZADO" + " " * 20 + "🤖")
    print("🤖" + "=" * 58 + "🤖")
    print()
    print("¡Bienvenido! Este chatbot puede responder preguntas basándose en")
    print("información que cargues desde PDFs, URLs o texto manual.")
    print()

def check_dependencies():
    """Verifica si las dependencias están instaladas"""
    missing_deps = []
    
    try:
        import PyPDF2
    except ImportError:
        missing_deps.append("PyPDF2 (para PDFs)")
    
    try:
        import requests
        import bs4
    except ImportError:
        missing_deps.append("requests y beautifulsoup4 (para URLs)")
    
    if missing_deps:
        print("⚠️ Dependencias faltantes para funcionalidades avanzadas:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print()
        print("Para instalar todas las dependencias:")
        print("pip install PyPDF2 requests beautifulsoup4")
        print()
        print("El chatbot funcionará con funcionalidades básicas (solo texto manual).")
        print()
        return False
    else:
        print("✅ Todas las dependencias están instaladas correctamente.")
        print()
        return True

def main():
    """Función principal"""
    show_welcome()
    
    # Verificar dependencias
    has_full_deps = check_dependencies()
    
    print("Opciones de inicio:")
    print("1. 🚀 Inicio completo (cargar datos + chat)")
    print("2. 💬 Solo chat (usar datos existentes)")
    print("3. 📚 Solo cargar datos")
    print("4. ❌ Salir")
    print()
    
    while True:
        choice = input("Selecciona una opción (1-4): ").strip()
        
        if choice == "1":
            # Inicio completo
            print("\n🚀 Iniciando chatbot completo...")
            try:
                from main_chatbot import main as chatbot_main
                chatbot_main()
            except ImportError:
                print("❌ Error: No se pudo importar el chatbot principal.")
                print("Asegúrate de que main_chatbot.py esté en el mismo directorio.")
            break
        
        elif choice == "2":
            # Solo chat
            print("\n💬 Iniciando solo chat...")
            try:
                from ultra_simple_chatbot import main as simple_main
                simple_main()
            except ImportError:
                print("❌ Error: No se pudo importar el chatbot simple.")
                print("Asegúrate de que ultra_simple_chatbot.py esté en el mismo directorio.")
            break
        
        elif choice == "3":
            # Solo cargar datos
            if not has_full_deps:
                print("❌ Para cargar PDFs y URLs necesitas instalar las dependencias.")
                print("Ejecuta: pip install PyPDF2 requests beautifulsoup4")
                continue
            
            print("\n📚 Iniciando cargador de datos...")
            try:
                from data_loader import main as loader_main
                loader_main()
            except ImportError:
                print("❌ Error: No se pudo importar el cargador de datos.")
                print("Asegúrate de que data_loader.py esté en el mismo directorio.")
            break
        
        elif choice == "4":
            # Salir
            print("\n👋 ¡Hasta luego!")
            break
        
        else:
            print("⚠️ Opción no válida. Por favor selecciona 1-4.")

if __name__ == "__main__":
    main()
