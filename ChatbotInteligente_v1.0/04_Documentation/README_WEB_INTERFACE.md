# 🌐 Interfaz Web - Cargador de Datos

Una interfaz web moderna y fácil de usar para cargar datos en tu chatbot.

## ✨ Características

- **📄 Carga de PDFs**: Individual o múltiples archivos
- **🌐 URLs**: Extrae contenido de páginas web
- **✏️ Texto Manual**: Añade información directamente
- **📁 Directorios**: Carga todos los PDFs de una carpeta
- **📊 Estadísticas**: Ve el estado de tu base de datos
- **🎨 Interfaz Moderna**: Diseño responsive y atractivo

## 🚀 Instalación

### 1. Instalar dependencias
```bash
pip install -r requirements_web.txt
```

### 2. Ejecutar la interfaz web
```bash
python start_web_interface.py
```

### 3. Abrir en el navegador
```
http://localhost:5000
```

## 📱 Uso de la Interfaz

### Subir PDFs
1. Ve a la pestaña **"PDFs"**
2. Selecciona uno o múltiples archivos PDF
3. Haz clic en **"Subir PDF"** o **"Subir PDFs"**

### Cargar URLs
1. Ve a la pestaña **"URLs"**
2. Ingresa la URL de la página web
3. Opcionalmente añade un título personalizado
4. Haz clic en **"Cargar URL"**

### Añadir Texto Manual
1. Ve a la pestaña **"Texto"**
2. Escribe un título para tu documento
3. Añade el contenido que quieres que aprenda el chatbot
4. Haz clic en **"Añadir Texto"**

### Cargar Directorio
1. Ve a la pestaña **"Directorio"**
2. Ingresa la ruta completa del directorio con PDFs
3. Haz clic en **"Cargar Directorio"**

## 📊 Estadísticas

La barra superior muestra:
- **Total de documentos** cargados
- **PDFs** procesados
- **URLs** cargadas
- **Texto manual** añadido

## 🛠️ Funciones Avanzadas

### Limpiar Base de Datos
- Botón rojo **"Limpiar Base de Datos"**
- ⚠️ **CUIDADO**: Esta acción elimina todos los datos

### Actualizar Estadísticas
- Botón verde **"Actualizar Estadísticas"**
- Refresca los contadores en tiempo real

## 📁 Estructura de Archivos

```
chat bot/
├── web_data_loader.py          # Aplicación Flask principal
├── start_web_interface.py      # Script de inicio
├── requirements_web.txt        # Dependencias web
├── templates/
│   └── index.html             # Interfaz HTML
├── uploads/                   # Archivos temporales (se crea automáticamente)
└── knowledge_base.json        # Base de datos (se crea automáticamente)
```

## 🔧 Configuración

### Cambiar Puerto
Edita `web_data_loader.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Cambia 5000 por tu puerto
```

### Cambiar Clave Secreta
Edita `web_data_loader.py`:
```python
app.secret_key = 'tu_clave_secreta_aqui'  # Cambia por una clave segura
```

## 🐛 Solución de Problemas

### Error: "No se pudo importar Flask"
```bash
pip install flask
```

### Error: "PyPDF2 no está instalado"
```bash
pip install PyPDF2
```

### Error: "requests no está instalado"
```bash
pip install requests beautifulsoup4
```

### Puerto ya en uso
Cambia el puerto en `web_data_loader.py` o cierra la aplicación que usa el puerto 5000.

## 📝 Notas

- Los archivos PDF se procesan temporalmente y se eliminan después de cargar
- El contenido web se limita a 10,000 caracteres por URL
- Los textos largos se dividen automáticamente en fragmentos
- La interfaz es completamente responsive (funciona en móviles)

## 🎯 Próximos Pasos

Después de cargar tus datos:
1. Usa `python start_chatbot.py` para iniciar el chat
2. Selecciona "Solo chat" para usar los datos cargados
3. ¡Disfruta conversando con tu chatbot personalizado!

---

**¡Disfruta cargando datos de forma fácil y visual! 🚀**
