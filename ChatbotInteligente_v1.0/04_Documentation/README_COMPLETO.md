# 🤖 Chatbot Personalizado - Sistema Completo

Un sistema completo de chatbot que permite cargar información desde PDFs, URLs y texto manual, y luego responder preguntas basándose en esa información.

## 🚀 Inicio Rápido

### Opción 1: Inicio Automático (Recomendado)
```bash
python start_chatbot.py
```

### Opción 2: Inicio Directo
```bash
python main_chatbot.py
```

## 📁 Archivos del Sistema

### Archivos Principales
- **`start_chatbot.py`** - Script de inicio con opciones
- **`main_chatbot.py`** - Chatbot completo con cargador integrado
- **`data_loader.py`** - Cargador independiente de datos
- **`ultra_simple_chatbot.py`** - Chatbot básico (solo texto manual)

### Archivos de Soporte
- **`pdf_extractor.py`** - Extracción de PDFs
- **`web_extractor.py`** - Extracción de contenido web
- **`knowledge_base.json`** - Base de datos (se crea automáticamente)

## 🎯 Flujo de Trabajo Recomendado

### 1. Cargar Datos Primero
```
python start_chatbot.py
→ Selecciona opción 1 (Inicio completo)
→ Selecciona opción 2, 3, 4 o 5 (Cargar datos)
→ Carga tus PDFs, URLs o texto
```

### 2. Usar el Chat
```
→ Selecciona opción 1 (Iniciar Chat)
→ Haz tus preguntas
→ Escribe 'salir' para volver al menú
```

## 📚 Opciones de Carga de Datos

### 📄 Cargar PDFs
**Opción 2: Cargar PDFs de directorio**
- Coloca todos tus PDFs en una carpeta
- Selecciona la opción 2
- Ingresa la ruta de la carpeta
- El sistema procesará todos los PDFs automáticamente

**Opción 3: Cargar PDF individual**
- Selecciona la opción 3
- Ingresa la ruta completa del archivo PDF
- El sistema procesará solo ese PDF

### 🌐 Cargar URLs
**Opción 4: Cargar URLs**
- Selecciona la opción 4
- Ingresa las URLs una por línea
- Termina con una línea vacía
- El sistema extraerá el contenido de cada URL

### ✏️ Añadir Texto Manual
**Opción 5: Añadir texto manual**
- Selecciona la opción 5
- Ingresa un título descriptivo
- Especifica la fuente
- Pega tu contenido
- Termina con "FIN" en una línea separada

## 💬 Uso del Chat

### Iniciar Chat
1. Selecciona "1. 💬 Iniciar Chat"
2. Escribe tu pregunta
3. Recibe respuestas basadas en tu información
4. Escribe "salir" para volver al menú

### Tipos de Preguntas
- **Preguntas directas**: "¿Qué es Python?"
- **Preguntas específicas**: "¿Cómo funciona la programación orientada a objetos?"
- **Búsquedas**: "Información sobre machine learning"
- **Comparaciones**: "Diferencias entre Python y Java"

## 📊 Gestión de Datos

### Ver Estadísticas
- Selecciona "6. 📊 Ver estadísticas"
- Ve cuántos documentos tienes cargados
- Revisa las fuentes de información

### Limpiar Base de Datos
- Selecciona "7. 🗑️ Limpiar base de datos"
- Confirma la operación
- Elimina toda la información cargada

## 🔧 Instalación de Dependencias

### Dependencias Básicas (Solo texto manual)
```bash
# No necesitas instalar nada
python ultra_simple_chatbot.py
```

### Dependencias Completas (PDFs y URLs)
```bash
pip install PyPDF2 requests beautifulsoup4
```

### Verificar Instalación
```bash
python start_chatbot.py
# El sistema verificará automáticamente las dependencias
```

## 🎯 Casos de Uso

### Para Estudiantes
1. **Cargar apuntes**: Sube PDFs de tus clases
2. **Cargar artículos**: URLs de papers y artículos
3. **Hacer preguntas**: "Explícame el tema X de la clase Y"

### Para Profesionales
1. **Cargar manuales**: PDFs de documentación técnica
2. **Cargar sitios web**: URLs de documentación oficial
3. **Consultar información**: "¿Cómo implementar X en Y?"

### Para Investigadores
1. **Cargar papers**: PDFs de artículos científicos
2. **Cargar fuentes**: URLs de bases de datos
3. **Hacer consultas**: "¿Qué dice la literatura sobre X?"

## 📈 Características Avanzadas

### Búsqueda Inteligente
- Encuentra información por palabras clave
- Ordena resultados por relevancia
- Muestra fragmentos más relevantes
- Indica la fuente de cada información

### Almacenamiento Persistente
- Los datos se guardan automáticamente
- Persiste entre sesiones
- Archivo JSON portable
- Fácil de respaldar

### División Inteligente
- Divide textos largos en fragmentos manejables
- Mantiene el contexto
- Optimiza la búsqueda

## 🛠️ Personalización

### Modificar Tamaño de Fragmentos
En `main_chatbot.py`, línea ~50:
```python
def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200):
    # Cambia chunk_size para fragmentos más grandes/pequeños
```

### Modificar Número de Resultados
En `main_chatbot.py`, línea ~200:
```python
def search_documents(self, query: str, n_results: int = 3):
    # Cambia n_results para más/menos resultados
```

## 🐛 Solución de Problemas

### Error: "No se puede importar"
- Verifica que todos los archivos estén en el mismo directorio
- Asegúrate de usar Python 3.6+

### Error: "PyPDF2 no está instalado"
```bash
pip install PyPDF2
```

### Error: "requests no está instalado"
```bash
pip install requests beautifulsoup4
```

### Error: "No se encuentra información"
- Añade más contenido a la base de datos
- Reformula tu pregunta
- Usa palabras clave más específicas

### Error: "Archivo no encontrado"
- El archivo `knowledge_base.json` se crea automáticamente
- Verifica permisos de escritura en el directorio

## 📋 Comandos Útiles

### Inicio Rápido
```bash
# Inicio completo
python start_chatbot.py

# Solo chat
python ultra_simple_chatbot.py

# Solo cargar datos
python data_loader.py
```

### Verificar Estado
```bash
# Ver estadísticas
python -c "from main_chatbot import MainChatbot; c = MainChatbot(); print(c.get_stats())"
```

### Limpiar Datos
```bash
# Limpiar base de datos
python -c "from main_chatbot import MainChatbot; c = MainChatbot(); c.clear_data()"
```

## 🎉 ¡Disfruta tu Chatbot Personalizado!

Este sistema te permite crear tu propia base de conocimientos inteligente:

1. **Carga información** desde cualquier fuente
2. **Haz preguntas** en lenguaje natural
3. **Recibe respuestas** basadas en tu contenido
4. **Mantén todo organizado** en una base de datos persistente

**¡Empieza cargando tus primeros documentos y haz tu primera pregunta!** 🚀

## 📞 Soporte

Si tienes problemas:
1. Revisa esta documentación
2. Verifica las dependencias
3. Prueba con contenido simple primero
4. Revisa los mensajes de error

---

**¡Tu chatbot personalizado está listo para usar!** 🤖✨
