import streamlit as st
import os
from chatbot import Chatbot
from pdf_extractor import PDFExtractor
from web_extractor import WebExtractor
from config import Config

# Configuración de la página
st.set_page_config(
    page_title=Config.PAGE_TITLE,
    page_icon=Config.PAGE_ICON,
    layout="wide"
)

# Inicializar el chatbot
@st.cache_resource
def get_chatbot():
    return Chatbot()

chatbot = get_chatbot()

# Título principal
st.title("🤖 Chatbot Personalizado")
st.markdown("---")

# Sidebar para configuración
with st.sidebar:
    st.header("📚 Gestión de Conocimiento")
    
    # Sección de PDFs
    st.subheader("📄 Cargar PDFs")
    uploaded_pdfs = st.file_uploader(
        "Selecciona archivos PDF",
        type=['pdf'],
        accept_multiple_files=True
    )
    
    if st.button("Procesar PDFs", type="primary"):
        if uploaded_pdfs:
            with st.spinner("Procesando PDFs..."):
                pdf_extractor = PDFExtractor()
                documents = []
                
                for pdf_file in uploaded_pdfs:
                    # Guardar archivo temporalmente
                    temp_path = f"temp_{pdf_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(pdf_file.getbuffer())
                    
                    # Extraer texto
                    text = pdf_extractor.extract_text_from_pdf(temp_path)
                    if text:
                        documents.append({
                            'filename': pdf_file.name,
                            'content': text,
                            'source': 'pdf'
                        })
                    
                    # Limpiar archivo temporal
                    os.remove(temp_path)
                
                if documents:
                    chatbot.add_documents(documents)
                    st.success(f"✅ Procesados {len(documents)} PDFs exitosamente")
                else:
                    st.error("❌ No se pudo extraer texto de los PDFs")
        else:
            st.warning("⚠️ Por favor selecciona al menos un archivo PDF")
    
    # Sección de URLs
    st.subheader("🌐 Cargar URLs")
    urls_text = st.text_area(
        "Ingresa URLs (una por línea)",
        placeholder="https://ejemplo.com\nhttps://otro-sitio.com"
    )
    
    if st.button("Procesar URLs", type="primary"):
        if urls_text:
            urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
            if urls:
                with st.spinner("Procesando URLs..."):
                    web_extractor = WebExtractor()
                    documents = web_extractor.extract_from_multiple_urls(urls)
                    
                    if documents:
                        chatbot.add_documents(documents)
                        st.success(f"✅ Procesadas {len(documents)} URLs exitosamente")
                    else:
                        st.error("❌ No se pudo extraer contenido de las URLs")
            else:
                st.warning("⚠️ Por favor ingresa al menos una URL válida")
        else:
            st.warning("⚠️ Por favor ingresa al menos una URL")
    
    # Estadísticas
    st.subheader("📊 Estadísticas")
    stats = chatbot.get_knowledge_stats()
    st.metric("Documentos en BD", stats['total_documents'])
    
    # Limpiar base de datos
    if st.button("🗑️ Limpiar Base de Datos", type="secondary"):
        chatbot.clear_knowledge_base()
        st.success("✅ Base de datos limpiada")
        st.rerun()

# Área principal de chat
st.header("💬 Chat con el Bot")

# Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial de chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input del usuario
if prompt := st.chat_input("Escribe tu pregunta aquí..."):
    # Añadir mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generar respuesta
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = chatbot.generate_response(
                prompt, 
                st.session_state.messages[:-1]  # Excluir el mensaje actual
            )
        st.markdown(response)
    
    # Añadir respuesta del bot
    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Chatbot personalizado con RAG | Powered by OpenAI & Streamlit</p>
    </div>
    """, 
    unsafe_allow_html=True
)
