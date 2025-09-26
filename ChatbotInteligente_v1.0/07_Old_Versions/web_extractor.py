import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict
from urllib.parse import urljoin, urlparse
from config import Config

class WebExtractor:
    def __init__(self):
        self.max_content_length = Config.MAX_WEB_CONTENT_LENGTH
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def extract_text_from_url(self, url: str) -> str:
        """
        Extrae texto de una URL específica
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
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
            if len(text) > self.max_content_length:
                text = text[:self.max_content_length] + "..."
            
            return text
            
        except Exception as e:
            print(f"Error al extraer contenido de {url}: {str(e)}")
            return ""
    
    def extract_links_from_url(self, url: str, max_links: int = 10) -> List[str]:
        """
        Extrae enlaces de una página web
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            links = []
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(url, href)
                
                # Filtrar enlaces válidos del mismo dominio
                if self._is_valid_url(full_url, url):
                    links.append(full_url)
                    
                if len(links) >= max_links:
                    break
            
            return links
            
        except Exception as e:
            print(f"Error al extraer enlaces de {url}: {str(e)}")
            return []
    
    def _is_valid_url(self, url: str, base_url: str) -> bool:
        """
        Verifica si una URL es válida y del mismo dominio
        """
        try:
            parsed_url = urlparse(url)
            parsed_base = urlparse(base_url)
            
            # Verificar que sea HTTP/HTTPS
            if parsed_url.scheme not in ['http', 'https']:
                return False
            
            # Verificar que sea del mismo dominio (opcional)
            return parsed_url.netloc == parsed_base.netloc
            
        except:
            return False
    
    def extract_from_multiple_urls(self, urls: List[str]) -> List[Dict[str, str]]:
        """
        Extrae contenido de múltiples URLs
        """
        documents = []
        
        for url in urls:
            text = self.extract_text_from_url(url)
            
            if text:
                documents.append({
                    'url': url,
                    'content': text,
                    'source': 'web',
                    'title': self._extract_title_from_url(url)
                })
                print(f"Procesado: {url} ({len(text)} caracteres)")
        
        return documents
    
    def _extract_title_from_url(self, url: str) -> str:
        """
        Extrae el título de una página web
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('title')
            return title.get_text().strip() if title else url
        except:
            return url
    
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
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
        
        return chunks
