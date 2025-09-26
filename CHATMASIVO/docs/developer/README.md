# 🚀 Chat Masivo WhatsApp - Sistema Profesional

Sistema completo de envío masivo de mensajes por WhatsApp utilizando la API de Twilio.

## ✨ Características

- 📊 **Panel de Estadísticas** en tiempo real
- 👥 **Gestión de Contactos** con grupos
- 📝 **Plantillas de Mensajes** reutilizables
- 📤 **Envío Masivo** segmentado por grupos
- 📥 **Exportación de Datos** a CSV
- 📋 **Sistema de Logging** completo
- 🔧 **Mensajes de Prueba** para validar configuración

## 🚀 Instalación y Configuración

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno
Edita el archivo `Twilio.env` con tus credenciales:
```
TWILIO_ACCOUNT_SID=tu_account_sid_aqui
TWILIO_AUTH_TOKEN=tu_auth_token_aqui
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
FLASK_SECRET_KEY=tu_clave_secreta_muy_larga_y_segura
```

### 3. Ejecutar la Aplicación
```bash
python codchat.py
```

### 4. Acceder a la Interfaz
Abre tu navegador en: `http://localhost:5000`

## 📁 Estructura del Proyecto

```
CHATMASIVO/
├── codchat.py              # Aplicación principal Flask
├── requirements.txt         # Dependencias Python
├── Twilio.env              # Variables de entorno
├── numeros_whatsapp.db     # Base de datos SQLite
├── chatmasivo.log          # Archivo de logs (se crea automáticamente)
└── templates/
    ├── interface.html      # Interfaz completa con tabs
    └── interface_simple.html # Interfaz simplificada
```

## 🔧 Uso del Sistema

### Agregar Contactos
1. Ve a la sección "Agregar Nuevo Contacto"
2. Completa nombre y teléfono
3. Selecciona un grupo (opcional)
4. Haz clic en "Agregar Contacto"

### Crear Grupos
1. Ve a la sección "Gestión de Grupos"
2. Ingresa nombre y descripción
3. Haz clic en "Crear Grupo"

### Enviar Mensajes Masivos
1. Ve a la sección "Envío Masivo"
2. Selecciona grupo (opcional)
3. Personaliza el mensaje
4. Haz clic en "Enviar Mensajes Masivos"

### Exportar Contactos
1. Haz clic en "Exportar CSV"
2. Se descargará un archivo con todos los contactos

## 📊 Monitoreo

- **Logs**: Revisa `chatmasivo.log` para ver el historial de envíos
- **Estadísticas**: Panel en tiempo real en la interfaz web
- **Base de Datos**: `numeros_whatsapp.db` contiene todos los datos

## ⚠️ Notas Importantes

- Asegúrate de tener credenciales válidas de Twilio
- El número de prueba es para testing únicamente
- Los mensajes se envían de forma secuencial para evitar límites de API
- Revisa los logs si hay errores en los envíos

## 🆘 Solución de Problemas

### Error de Importación
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Error de Twilio
- Verifica las credenciales en `Twilio.env`
- Asegúrate de que el número de WhatsApp esté verificado

### Error de Base de Datos
- Elimina `numeros_whatsapp.db` para recrear la base de datos
- Ejecuta `python codchat.py` nuevamente

## 📞 Soporte

Para problemas técnicos, revisa:
1. Los logs en `chatmasivo.log`
2. La consola donde ejecutas el programa
3. Las estadísticas en la interfaz web
