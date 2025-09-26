import json
import os
import numpy as np
from typing import List, Dict
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SimpleVectorStore:
    def __init__(self, data_file="knowledge_base.json"):
        self.data_file = data_file
        self.documents = []
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.document_vectors = None
        self.load_data()
    
    def load_data(self):
        """Carga datos existentes del archivo JSON"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.documents = data.get('documents', [])
                    if self.documents:
                        self._build_vectors()
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
        
        # Reconstruir vectores
        self._build_vectors()
        # Guardar datos
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
    
    def _build_vectors(self):
        """Construye los vectores TF-IDF para todos los documentos"""
        if not self.documents:
            return
        
        try:
            texts = [doc['content'] for doc in self.documents]
            self.document_vectors = self.vectorizer.fit_transform(texts)
            print(f"✅ Vectores construidos para {len(texts)} documentos")
        except Exception as e:
            print(f"❌ Error construyendo vectores: {e}")
            self.document_vectors = None
    
    def search_similar_documents(self, query: str, n_results: int = 5) -> List[Dict]:
        """Busca documentos similares a la consulta"""
        if not self.documents or self.document_vectors is None:
            return []
        
        try:
            # Vectorizar la consulta
            query_vector = self.vectorizer.transform([query])
            
            # Calcular similitud coseno
            similarities = cosine_similarity(query_vector, self.document_vectors).flatten()
            
            # Obtener los índices de los documentos más similares
            top_indices = similarities.argsort()[-n_results:][::-1]
            
            # Formatear resultados
            results = []
            for idx in top_indices:
                if similarities[idx] > 0.1:  # Umbral mínimo de similitud
                    results.append({
                        'content': self.documents[idx]['content'],
                        'metadata': {
                            'source': self.documents[idx]['source'],
                            'filename': self.documents[idx]['filename'],
                            'url': self.documents[idx]['url'],
                            'title': self.documents[idx]['title']
                        },
                        'similarity': float(similarities[idx])
                    })
            
            return results
            
        except Exception as e:
            print(f"❌ Error en búsqueda: {e}")
            return []
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas de la base de conocimientos"""
        return {
            'total_documents': len(self.documents),
            'data_file': self.data_file,
            'has_vectors': self.document_vectors is not None
        }
    
    def clear_data(self):
        """Limpia todos los datos"""
        self.documents = []
        self.document_vectors = None
        if os.path.exists(self.data_file):
            os.remove(self.data_file)
        print("✅ Base de conocimientos limpiada")
