import openai
from typing import List, Dict
from vector_store import VectorStore
from config import Config

class Chatbot:
    def __init__(self):
        self.vector_store = VectorStore()
        openai.api_key = Config.OPENAI_API_KEY
        self.chat_model = Config.CHAT_MODEL
        
    def generate_response(self, user_query: str, conversation_history: List[Dict] = None) -> str:
        """
        Genera una respuesta usando RAG (Retrieval Augmented Generation)
        """
        try:
            # Buscar documentos relevantes
            similar_docs = self.vector_store.search_similar_documents(user_query, n_results=3)
            
            # Construir contexto
            context = self._build_context(similar_docs)
            
            # Construir historial de conversación
            messages = self._build_messages(user_query, context, conversation_history)
            
            # Generar respuesta
            response = openai.ChatCompletion.create(
                model=self.chat_model,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Error al generar respuesta: {str(e)}"
    
    def _build_context(self, similar_docs: List[Dict]) -> str:
        """
        Construye el contexto a partir de los documentos similares
        """
        if not similar_docs:
            return "No se encontró información relevante en la base de conocimientos."
        
        context_parts = []
        for doc in similar_docs:
            source_info = ""
            metadata = doc['metadata']
            
            if metadata.get('source') == 'pdf':
                source_info = f" (Fuente: {metadata.get('filename', 'PDF')})"
            elif metadata.get('source') == 'web':
                source_info = f" (Fuente: {metadata.get('title', metadata.get('url', 'Web'))})"
            
            context_parts.append(f"{doc['content']}{source_info}")
        
        return "\n\n".join(context_parts)
    
    def _build_messages(self, user_query: str, context: str, conversation_history: List[Dict] = None) -> List[Dict]:
        """
        Construye los mensajes para la API de OpenAI
        """
        system_prompt = f"""Eres un asistente virtual especializado que responde preguntas basándose en la información proporcionada. 

INSTRUCCIONES:
- Responde en español
- Usa únicamente la información del contexto proporcionado
- Si no encuentras información relevante en el contexto, indícalo claramente
- Sé preciso y útil en tus respuestas
- Mantén un tono profesional pero amigable
- Si la pregunta no está relacionada con el contexto, explica que solo puedes ayudar con información de la base de conocimientos

CONTEXTO:
{context}"""

        messages = [{"role": "system", "content": system_prompt}]
        
        # Añadir historial de conversación si existe
        if conversation_history:
            for msg in conversation_history[-6:]:  # Limitar a las últimas 6 interacciones
                messages.append(msg)
        
        # Añadir la consulta actual
        messages.append({"role": "user", "content": user_query})
        
        return messages
    
    def add_documents(self, documents: List[Dict[str, str]]):
        """
        Añade documentos a la base de conocimientos
        """
        self.vector_store.add_documents(documents)
    
    def get_knowledge_stats(self) -> Dict:
        """
        Obtiene estadísticas de la base de conocimientos
        """
        return self.vector_store.get_collection_stats()
    
    def clear_knowledge_base(self):
        """
        Limpia la base de conocimientos
        """
        self.vector_store.clear_collection()
