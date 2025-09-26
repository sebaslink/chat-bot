# 📦 INSTRUCCIONES PARA CREAR INSTALADOR.EXE

## 🎯 Opciones Disponibles

### Opción 1: Ejecutable Simple (Recomendado para principiantes)
- **Archivo**: `crear_ejecutable_simple.py`
- **Resultado**: Carpeta portable con ejecutable .exe
- **Ventajas**: Fácil de crear, no requiere Inno Setup
- **Desventajas**: No es un instalador tradicional

### Opción 2: Instalador Completo (Recomendado para distribución)
- **Archivo**: `crear_instalador.py`
- **Resultado**: Instalador .exe profesional
- **Ventajas**: Instalador tradicional, desinstalador incluido
- **Desventajas**: Requiere Inno Setup

## 🚀 MÉTODO AUTOMÁTICO (Más Fácil)

1. **Ejecuta el archivo**: `instalador_automatico.bat`
2. **Selecciona una opción**:
   - Opción 1: Ejecutable simple
   - Opción 2: Instalador completo
3. **Espera** a que termine el proceso
4. **Revisa** las carpetas generadas

## 🔧 MÉTODO MANUAL

### Para Ejecutable Simple:

```bash
# 1. Instalar PyInstaller
pip install pyinstaller

# 2. Crear ejecutable
python crear_ejecutable_simple.py
```

### Para Instalador Completo:

```bash
# 1. Instalar dependencias
pip install pyinstaller

# 2. Descargar e instalar Inno Setup
# https://jrsoftware.org/isinfo.php

# 3. Crear instalador
python crear_instalador.py
```

## 📁 ESTRUCTURA GENERADA

### Ejecutable Simple:
```
ChatMasivo_Portable/
├── ChatMasivo.exe          # Ejecutable principal
├── templates/              # Plantillas HTML
├── static/                 # Archivos estáticos
├── config/                 # Configuración
├── Twilio.env.example      # Ejemplo de configuración
├── CONFIGURACION_INICIAL.txt
└── README.txt
```

### Instalador Completo:
```
dist_instalador/
└── ChatMasivo_Instalador.exe  # Instalador profesional
```

## ⚙️ CONFIGURACIÓN REQUERIDA

### Antes de crear el instalador:

1. **Configura Twilio**:
   - Edita `Twilio.env` con tus credenciales
   - O deja `Twilio.env.example` para que el usuario lo configure

2. **Verifica archivos**:
   - `app/codchat.py` o `codigo/codchat.py` (archivo principal)
   - `templates/` (plantillas HTML)
   - `static/` (archivos estáticos)
   - `config/` (configuración)

## 🎨 PERSONALIZACIÓN

### Cambiar icono:
- Reemplaza `imagen/icono.jpg` con tu icono
- Formatos soportados: .ico, .jpg, .png

### Cambiar información de la aplicación:
- Edita `crear_instalador.py`
- Modifica las secciones `[Setup]` en el script de Inno Setup

### Agregar archivos adicionales:
- Edita la función `crear_estructura_instalador()`
- Agrega archivos a la lista `archivos_copiar`

## 🐛 SOLUCIÓN DE PROBLEMAS

### Error: "Python no encontrado"
- Instala Python desde https://www.python.org/downloads/
- Marca "Add Python to PATH" durante la instalación

### Error: "PyInstaller no encontrado"
- Ejecuta: `pip install pyinstaller`

### Error: "Inno Setup no encontrado"
- Descarga desde: https://jrsoftware.org/isinfo.php
- Instala en la ubicación por defecto

### Error: "Archivo principal no encontrado"
- Verifica que existe `app/codchat.py` o `codigo/codchat.py`
- Ajusta la ruta en el script si es necesario

### El ejecutable no funciona:
- Verifica que `Twilio.env` esté configurado correctamente
- Revisa que todas las dependencias estén incluidas
- Ejecuta desde la carpeta correcta

## 📋 CHECKLIST PRE-INSTALACIÓN

- [ ] Python instalado y en PATH
- [ ] PyInstaller instalado (`pip install pyinstaller`)
- [ ] Archivo principal existe (`app/codchat.py` o `codigo/codchat.py`)
- [ ] Carpeta `templates/` existe
- [ ] Carpeta `static/` existe
- [ ] Archivo `Twilio.env` configurado (opcional)
- [ ] Inno Setup instalado (solo para instalador completo)

## 🎉 DESPUÉS DE CREAR EL INSTALADOR

### Para Ejecutable Simple:
1. Copia la carpeta `ChatMasivo_Portable/` a la computadora destino
2. Configura `Twilio.env` con las credenciales
3. Ejecuta `ChatMasivo.exe`
4. Abre http://localhost:5000 en el navegador

### Para Instalador Completo:
1. Distribuye `ChatMasivo_Instalador.exe`
2. El usuario ejecuta el instalador
3. Sigue las instrucciones del instalador
4. La aplicación se instalará automáticamente

## 📞 SOPORTE

Si tienes problemas:
1. Revisa los logs de error
2. Verifica que todas las dependencias estén instaladas
3. Asegúrate de que los archivos estén en las ubicaciones correctas
4. Consulta la documentación de PyInstaller e Inno Setup
