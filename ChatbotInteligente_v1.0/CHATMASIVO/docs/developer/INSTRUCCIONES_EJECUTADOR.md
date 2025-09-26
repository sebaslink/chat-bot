# 🚀 Ejecutadores para Chat Masivo WhatsApp

## Archivos de Ejecución Disponibles

### 1. `ejecutar.bat` (Windows) - Ejecutador Principal
- **Uso**: Doble clic en el archivo
- **Funciones**:
  - Menú interactivo para elegir versión
  - Instalación automática de dependencias
  - Opciones para todas las versiones del programa

### 2. `iniciar_simple.bat` (Windows) - Ejecutador Rápido
- **Uso**: Doble clic en el archivo
- **Funciones**:
  - Inicia directamente la versión simple
  - Instalación automática de dependencias
  - Ideal para uso diario

### 3. `ejecutar.sh` (Linux/Mac) - Ejecutador Unix
- **Uso**: `./ejecutar.sh` en terminal
- **Funciones**:
  - Menú interactivo con colores
  - Instalación automática de dependencias
  - Compatible con sistemas Unix

## Versiones Disponibles

### 🔹 Versión Simple (Recomendada)
- **Archivo**: `codchat_simple.py`
- **Características**:
  - Interfaz limpia y fácil de usar
  - Funcionalidades básicas de envío masivo
  - Exportación a CSV
  - Descarga de plantilla Excel
  - Sin dependencias externas pesadas

### 🔹 Versión Demo
- **Archivo**: `codchat_demo.py`
- **Características**:
  - Todas las funciones de la versión simple
  - Importación desde Excel (.xlsx)
  - Funcionalidades avanzadas de gestión

### 🔹 Versión Completa
- **Archivo**: `codchat.py`
- **Características**:
  - Todas las funcionalidades disponibles
- **Nota**: Requiere configuración adicional

## Instrucciones de Uso

### Para Windows:
1. **Opción 1**: Doble clic en `ejecutar.bat` y selecciona la versión
2. **Opción 2**: Doble clic en `iniciar_simple.bat` para inicio rápido

### Para Linux/Mac:
1. Abre terminal en la carpeta del proyecto
2. Ejecuta: `./ejecutar.sh`
3. Selecciona la versión deseada

## Requisitos Previos

- Python 3.7 o superior instalado
- Conexión a internet (para instalar dependencias)
- Archivo `requirements.txt` en la carpeta del proyecto

## Solución de Problemas

### Si no se ejecuta:
1. Verifica que Python esté instalado: `python --version`
2. Verifica que estés en la carpeta correcta del proyecto
3. Ejecuta manualmente: `python codchat_simple.py`

### Si faltan dependencias:
1. Ejecuta: `pip install -r requirements.txt`
2. O usa la opción "Instalar dependencias" en el menú

## Acceso a la Aplicación

Una vez iniciado el servidor, la aplicación estará disponible en:
- **URL**: http://localhost:5000
- **Red local**: http://[tu-ip]:5000

## Detener el Servidor

- **Windows**: Presiona `Ctrl+C` en la ventana de comandos
- **Linux/Mac**: Presiona `Ctrl+C` en la terminal
