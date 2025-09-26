# 🤖 Chat Masivo WhatsApp - Sistema Unificado

Sistema completo de chat masivo para WhatsApp con integración de Twilio, interfaz web y gestión de contactos.

## 🚀 Características Principales

- **Chat Masivo**: Envío masivo de mensajes por WhatsApp
- **Interfaz Web**: Panel de control intuitivo y moderno
- **Gestión de Contactos**: Agregar, editar, eliminar y organizar contactos
- **Grupos**: Organización de contactos por categorías
- **Plantillas**: Mensajes personalizables y reutilizables
- **Importación Excel**: Carga masiva de contactos desde archivos Excel
- **Estadísticas**: Monitoreo en tiempo real de envíos
- **Logs Detallados**: Seguimiento completo de todas las operaciones

## 📋 Requisitos del Sistema

- Python 3.8 o superior
- Cuenta de Twilio (para envío real de mensajes)
- Navegador web moderno

## 🔧 Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone [URL_DEL_REPOSITORIO]
cd chat-bot
```

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar Credenciales de Twilio

#### Opción A: Variables de Entorno (Recomendado)

Crea un archivo `.env` en la raíz del proyecto:

```bash
# Credenciales de Twilio
TWILIO_ACCOUNT_SID=tu_account_sid_aqui
TWILIO_AUTH_TOKEN=tu_auth_token_aqui
TWILIO_WHATSAPP_FROM=whatsapp:+tu_numero_twilio

# Flask
FLASK_SECRET_KEY=tu_clave_secreta_flask_aqui

# Número de prueba (opcional)
NUMERO_PRUEBA=+tu_numero_prueba
```

#### Opción B: Archivos de Configuración

1. Copia los archivos de ejemplo:
   ```bash
   cp CHATMASIVO/config/twilio/Twilio.env.example CHATMASIVO/config/twilio/Twilio.env
   cp CHATMASIVO/config/app/Twilio.env.example CHATMASIVO/config/app/Twilio.env
   ```

2. Edita los archivos con tus credenciales reales.

### 4. Configurar Twilio

1. Ve a [Twilio Console](https://console.twilio.com/)
2. Obtén tu Account SID y Auth Token
3. Configura un número de WhatsApp:
   - Ve a Messaging > Senders > WhatsApp senders
   - Agrega un nuevo sender
   - Sigue el proceso de verificación

### 5. Ejecutar la Aplicación

```bash
python SISTEMA_UNIFICADO_FINAL.py
```

La aplicación estará disponible en: `http://localhost:5000`

## 📁 Estructura del Proyecto

```
chat-bot/
├── CHATMASIVO/                 # Módulo principal de chat masivo
│   ├── config/                 # Configuraciones
│   │   ├── twilio/            # Configuración de Twilio
│   │   └── app/               # Configuración de la aplicación
│   ├── scripts/               # Scripts utilitarios
│   ├── templates/             # Plantillas HTML
│   └── docs/                  # Documentación
├── ChatbotInteligente_v1.0/   # Versión anterior del chatbot
├── templates/                  # Plantillas principales
├── static/                     # Archivos estáticos
├── data/                       # Base de datos y datos
└── requirements.txt           # Dependencias de Python
```

## 🔒 Seguridad

- **NUNCA** subas archivos `.env` o con credenciales reales
- Usa variables de entorno en producción
- Mantén tus credenciales de Twilio seguras
- El archivo `.gitignore` protege automáticamente los archivos sensibles

## 🚀 Despliegue

### Variables de Entorno en GitLab

Configura estas variables en tu proyecto de GitLab:

- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_WHATSAPP_FROM`
- `FLASK_SECRET_KEY`

### Despliegue en Railway

```bash
python subir_a_railway.py
```

### Despliegue en Render

```bash
python subir_a_render_v2.py
```

## 📖 Uso del Sistema

### 1. Agregar Contactos

- Usa la interfaz web para agregar contactos individuales
- Importa desde Excel usando la plantilla proporcionada
- Organiza contactos en grupos

### 2. Crear Mensajes

- Usa las plantillas predefinidas
- Crea mensajes personalizados
- Combina texto fijo con texto aleatorio

### 3. Enviar Mensajes

- Selecciona el grupo de destinatarios
- Elige la plantilla de mensaje
- Envía masivamente o individualmente

### 4. Monitorear Resultados

- Revisa las estadísticas en tiempo real
- Consulta los logs de envío
- Exporta reportes de resultados

## 🛠️ Desarrollo

### Modo Demo

El sistema puede funcionar en modo demo sin credenciales de Twilio:

```bash
python CHATMASIVO/scripts/utilities/codchat_demo.py
```

### Estructura de Base de Datos

- `grupos`: Categorías de contactos
- `numeros`: Lista de contactos
- `mensajes_log`: Registro de envíos
- `plantillas`: Plantillas de mensajes

## 📞 Soporte

Para problemas o preguntas:

1. Revisa los logs en `chatmasivo.log`
2. Verifica la configuración de Twilio
3. Consulta la documentación en `CHATMASIVO/docs/`

## 📄 Licencia

Este proyecto es de uso interno. No distribuir sin autorización.

---

**¡Sistema listo para usar! 🎉**

Para comenzar, ejecuta `python SISTEMA_UNIFICADO_FINAL.py` y accede a `http://localhost:5000`
