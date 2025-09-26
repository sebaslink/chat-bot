import chromadb
from chromadb.config import Settings
import os
from typing import List, Dict
from sentence_transformers import SentenceTransformer
import numpy as np
from config import Config

class VectorStore:
    def __init__(self):
        self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)
        self.client = chromadb.PersistentClient(path=Config.VECTOR_DB_PATH)
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(self, documents: List[Dict[str, str]]):
        """
        Añade documentos a la base de datos vectorial
        """
        texts = []
        metadatas = []
        ids = []
        
        for i, doc in enumerate(documents):
            # Dividir el documento en chunks si es muy largo
            chunks = self._chunk_text(doc['content'])
            
            for j, chunk in enumerate(chunks):
                if chunk.strip():  # Solo añadir chunks no vacíos
                    texts.append(chunk)
                    metadatas.append({
                        'source': doc.get('source', 'unknown'),
                        'filename': doc.get('filename', ''),
                        'url': doc.get('url', ''),
                        'title': doc.get('title', ''),
                        'chunk_index': j,
                        'total_chunks': len(chunks)
                    })
                    ids.append(f"{doc.get('source', 'unknown')}_{i}_{j}")
        
        if texts:
            # Generar embeddings
            embeddings = self.embedding_model.encode(texts).tolist()
            
            # Añadir a la colección
            self.collection.add(
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"Añadidos {len(texts)} chunks a la base de datos vectorial")
    
    def search_similar_documents(self, query: str, n_results: int = 5) -> List[Dict]:
        """
        Busca documentos similares a la consulta
        """
        # Generar embedding de la consulta
        query_embedding = self.embedding_model.encode([query]).tolist()[0]
        
        # Buscar en la base de datos
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=['documents', 'metadatas', 'distances']
        )
        
        # Formatear resultados
        similar_docs = []
        for i in range(len(results['documents'][0])):
            similar_docs.append({
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i]
            })
        
        return similar_docs
    
    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """
        Divide el texto en fragmentos más pequeños
        """
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
    
    def get_collection_stats(self) -> Dict:
        """
        Obtiene estadísticas de la colección
        """
        count = self.collection.count()
        return {
            'total_documents': count,
            'collection_name': self.collection.name
        }
    
    def clear_collection(self):
        """
        Limpia toda la colección
        """
        self.client.delete_collection("documents")
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
        print("Colección limpiada")
