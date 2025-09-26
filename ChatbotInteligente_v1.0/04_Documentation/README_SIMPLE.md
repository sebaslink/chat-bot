# 🤖 Chatbot Personalizado - Versión Ultra Simple

Un chatbot inteligente que funciona **solo con Python estándar** (sin dependencias externas complejas) para proporcionar respuestas basadas en información personalizada.

## ✨ Características

- **Sin dependencias externas**: Funciona solo con Python estándar
- **Almacenamiento en JSON**: Base de datos simple y portable
- **Búsqueda inteligente**: Encuentra información relevante usando similitud de texto
- **Interfaz de consola**: Fácil de usar desde la terminal
- **Persistencia**: Los datos se guardan automáticamente
- **Flexible**: Añade información de cualquier fuente

## 🚀 Instalación y Uso

### Requisitos
- Python 3.6 o superior
- **¡Eso es todo!** No necesitas instalar nada más.

### Uso Rápido

1. **Ejecuta el chatbot**:
```bash
python ultra_simple_chatbot.py
```

2. **Añade información**:
   - Selecciona opción 2
   - Ingresa un título y fuente
   - Pega tu contenido
   - Escribe "FIN" para terminar

3. **Haz preguntas**:
   - Selecciona opción 1
   - Escribe tu pregunta
   - Recibe respuestas basadas en tu información

## 📖 Guía de Uso

### Menú Principal
```
1. Hacer una pregunta
2. Añadir texto manualmente
3. Ver estadísticas
4. Limpiar base de datos
5. Salir
```

### Añadir Información

**Opción 2: Añadir texto manualmente**
- Título: Nombre descriptivo del documento
- Fuente: Origen de la información (ej: "manual", "web", "pdf")
- Contenido: Pega todo el texto que quieres que el bot conozca
- Termina con "FIN" en una línea separada

**Ejemplo:**
```
Título del documento: Manual de Python
Fuente: manual
Ingresa el contenido:
Python es un lenguaje de programación...
[tu contenido aquí]
FIN
```

### Hacer Preguntas

**Opción 1: Hacer una pregunta**
- Escribe tu pregunta en lenguaje natural
- El bot buscará información relevante
- Te dará respuestas basadas en el contenido cargado

**Ejemplos de preguntas:**
- "¿Qué es Python?"
- "¿Cómo funciona la programación?"
- "Explícame sobre [tema específico]"

## 📁 Archivos del Proyecto

```
chat-bot/
├── ultra_simple_chatbot.py    # Chatbot principal (¡ÚNICO ARCHIVO NECESARIO!)
├── knowledge_base.json        # Base de datos (se crea automáticamente)
├── pdf_extractor.py          # Para PDFs (opcional)
├── web_extractor.py          # Para web (opcional)
├── console_chatbot.py        # Versión con dependencias externas
├── simple_app.py             # Versión con Streamlit
└── README_SIMPLE.md          # Esta guía
```

## 🔧 Funcionalidades Avanzadas

### Búsqueda Inteligente
- Encuentra información por palabras clave
- Ordena resultados por relevancia
- Muestra fragmentos más relevantes

### Gestión de Datos
- Almacenamiento automático en JSON
- División inteligente de textos largos
- Metadatos de origen para cada fragmento

### Interfaz Amigable
- Menú intuitivo
- Mensajes claros y útiles
- Manejo de errores robusto

## 📊 Estadísticas

**Opción 3: Ver estadísticas**
- Número total de documentos
- Ubicación del archivo de datos
- Estado de la base de conocimientos

## 🗑️ Limpieza de Datos

**Opción 4: Limpiar base de datos**
- Elimina toda la información cargada
- Confirma antes de proceder
- Útil para empezar de nuevo

## 💡 Consejos de Uso

### Para Mejores Resultados:
1. **Añade información variada**: Diferentes temas y fuentes
2. **Usa títulos descriptivos**: Ayudan a identificar el contenido
3. **Haz preguntas específicas**: Más detalles = mejores respuestas
4. **Revisa las fuentes**: El bot te dice de dónde viene la información

### Ejemplos de Contenido:
- Manuales técnicos
- Artículos de blog
- Documentación
- Notas personales
- Cualquier texto que quieras consultar

## 🚀 Casos de Uso

### Personal
- **Notas de estudio**: Carga tus apuntes y haz preguntas
- **Documentación personal**: Organiza tu información
- **Base de conocimientos**: Crea tu propia Wikipedia personal

### Profesional
- **Manuales de empresa**: Consulta rápida de procedimientos
- **Documentación técnica**: Referencia rápida de APIs
- **Base de datos de clientes**: Información organizada

### Educativo
- **Material de curso**: Carga libros y artículos
- **Apuntes de clase**: Organiza tu aprendizaje
- **Preparación de exámenes**: Repasa con preguntas

## 🔍 Cómo Funciona

1. **Almacenamiento**: Divide el texto en fragmentos manejables
2. **Indexación**: Crea un índice de palabras para búsqueda rápida
3. **Búsqueda**: Encuentra fragmentos con palabras en común
4. **Ranking**: Ordena por relevancia (más palabras comunes = más relevante)
5. **Respuesta**: Construye una respuesta basada en los fragmentos más relevantes

## 🛠️ Personalización

### Modificar el Código
- Cambia `chunk_size` para fragmentos más grandes/pequeños
- Ajusta `n_results` para más/menos resultados
- Modifica los mensajes de respuesta

### Añadir Funcionalidades
- Integración con archivos
- Búsqueda por fecha
- Categorización automática
- Exportar/importar datos

## 🐛 Solución de Problemas

### Error: "No se puede importar"
- Asegúrate de usar Python 3.6+
- Verifica que el archivo esté en el directorio correcto

### Error: "No se encuentra información"
- Añade más contenido a la base de datos
- Reformula tu pregunta
- Usa palabras clave más específicas

### Error: "Archivo no encontrado"
- El archivo `knowledge_base.json` se crea automáticamente
- Verifica permisos de escritura en el directorio

## 📈 Próximas Mejoras

- [ ] Interfaz web simple
- [ ] Soporte para archivos PDF
- [ ] Extracción de contenido web
- [ ] Búsqueda por categorías
- [ ] Exportar conversaciones
- [ ] Múltiples bases de datos

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Ideas para mejorar:
- Mejores algoritmos de búsqueda
- Interfaz más amigable
- Nuevas funcionalidades
- Optimizaciones de rendimiento

## 📞 Soporte

Si tienes problemas:
1. Revisa esta documentación
2. Verifica que Python funcione correctamente
3. Prueba con contenido simple primero
4. Revisa los mensajes de error

---

## 🎉 ¡Disfruta tu Chatbot Personalizado!

Este chatbot te permite crear tu propia base de conocimientos personalizada usando solo Python. Es perfecto para:
- Estudiantes que quieren organizar sus apuntes
- Profesionales que necesitan consultar documentación
- Cualquier persona que quiera una "memoria externa" inteligente

**¡Empieza añadiendo información y haz tu primera pregunta!** 🚀
