#!/usr/bin/env python3
"""
Chatbot principal con cargador de datos integrado
Permite cargar URLs y PDFs, luego usar el chat
"""

import json
import os
import re
from typing import List, Dict

class MainChatbot:
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
    
    def add_text_document(self, content: str, source: str = "manual", title: str = ""):
        """Añade un documento de texto a la base de conocimientos"""
        if not content.strip():
            print("⚠️ El contenido no puede estar vacío")
            return False
        
        # Dividir en chunks si es muy largo
        chunks = self._chunk_text(content)
        
        for i, chunk in enumerate(chunks):
            if chunk.strip():
                self.documents.append({
                    'id': f"{source}_{len(self.documents)}",
                    'content': chunk,
                    'source': source,
                    'title': title,
                    'chunk_index': i,
                    'total_chunks': len(chunks)
                })
        
        self.save_data()
        print(f"✅ Añadido documento '{title}' con {len(chunks)} fragmentos")
        return True
    
    def load_pdf(self, pdf_path: str) -> bool:
        """Carga un archivo PDF"""
        try:
            import PyPDF2
            
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                # Procesar todas las páginas
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
                
                if text.strip():
                    filename = os.path.basename(pdf_path)
                    return self.add_text_document(text, "pdf", filename)
                else:
                    print(f"❌ No se pudo extraer texto del PDF: {pdf_path}")
                    return False
                    
        except ImportError:
            print("❌ PyPDF2 no está instalado. Instálalo con: pip install PyPDF2")
            return False
        except Exception as e:
            print(f"❌ Error procesando PDF {pdf_path}: {str(e)}")
            return False
    
    def load_pdfs_from_directory(self, directory_path: str) -> int:
        """Carga todos los PDFs de un directorio"""
        if not os.path.exists(directory_path):
            print(f"❌ El directorio {directory_path} no existe")
            return 0
        
        loaded_count = 0
        for filename in os.listdir(directory_path):
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(directory_path, filename)
                print(f"📄 Procesando: {filename}")
                if self.load_pdf(pdf_path):
                    loaded_count += 1
        
        return loaded_count
    
    def load_url(self, url: str) -> bool:
        """Carga contenido de una URL"""
        try:
            import requests
            from bs4 import BeautifulSoup
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remover scripts y estilos
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extraer texto
            text = soup.get_text()
            
            # Limpiar texto
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Limitar longitud
            if len(text) > 10000:
                text = text[:10000] + "..."
            
            if text.strip():
                # Obtener título
                title = soup.find('title')
                title_text = title.get_text().strip() if title else url
                
                return self.add_text_document(text, "web", title_text)
            else:
                print(f"❌ No se pudo extraer contenido de la URL: {url}")
                return False
                
        except ImportError:
            print("❌ requests o beautifulsoup4 no están instalados. Instálalos con: pip install requests beautifulsoup4")
            return False
        except Exception as e:
            print(f"❌ Error procesando URL {url}: {str(e)}")
            return False
    
    def load_urls(self, urls: List[str]) -> int:
        """Carga contenido de múltiples URLs"""
        loaded_count = 0
        for url in urls:
            print(f"🌐 Procesando: {url}")
            if self.load_url(url):
                loaded_count += 1
        
        return loaded_count
    
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
                source_info = f" (Fuente: {doc['source']}"
                if doc.get('title'):
                    source_info += f" - {doc['title']}"
                source_info += ")"
                
                content_preview = doc['content'][:300]
                if len(doc['content']) > 300:
                    content_preview += "..."
                
                response_parts.append(f"{i}. {content_preview}{source_info}")
            
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
            response += " ¿Te gustaría añadir más información o hacer una pregunta diferente?"
        
        return response
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas de la base de conocimientos"""
        sources = {}
        for doc in self.documents:
            source = doc.get('source', 'unknown')
            sources[source] = sources.get(source, 0) + 1
        
        return {
            'total_documents': len(self.documents),
            'sources': sources,
            'data_file': self.data_file
        }
    
    def clear_data(self):
        """Limpia todos los datos"""
        self.documents = []
        if os.path.exists(self.data_file):
            os.remove(self.data_file)
        print("✅ Base de conocimientos limpiada")

def main():
    """Función principal del chatbot con cargador integrado"""
    print("🤖 Chatbot Personalizado - Cargador y Chat Integrado")
    print("=" * 60)
    
    chatbot = MainChatbot()
    
    while True:
        print("\n" + "=" * 60)
        print("Opciones disponibles:")
        print("1. 💬 Iniciar Chat")
        print("2. 📄 Cargar PDFs de directorio")
        print("3. 📄 Cargar PDF individual")
        print("4. 🌐 Cargar URLs")
        print("5. ✏️ Añadir texto manual")
        print("6. 📊 Ver estadísticas")
        print("7. 🗑️ Limpiar base de datos")
        print("8. 🚪 Salir")
        
        choice = input("\nSelecciona una opción (1-8): ").strip()
        
        if choice == "1":
            # Iniciar Chat
            print("\n" + "=" * 60)
            print("💬 CHAT ACTIVO - Escribe 'salir' para volver al menú principal")
            print("=" * 60)
            
            while True:
                query = input("\n🤔 Tu pregunta: ").strip()
                
                if query.lower() in ['salir', 'exit', 'quit', 'volver']:
                    print("👋 Volviendo al menú principal...")
                    break
                
                if query:
                    print("\n🤖 Respuesta:")
                    print("-" * 40)
                    response = chatbot.generate_response(query)
                    print(response)
                else:
                    print("⚠️ Por favor ingresa una pregunta válida.")
        
        elif choice == "2":
            # Cargar PDFs de directorio
            directory = input("\nIngresa la ruta del directorio con PDFs: ").strip()
            if directory:
                count = chatbot.load_pdfs_from_directory(directory)
                print(f"✅ Cargados {count} PDFs exitosamente")
            else:
                print("⚠️ Por favor ingresa una ruta válida.")
        
        elif choice == "3":
            # Cargar PDF individual
            pdf_path = input("\nIngresa la ruta del archivo PDF: ").strip()
            if pdf_path and os.path.exists(pdf_path):
                if chatbot.load_pdf(pdf_path):
                    print("✅ PDF cargado exitosamente")
                else:
                    print("❌ Error cargando el PDF")
            else:
                print("❌ Archivo no encontrado.")
        
        elif choice == "4":
            # Cargar URLs
            print("\nIngresa las URLs (una por línea, termina con una línea vacía):")
            urls = []
            while True:
                url = input().strip()
                if not url:
                    break
                urls.append(url)
            
            if urls:
                count = chatbot.load_urls(urls)
                print(f"✅ Cargadas {count} URLs exitosamente")
            else:
                print("⚠️ No se ingresaron URLs válidas.")
        
        elif choice == "5":
            # Añadir texto manual
            print("\nAñadir información manual:")
            title = input("Título del documento: ").strip()
            source = input("Fuente (ej: 'manual', 'web', 'pdf'): ").strip() or "manual"
            
            print("\nIngresa el contenido (termina con una línea que contenga solo 'FIN'):")
            content_lines = []
            while True:
                line = input()
                if line.strip() == "FIN":
                    break
                content_lines.append(line)
            
            content = "\n".join(content_lines)
            if content.strip():
                if chatbot.add_text_document(content, source, title):
                    print("✅ Texto añadido exitosamente")
            else:
                print("⚠️ No se ingresó contenido válido.")
        
        elif choice == "6":
            # Ver estadísticas
            stats = chatbot.get_stats()
            print(f"\n📊 Estadísticas:")
            print(f"  - Total de documentos: {stats['total_documents']}")
            print(f"  - Archivo de datos: {stats['data_file']}")
            print(f"  - Por fuente:")
            for source, count in stats['sources'].items():
                print(f"    * {source}: {count} documentos")
        
        elif choice == "7":
            # Limpiar base de datos
            confirm = input("\n¿Estás seguro de que quieres limpiar la base de datos? (s/n): ").strip().lower()
            if confirm == 's':
                chatbot.clear_data()
            else:
                print("Operación cancelada.")
        
        elif choice == "8":
            # Salir
            print("\n👋 ¡Hasta luego!")
            break
        
        else:
            print("⚠️ Opción no válida. Por favor selecciona 1-8.")

if __name__ == "__main__":
    main()
