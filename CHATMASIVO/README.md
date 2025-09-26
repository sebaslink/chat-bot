# 🚀 CHAT MASIVO - SISTEMA DE MENSAJERÍA WHATSAPP

## 📋 DESCRIPCIÓN
Sistema completo para envío masivo de mensajes por WhatsApp usando Twilio. Incluye gestión de contactos, grupos, plantillas y estadísticas.

## 🏗️ ESTRUCTURA DEL PROYECTO

```
CHATMASIVO/
├── main.py                     # Aplicación principal
├── requirements.txt            # Dependencias Python
├── README.md                   # Este archivo
│
├── app/                        # Aplicación Flask
│   └── codchat.py             # Código principal
│
├── scripts/                    # Scripts de Python
│   ├── installer/             # Scripts del instalador
│   ├── utilities/             # Utilidades
│   └── tests/                 # Scripts de prueba
│
├── executables/               # Archivos ejecutables
│   ├── launchers/            # Lanzadores principales
│   └── utilities/            # Utilidades .bat
│
├── config/                    # Configuración
│   ├── twilio/               # Configuración Twilio
│   └── app/                  # Configuración de la app
│
├── docs/                      # Documentación
│   ├── user/                 # Documentación de usuario
│   └── developer/            # Documentación de desarrollador
│
├── data/                      # Datos
│   ├── excel/                # Archivos Excel
│   ├── csv/                  # Archivos CSV
│   └── database/             # Bases de datos
│
├── templates/                 # Plantillas HTML
├── static/                    # Archivos estáticos
│   ├── images/               # Imágenes
│   └── uploads/              # Archivos subidos
│
├── logs/                      # Archivos de log
│   ├── app/                  # Logs de la aplicación
│   └── system/               # Logs del sistema
│
├── backup/                    # Respaldos
└── temp/                     # Archivos temporales
```

## 🚀 INSTALACIÓN RÁPIDA

### Opción 1: Ejecutable (Recomendado)
```bash
# Ejecutar el instalador
executables/launchers/CREAR_INSTALADOR.bat
```

### Opción 2: Desde código fuente
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python main.py
```

## ⚙️ CONFIGURACIÓN

1. **Configurar Twilio:**
   - Edita `config/twilio/Twilio.env`
   - Agrega tus credenciales de Twilio

2. **Ejecutar aplicación:**
   - Ejecuta `main.py` o usa los lanzadores en `executables/launchers/`
   - Abre http://localhost:5000 en tu navegador

## 📚 DOCUMENTACIÓN

- **Usuario:** `docs/user/` - Guías de uso
- **Desarrollador:** `docs/developer/` - Documentación técnica

## 🛠️ DESARROLLO

### Scripts disponibles:
- **Instalador:** `scripts/installer/`
- **Utilidades:** `scripts/utilities/`
- **Pruebas:** `scripts/tests/`

### Lanzadores:
- **Principal:** `executables/launchers/`
- **Utilidades:** `executables/utilities/`

## 📞 SOPORTE

Para soporte técnico, consulta la documentación en `docs/` o contacta al desarrollador.

## 📄 LICENCIA

Proyecto privado - Todos los derechos reservados.

---
**Versión:** 1.0  
**Última actualización:** 2024
