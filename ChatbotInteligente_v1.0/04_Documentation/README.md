# 🤖 Chatbot Personalizado con RAG

Un chatbot inteligente que se entrena con información de páginas web y documentos PDF para proporcionar respuestas personalizadas y precisas.

## ✨ Características

- **Extracción de PDFs**: Procesa documentos PDF y extrae su contenido
- **Extracción Web**: Obtiene información de páginas web
- **Base de Datos Vectorial**: Almacena y busca información usando embeddings
- **RAG (Retrieval Augmented Generation)**: Combina búsqueda de información con generación de texto
- **Interfaz Web**: Interfaz amigable con Streamlit
- **Chat Persistente**: Mantiene el historial de conversación

## 🚀 Instalación

1. **Clona el repositorio**:
```bash
git clone <tu-repositorio>
cd chat-bot
```

2. **Instala las dependencias**:
```bash
pip install -r requirements.txt
```

3. **Configura las variables de entorno**:
   - Copia `env_example.txt` a `.env`
   - Añade tu clave de API de OpenAI:
```
OPENAI_API_KEY=tu_clave_api_aqui
```

## 📖 Uso

### Opción 1: Interfaz Web (Recomendado)

1. **Ejecuta la aplicación**:
```bash
streamlit run app.py
```

2. **Abre tu navegador** en `http://localhost:8501`

3. **Carga tus datos**:
   - Sube archivos PDF en el sidebar
   - Ingresa URLs de páginas web
   - Haz clic en "Procesar" para cada tipo de contenido

4. **¡Comienza a chatear!** Escribe tus preguntas en el área de chat

### Opción 2: Script de Carga

```bash
python load_data.py
```

## 📁 Estructura del Proyecto

```
chat-bot/
├── app.py                 # Interfaz principal con Streamlit
├── chatbot.py            # Lógica del chatbot con RAG
├── vector_store.py       # Gestión de base de datos vectorial
├── pdf_extractor.py      # Extracción de contenido PDF
├── web_extractor.py      # Extracción de contenido web
├── config.py             # Configuración del proyecto
├── load_data.py          # Script para cargar datos
├── requirements.txt      # Dependencias de Python
├── env_example.txt       # Ejemplo de variables de entorno
└── README.md            # Este archivo
```

## 🔧 Configuración

### Variables de Entorno

- `OPENAI_API_KEY`: Tu clave de API de OpenAI (requerida)
- `VECTOR_DB_PATH`: Ruta de la base de datos vectorial (opcional)
- `EMBEDDING_MODEL`: Modelo de embeddings (opcional)
- `CHAT_MODEL`: Modelo de chat (opcional)

### Personalización

Puedes modificar `config.py` para ajustar:
- Modelos de IA utilizados
- Tamaño de chunks de texto
- Límites de procesamiento
- Configuración de la interfaz

## 📊 Funcionalidades

### Gestión de Documentos
- **PDFs**: Procesa múltiples archivos PDF simultáneamente
- **Web**: Extrae contenido de URLs individuales o múltiples
- **Chunking**: Divide textos largos en fragmentos manejables
- **Metadata**: Almacena información de origen para cada documento

### Búsqueda Inteligente
- **Embeddings**: Convierte texto en vectores para búsqueda semántica
- **Similitud**: Encuentra contenido relevante usando distancia coseno
- **Ranking**: Ordena resultados por relevancia

### Generación de Respuestas
- **RAG**: Combina información recuperada con generación de texto
- **Contexto**: Usa documentos relevantes para generar respuestas precisas
- **Historial**: Mantiene contexto de la conversación

## 🛠️ Desarrollo

### Añadir Nuevos Extractores

1. Crea una nueva clase en un archivo separado
2. Implementa métodos `extract_text()` y `chunk_text()`
3. Integra con `vector_store.py`

### Personalizar el Chatbot

Modifica `chatbot.py` para:
- Cambiar el prompt del sistema
- Ajustar parámetros de generación
- Añadir nuevas funcionalidades

## 🐛 Solución de Problemas

### Error de API Key
```
Error: No se encontró OPENAI_API_KEY
```
**Solución**: Asegúrate de configurar tu clave de API en el archivo `.env`

### Error de Memoria
```
Error: Memoria insuficiente
```
**Solución**: Reduce el tamaño de los chunks en `config.py` o procesa menos documentos a la vez

### Error de Conexión Web
```
Error: No se pudo conectar a la URL
```
**Solución**: Verifica que las URLs sean válidas y accesibles

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📞 Soporte

Si tienes preguntas o problemas:
- Abre un issue en GitHub
- Revisa la documentación
- Consulta los logs de error

---

¡Disfruta usando tu chatbot personalizado! 🚀
