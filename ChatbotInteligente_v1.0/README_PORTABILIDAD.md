# 🌐 Chatbot Inteligente v1.0 - Guía de Portabilidad

## 📦 **¿Es esta carpeta portátil?**

**¡SÍ!** La carpeta `ChatbotInteligente_v1.0` está diseñada para funcionar en cualquier computadora con Windows, pero necesita una instalación inicial.

## 🚀 **Instalación en Otra Computadora**

### **Método 1: Instalación Automática (Recomendado)**

1. **Copia la carpeta completa** `ChatbotInteligente_v1.0` a la nueva computadora
2. **Ejecuta** `INSTALAR_EN_OTRA_COMPUTADORA.bat`
3. **El instalador detectará automáticamente:**
   - Sistema operativo
   - Arquitectura (32-bit o 64-bit)
   - Ubicación de Python
   - Versión de Python
4. **Se creará un ejecutable personalizado** para esa computadora
5. **¡Listo!** Usa `EJECUTAR_CHATBOT.bat` para iniciar el sistema

### **Método 2: Instalación Manual**

1. **Instala Python 3.8+** desde [python.org](https://python.org)
2. **Marca "Add Python to PATH"** durante la instalación
3. **Copia la carpeta** `ChatbotInteligente_v1.0` a la nueva computadora
4. **Abre una terminal** en la carpeta del proyecto
5. **Instala dependencias:**
   ```bash
   pip install -r requirements_completo.txt
   ```
6. **Ejecuta el sistema:**
   ```bash
   python SISTEMA_UNIFICADO_FINAL.py
   ```

## 🔧 **Requisitos del Sistema**

### **Mínimos:**
- **Sistema operativo:** Windows 10/11 (32-bit o 64-bit)
- **Python:** 3.8 o superior
- **Memoria RAM:** 4GB mínimo, 8GB recomendado
- **Espacio en disco:** 2GB libres
- **Navegador:** Chrome, Firefox, Edge (últimas versiones)

### **Recomendados:**
- **Sistema operativo:** Windows 11 64-bit
- **Python:** 3.11 o superior
- **Memoria RAM:** 8GB o más
- **Espacio en disco:** 5GB libres
- **Conexión a internet:** Para instalar dependencias

## 📁 **Estructura de Archivos Portátil**

```
ChatbotInteligente_v1.0/
├── 📄 INSTALAR_EN_OTRA_COMPUTADORA.bat    # Instalador automático
├── 📄 EJECUTAR_CHATBOT_FINAL.bat          # Ejecutable original
├── 📄 EJECUTAR_CHATBOT_CORREGIDO.bat      # Ejecutable alternativo
├── 📄 SISTEMA_UNIFICADO_FINAL.py          # Sistema principal
├── 📄 requirements_completo.txt            # Dependencias
├── 📄 README_PORTABILIDAD.md               # Esta guía
├── 📄 README_ACTUALIZADO.md                # Documentación completa
├── 📄 CHANGELOG_v1.0.md                    # Historial de cambios
├── 📁 templates/                           # Plantillas HTML
├── 📁 static/                             # Recursos estáticos
├── 📁 data/                               # Base de datos (se crea automáticamente)
├── 📁 CHATMASIVO/                         # Chat Masivo original
└── 📁 logs/                               # Logs del sistema (se crea automáticamente)
```

## 🎯 **Archivos Generados Automáticamente**

Después de ejecutar `INSTALAR_EN_OTRA_COMPUTADORA.bat`, se crearán:

```
ChatbotInteligente_v1.0/
├── 📄 EJECUTAR_CHATBOT.bat                # Ejecutable personalizado
├── 📄 INICIAR_SISTEMA.bat                 # Script de inicio rápido
├── 📄 INFO_SISTEMA_LOCAL.txt              # Información de la instalación
├── 📁 data/                               # Base de datos creada
│   ├── 📄 knowledge_base.json             # Base de conocimientos
│   └── 📁 database/                       # Bases de datos SQLite
│       ├── 📄 users.db                    # Usuarios
│       ├── 📄 chatbot.db                  # Chatbot
│       └── 📄 contactos.db                # Contactos
└── 📁 logs/                               # Logs del sistema
```

## 🔄 **Proceso de Instalación Automática**

### **Paso 1: Detección del Sistema**
- ✅ Detecta Windows (32-bit o 64-bit)
- ✅ Detecta Python instalado
- ✅ Detecta ubicación de Python
- ✅ Detecta versión de Python

### **Paso 2: Configuración**
- ✅ Crea directorios necesarios
- ✅ Instala dependencias automáticamente
- ✅ Crea bases de datos SQLite
- ✅ Crea usuarios por defecto

### **Paso 3: Personalización**
- ✅ Crea ejecutable personalizado para esa PC
- ✅ Configura rutas específicas del sistema
- ✅ Genera archivo de información local

## 👥 **Usuarios por Defecto**

Después de la instalación, tendrás estos usuarios:

| Usuario | Contraseña | Rol | Acceso |
|---------|------------|-----|--------|
| `admin` | `admin123` | Administrativo | Sistema completo |
| `jperez` | `123456` | Asesor | Chat Masivo |

## 🌐 **URLs del Sistema**

- **URL Principal:** `http://localhost:5000`
- **URL Chat Masivo:** `http://localhost:5001`

## 🚨 **Solución de Problemas**

### **Error: "Python no está instalado"**
- **Solución:** Instala Python desde [python.org](https://python.org)
- **Importante:** Marca "Add Python to PATH" durante la instalación

### **Error: "No se pudieron instalar las dependencias"**
- **Solución:** Verifica tu conexión a internet
- **Alternativa:** Instala manualmente con `pip install -r requirements_completo.txt`

### **Error: "Puerto 5000 ya está en uso"**
- **Solución:** Cierra otras aplicaciones que usen el puerto 5000
- **Alternativa:** Reinicia la computadora

### **Error: "No se puede acceder a la base de datos"**
- **Solución:** Ejecuta `INSTALAR_EN_OTRA_COMPUTADORA.bat` nuevamente
- **Verifica:** Que la carpeta `data` se haya creado correctamente

## 📋 **Lista de Verificación para Nueva Instalación**

- [ ] **Python 3.8+ instalado** y en el PATH
- [ ] **Carpeta copiada** completamente a la nueva computadora
- [ ] **Instalador ejecutado** `INSTALAR_EN_OTRA_COMPUTADORA.bat`
- [ ] **Dependencias instaladas** correctamente
- [ ] **Ejecutable personalizado creado** `EJECUTAR_CHATBOT.bat`
- [ ] **Sistema probado** con usuarios por defecto
- [ ] **URLs accesibles** en el navegador

## 🔒 **Consideraciones de Seguridad**

- **Contraseñas por defecto:** Cambia las contraseñas después de la instalación
- **Puertos:** El sistema usa puertos 5000 y 5001 (asegúrate de que estén libres)
- **Firewall:** Puede que necesites permitir el acceso en el firewall de Windows

## 📞 **Soporte**

Si tienes problemas con la instalación:

1. **Verifica** que Python esté instalado correctamente
2. **Ejecuta** el instalador como administrador
3. **Revisa** el archivo `INFO_SISTEMA_LOCAL.txt` para información del sistema
4. **Contacta** al equipo de soporte con los detalles del error

---

## ✅ **Resumen**

**La carpeta `ChatbotInteligente_v1.0` ES completamente portátil** y puede funcionar en cualquier computadora con Windows. Solo necesitas:

1. **Copiar la carpeta** a la nueva computadora
2. **Ejecutar** `INSTALAR_EN_OTRA_COMPUTADORA.bat`
3. **¡Listo!** El sistema estará funcionando

**Versión:** 1.0  
**Última actualización:** 25 de Septiembre de 2025  
**Compatibilidad:** Windows 10/11, Python 3.8+
