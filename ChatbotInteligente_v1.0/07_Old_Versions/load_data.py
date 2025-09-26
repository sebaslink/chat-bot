#!/usr/bin/env python3
"""
Script para cargar datos en el chatbot
"""

import os
from chatbot import Chatbot
from pdf_extractor import PDFExtractor
from web_extractor import WebExtractor

def load_pdfs_from_directory(directory_path: str):
    """
    Carga todos los PDFs de un directorio
    """
    print(f"Cargando PDFs desde: {directory_path}")
    
    pdf_extractor = PDFExtractor()
    chatbot = Chatbot()
    
    documents = pdf_extractor.extract_text_from_pdfs_in_directory(directory_path)
    
    if documents:
        chatbot.add_documents(documents)
        print(f"✅ Cargados {len(documents)} PDFs exitosamente")
    else:
        print("❌ No se encontraron PDFs válidos")

def load_urls(urls: list):
    """
    Carga contenido de URLs
    """
    print(f"Cargando {len(urls)} URLs...")
    
    web_extractor = WebExtractor()
    chatbot = Chatbot()
    
    documents = web_extractor.extract_from_multiple_urls(urls)
    
    if documents:
        chatbot.add_documents(documents)
        print(f"✅ Cargadas {len(documents)} URLs exitosamente")
    else:
        print("❌ No se pudo cargar contenido de las URLs")

def main():
    """
    Función principal para cargar datos
    """
    print("🤖 Cargador de datos para el Chatbot")
    print("=" * 50)
    
    # Ejemplo: Cargar PDFs de un directorio
    pdf_directory = "pdfs"  # Cambia por tu directorio
    if os.path.exists(pdf_directory):
        load_pdfs_from_directory(pdf_directory)
    else:
        print(f"⚠️ Directorio {pdf_directory} no encontrado")
    
    # Ejemplo: Cargar URLs
    example_urls = [
        "https://es.wikipedia.org/wiki/Inteligencia_artificial",
        "https://es.wikipedia.org/wiki/Machine_learning"
    ]
    
    print("\n¿Deseas cargar URLs de ejemplo? (s/n): ", end="")
    response = input().lower()
    
    if response == 's':
        load_urls(example_urls)
    
    print("\n✅ Carga de datos completada")

if __name__ == "__main__":
    main()
