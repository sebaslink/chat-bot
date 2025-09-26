# 🌐 Sistema Conectado - Chat Masivo WhatsApp

Sistema que permite conectar múltiples computadoras y sincronizar usuarios entre ellas.

## 🎯 **CARACTERÍSTICAS PRINCIPALES:**

- ✅ **Sincronización de usuarios** entre computadoras
- ✅ **Servidor central** en la nube (Render)
- ✅ **Computadoras cliente** que se conectan al servidor
- ✅ **Creación de usuarios** desde cualquier computadora
- ✅ **Acceso compartido** a los mismos usuarios
- ✅ **Modo offline** cuando no hay conexión

## 🏗️ **ARQUITECTURA:**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Computadora   │    │   Computadora   │    │   Computadora   │
│      A          │    │      B          │    │      C          │
│                 │    │                 │    │                 │
│  ┌───────────┐  │    │  ┌───────────┐  │    │  ┌───────────┐  │
│  │  Cliente  │  │    │  │  Cliente  │  │    │  │  Cliente  │  │
│  │  Local    │  │    │  │  Local    │  │    │  │  Local    │  │
│  └───────────┘  │    │  └───────────┘  │    │  └───────────┘  │
│        │        │    │        │        │    │        │        │
│        │        │    │        │        │    │        │        │
└────────┼────────┘    └────────┼────────┘    └────────┼────────┘
         │                      │                      │
         └──────────────────────┼──────────────────────┘
                                │
                    ┌─────────────────┐
                    │  Servidor       │
                    │  Central        │
                    │  (Render)       │
                    │                 │
                    │  ┌───────────┐  │
                    │  │  Base de  │  │
                    │  │  Datos    │  │
                    │  │  Central  │  │
                    │  └───────────┘  │
                    └─────────────────┘
```

## 🚀 **INSTALACIÓN:**

### **Paso 1: Configurar Servidor Central**

1. **En tu computadora principal:**
   ```bash
   python configurar_servidor_central.py
   ```

2. **Desplegar en Render:**
   - Subir el código a GitHub
   - Conectar con Render
   - Configurar variables de entorno

3. **Obtener URL del servidor:**
   - Ejemplo: `https://tu-app.onrender.com`

### **Paso 2: Configurar Computadoras Cliente**

1. **En cada computadora cliente:**
   ```bash
   # Clonar el repositorio
   git clone https://github.com/sebaslink/chat-bot.git
   cd chat-bot
   
   # Configurar como cliente
   python configurar_computadora_cliente.py
   ```

2. **Ingresar URL del servidor central** cuando se solicite

### **Paso 3: Usar el Sistema Conectado**

```bash
# Ejecutar sistema conectado
python sistema_conectado.py
```

## 📋 **FUNCIONALIDADES:**

### **🔄 Sincronización Automática:**
- Los usuarios se sincronizan automáticamente
- Cambios en una computadora se reflejan en todas
- Funciona en tiempo real

### **👤 Gestión de Usuarios:**
- Crear usuarios desde cualquier computadora
- Los usuarios están disponibles en todas las computadoras
- Roles: Administrador, Asesor, Programador

### **🌐 Modo Conectado vs Local:**
- **Conectado**: Sincroniza con servidor central
- **Local**: Funciona sin conexión (modo offline)

## 🛠️ **CONFIGURACIÓN AVANZADA:**

### **Variables de Entorno:**

```bash
# Servidor Central
SERVIDOR_CENTRAL_URL=https://tu-app.onrender.com
MODO_CONECTADO=true

# Base de Datos
DATABASE_URL=sqlite:///data/database/users.db
```

### **Archivos de Configuración:**

- `config_servidor_central.json` - Configuración del servidor
- `config_cliente.json` - Configuración del cliente
- `sistema_conectado.py` - Sistema principal conectado

## 📱 **USO DEL SISTEMA:**

### **1. Crear Usuario:**
```bash
python sistema_conectado.py
# Seleccionar opción 2: Crear nuevo usuario
```

### **2. Listar Usuarios:**
```bash
python sistema_conectado.py
# Seleccionar opción 1: Listar usuarios
```

### **3. Sincronizar:**
```bash
python sistema_conectado.py
# Seleccionar opción 3: Sincronizar con servidor
```

## 🔧 **SOLUCIÓN DE PROBLEMAS:**

### **Error de Conexión:**
```bash
# Verificar conexión al servidor
python -c "import requests; print(requests.get('https://tu-app.onrender.com/api/auth/check').status_code)"
```

### **Sincronización Fallida:**
```bash
# Reconfigurar cliente
python configurar_computadora_cliente.py
```

### **Usuarios No Sincronizados:**
```bash
# Sincronizar manualmente
python sistema_conectado.py
# Opción 3: Sincronizar con servidor
```

## 📊 **VENTAJAS DEL SISTEMA CONECTADO:**

| **Característica** | **Sistema Local** | **Sistema Conectado** |
|-------------------|------------------|----------------------|
| **Usuarios** | Solo locales | Compartidos |
| **Sincronización** | No | Automática |
| **Acceso** | Una computadora | Múltiples computadoras |
| **Backup** | Manual | Automático |
| **Escalabilidad** | Limitada | Alta |

## 🎯 **CASOS DE USO:**

### **🏢 Oficina:**
- Múltiples computadoras con acceso a los mismos usuarios
- Administrador crea usuarios desde su computadora
- Asesores acceden desde sus computadoras

### **🏠 Trabajo Remoto:**
- Servidor central en la nube
- Trabajadores se conectan desde casa
- Sincronización automática de usuarios

### **👥 Equipo de Trabajo:**
- Usuarios compartidos entre miembros del equipo
- Gestión centralizada de accesos
- Control de permisos por rol

## 🚀 **PRÓXIMAS MEJORAS:**

- [ ] Sincronización de contactos
- [ ] Sincronización de mensajes
- [ ] Notificaciones en tiempo real
- [ ] Dashboard centralizado
- [ ] Backup automático

---

**¡Sistema conectado listo para usar! 🌐**

Para comenzar, ejecuta `python configurar_servidor_central.py` en tu computadora principal.
