import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    # Configuración de OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Configuración de la base de datos vectorial
    VECTOR_DB_PATH = "vector_db"
    
    # Configuración del modelo
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    CHAT_MODEL = "gpt-3.5-turbo"
    
    # Configuración de extracción
    MAX_PDF_PAGES = 50
    MAX_WEB_CONTENT_LENGTH = 10000
    
    # Configuración de la interfaz
    PAGE_TITLE = "Chatbot Personalizado"
    PAGE_ICON = "🤖"
