import PyPDF2
import os
from typing import List, Dict
from config import Config

class PDFExtractor:
    def __init__(self):
        self.max_pages = Config.MAX_PDF_PAGES
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extrae texto de un archivo PDF
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                # Limitar el número de páginas a procesar
                max_pages = min(len(pdf_reader.pages), self.max_pages)
                
                for page_num in range(max_pages):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
                
                return text.strip()
        except Exception as e:
            print(f"Error al procesar PDF {pdf_path}: {str(e)}")
            return ""
    
    def extract_text_from_pdfs_in_directory(self, directory_path: str) -> List[Dict[str, str]]:
        """
        Extrae texto de todos los PDFs en un directorio
        """
        documents = []
        
        if not os.path.exists(directory_path):
            print(f"El directorio {directory_path} no existe")
            return documents
        
        for filename in os.listdir(directory_path):
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(directory_path, filename)
                text = self.extract_text_from_pdf(pdf_path)
                
                if text:
                    documents.append({
                        'filename': filename,
                        'content': text,
                        'source': 'pdf',
                        'path': pdf_path
                    })
                    print(f"Procesado: {filename} ({len(text)} caracteres)")
        
        return documents
    
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """
        Divide el texto en fragmentos más pequeños para mejor procesamiento
        """
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Intentar cortar en un punto lógico (final de oración)
            if end < len(text):
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                cut_point = max(last_period, last_newline)
                
                if cut_point > start + chunk_size // 2:  # Solo si el corte es razonable
                    chunk = chunk[:cut_point + 1]
                    end = start + cut_point + 1
            
            chunks.append(chunk.strip())
            start = end - overlap
        
        return chunks
