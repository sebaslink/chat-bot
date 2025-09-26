# 🖥️ Guía de Instalación en Otra Computadora

Esta guía te ayudará a instalar y configurar el sistema de Chat Masivo WhatsApp en una nueva computadora.

## 📋 Requisitos Previos

### Sistema Operativo
- **Windows 10/11** (recomendado)
- **macOS 10.14+**
- **Linux Ubuntu 18.04+**

### Software Requerido
- **Python 3.8 o superior**
- **Navegador web moderno** (Chrome, Firefox, Edge)
- **Conexión a internet**

## 🚀 Instalación Automática (Recomendado)

### Paso 1: Descargar el Proyecto
```bash
# Si tienes Git instalado
git clone [URL_DEL_REPOSITORIO]
cd chat-bot

# O descarga el ZIP y extrae
```

### Paso 2: Ejecutar Instalador Automático
```bash
# En Windows
python instalar_en_nueva_computadora.py

# En macOS/Linux
python3 instalar_en_nueva_computadora.py
```

### Paso 3: Seguir las Instrucciones
El instalador automático te guiará a través de:
1. ✅ Verificación de Python
2. 📦 Instalación de dependencias
3. 📁 Creación de directorios
4. 🧹 Limpieza de archivos duplicados
5. 🔧 Configuración de credenciales
6. 🚀 Creación de scripts de ejecución

## 🔧 Configuración Manual de Credenciales

Si prefieres configurar las credenciales manualmente o después de la instalación:

### Opción 1: Script Interactivo
```bash
python configurar_credenciales.py
```

### Opción 2: Configuración Manual

#### 1. Crear archivo `.env` en la raíz del proyecto:
```bash
# Configuración de Twilio
TWILIO_ACCOUNT_SID=tu_account_sid_aqui
TWILIO_AUTH_TOKEN=tu_auth_token_aqui
TWILIO_WHATSAPP_FROM=whatsapp:+tu_numero_twilio
FLASK_SECRET_KEY=tu_clave_secreta_flask
NUMERO_PRUEBA=+tu_numero_prueba
```

#### 2. Configurar archivos específicos:
- `CHATMASIVO/config/twilio/Twilio.env`
- `CHATMASIVO/config/app/Twilio.env`

## 🔑 Obtener Credenciales de Twilio

### 1. Crear Cuenta en Twilio
- Ve a [https://www.twilio.com/](https://www.twilio.com/)
- Regístrate o inicia sesión
- Verifica tu número de teléfono

### 2. Obtener Credenciales
1. Ve a [Twilio Console](https://console.twilio.com/)
2. En el dashboard, encontrarás:
   - **Account SID**: Comienza con "AC..."
   - **Auth Token**: 32 caracteres alfanuméricos

### 3. Configurar WhatsApp
1. Ve a **Messaging** > **Senders** > **WhatsApp senders**
2. Haz clic en **Add sender**
3. Selecciona un número de teléfono
4. Sigue el proceso de verificación
5. Anota el número en formato: `+1234567890`

## 🏃‍♂️ Ejecutar el Sistema

### Windows
```bash
# Opción 1: Doble clic en el archivo
EJECUTAR_CHATBOT.bat

# Opción 2: Desde terminal
python SISTEMA_UNIFICADO_FINAL.py
```

### macOS/Linux
```bash
# Opción 1: Script ejecutable
./ejecutar_chatbot.sh

# Opción 2: Desde terminal
python3 SISTEMA_UNIFICADO_FINAL.py
```

### Acceder al Sistema
1. Abre tu navegador
2. Ve a: `http://localhost:5000`
3. ¡Listo! El sistema está funcionando

## 🔍 Verificación de Instalación

### Verificar Archivos Importantes
```bash
# Verificar que existan estos archivos:
SISTEMA_UNIFICADO_FINAL.py
requirements.txt
configurar_credenciales.py
.env (con tus credenciales)
```

### Verificar Directorios
```bash
# Verificar que existan estos directorios:
CHATMASIVO/
templates/
static/
data/
```

### Probar Funcionalidad
1. Abre el navegador en `http://localhost:5000`
2. Intenta agregar un contacto
3. Envía un mensaje de prueba
4. Revisa los logs en `chatmasivo.log`

## 🛠️ Solución de Problemas

### Error: "Python no encontrado"
```bash
# Instalar Python desde python.org
# O usar gestor de paquetes:
# Windows: choco install python
# macOS: brew install python
# Ubuntu: sudo apt install python3
```

### Error: "Módulo no encontrado"
```bash
# Reinstalar dependencias
pip install -r requirements.txt
# O
pip3 install -r requirements.txt
```

### Error: "Puerto 5000 en uso"
```bash
# Cambiar puerto en SISTEMA_UNIFICADO_FINAL.py
# Buscar: app.run(port=5000)
# Cambiar a: app.run(port=5001)
```

### Error: "Credenciales de Twilio inválidas"
1. Verifica que las credenciales sean correctas
2. Asegúrate de que la cuenta de Twilio esté activa
3. Verifica que el número de WhatsApp esté verificado
4. Revisa el formato de las credenciales

## 📱 Modo Demo

Si no tienes credenciales de Twilio, el sistema funcionará en **modo demo**:
- ✅ Todas las funciones están disponibles
- ✅ Los mensajes se simulan en los logs
- ✅ No se envían mensajes reales
- ✅ Perfecto para pruebas y desarrollo

## 🔒 Seguridad

### Archivos Sensibles
- **NUNCA** compartas archivos `.env`
- **NUNCA** subas credenciales a repositorios públicos
- Mantén las credenciales de Twilio seguras
- Usa variables de entorno en producción

### Archivos Protegidos por .gitignore
```
.env
*.env
Twilio.env
configuracion_whatsapp.txt
numeros_prueba_twilio.txt
*.db
*.log
```

## 📞 Soporte

### Logs del Sistema
- **Log principal**: `chatmasivo.log`
- **Logs de aplicación**: `logs/`
- **Base de datos**: `data/database/`

### Documentación Adicional
- `README_GITLAB.md` - Documentación completa
- `CHATMASIVO/docs/` - Documentación técnica
- `GUIA_INSTALACION_OTRA_COMPUTADORA.md` - Esta guía

### Contacto
Si tienes problemas:
1. Revisa los logs
2. Consulta la documentación
3. Verifica la configuración
4. Prueba en modo demo primero

## ✅ Lista de Verificación

Antes de usar el sistema, asegúrate de tener:

- [ ] Python 3.8+ instalado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Archivo `.env` configurado (o modo demo)
- [ ] Directorios creados correctamente
- [ ] Sistema ejecutándose en `http://localhost:5000`
- [ ] Navegador abierto y funcionando
- [ ] Logs sin errores críticos

---

**¡Instalación completada! 🎉**

Tu sistema de Chat Masivo WhatsApp está listo para usar en la nueva computadora.
