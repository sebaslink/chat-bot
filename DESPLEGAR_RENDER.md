# 🌐 **GUÍA COMPLETA - DESPLEGAR EN RENDER**

## 📋 **PASOS PARA DESPLEGAR EN RENDER**

### **Paso 1: Preparar el Repositorio en GitHub**
1. **Crear repositorio en GitHub**:
   - Ve a https://github.com
   - Haz clic en "New repository"
   - Nombre: `chatbot-unificado` (o el que prefieras)
   - Marca como "Public" (necesario para plan gratuito)
   - NO marques "Add README" (ya tenemos archivos)

2. **Subir archivos**:
   - Descarga GitHub Desktop o usa Git desde terminal
   - Clona tu repositorio
   - Copia todos los archivos del proyecto
   - Haz commit y push

### **Paso 2: Desplegar en Render**
1. **Ir a Render**:
   - Ve a https://render.com
   - Regístrate con tu cuenta de GitHub
   - Haz clic en "New +" → "Web Service"

2. **Conectar repositorio**:
   - Selecciona tu repositorio de GitHub
   - Render detectará automáticamente que es Python

3. **Configurar el despliegue**:
   - **Name**: `chatbot-unificado` (o el que prefieras)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn SISTEMA_UNIFICADO_FINAL:app --bind 0.0.0.0:$PORT`
   - **Plan**: `Free`

### **Paso 3: Configurar Variables de Entorno**
En Render Dashboard → Environment Variables:
```
RAILWAY_ENVIRONMENT=production
PORT=5000
TWILIO_ACCOUNT_SID=tu_account_sid (opcional)
TWILIO_AUTH_TOKEN=tu_auth_token (opcional)
OPENAI_API_KEY=tu_api_key (opcional)
```

### **Paso 4: Desplegar**
1. **Hacer clic en "Create Web Service"**
2. **Render comenzará a desplegar automáticamente**
3. **El proceso tomará 3-5 minutos**
4. **Al finalizar, obtendrás una URL como**: `https://chatbot-unificado.onrender.com`

## 🔧 **CONFIGURACIÓN ESPECÍFICA PARA RENDER**

### **Archivos Necesarios**
- ✅ `requirements.txt` - Dependencias
- ✅ `Procfile` - Comando de inicio
- ✅ `runtime.txt` - Versión de Python
- ✅ `.gitignore` - Archivos a ignorar

### **Comando de Inicio**
```
gunicorn SISTEMA_UNIFICADO_FINAL:app --bind 0.0.0.0:$PORT
```

### **Puerto**
Render asigna automáticamente el puerto en la variable `$PORT`

## 📱 **ACCESO DESPUÉS DEL DESPLIEGUE**

### **URL de tu Aplicación**
- `https://tu-app.onrender.com` (URL que te dé Render)

### **Login por Defecto**
- **Usuario**: `admin`
- **Contraseña**: `admin123`

### **Funcionalidades Disponibles**
- ✅ Sistema de login con roles
- ✅ Chatbot inteligente
- ✅ Carga de documentos
- ✅ Base de datos integrada
- ✅ Gestión de usuarios
- ⚠️ Chat Masivo (requiere Twilio)

## 🛠️ **SOLUCIÓN DE PROBLEMAS**

### **Error: "Build failed"**
- Verifica que `requirements.txt` esté completo
- Revisa los logs de build en Render

### **Error: "Application crashed"**
- Verifica que el comando de inicio sea correcto
- Revisa los logs de runtime en Render

### **Error: "Module not found"**
- Asegúrate de que todas las dependencias estén en `requirements.txt`
- Render reinstalará automáticamente

## 📊 **MONITOREO**

### **Logs de la Aplicación**
- Render Dashboard → Logs
- Monitorea errores y rendimiento

### **Métricas**
- Render proporciona métricas básicas
- Monitorea el uso de recursos

## 🔄 **ACTUALIZACIONES**

### **Actualizar la Aplicación**
1. Haz cambios en tu código local
2. Sube cambios a GitHub
3. Render desplegará automáticamente

### **Rollback**
1. Render Dashboard → Deployments
2. Selecciona deployment anterior
3. Haz clic en "Rollback"

## 💡 **CONSEJOS ADICIONALES**

### **Optimización para Render**
- Render tiene recursos limitados en plan gratuito
- La aplicación puede tardar en responder si está inactiva
- Para mayor rendimiento, considera plan de pago

### **Seguridad**
- Cambia contraseñas por defecto
- Usa variables de entorno para datos sensibles
- No subas archivos `.env`

### **Backup**
- Render no hace backup automático de bases de datos
- Implementa backup manual si es necesario

## 🎉 **¡FELICITACIONES!**

Tu aplicación estará disponible 24/7 en la nube y todos podrán acceder a ella desde cualquier lugar del mundo.

**Próximos pasos:**
1. 📤 Subir a GitHub
2. 🌐 Desplegar en Render
3. ⚙️ Configurar variables
4. 🎉 ¡Disfrutar de tu aplicación en la nube!

---

**📚 Documentación de Render**: https://render.com/docs
**🔧 Soporte**: https://render.com/help
