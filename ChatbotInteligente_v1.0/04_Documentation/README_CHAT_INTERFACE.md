# 💬 Interfaz Web con Chat Integrado

Una interfaz web completa que combina la carga de datos con un chatbot integrado para pruebas en tiempo real.

## ✨ **Nuevas Características**

### 🤖 **Pestaña de Chat**
- **Chat en tiempo real** con el chatbot
- **Interfaz moderna** tipo WhatsApp/Telegram
- **Indicador de escritura** animado
- **Sugerencias de preguntas** predefinidas
- **Historial de conversación** persistente
- **Estadísticas en vivo** de documentos cargados

### 🎨 **Diseño Mejorado**
- **5 pestañas organizadas**: PDFs, URLs, Texto, Directorio, **Chat**
- **Interfaz responsive** que funciona en móviles
- **Animaciones suaves** y transiciones
- **Colores y gradientes** modernos
- **Iconos FontAwesome** para mejor UX

## 🚀 **Cómo Usar**

### **1. Ejecutar la Interfaz**
```bash
# Opción A: Ejecutable automático
python ejecutar_interfaz_web.py

# Opción B: Directo
python web_data_loader.py

# Opción C: Doble clic (Windows)
EJECUTAR_INTERFAZ_WEB.bat
```

### **2. Abrir en el Navegador**
```
http://localhost:5000
```

### **3. Usar las Pestañas**

#### **📄 PDFs** - Cargar documentos
- Subir PDF individual
- Subir múltiples PDFs
- Vista previa de archivos

#### **🌐 URLs** - Extraer contenido web
- Ingresar URL
- Título personalizado
- Extracción automática

#### **✏️ Texto** - Añadir información manual
- Título del documento
- Contenido libre
- Fuente personalizable

#### **📁 Directorio** - Cargar PDFs masivamente
- Ruta del directorio
- Procesamiento automático

#### **💬 Chat** - ¡NUEVO! Probar el chatbot
- Conversación en tiempo real
- Preguntas sugeridas
- Respuestas basadas en datos cargados
- Estadísticas en vivo

## 🎯 **Funcionalidades del Chat**

### **💬 Conversación Inteligente**
- Respuestas basadas en los datos cargados
- Búsqueda semántica en documentos
- Respuestas contextuales y relevantes

### **🎨 Interfaz de Chat**
- **Mensajes del usuario** (azul, derecha)
- **Mensajes del bot** (gris, izquierda)
- **Avatares** diferenciados
- **Timestamps** en cada mensaje
- **Scroll automático** al final

### **⚡ Características Avanzadas**
- **Indicador de escritura** con animación
- **Sugerencias rápidas** para empezar
- **Envío con Enter** (Shift+Enter para nueva línea)
- **Estadísticas en vivo** de documentos
- **Manejo de errores** elegante

### **🔧 Preguntas Sugeridas**
- "¿Qué información tienes disponible?"
- "Resume el contenido principal"
- "¿Cuántos documentos has procesado?"

## 📊 **Flujo de Trabajo Recomendado**

### **1. Cargar Datos**
1. Ve a las pestañas **PDFs**, **URLs**, **Texto** o **Directorio**
2. Carga tu información
3. Verifica las **estadísticas** en la barra superior

### **2. Probar el Chatbot**
1. Ve a la pestaña **Chat**
2. Haz preguntas sobre tu contenido
3. Usa las **sugerencias** para empezar
4. Observa las **respuestas contextuales**

### **3. Iterar y Mejorar**
1. Añade más datos si es necesario
2. Prueba diferentes preguntas
3. Refina el contenido según las respuestas

## 🛠️ **Configuración Técnica**

### **Archivos Principales**
- `web_data_loader.py` - Aplicación Flask principal
- `templates/index.html` - Interfaz web completa
- `ultra_simple_chatbot.py` - Motor del chatbot
- `data_loader.py` - Gestión de datos

### **Rutas API**
- `POST /chat` - Enviar mensajes al chatbot
- `GET /get_stats` - Obtener estadísticas
- `POST /add_text` - Añadir texto manual
- `POST /upload_pdf` - Subir PDFs
- `POST /add_url` - Cargar URLs

### **Base de Datos**
- `knowledge_base.json` - Datos en formato JSON
- Búsqueda por similitud de palabras
- Fragmentación automática de textos largos

## 🎨 **Personalización**

### **Cambiar Colores del Chat**
Edita `templates/index.html`:
```css
.user-message .message-avatar {
    background: linear-gradient(135deg, #tu-color-1, #tu-color-2);
}
```

### **Añadir Preguntas Sugeridas**
Edita el HTML:
```html
<button class="suggestion-btn" onclick="sendSuggestion('Tu pregunta')">
    Tu pregunta personalizada
</button>
```

### **Modificar Respuestas del Bot**
Edita `ultra_simple_chatbot.py`:
```python
def _generate_fallback_response(self, query: str) -> str:
    return "Tu respuesta personalizada"
```

## 🐛 **Solución de Problemas**

### **Chat no responde**
- Verifica que `ultra_simple_chatbot.py` esté en el directorio
- Comprueba la consola del navegador (F12)
- Asegúrate de que hay datos cargados

### **Error de conexión**
- Verifica que el servidor esté ejecutándose
- Comprueba la URL: `http://localhost:5000`
- Reinicia el servidor si es necesario

### **Respuestas vacías**
- Carga algunos datos primero
- Prueba con preguntas más específicas
- Verifica las estadísticas de documentos

## 🚀 **Próximos Pasos**

1. **Carga tus datos** usando las pestañas de carga
2. **Prueba el chat** con diferentes preguntas
3. **Refina el contenido** según las respuestas
4. **Comparte** la interfaz con otros usuarios
5. **Personaliza** según tus necesidades

---

**¡Disfruta de tu interfaz web completa con chat integrado! 🎉**
