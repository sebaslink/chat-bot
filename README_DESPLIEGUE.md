# 🚀 Guía de Despliegue - Sistema Unificado Chatbot y Chat Masivo

## 🌐 **OPCIONES GRATUITAS PARA DESPLEGAR**

### 1. **Railway** (Recomendado) ⭐
- **Gratis**: $5 de crédito mensual
- **Fácil**: Despliegue automático desde GitHub
- **Base de datos**: SQLite incluida
- **URL**: `https://tu-app.railway.app`

### 2. **Render** (Muy bueno)
- **Gratis**: 750 horas/mes
- **Base de datos**: PostgreSQL gratuita
- **URL**: `https://tu-app.onrender.com`

### 3. **Heroku** (Tradicional)
- **Gratis**: 550-1000 horas/mes
- **Base de datos**: PostgreSQL gratuita
- **URL**: `https://tu-app.herokuapp.com`

### 4. **PythonAnywhere** (Específico para Python)
- **Gratis**: 1 aplicación web
- **Base de datos**: MySQL/PostgreSQL
- **URL**: `https://tu-usuario.pythonanywhere.com`

## 📋 **INSTRUCCIONES DE DESPLIEGUE EN RAILWAY**

### Paso 1: Preparar el Repositorio
1. **Subir tu código a GitHub**:
   - Crea un repositorio en GitHub
   - Sube todos los archivos del proyecto
   - Asegúrate de incluir todos los archivos necesarios

### Paso 2: Desplegar en Railway
1. **Ir a Railway**:
   - Visita: https://railway.app
   - Regístrate con tu cuenta de GitHub

2. **Crear nuevo proyecto**:
   - Haz clic en "New Project"
   - Selecciona "Deploy from GitHub repo"
   - Elige tu repositorio

3. **Configurar el despliegue**:
   - Railway detectará automáticamente que es una aplicación Python
   - Usará el archivo `requirements.txt` para instalar dependencias
   - Usará el archivo `Procfile` para ejecutar la aplicación

### Paso 3: Configurar Variables de Entorno
1. **En Railway Dashboard**:
   - Ve a tu proyecto
   - Haz clic en "Variables"
   - Agrega las siguientes variables:

```
RAILWAY_ENVIRONMENT=production
PORT=5000
```

### Paso 4: Desplegar
1. **Railway desplegará automáticamente**:
   - El proceso tomará 2-5 minutos
   - Verás el progreso en tiempo real
   - Al finalizar, obtendrás una URL como: `https://tu-app.railway.app`

## 🔧 **CONFIGURACIÓN ADICIONAL**

### Para Twilio (Chat Masivo)
1. **Obtener credenciales de Twilio**:
   - Regístrate en https://twilio.com
   - Obtén tu Account SID y Auth Token
   - Obtén un número de teléfono

2. **Configurar en Railway**:
   - Ve a Variables de Entorno
   - Agrega:
   ```
   TWILIO_ACCOUNT_SID=tu_account_sid
   TWILIO_AUTH_TOKEN=tu_auth_token
   TWILIO_PHONE_NUMBER=tu_numero_twilio
   ```

### Para OpenAI (Chatbot)
1. **Obtener API Key de OpenAI**:
   - Regístrate en https://openai.com
   - Obtén tu API Key

2. **Configurar en Railway**:
   - Ve a Variables de Entorno
   - Agrega:
   ```
   OPENAI_API_KEY=tu_api_key
   ```

## 📱 **USO DESPUÉS DEL DESPLIEGUE**

### Acceso a la Aplicación
1. **URL Principal**: `https://tu-app.railway.app`
2. **Login por defecto**:
   - Usuario: `admin`
   - Contraseña: `admin123`

### Funcionalidades Disponibles
- ✅ **Sistema de Login** con roles de usuario
- ✅ **Chatbot Inteligente** con IA
- ✅ **Carga de Documentos** (PDF, Word, Excel, etc.)
- ✅ **Base de Datos Integrada**
- ✅ **Gestión de Usuarios**
- ✅ **Interfaz Web Responsive**

### Nota sobre Chat Masivo
- El Chat Masivo requiere configuración de Twilio
- Sin Twilio, solo funcionará el Chatbot principal
- Para activar Chat Masivo, configura las variables de Twilio

## 🛠️ **SOLUCIÓN DE PROBLEMAS**

### Error: "Module not found"
- Verifica que `requirements.txt` contenga todas las dependencias
- Railway reinstalará automáticamente las dependencias

### Error: "Port already in use"
- Railway maneja automáticamente el puerto
- No necesitas configurar puertos manualmente

### Error: "Database not found"
- Las bases de datos SQLite se crean automáticamente
- Verifica que los directorios `data/database` existan

### Error: "Twilio not configured"
- Configura las variables de entorno de Twilio
- Sin Twilio, el Chat Masivo no funcionará

## 📊 **MONITOREO**

### Logs de la Aplicación
1. **En Railway Dashboard**:
   - Ve a tu proyecto
   - Haz clic en "Deployments"
   - Selecciona el deployment activo
   - Ve a la pestaña "Logs"

### Métricas de Uso
- Railway proporciona métricas básicas de uso
- Monitorea el uso de recursos en el dashboard

## 🔄 **ACTUALIZACIONES**

### Actualizar la Aplicación
1. **Hacer cambios en tu código local**
2. **Subir cambios a GitHub**:
   ```bash
   git add .
   git commit -m "Actualización"
   git push origin main
   ```
3. **Railway desplegará automáticamente** los cambios

### Rollback
1. **En Railway Dashboard**:
   - Ve a "Deployments"
   - Selecciona un deployment anterior
   - Haz clic en "Redeploy"

## 💡 **CONSEJOS ADICIONALES**

### Optimización de Rendimiento
- Railway proporciona recursos limitados en el plan gratuito
- Para mayor rendimiento, considera actualizar a un plan de pago

### Seguridad
- Cambia las contraseñas por defecto después del despliegue
- Usa variables de entorno para datos sensibles
- No subas archivos `.env` al repositorio

### Backup
- Railway no proporciona backup automático de bases de datos
- Implementa un sistema de backup manual si es necesario

## 🆘 **SOPORTE**

### Documentación de Railway
- https://docs.railway.app

### Comunidad
- Discord de Railway
- GitHub Issues de tu repositorio

### Contacto
- Si tienes problemas específicos con la aplicación, revisa los logs
- Verifica que todas las dependencias estén instaladas correctamente

---

## 🎉 **¡FELICITACIONES!**

Tu aplicación estará disponible 24/7 en la nube y todos podrán acceder a ella desde cualquier lugar del mundo.

**URL de tu aplicación**: `https://tu-app.railway.app`
