#!/usr/bin/env python3
"""
Integración del chatbot con el chat masivo
Permite usar la base de conocimientos del chatbot en el chat masivo
"""

import os
import sys
import json
from datetime import datetime

# Agregar el path del chatbot principal
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '01_Core_Chatbot'))

try:
    from ultra_simple_chatbot import UltraSimpleChatbot
    CHATBOT_AVAILABLE = True
except ImportError:
    CHATBOT_AVAILABLE = False
    print("⚠️ Chatbot no disponible. Instalando dependencias...")

class ChatbotIntegration:
    def __init__(self):
        self.chatbot = None
        self.knowledge_base_path = os.path.join(os.path.dirname(__file__), '..', '05_Data', 'knowledge_base.json')
        self.sync_status_path = os.path.join(os.path.dirname(__file__), 'data', 'sync_status.json')
        self.init_chatbot()
    
    def init_chatbot(self):
        """Inicializa el chatbot si está disponible"""
        if not CHATBOT_AVAILABLE:
            print("❌ Chatbot no disponible. Funcionalidades limitadas.")
            return False
        
        try:
            # Usar la base de conocimientos compartida
            self.chatbot = UltraSimpleChatbot(self.knowledge_base_path)
            print("✅ Chatbot integrado exitosamente")
            return True
        except Exception as e:
            print(f"❌ Error inicializando chatbot: {e}")
            return False
    
    def get_chatbot_response(self, message):
        """Obtiene respuesta del chatbot"""
        if not self.chatbot:
            return "Chatbot no disponible. Respuesta por defecto."
        
        try:
            return self.chatbot.generate_response(message)
        except Exception as e:
            return f"Error generando respuesta: {str(e)}"
    
    def get_knowledge_stats(self):
        """Obtiene estadísticas de la base de conocimientos"""
        if not self.chatbot:
            return {
                'total_documents': 0,
                'sources': {},
                'available': False
            }
        
        try:
            stats = self.chatbot.get_stats()
            stats['available'] = True
            return stats
        except Exception as e:
            return {
                'total_documents': 0,
                'sources': {},
                'available': False,
                'error': str(e)
            }
    
    def sync_with_chatbot(self):
        """Sincroniza con el chatbot principal"""
        try:
            # Verificar si existe el archivo de sincronización
            if os.path.exists(self.sync_status_path):
                with open(self.sync_status_path, 'r', encoding='utf-8') as f:
                    sync_data = json.load(f)
                
                print(f"📊 Última sincronización: {sync_data.get('timestamp', 'Desconocida')}")
                print(f"📄 Documentos disponibles: {sync_data.get('total_documents', 0)}")
                
                return sync_data
            else:
                print("⚠️ No hay datos de sincronización disponibles")
                return None
        except Exception as e:
            print(f"❌ Error sincronizando: {e}")
            return None
    
    def generate_smart_message(self, base_message, contact_name="Usuario"):
        """Genera un mensaje inteligente usando el chatbot"""
        if not self.chatbot:
            return base_message
        
        try:
            # Crear un prompt para generar un mensaje personalizado
            prompt = f"Genera un mensaje personalizado para {contact_name} basado en: {base_message}"
            response = self.chatbot.generate_response(prompt)
            
            # Si la respuesta es muy genérica, usar el mensaje base
            if len(response) < 50 or "no encontré información" in response.lower():
                return base_message
            
            return response
        except Exception as e:
            print(f"Error generando mensaje inteligente: {e}")
            return base_message
    
    def search_knowledge(self, query):
        """Busca información en la base de conocimientos"""
        if not self.chatbot:
            return []
        
        try:
            return self.chatbot.search_documents(query, n_results=5)
        except Exception as e:
            print(f"Error buscando en conocimiento: {e}")
            return []
    
    def get_available_topics(self):
        """Obtiene temas disponibles en la base de conocimientos"""
        if not self.chatbot:
            return []
        
        try:
            # Buscar documentos y extraer temas
            docs = self.chatbot.documents
            topics = set()
            
            for doc in docs[:10]:  # Limitar a los primeros 10
                if doc.get('title'):
                    topics.add(doc['title'])
                elif doc.get('source'):
                    topics.add(doc['source'].title())
            
            return list(topics)
        except Exception as e:
            print(f"Error obteniendo temas: {e}")
            return []

def test_integration():
    """Prueba la integración del chatbot"""
    print("🧪 Probando integración del chatbot...")
    
    integration = ChatbotIntegration()
    
    # Probar estadísticas
    stats = integration.get_knowledge_stats()
    print(f"📊 Estadísticas: {stats}")
    
    # Probar sincronización
    sync_data = integration.sync_with_chatbot()
    print(f"🔄 Sincronización: {sync_data}")
    
    # Probar respuesta del chatbot
    if integration.chatbot:
        response = integration.get_chatbot_response("¿Qué información tienes disponible?")
        print(f"🤖 Respuesta del chatbot: {response[:100]}...")
    
    # Probar temas disponibles
    topics = integration.get_available_topics()
    print(f"📚 Temas disponibles: {topics[:5]}")
    
    print("✅ Prueba de integración completada")

if __name__ == "__main__":
    test_integration()
