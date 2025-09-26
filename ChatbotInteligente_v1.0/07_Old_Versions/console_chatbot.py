#!/usr/bin/env python3
"""
Chatbot de consola simple que funciona sin dependencias externas complejas
"""

import json
import os
import re
from typing import List, Dict
from pdf_extractor import PDFExtractor
from web_extractor import WebExtractor

class ConsoleChatbot:
    def __init__(self, data_file="knowledge_base.json"):
        self.data_file = data_file
        self.documents = []
        self.conversation_history = []
        self.load_data()
    
    def load_data(self):
        """Carga datos existentes del archivo JSON"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.documents = data.get('documents', [])
                print(f"✅ Cargados {len(self.documents)} documentos existentes")
            except Exception as e:
                print(f"⚠️ Error cargando datos existentes: {e}")
                self.documents = []
    
    def save_data(self):
        """Guarda los datos en el archivo JSON"""
        try:
            data = {
                'documents': self.documents,
                'total_documents': len(self.documents)
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ Datos guardados: {len(self.documents)} documentos")
        except Exception as e:
            print(f"❌ Error guardando datos: {e}")
    
    def add_documents(self, documents: List[Dict[str, str]]):
        """Añade documentos a la base de conocimientos"""
        for doc in documents:
            # Dividir en chunks si es muy largo
            chunks = self._chunk_text(doc['content'])
            
            for i, chunk in enumerate(chunks):
                if chunk.strip():
                    self.documents.append({
                        'id': f"{doc.get('source', 'unknown')}_{len(self.documents)}",
                        'content': chunk,
                        'source': doc.get('source', 'unknown'),
                        'filename': doc.get('filename', ''),
                        'url': doc.get('url', ''),
                        'title': doc.get('title', ''),
                        'chunk_index': i,
                        'total_chunks': len(chunks)
                    })
        
        self.save_data()
        print(f"✅ Añadidos {len(documents)} documentos a la base de conocimientos")
    
    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Divide el texto en fragmentos más pequeños"""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Intentar cortar en un punto lógico
            if end < len(text):
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                cut_point = max(last_period, last_newline)
                
                if cut_point > start + chunk_size // 2:
                    chunk = chunk[:cut_point + 1]
                    end = start + cut_point + 1
            
            chunks.append(chunk.strip())
            start = end - overlap
        
        return [chunk for chunk in chunks if chunk.strip()]
    
    def search_documents(self, query: str, n_results: int = 3) -> List[Dict]:
        """Busca documentos relevantes usando búsqueda de texto simple"""
        if not self.documents:
            return []
        
        query_words = set(query.lower().split())
        scored_docs = []
        
        for doc in self.documents:
            content_words = set(doc['content'].lower().split())
            
            # Calcular similitud simple por palabras comunes
            common_words = query_words.intersection(content_words)
            score = len(common_words) / len(query_words) if query_words else 0
            
            if score > 0:
                scored_docs.append((doc, score))
        
        # Ordenar por puntuación
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        
        return [doc for doc, score in scored_docs[:n_results]]
    
    def generate_response(self, user_query: str) -> str:
        """Genera una respuesta basada en el contenido disponible"""
        try:
            # Buscar documentos relevantes
            similar_docs = self.search_documents(user_query, n_results=3)
            
            if not similar_docs:
                return self._generate_fallback_response(user_query)
            
            # Construir respuesta
            response_parts = []
            
            # Saludo inicial
            if any(word in user_query.lower() for word in ['hola', 'hi', 'hello', 'buenos']):
                response_parts.append("¡Hola! Te puedo ayudar con información de la base de conocimientos.")
            
            # Información principal
            response_parts.append("Basándome en la información disponible:")
            response_parts.append("")
            
            for i, doc in enumerate(similar_docs[:2], 1):
                source_info = ""
                if doc['source'] == 'pdf':
                    source_info = f" (Fuente: {doc['filename']})"
                elif doc['source'] == 'web':
                    source_info = f" (Fuente: {doc['title'] or doc['url']})"
                
                response_parts.append(f"{i}. {doc['content'][:300]}...{source_info}")
            
            # Información adicional
            if len(similar_docs) > 2:
                response_parts.append("")
                response_parts.append(f"También encontré información adicional en {len(similar_docs) - 2} fuentes más.")
            
            response_parts.append("")
            response_parts.append("¿Te gustaría saber más sobre algún tema específico?")
            
            return "\n".join(response_parts)
            
        except Exception as e:
            return f"Lo siento, hubo un error procesando tu consulta: {str(e)}"
    
    def _generate_fallback_response(self, query: str) -> str:
        """Genera una respuesta cuando no se encuentra información relevante"""
        response = "Lo siento, no encontré información específica sobre tu consulta en la base de conocimientos."
        
        if any(word in query.lower() for word in ['qué', 'what', 'cómo', 'how', 'cuándo', 'when']):
            response += " ¿Podrías reformular tu pregunta o ser más específico?"
        elif any(word in query.lower() for word in ['dónde', 'where', 'quién', 'who']):
            response += " ¿Tienes más detalles sobre lo que buscas?"
        else:
            response += " ¿Te gustaría cargar más documentos o hacer una pregunta diferente?"
        
        return response
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas de la base de conocimientos"""
        return {
            'total_documents': len(self.documents),
            'data_file': self.data_file
        }
    
    def clear_data(self):
        """Limpia todos los datos"""
        self.documents = []
        if os.path.exists(self.data_file):
            os.remove(self.data_file)
        print("✅ Base de conocimientos limpiada")

def main():
    """Función principal del chatbot de consola"""
    print("🤖 Chatbot Personalizado - Versión Consola")
    print("=" * 50)
    
    chatbot = ConsoleChatbot()
    
    while True:
        print("\n" + "=" * 50)
        print("Opciones disponibles:")
        print("1. Hacer una pregunta")
        print("2. Cargar PDFs")
        print("3. Cargar URLs")
        print("4. Ver estadísticas")
        print("5. Limpiar base de datos")
        print("6. Salir")
        
        choice = input("\nSelecciona una opción (1-6): ").strip()
        
        if choice == "1":
            # Hacer pregunta
            query = input("\n¿Qué te gustaría saber? ").strip()
            if query:
                print("\n🤖 Respuesta:")
                print("-" * 30)
                response = chatbot.generate_response(query)
                print(response)
            else:
                print("⚠️ Por favor ingresa una pregunta válida.")
        
        elif choice == "2":
            # Cargar PDFs
            pdf_directory = input("\nIngresa la ruta del directorio con PDFs (o presiona Enter para usar 'pdfs'): ").strip()
            if not pdf_directory:
                pdf_directory = "pdfs"
            
            if os.path.exists(pdf_directory):
                pdf_extractor = PDFExtractor()
                documents = pdf_extractor.extract_text_from_pdfs_in_directory(pdf_directory)
                if documents:
                    chatbot.add_documents(documents)
                else:
                    print("❌ No se encontraron PDFs válidos en el directorio.")
            else:
                print(f"❌ El directorio {pdf_directory} no existe.")
        
        elif choice == "3":
            # Cargar URLs
            print("\nIngresa las URLs (una por línea, termina con una línea vacía):")
            urls = []
            while True:
                url = input().strip()
                if not url:
                    break
                urls.append(url)
            
            if urls:
                web_extractor = WebExtractor()
                documents = web_extractor.extract_from_multiple_urls(urls)
                if documents:
                    chatbot.add_documents(documents)
                else:
                    print("❌ No se pudo extraer contenido de las URLs.")
            else:
                print("⚠️ No se ingresaron URLs válidas.")
        
        elif choice == "4":
            # Ver estadísticas
            stats = chatbot.get_stats()
            print(f"\n📊 Estadísticas:")
            print(f"  - Documentos en BD: {stats['total_documents']}")
            print(f"  - Archivo de datos: {stats['data_file']}")
        
        elif choice == "5":
            # Limpiar base de datos
            confirm = input("\n¿Estás seguro de que quieres limpiar la base de datos? (s/n): ").strip().lower()
            if confirm == 's':
                chatbot.clear_data()
            else:
                print("Operación cancelada.")
        
        elif choice == "6":
            # Salir
            print("\n👋 ¡Hasta luego!")
            break
        
        else:
            print("⚠️ Opción no válida. Por favor selecciona 1-6.")

if __name__ == "__main__":
    main()
