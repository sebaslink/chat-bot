import re
from typing import List, Dict
from simple_vector_store import SimpleVectorStore

class SimpleChatbot:
    def __init__(self):
        self.vector_store = SimpleVectorStore()
        self.conversation_history = []
    
    def generate_response(self, user_query: str) -> str:
        """Genera una respuesta basada en el contenido disponible"""
        try:
            # Buscar documentos relevantes
            similar_docs = self.vector_store.search_similar_documents(user_query, n_results=3)
            
            if not similar_docs:
                return self._generate_fallback_response(user_query)
            
            # Construir respuesta basada en los documentos encontrados
            response = self._build_response_from_documents(user_query, similar_docs)
            
            # Guardar en historial
            self.conversation_history.append({
                'user': user_query,
                'bot': response
            })
            
            return response
            
        except Exception as e:
            return f"Lo siento, hubo un error procesando tu consulta: {str(e)}"
    
    def _build_response_from_documents(self, query: str, documents: List[Dict]) -> str:
        """Construye una respuesta basada en los documentos encontrados"""
        # Extraer información relevante de los documentos
        relevant_info = []
        sources = []
        
        for doc in documents:
            content = doc['content']
            metadata = doc['metadata']
            
            # Añadir información de la fuente
            source_info = ""
            if metadata.get('source') == 'pdf':
                source_info = f" (Fuente: {metadata.get('filename', 'PDF')})"
            elif metadata.get('source') == 'web':
                source_info = f" (Fuente: {metadata.get('title', metadata.get('url', 'Web'))})"
            
            relevant_info.append(f"{content}{source_info}")
            sources.append(metadata.get('source', 'unknown'))
        
        # Construir respuesta
        response_parts = []
        
        # Saludo inicial
        if any(word in query.lower() for word in ['hola', 'hi', 'hello', 'buenos']):
            response_parts.append("¡Hola! Te puedo ayudar con información de la base de conocimientos.")
        
        # Información principal
        if relevant_info:
            response_parts.append("Basándome en la información disponible:")
            response_parts.append("")
            
            for i, info in enumerate(relevant_info[:2], 1):  # Máximo 2 fuentes
                response_parts.append(f"{i}. {info}")
        
        # Información adicional si hay más fuentes
        if len(relevant_info) > 2:
            response_parts.append("")
            response_parts.append(f"También encontré información adicional en {len(relevant_info) - 2} fuentes más.")
        
        # Sugerencia de seguimiento
        response_parts.append("")
        response_parts.append("¿Te gustaría saber más sobre algún tema específico?")
        
        return "\n".join(response_parts)
    
    def _generate_fallback_response(self, query: str) -> str:
        """Genera una respuesta cuando no se encuentra información relevante"""
        responses = [
            "Lo siento, no encontré información específica sobre tu consulta en la base de conocimientos.",
            "No tengo información suficiente para responder tu pregunta con precisión.",
            "La información que buscas no está disponible en los documentos cargados.",
            "No pude encontrar datos relevantes para tu consulta."
        ]
        
        # Respuesta base
        response = responses[0]
        
        # Sugerencias basadas en el tipo de consulta
        if any(word in query.lower() for word in ['qué', 'what', 'cómo', 'how', 'cuándo', 'when']):
            response += " ¿Podrías reformular tu pregunta o ser más específico?"
        elif any(word in query.lower() for word in ['dónde', 'where', 'quién', 'who']):
            response += " ¿Tienes más detalles sobre lo que buscas?"
        else:
            response += " ¿Te gustaría cargar más documentos o hacer una pregunta diferente?"
        
        return response
    
    def add_documents(self, documents: List[Dict[str, str]]):
        """Añade documentos a la base de conocimientos"""
        self.vector_store.add_documents(documents)
    
    def get_knowledge_stats(self) -> Dict:
        """Obtiene estadísticas de la base de conocimientos"""
        return self.vector_store.get_stats()
    
    def clear_knowledge_base(self):
        """Limpia la base de conocimientos"""
        self.vector_store.clear_data()
        self.conversation_history = []
    
    def get_conversation_history(self) -> List[Dict]:
        """Obtiene el historial de conversación"""
        return self.conversation_history
    
    def clear_conversation_history(self):
        """Limpia el historial de conversación"""
        self.conversation_history = []
