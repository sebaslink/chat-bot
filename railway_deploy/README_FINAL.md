# 🤖 **SISTEMA UNIFICADO CHATBOT Y CHAT MASIVO**

## 📋 **DESCRIPCIÓN**
Sistema completo de chatbot inteligente con chat masivo por WhatsApp, incluyendo sistema de autenticación por roles y gestión de usuarios.

## 🚀 **CARACTERÍSTICAS PRINCIPALES**

### **Sistema de Autenticación**
- Login con usuario y contraseña
- Control de acceso por roles:
  - **Asesor**: Acceso directo al Chat Masivo
  - **Administrador**: Acceso completo al sistema
  - **Programador**: Acceso completo al sistema

### **Chatbot Inteligente**
- Chat con IA usando OpenAI
- Carga de documentos (PDF, Word, Excel, PowerPoint, Imágenes)
- Extracción de contenido web
- Base de conocimientos integrada

### **Chat Masivo por WhatsApp**
- Integración con Twilio
- Gestión de contactos y grupos
- Envío de mensajes masivos
- Plantillas personalizables

### **Gestión de Base de Datos**
- Visualización de estadísticas
- Gestión de usuarios
- Exportación y backup de datos

## 📁 **ESTRUCTURA DEL PROYECTO**

```
chat bot/
├── SISTEMA_UNIFICADO_FINAL.py    # Aplicación principal
├── EJECUTAR_CHATBOT_FINAL.bat    # Ejecutable principal
├── requirements.txt              # Dependencias Python
├── Procfile                      # Configuración para despliegue
├── runtime.txt                   # Versión de Python
├── data/                         # Bases de datos
│   ├── database/
│   └── knowledge_base.json
├── static/                       # Archivos estáticos
│   ├── uploads/
│   └── cache_buster.js
├── templates/                    # Plantillas HTML
│   ├── login.html
│   ├── chatbot_principal.html
│   └── chatmasivo_original.html
├── CHATMASIVO/                   # Aplicación Chat Masivo
│   ├── main.py
│   ├── templates/
│   └── static/
└── ChatbotInteligente_v1.0/      # Paquete de instalación
    ├── SISTEMA_UNIFICADO_FINAL.py
    ├── templates/
    ├── static/
    └── data/
```

## 🛠️ **INSTALACIÓN Y USO**

### **Instalación Local**
1. Ejecutar `EJECUTAR_CHATBOT_FINAL.bat`
2. El sistema se abrirá automáticamente en el navegador
3. Usar credenciales por defecto: `admin/admin123`

### **Instalación en Otra Computadora**
1. Usar la carpeta `ChatbotInteligente_v1.0/`
2. Ejecutar `INSTALAR_EN_OTRA_COMPUTADORA.bat`

### **Despliegue en la Nube**
- Ver `README_DESPLIEGUE.md` para instrucciones detalladas
- Compatible con Railway, Render, Heroku

## 🔧 **CONFIGURACIÓN**

### **Variables de Entorno**
- `OPENAI_API_KEY`: Clave de API de OpenAI
- `TWILIO_ACCOUNT_SID`: SID de cuenta Twilio
- `TWILIO_AUTH_TOKEN`: Token de autenticación Twilio
- `TWILIO_PHONE_NUMBER`: Número de teléfono Twilio

### **Puertos**
- **5000**: Sistema principal (Chatbot)
- **5001**: Chat Masivo original

## 📊 **FUNCIONALIDADES POR ROL**

### **Asesor**
- Acceso directo al Chat Masivo
- Gestión de contactos
- Envío de mensajes masivos

### **Administrador/Programador**
- Acceso completo al Chatbot
- Gestión de usuarios
- Visualización de base de datos
- Acceso al Chat Masivo desde botón

## 🎯 **URLS DEL SISTEMA**

- **Principal**: http://localhost:5000
- **Login**: http://localhost:5000/login
- **Chatbot**: http://localhost:5000/chatbot
- **Chat Masivo**: http://localhost:5001

## 📝 **NOTAS TÉCNICAS**

- **Framework**: Flask
- **Base de datos**: SQLite
- **IA**: OpenAI GPT
- **WhatsApp**: Twilio API
- **Frontend**: HTML/CSS/JavaScript

## 🔄 **ACTUALIZACIONES**

- Sistema de login implementado
- Redirección automática por roles
- Integración completa con Chat Masivo
- Gestión de usuarios funcional
- Interfaz responsive y moderna

## 📞 **SOPORTE**

Para soporte técnico o consultas, revisar la documentación en `ChatbotInteligente_v1.0/` o los archivos de configuración.
