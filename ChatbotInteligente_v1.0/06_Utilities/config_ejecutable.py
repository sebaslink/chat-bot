#!/usr/bin/env python3
"""
Configuración para el ejecutable de la interfaz web
"""

# Configuración del servidor web
SERVER_CONFIG = {
    'host': '0.0.0.0',  # Cambiar a '127.0.0.1' para solo acceso local
    'port': 5000,        # Puerto del servidor
    'debug': False,      # Modo debug (True para desarrollo)
}

# Dependencias requeridas
REQUIRED_DEPENDENCIES = [
    "Flask==2.3.3",
    "Werkzeug==2.3.7",
    "PyPDF2==3.0.1", 
    "requests==2.31.0",
    "beautifulsoup4==4.12.2",
    "numpy",
    "sentence-transformers"
]

# Dependencias opcionales (para funcionalidades avanzadas)
OPTIONAL_DEPENDENCIES = [
    "chromadb==0.4.15",  # Base de datos vectorial
    "torch",             # Para modelos de ML más avanzados
]

# Configuración de archivos
FILE_CONFIG = {
    'upload_folder': 'uploads',
    'data_file': 'knowledge_base.json',
    'max_file_size': 16 * 1024 * 1024,  # 16MB
    'allowed_extensions': ['pdf']
}

# Mensajes de la interfaz
MESSAGES = {
    'welcome': "🤖 Bienvenido a la Interfaz Web del Chatbot",
    'installing': "📦 Instalando dependencias...",
    'starting': "🚀 Iniciando servidor...",
    'ready': "✅ ¡Interfaz lista! Abre http://localhost:5000",
    'error': "❌ Error: {error}",
    'success': "✅ {message}"
}

# Configuración de la interfaz web
WEB_INTERFACE_CONFIG = {
    'title': 'Cargador de Datos - Chatbot',
    'description': 'Sube PDFs, URLs y texto para entrenar tu chatbot',
    'version': '1.0.0',
    'author': 'Asistente IA'
}
