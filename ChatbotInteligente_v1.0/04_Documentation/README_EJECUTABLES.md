# 🚀 Ejecutables para la Interfaz Web

Archivos ejecutables que instalan automáticamente todas las dependencias y ejecutan la interfaz web.

## 📁 Archivos Disponibles

### 🐍 **ejecutar_interfaz_web.py** (Recomendado)
- **Uso**: `python ejecutar_interfaz_web.py`
- **Funciones**:
  - ✅ Instala automáticamente todas las dependencias
  - ✅ Verifica la versión de Python
  - ✅ Crea directorios necesarios
  - ✅ Ejecuta la interfaz web
  - ✅ Manejo de errores completo

### 🪟 **EJECUTAR_INTERFAZ_WEB.bat** (Windows)
- **Uso**: Doble clic o `EJECUTAR_INTERFAZ_WEB.bat`
- **Funciones**:
  - ✅ Verifica Python automáticamente
  - ✅ Ejecuta el script Python
  - ✅ Interfaz visual con colores
  - ✅ Pausa al finalizar

### ⚡ **EJECUTAR_INTERFAZ_WEB.ps1** (PowerShell)
- **Uso**: `.\EJECUTAR_INTERFAZ_WEB.ps1`
- **Funciones**:
  - ✅ Verificación avanzada de Python
  - ✅ Manejo de errores detallado
  - ✅ Interfaz con colores y emojis
  - ✅ Compatible con PowerShell 5.1+

## 🎯 **Uso Rápido**

### Opción 1: Doble Clic (Más Fácil)
1. **Haz doble clic** en `EJECUTAR_INTERFAZ_WEB.bat`
2. **Espera** a que instale las dependencias
3. **Abre** tu navegador en `http://localhost:5000`

### Opción 2: Línea de Comandos
```bash
# Opción A: Python directo
python ejecutar_interfaz_web.py

# Opción B: Batch (Windows)
EJECUTAR_INTERFAZ_WEB.bat

# Opción C: PowerShell
.\EJECUTAR_INTERFAZ_WEB.ps1
```

## ⚙️ **Configuración**

Edita `config_ejecutable.py` para personalizar:

```python
# Cambiar puerto del servidor
SERVER_CONFIG = {
    'port': 8080,  # Cambiar de 5000 a 8080
}

# Añadir dependencias adicionales
REQUIRED_DEPENDENCIES = [
    "Flask==2.3.3",
    # ... otras dependencias
    "mi_paquete_personalizado"  # Añadir aquí
]
```

## 🔧 **Solución de Problemas**

### Error: "Python no encontrado"
```bash
# Instalar Python desde https://python.org
# Asegúrate de marcar "Add Python to PATH"
```

### Error: "Módulo no encontrado"
```bash
# El ejecutable instalará automáticamente las dependencias
# Si falla, ejecuta manualmente:
pip install Flask PyPDF2 requests beautifulsoup4 numpy sentence-transformers
```

### Error: "Puerto en uso"
```bash
# Cambia el puerto en config_ejecutable.py
SERVER_CONFIG = {
    'port': 8080,  # Usar puerto diferente
}
```

### Error: "Permisos de PowerShell"
```powershell
# Ejecutar como administrador o cambiar política:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📊 **Funcionalidades del Ejecutable**

- **🔍 Verificación Automática**: Python, dependencias, archivos
- **📦 Instalación Inteligente**: Solo instala lo que falta
- **🛠️ Configuración Flexible**: Fácil personalización
- **📱 Interfaz Visual**: Colores, emojis, mensajes claros
- **⚠️ Manejo de Errores**: Mensajes informativos
- **🚀 Inicio Rápido**: Un clic y listo

## 🎨 **Personalización Avanzada**

### Cambiar Mensajes
Edita `config_ejecutable.py`:
```python
MESSAGES = {
    'welcome': "🎉 ¡Mi Chatbot Personalizado!",
    'ready': "✅ ¡Listo! Ve a http://localhost:5000"
}
```

### Añadir Dependencias
```python
REQUIRED_DEPENDENCIES = [
    "Flask==2.3.3",
    "mi_nueva_dependencia==1.0.0"
]
```

### Cambiar Configuración del Servidor
```python
SERVER_CONFIG = {
    'host': '127.0.0.1',  # Solo acceso local
    'port': 8080,         # Puerto personalizado
    'debug': True         # Modo desarrollo
}
```

## 🚀 **Próximos Pasos**

1. **Ejecuta** uno de los archivos ejecutables
2. **Espera** a que instale las dependencias
3. **Abre** `http://localhost:5000` en tu navegador
4. **Carga** tus datos (PDFs, URLs, texto)
5. **Usa** `python start_chatbot.py` para chatear

---

**¡Disfruta de tu interfaz web fácil de usar! 🎉**
