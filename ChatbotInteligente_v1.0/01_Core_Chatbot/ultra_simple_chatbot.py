#!/usr/bin/env python3
"""
Chatbot ultra simple que funciona solo con Python estándar
"""

import json
import os
import re
from typing import List, Dict

class UltraSimpleChatbot:
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
    
    def add_text_document(self, content: str, source: str = "manual", title: str = ""):
        """Añade un documento de texto a la base de conocimientos"""
        if not content.strip():
            print("⚠️ El contenido no puede estar vacío")
            return
        
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
        """Busca documentos relevantes usando búsqueda inteligente y precisa"""
        if not self.documents:
            return []
        
        query_lower = query.lower()
        query_words = set(query_lower.split())
        scored_docs = []
        
        for doc in self.documents:
            content_lower = doc['content'].lower()
            content_words = set(content_lower.split())
            
            # Calcular múltiples tipos de similitud
            score = 0
            
            # 1. Coincidencia exacta de palabras (peso alto)
            common_words = query_words.intersection(content_words)
            if common_words:
                exact_score = len(common_words) / len(query_words)
                score += exact_score * 0.5
            
            # 2. Coincidencia de frases completas (peso muy alto)
            if len(query_lower) > 3 and query_lower in content_lower:
                score += 0.8
            
            # 3. Coincidencia de frases parciales (peso medio)
            phrase_score = self._calculate_phrase_similarity(query_lower, content_lower)
            score += phrase_score * 0.3
            
            # 4. Coincidencia semántica (peso medio)
            semantic_score = self._calculate_semantic_similarity(query_words, content_words)
            score += semantic_score * 0.2
            
            # 5. Bonus por título relevante (peso alto)
            if doc.get('title'):
                title_lower = doc['title'].lower()
                title_words = set(title_lower.split())
                title_common = query_words.intersection(title_words)
                if title_common:
                    title_score = len(title_common) / len(query_words)
                    score += title_score * 0.3
                
                # Bonus extra si la consulta está en el título
                if query_lower in title_lower:
                    score += 0.5
            
            # 6. Bonus por tipo de fuente relevante
            source_bonus = self._calculate_source_relevance(query_lower, doc['source'])
            score += source_bonus * 0.1
            
            # 7. Bonus por longitud del contenido (contenido más largo = más información)
            if len(doc['content']) > 500:
                score += 0.1
            
            if score > 0:
                scored_docs.append((doc, score))
        
        # Ordenar por puntuación
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        
        return [doc for doc, score in scored_docs[:n_results]]
    
    def _calculate_phrase_similarity(self, query: str, content: str) -> float:
        """Calcula similitud por frases completas"""
        query_phrases = [phrase.strip() for phrase in query.split() if len(phrase.strip()) > 2]
        if not query_phrases:
            return 0
        
        matches = 0
        for phrase in query_phrases:
            if phrase in content:
                matches += 1
        
        return matches / len(query_phrases)
    
    def _calculate_semantic_similarity(self, query_words: set, content_words: set) -> float:
        """Calcula similitud semántica simple usando sinónimos básicos"""
        # Diccionario simple de sinónimos
        synonyms = {
            'información': ['info', 'datos', 'contenido', 'detalles'],
            'documento': ['archivo', 'texto', 'contenido'],
            'página': ['web', 'sitio', 'url'],
            'universidad': ['universidad', 'institución', 'centro', 'escuela'],
            'carrera': ['programa', 'estudio', 'carrera'],
            'estudiante': ['alumno', 'estudiante', 'estudiante'],
            'profesor': ['docente', 'maestro', 'profesor'],
            'curso': ['materia', 'asignatura', 'curso'],
            'campus': ['sede', 'campus', 'instalación']
        }
        
        # Expandir palabras de consulta con sinónimos
        expanded_query = query_words.copy()
        for word in query_words:
            for key, syns in synonyms.items():
                if word in syns or key in word:
                    expanded_query.update(syns)
        
        # Calcular intersección con palabras expandidas
        common_words = expanded_query.intersection(content_words)
        if not query_words:
            return 0
        
        return len(common_words) / len(query_words)
    
    def _calculate_source_relevance(self, query: str, source: str) -> float:
        """Calcula relevancia basada en el tipo de fuente"""
        source_relevance = {
            'web': 0.1,  # Las páginas web suelen tener información más actualizada
            'pdf': 0.05,  # Los PDFs pueden tener información más detallada
            'manual': 0.02,  # El texto manual es menos prioritario
            'url': 0.1
        }
        
        # Bonus adicional si la consulta menciona el tipo de fuente
        if 'web' in query or 'página' in query or 'sitio' in query:
            return source_relevance.get(source, 0) + 0.05
        elif 'pdf' in query or 'documento' in query:
            return source_relevance.get(source, 0) + 0.05
        
        return source_relevance.get(source, 0)
    
    def generate_response(self, user_query: str) -> str:
        """Genera una respuesta natural y exploradora basada en el contenido disponible"""
        try:
            # Analizar el tipo de consulta
            query_type = self._analyze_query_type(user_query)
            
            # Buscar documentos relevantes
            similar_docs = self.search_documents(user_query, n_results=5)
            
            if not similar_docs:
                return self._generate_helpful_fallback_response(user_query, query_type)
            
            # Generar respuesta natural y exploradora
            response = self._generate_exploratory_response(user_query, similar_docs, query_type)
            
            return response
            
        except Exception as e:
            return f"¡Ups! 😅 Hubo un pequeño error procesando tu consulta: {str(e)}. ¿Podrías intentar de nuevo?"
    
    def _analyze_query_type(self, query: str) -> str:
        """Analiza el tipo de consulta del usuario"""
        query_lower = query.lower()
        
        # Saludos
        if any(word in query_lower for word in ['hola', 'hi', 'hello', 'buenos', 'buenas']):
            return 'greeting'
        
        # Preguntas sobre información disponible
        if any(word in query_lower for word in ['qué', 'que', 'información', 'info', 'tienes', 'disponible', 'contenido']):
            return 'info_request'
        
        # Preguntas sobre estadísticas
        if any(word in query_lower for word in ['cuántos', 'cuantos', 'documentos', 'archivos', 'procesado', 'cargado']):
            return 'stats_request'
        
        # Preguntas sobre capacidades
        if any(word in query_lower for word in ['puedes', 'hacer', 'ayudar', 'funciones', 'capacidades']):
            return 'capabilities_request'
        
        # Preguntas específicas
        if '?' in query or any(word in query_lower for word in ['cómo', 'como', 'por qué', 'porque', 'cuándo', 'cuando', 'dónde', 'donde']):
            return 'specific_question'
        
        # Solicitudes de resumen
        if any(word in query_lower for word in ['resume', 'resumen', 'resumir', 'principales', 'temas', 'ideas']):
            return 'summary_request'
        
        return 'general'
    
    def _generate_helpful_fallback_response(self, query: str, query_type: str) -> str:
        """Genera una respuesta útil cuando no se encuentra información relevante"""
        responses = {
            'greeting': "¡Hola! 👋 Soy tu asistente personalizado. Aunque no tengo información cargada aún, puedo ayudarte una vez que subas documentos, URLs o texto. ¿Te gustaría saber cómo cargar información?",
            'info_request': "🤔 No tengo información cargada en este momento. Para poder ayudarte, necesito que primero cargues algunos documentos, URLs o texto. ¿Quieres que te explique cómo hacerlo?",
            'stats_request': f"📊 Actualmente tengo {len(self.documents)} documentos en mi base de conocimientos. Si no ves información, es posible que necesites cargar más contenido.",
            'capabilities_request': "🚀 Puedo ayudarte a analizar y responder preguntas sobre documentos PDF, contenido de páginas web, y texto que hayas cargado. ¡Solo necesito que primero subas algo de información!",
            'summary_request': "📝 Me encantaría hacer un resumen, pero primero necesito que cargues algunos documentos o URLs para poder analizarlos.",
            'general': "🤷‍♂️ No encontré información específica sobre tu consulta. ¿Podrías ser más específico o cargar algunos documentos primero?"
        }
        
        return responses.get(query_type, responses['general'])
    
    def _generate_exploratory_response(self, query: str, similar_docs: list, query_type: str) -> str:
        """Genera una respuesta directa y natural"""
        response_parts = []
        
        # Respuesta directa basada en el tipo de consulta
        if query_type == 'greeting':
            response_parts.append("¡Hola! 👋")
        elif query_type == 'info_request':
            response_parts.append("Te cuento lo que encontré:")
        elif query_type == 'stats_request':
            response_parts.append(f"📊 Tengo {len(self.documents)} documentos cargados. Aquí está la información:")
        else:
            response_parts.append("Basándome en la información disponible:")
        
            response_parts.append("")
        
        # Presentar información de manera directa y natural
        for i, doc in enumerate(similar_docs[:2], 1):
            # Extraer información específica y relevante
            key_info = self._extract_key_information(doc['content'], query)
            
            if key_info:
                # Presentar de manera más natural
                if i == 1:
                    response_parts.append(f"{key_info}")
                else:
                    response_parts.append("")
                    response_parts.append(f"También encontré:")
                    response_parts.append(f"{key_info}")
        
        # Información adicional si hay más documentos
        if len(similar_docs) > 2:
            additional_count = len(similar_docs) - 2
            response_parts.append("")
            response_parts.append(f"💡 Hay {additional_count} fuentes más con información relacionada.")
        
        # Pregunta de seguimiento más natural
        response_parts.append("")
        if query_type == 'specific_question':
            response_parts.append("¿Te gustaría que profundice en algún aspecto específico?")
        elif query_type == 'summary_request':
            response_parts.append("¿Necesitas más detalles sobre algún tema en particular?")
        else:
            response_parts.append("¿Hay algo más específico que te gustaría saber?")
        
        return "\n".join(response_parts)
    
    def _get_source_type_emoji(self, source: str) -> str:
        """Obtiene un emoji representativo del tipo de fuente"""
        source_emojis = {
            'web': '🌐',
            'pdf': '📄',
            'manual': '✏️',
            'url': '🔗'
        }
        return source_emojis.get(source, '📚')
    
    def _get_friendly_source_name(self, doc: dict) -> str:
        """Obtiene un nombre amigable para la fuente"""
        if doc.get('title') and doc['title'] != doc.get('source', ''):
            return doc['title']
        elif doc['source'] == 'web':
            return "Página Web"
        elif doc['source'] == 'pdf':
            return "Documento PDF"
        elif doc['source'] == 'manual':
            return "Texto Manual"
        else:
            return doc['source'].title()
    
    def _extract_key_information(self, content: str, query: str) -> str:
        """Extrae información clave del contenido basada en la consulta"""
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        # Dividir en oraciones más inteligentemente
        sentences = []
        for delimiter in ['.', '!', '?', '\n']:
            if delimiter in content:
                sentences.extend([s.strip() for s in content.split(delimiter) if s.strip()])
                break
        
        if not sentences:
            sentences = [content]
        
        # Calcular relevancia de cada oración
        scored_sentences = []
        for sentence in sentences:
            if len(sentence) < 10:  # Ignorar oraciones muy cortas
                continue
                
            sentence_lower = sentence.lower()
            score = 0
            
            # Puntuación por palabras clave exactas
            for word in query_words:
                if word in sentence_lower:
                    score += 2
            
            # Puntuación por frases completas
            if len(query_lower) > 3 and query_lower in sentence_lower:
                score += 5
            
            # Puntuación por palabras relacionadas
            related_words = self._get_related_words(query_words)
            for word in related_words:
                if word in sentence_lower:
                    score += 1
            
            if score > 0:
                scored_sentences.append((sentence, score))
        
        # Ordenar por relevancia
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        
        if scored_sentences:
            # Tomar las 2 oraciones más relevantes
            best_sentences = [sentence for sentence, score in scored_sentences[:2]]
            return '. '.join(best_sentences) + '.'
        else:
            # Si no hay coincidencias, tomar las primeras oraciones informativas
            informative_sentences = [s for s in sentences[:3] if len(s) > 20]
            if informative_sentences:
                return '. '.join(informative_sentences[:2]) + '.'
            else:
                return content[:200] + '...' if len(content) > 200 else content
    
    def _get_related_words(self, query_words: set) -> set:
        """Obtiene palabras relacionadas para mejorar la búsqueda"""
        related_words = set()
        
        # Diccionario de sinónimos y palabras relacionadas
        synonyms = {
            'universidad': ['institución', 'centro', 'escuela', 'campus', 'sede'],
            'carrera': ['programa', 'estudio', 'especialidad', 'profesión'],
            'medicina': ['salud', 'médico', 'hospital', 'clínica', 'enfermería'],
            'estudiante': ['alumno', 'estudiante', 'estudiante'],
            'profesor': ['docente', 'maestro', 'catedrático'],
            'curso': ['materia', 'asignatura', 'clase', 'módulo'],
            'información': ['info', 'datos', 'contenido', 'detalles'],
            'precio': ['costo', 'valor', 'tarifa', 'pago'],
            'requisitos': ['requisito', 'requisito', 'condición', 'necesario'],
            'duración': ['tiempo', 'período', 'años', 'meses'],
            'modalidad': ['presencial', 'virtual', 'online', 'híbrido'],
            'horario': ['horario', 'horario', 'turno', 'jornada'],
            'certificado': ['título', 'diploma', 'certificación', 'grado']
        }
        
        for word in query_words:
            for key, related in synonyms.items():
                if word in related or key in word:
                    related_words.update(related)
                    related_words.add(key)
        
        return related_words
    
    def _generate_exploration_suggestions(self, query: str, similar_docs: list) -> str:
        """Genera sugerencias para explorar más"""
        suggestions = []
        
        # Analizar temas encontrados
        topics = set()
        for doc in similar_docs:
            if doc.get('title'):
                topics.add(doc['title'])
        
        if topics:
            suggestions.append(f"🎯 **Temas relacionados que podrías explorar:**")
            for topic in list(topics)[:3]:
                suggestions.append(f"• {topic}")
            suggestions.append("")
        
        # Sugerencias de seguimiento
        suggestions.append("💬 **¿Te gustaría que profundice en algún tema específico?**")
        suggestions.append("Puedes preguntarme sobre:")
        suggestions.append("• Detalles específicos de cualquier tema")
        suggestions.append("• Más información sobre las fuentes")
        suggestions.append("• Resúmenes de contenido específico")
        
        return "\n".join(suggestions)
    
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
    """Función principal del chatbot ultra simple"""
    print("🤖 Chatbot Personalizado - Versión Ultra Simple")
    print("=" * 60)
    
    chatbot = UltraSimpleChatbot()
    
    while True:
        print("\n" + "=" * 60)
        print("Opciones disponibles:")
        print("1. Hacer una pregunta")
        print("2. Añadir texto manualmente")
        print("3. Ver estadísticas")
        print("4. Limpiar base de datos")
        print("5. Salir")
        
        choice = input("\nSelecciona una opción (1-5): ").strip()
        
        if choice == "1":
            # Hacer pregunta
            query = input("\n¿Qué te gustaría saber? ").strip()
            if query:
                print("\n🤖 Respuesta:")
                print("-" * 40)
                response = chatbot.generate_response(query)
                print(response)
            else:
                print("⚠️ Por favor ingresa una pregunta válida.")
        
        elif choice == "2":
            # Añadir texto manualmente
            print("\nAñadir información a la base de conocimientos:")
            title = input("Título del documento (opcional): ").strip()
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
                chatbot.add_text_document(content, source, title)
            else:
                print("⚠️ No se ingresó contenido válido.")
        
        elif choice == "3":
            # Ver estadísticas
            stats = chatbot.get_stats()
            print(f"\n📊 Estadísticas:")
            print(f"  - Documentos en BD: {stats['total_documents']}")
            print(f"  - Archivo de datos: {stats['data_file']}")
        
        elif choice == "4":
            # Limpiar base de datos
            confirm = input("\n¿Estás seguro de que quieres limpiar la base de datos? (s/n): ").strip().lower()
            if confirm == 's':
                chatbot.clear_data()
            else:
                print("Operación cancelada.")
        
        elif choice == "5":
            # Salir
            print("\n👋 ¡Hasta luego!")
            break
        
        else:
            print("⚠️ Opción no válida. Por favor selecciona 1-5.")

if __name__ == "__main__":
    main()
