#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CHAT MASIVO WHATSAPP - VERSIÓN SIMPLIFICADA
Sistema de envío masivo de mensajes por WhatsApp usando Twilio
Versión sin dependencias externas (pandas/openpyxl)
"""

import os
import sqlite3
import logging
import csv
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from twilio.rest import Client
from dotenv import load_dotenv
import io


# Cargar variables de entorno
load_dotenv('Twilio.env')

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chat_masivo.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuración de Flask
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'clave_super_secreta_para_flask_2024_chatmasivo')

# Configuración de Twilio
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_FROM = os.getenv('TWILIO_WHATSAPP_FROM', 'whatsapp:+TU_NUMERO_TWILIO')

# Modo demo (sin credenciales reales de Twilio)
MODO_DEMO = not (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and 
                 TWILIO_ACCOUNT_SID != 'ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' and 
                 TWILIO_AUTH_TOKEN != 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')


if MODO_DEMO:
    logger.info("=" * 50)
    logger.info("CHAT MASIVO WHATSAPP - MODO DEMO")
    logger.info("=" * 50)
    logger.info("El sistema funciona sin credenciales de Twilio")
    logger.info("Los mensajes se simulan en los logs")
    logger.info("Todas las funciones estan disponibles")
    logger.info("=" * 50)
    logger.info("Accede a: http://localhost:5000")
    logger.info("=" * 50)
else:
    logger.info("=" * 50)
    logger.info("CHAT MASIVO WHATSAPP - MODO PRODUCCION")
    logger.info("=" * 50)
    logger.info("Credenciales de Twilio configuradas correctamente")
    logger.info("Los mensajes se enviaran por WhatsApp real")
    logger.info("Todas las funciones estan disponibles")
    logger.info("=" * 50)
    logger.info("Accede a: http://localhost:5000")
    logger.info("=" * 50)

def init_db():
    """Inicializar base de datos SQLite"""
    try:
        conn = sqlite3.connect('numeros_whatsapp.db')
        cursor = conn.cursor()
        
        # Tabla de números
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS numeros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT DEFAULT '',
                telefono TEXT NOT NULL UNIQUE,
                carrera TEXT DEFAULT '',
                grupo_id INTEGER DEFAULT NULL,
                activo BOOLEAN DEFAULT 1,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (grupo_id) REFERENCES grupos (id)
            )
        ''')
        
        # Tabla de grupos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS grupos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                descripcion TEXT DEFAULT '',
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de logs de mensajes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensajes_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telefono TEXT NOT NULL,
                mensaje TEXT NOT NULL,
                estado TEXT NOT NULL,
                fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                error_detalle TEXT DEFAULT NULL
            )
        ''')
        
        # Tabla de plantillas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plantillas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                contenido TEXT NOT NULL,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Verificar si las columnas necesarias existen, si no, agregarlas
        cursor.execute("PRAGMA table_info(numeros)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'apellido' not in columns:
            cursor.execute('ALTER TABLE numeros ADD COLUMN apellido TEXT DEFAULT ""')
            logger.info("Columna apellido agregada a la tabla numeros")
        
        if 'carrera' not in columns:
            cursor.execute('ALTER TABLE numeros ADD COLUMN carrera TEXT DEFAULT ""')
            logger.info("Columna carrera agregada a la tabla numeros")
        
        conn.commit()
        conn.close()
        logger.info("Base de datos inicializada correctamente")
        
    except Exception as e:
        logger.error(f"Error inicializando base de datos: {e}")

def contar_contactos_activos():
    """Contar contactos activos en la base de datos"""
    conn = sqlite3.connect('numeros_whatsapp.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM numeros WHERE activo = 1')
    count = cursor.fetchone()[0]
    conn.close()
    return count

def agregar_numero(nombre, apellido, telefono, carrera, grupo_id=None):
    """Agregar nuevo número a la base de datos con límite de 5000"""
    # Verificar límite de contactos
    if contar_contactos_activos() >= 5000:
        logger.warning(f"Límite de 5000 contactos alcanzado")
        return False, "Límite de 5000 contactos alcanzado"
    
    try:
        conn = sqlite3.connect('numeros_whatsapp.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO numeros (nombre, apellido, telefono, carrera, grupo_id) VALUES (?, ?, ?, ?, ?)', 
                      (nombre, apellido, telefono, carrera, grupo_id))
        conn.commit()
        conn.close()
        logger.info(f"Número {telefono} agregado exitosamente")
        return True, "Contacto agregado exitosamente"
    except sqlite3.IntegrityError:
        logger.warning(f"El número {telefono} ya existe")
        return False, "El número ya existe"

def desactivar_numero(numero_id):
    """Desactivar número (no eliminar)"""
    conn = sqlite3.connect('numeros_whatsapp.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE numeros SET activo = 0 WHERE id = ?', (numero_id,))
    conn.commit()
    conn.close()

def eliminar_todos_contactos():
    """Eliminar todos los contactos de la base de datos"""
    try:
        conn = sqlite3.connect('numeros_whatsapp.db')
        cursor = conn.cursor()
        
        # Contar contactos antes de eliminar
        cursor.execute('SELECT COUNT(*) FROM numeros WHERE activo = 1')
        total_contactos = cursor.fetchone()[0]
        
        # Eliminar todos los contactos
        cursor.execute('DELETE FROM numeros')
        
        # Limpiar logs de mensajes también
        cursor.execute('DELETE FROM mensajes_log')
        
        conn.commit()
        conn.close()
        
        logger.info(f"Todos los contactos eliminados: {total_contactos} contactos")
        return True, f"Se eliminaron {total_contactos} contactos exitosamente"
        
    except Exception as e:
        logger.error(f"Error eliminando contactos: {e}")
        return False, f"Error eliminando contactos: {str(e)}"

def get_numeros_activos(grupo_id=None):
    """Obtener números activos de la base de datos"""
    conn = sqlite3.connect('numeros_whatsapp.db')
    cursor = conn.cursor()
    
    if grupo_id:
        cursor.execute('''
            SELECT n.id, n.nombre, n.apellido, n.telefono, n.carrera, g.nombre as grupo_nombre
            FROM numeros n
            LEFT JOIN grupos g ON n.grupo_id = g.id
            WHERE n.activo = 1 AND n.grupo_id = ?
            ORDER BY n.fecha_registro DESC
        ''', (grupo_id,))
    else:
        cursor.execute('''
            SELECT n.id, n.nombre, n.apellido, n.telefono, n.carrera, g.nombre as grupo_nombre
            FROM numeros n
            LEFT JOIN grupos g ON n.grupo_id = g.id
            WHERE n.activo = 1
            ORDER BY n.fecha_registro DESC
        ''')
    
    numeros = cursor.fetchall()
    conn.close()
    return numeros

def get_grupos():
    """Obtener lista de grupos"""
    conn = sqlite3.connect('numeros_whatsapp.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre, descripcion FROM grupos ORDER BY nombre')
    grupos = cursor.fetchall()
    conn.close()
    return grupos

def crear_grupo(nombre, descripcion=''):
    """Crear nuevo grupo"""
    try:
        conn = sqlite3.connect('numeros_whatsapp.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO grupos (nombre, descripcion) VALUES (?, ?)', (nombre, descripcion))
        conn.commit()
        conn.close()
        logger.info(f"Grupo '{nombre}' creado exitosamente")
        return True
    except sqlite3.IntegrityError:
        logger.warning(f"El grupo '{nombre}' ya existe")
        return False

def generar_mensaje(nombre, intro="mane", texto_random=None, texto_fijo="Este es el mensaje predeterminado."):
    """Generar mensaje personalizado y único para cada contacto"""
    import random
    
    # Plantillas de saludos personalizados
    saludos = [
        f"Hola {intro} {nombre}",
        f"¡Hola {nombre}!",
        f"Querido/a {nombre}",
        f"Estimado/a {nombre}",
        f"¡Hola {intro} {nombre}!"
    ]
    
    # Plantillas de introducción variadas
    introducciones = [
        "✨ ¡Inicia tu carrera profesional en la Universidad Continental!",
        "🎓 ¡Descubre tu futuro profesional con nosotros!",
        "🚀 ¡Tu futuro profesional te espera en la Universidad Continental!",
        "💼 ¡Comienza tu camino hacia el éxito profesional!",
        "🌟 ¡Abre las puertas a tu carrera profesional!"
    ]
    
    # Plantillas de contenido variadas
    contenidos = [
        "Conoce todo lo que te espera en la modalidad presencial 🏫",
        "Descubre las oportunidades que tenemos para ti 🎯",
        "Explora las carreras que transformarán tu futuro 📚",
        "Conoce nuestros programas académicos de excelencia 🏆",
        "Descubre la educación que cambiará tu vida 💡"
    ]
    
    # Plantillas de evento variadas
    eventos = [
        "📅 Miércoles 24 de septiembre\n🕕 6:00 p.m.\n💻 Vía Zoom",
        "📅 Jueves 25 de septiembre\n🕕 7:00 p.m.\n💻 Vía Zoom",
        "📅 Viernes 26 de septiembre\n🕕 6:30 p.m.\n💻 Vía Zoom",
        "📅 Sábado 27 de septiembre\n🕕 10:00 a.m.\n💻 Vía Zoom",
        "📅 Domingo 28 de septiembre\n🕕 5:00 p.m.\n💻 Vía Zoom"
    ]
    
    # Plantillas de cierre variadas
    cierres = [
        "¡Te esperamos! 🚀",
        "¡No te lo pierdas! ⭐",
        "¡Será un placer verte! 👋",
        "¡Esperamos verte pronto! 🤝",
        "¡Te esperamos con mucha ilusión! 💫"
    ]
    
    # Seleccionar elementos aleatorios para personalizar
    saludo = random.choice(saludos)
    introduccion = random.choice(introducciones)
    contenido = random.choice(contenidos)
    evento = random.choice(eventos)
    cierre = random.choice(cierres)
    
    # Construir mensaje personalizado
    mensaje = f"""{saludo}, {introduccion}
{contenido}
{evento}
👉 Regístrate aquí: https://us02web.zoom.us/meeting/register/Dlpc8_aXSMmq1xBbV3OLhg
{cierre}"""
    
    return mensaje

def enviar_whatsapp_masivo(numeros, intro="mane", texto_random=None, texto_fijo="Este es el mensaje predeterminado."):
    """Enviar mensajes masivos por WhatsApp"""
    if MODO_DEMO:
        logger.info("=" * 50)
        logger.info("🚀 SIMULANDO ENVÍO MASIVO (MODO DEMO)")
        logger.info("=" * 50)
        
        for numero in numeros:
            nombre = numero[1] + " " + numero[2] if numero[2] else numero[1]
            telefono = numero[3]
            mensaje = generar_mensaje(nombre, intro, texto_random, texto_fijo)
            
            logger.info(f"📱 SIMULANDO envío a {telefono} ({nombre})")
            logger.info(f"💬 Mensaje personalizado:")
            logger.info(f"{mensaje}")
            logger.info("-" * 30)
            
            # Simular delay
            import time
            time.sleep(0.1)
        
        logger.info(f"✅ SIMULACIÓN COMPLETADA: {len(numeros)} mensajes")
        logger.info("=" * 50)
        return True
    else:
        # Código real de Twilio (cuando tengas credenciales)
        try:
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            
            for numero in numeros:
                nombre = numero[1] + " " + numero[2] if numero[2] else numero[1]
                telefono = numero[3]
                mensaje = generar_mensaje(nombre, intro, texto_random, texto_fijo)
                
                logger.info(f"📱 Enviando mensaje personalizado a {telefono} ({nombre})")
                logger.info(f"💬 Mensaje: {mensaje[:100]}...")
                
                try:
                    message = client.messages.create(
                        body=mensaje,
                        from_=TWILIO_WHATSAPP_FROM,
                        to=f'whatsapp:+{telefono}'
                    )
                    logger.info(f"✅ Mensaje enviado a {telefono}: {message.sid}")
                    log_mensaje(telefono, mensaje, "enviado")
                except Exception as e:
                    error_msg = str(e)
                    logger.error(f"Error enviando a {telefono}: {error_msg}")
                    
                    # Manejar errores específicos de Twilio
                    if "21211" in error_msg:
                        logger.error(f"El número {telefono} no está registrado en WhatsApp o no está permitido para tu cuenta Trial")
                    elif "21212" in error_msg:
                        logger.error(f"El número {telefono} no es un número de WhatsApp válido")
                    elif "21214" in error_msg:
                        logger.error(f"El número {telefono} no está en la lista de números permitidos para tu cuenta Trial")
                    
                    log_mensaje(telefono, mensaje, "error", error_msg)
            
            return True
        except Exception as e:
            logger.error(f"Error en envío masivo: {e}")
            return False

def verificar_numero_trial(telefono):
    """Verificar si un número está permitido para cuentas Trial de Twilio"""
    # Números mágicos de Twilio para pruebas
    numeros_magicos = [
        "+15005550006",  # Número mágico de Twilio
        "+15005550001",  # Número mágico de Twilio
        "+15005550002",  # Número mágico de Twilio
        "+15005550003",  # Número mágico de Twilio
        "+15005550004",  # Número mágico de Twilio
        "+15005550005",  # Número mágico de Twilio
        "+15005550007",  # Número mágico de Twilio
        "+15005550008",  # Número mágico de Twilio
        "+15005550009",  # Número mágico de Twilio
        "+15005550010",  # Número mágico de Twilio
    ]
    
    # Verificar si el número está en formato correcto
    if not telefono.startswith('+'):
        telefono = f'+{telefono}'
    
    return telefono in numeros_magicos

def log_mensaje(telefono, mensaje, estado, error_detalle=None):
    """Registrar mensaje en log"""
    conn = sqlite3.connect('numeros_whatsapp.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO mensajes_log (telefono, mensaje, estado, error_detalle)
        VALUES (?, ?, ?, ?)
    ''', (telefono, mensaje, estado, error_detalle))
    conn.commit()
    conn.close()

def get_estadisticas():
    """Obtener estadísticas del sistema"""
    conn = sqlite3.connect('numeros_whatsapp.db')
    cursor = conn.cursor()
    
    # Total de contactos activos
    cursor.execute('SELECT COUNT(*) FROM numeros WHERE activo = 1')
    total_contactos = cursor.fetchone()[0]
    
    # Mensajes enviados hoy
    hoy = datetime.now().date()
    cursor.execute('SELECT COUNT(*) FROM mensajes_log WHERE DATE(fecha_envio) = ? AND estado = "enviado"', (hoy,))
    mensajes_hoy = cursor.fetchone()[0]
    
    # Mensajes enviados esta semana
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    cursor.execute('SELECT COUNT(*) FROM mensajes_log WHERE DATE(fecha_envio) >= ? AND estado = "enviado"', (inicio_semana,))
    mensajes_semana = cursor.fetchone()[0]
    
    # Errores recientes
    cursor.execute('SELECT COUNT(*) FROM mensajes_log WHERE estado = "error" AND DATE(fecha_envio) = ?', (hoy,))
    errores_recientes = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'total_contactos': total_contactos,
        'mensajes_hoy': mensajes_hoy,
        'mensajes_semana': mensajes_semana,
        'errores_recientes': errores_recientes
    }

def exportar_contactos_csv():
    """Exportar contactos a CSV"""
    numeros = get_numeros_activos()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Escribir encabezados
    writer.writerow(['ID', 'Nombre', 'Apellido', 'Teléfono', 'Carrera', 'Grupo'])
    
    # Escribir datos
    for numero in numeros:
        writer.writerow([
            numero[0],  # ID
            numero[1],  # Nombre
            numero[2],  # Apellido
            numero[3],  # Teléfono
            numero[4],  # Carrera
            numero[5] or 'Sin grupo'  # Grupo
        ])
    
    output.seek(0)
    return output.getvalue()

def crear_plantilla_excel():
    """Crear plantilla de Excel para importar contactos"""
    try:
        import pandas as pd
        
        # Crear DataFrame con ejemplo
        data = {
            'nombre': ['Juan', 'María', 'Carlos'],
            'apellido': ['Pérez', 'González', 'López'],
            'numero': ['51987654321', '51912345678', '51911223344'],
            'carrera': ['Ingeniería', 'Medicina', 'Derecho']
        }
        
        df = pd.DataFrame(data)
        
        # Crear archivo Excel en memoria
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Contactos', index=False)
        
        output.seek(0)
        return output.getvalue()
        
    except ImportError as e:
        logger.warning(f"Pandas no disponible, creando plantilla CSV: {e}")
        # Fallback a CSV si pandas no está disponible
        return crear_plantilla_csv()
    except Exception as e:
        logger.error(f"Error creando plantilla Excel: {e}")
        return None

def crear_plantilla_csv():
    """Crear plantilla CSV como respaldo"""
    try:
        # Crear datos de ejemplo
        data = [
            ['nombre', 'apellido', 'numero', 'carrera'],
            ['Juan', 'Pérez', '51987654321', 'Ingeniería'],
            ['María', 'González', '51912345678', 'Medicina'],
            ['Carlos', 'López', '51911223344', 'Derecho']
        ]
        
        # Crear archivo CSV en memoria
        output = io.StringIO()
        writer = csv.writer(output)
        
        for row in data:
            writer.writerow(row)
        
        output.seek(0)
        return output.getvalue().encode('utf-8')
        
    except Exception as e:
        logger.error(f"Error creando plantilla CSV: {e}")
        return None

# Rutas de Flask
@app.route('/')
def index():
    """Página principal"""
    numeros = get_numeros_activos()
    grupos = get_grupos()
    estadisticas = get_estadisticas()
    
    return render_template('interface_simple.html', 
                         numeros=numeros, 
                         grupos=grupos, 
                         estadisticas=estadisticas,
                         numero_prueba="1234567890")

@app.route('/agregar', methods=['POST'])
def agregar():
    """Agregar nuevo contacto"""
    nombre = request.form.get('nombre', '').strip()
    apellido = request.form.get('apellido', '').strip()
    telefono = request.form.get('telefono', '').strip()
    carrera = request.form.get('carrera', '').strip()
    grupo_id = request.form.get('grupo_id', '')
    
    if not nombre or not telefono:
        flash('Nombre y teléfono son obligatorios', 'error')
        return redirect(url_for('index'))
    
    # Limpiar número (solo dígitos)
    telefono = ''.join(filter(str.isdigit, telefono))
    
    # Convertir grupo_id a int si existe
    grupo_id = int(grupo_id) if grupo_id and grupo_id != '' else None
    
    success, message = agregar_numero(nombre, apellido, telefono, carrera, grupo_id)
    if success:
        flash(f'Contacto {nombre} {apellido} agregado exitosamente', 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('index'))

@app.route('/desactivar/<int:numero_id>')
def desactivar(numero_id):
    """Desactivar número"""
    desactivar_numero(numero_id)
    flash('Número desactivado', 'info')
    return redirect(url_for('index'))

@app.route('/eliminar_todos_contactos', methods=['POST'])
def eliminar_todos_contactos_route():
    """Eliminar todos los contactos"""
    try:
        success, message = eliminar_todos_contactos()
        if success:
            flash(message, 'success')
        else:
            flash(message, 'error')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/enviar_masivo', methods=['POST'])
def enviar_masivo():
    """Enviar mensajes masivos"""
    intro = request.form.get('intro', 'mane')
    texto_random = request.form.get('texto_random', '')
    texto_fijo = request.form.get('texto_fijo', 'Este es el mensaje predeterminado.')
    grupo_id = request.form.get('grupo_id', '')
    
    # Obtener números según el grupo seleccionado
    if grupo_id and grupo_id != '':
        numeros = get_numeros_activos(int(grupo_id))
    else:
        numeros = get_numeros_activos()
    
    if not numeros:
        flash('No hay contactos activos para enviar mensajes', 'warning')
        return redirect(url_for('index'))
    
    # Enviar mensajes
    if enviar_whatsapp_masivo(numeros, intro, texto_random, texto_fijo):
        flash(f'Mensajes enviados a {len(numeros)} contactos', 'success')
    else:
        flash('Error enviando mensajes', 'error')
    
    return redirect(url_for('index'))

@app.route('/api/enviar_prueba', methods=['POST'])
def enviar_prueba():
    """Enviar mensaje de prueba"""
    # Usar un número de prueba válido
    numero_prueba = "51914649592"  # Número de prueba válido
    
    if MODO_DEMO:
        logger.info("=" * 30)
        logger.info("SIMULANDO MENSAJE DE PRUEBA")
        logger.info("=" * 30)
        logger.info(f"Número: {numero_prueba}")
        logger.info("Mensaje: Hola, este es un mensaje de prueba del sistema de chat masivo.")
        logger.info("SIMULACION EXITOSA")
        logger.info("=" * 30)
        
        return jsonify({
            'success': True,
            'message': 'Mensaje de prueba simulado exitosamente (Modo Demo)'
        })
    else:
        # Código real de Twilio
        try:
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            
            # Verificar si es una cuenta Trial
            if verificar_numero_trial(numero_prueba):
                logger.info(f"Usando número mágico de Twilio: {numero_prueba}")
            else:
                logger.warning(f"El número {numero_prueba} no es un número mágico de Twilio")
            
            mensaje_prueba = "Hola, este es un mensaje de prueba del sistema de chat masivo WhatsApp. 🚀"
            
            message = client.messages.create(
                body=mensaje_prueba,
                from_=TWILIO_WHATSAPP_FROM,
                to=f'whatsapp:+{numero_prueba}'
            )
            
            logger.info(f"Mensaje de prueba enviado exitosamente. SID: {message.sid}")
            
            return jsonify({
                'success': True,
                'message': f'Mensaje de prueba enviado exitosamente. SID: {message.sid}',
                'sid': message.sid,
                'numero_usado': numero_prueba
            })
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error enviando mensaje de prueba: {error_msg}")
            
            # Manejar errores específicos
            if "21211" in error_msg:
                error_detalle = "El número no está registrado en WhatsApp o no está permitido para tu cuenta Trial. Usa números mágicos de Twilio para pruebas."
            elif "21212" in error_msg:
                error_detalle = "El número no es un número de WhatsApp válido."
            elif "21214" in error_msg:
                error_detalle = "El número no está en la lista de números permitidos para tu cuenta Trial."
            else:
                error_detalle = error_msg
            
            return jsonify({
                'success': False,
                'message': f'Error enviando mensaje de prueba: {error_detalle}',
                'error_code': error_msg,
                'sugerencia': 'Para cuentas Trial, usa números mágicos de Twilio como 15005550006'
            })

@app.route('/api/estadisticas')
def api_estadisticas():
    """API para obtener estadísticas"""
    return jsonify(get_estadisticas())

@app.route('/importar_excel', methods=['POST'])
def importar_excel():
    """Importar contactos desde archivo Excel"""
    try:
        if 'archivo' not in request.files:
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(url_for('index'))
        
        archivo = request.files['archivo']
        if archivo.filename == '':
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(url_for('index'))
        
        if archivo and archivo.filename.lower().endswith(('.xlsx', '.xls', '.csv')):
            # Leer el archivo
            if archivo.filename.lower().endswith('.csv'):
                # Procesar CSV
                contenido = archivo.read().decode('utf-8')
                lineas = contenido.strip().split('\n')
                
                contactos_importados = 0
                for i, linea in enumerate(lineas[1:], 1):  # Saltar encabezado
                    try:
                        datos = linea.split(',')
                        if len(datos) >= 4:
                            nombre = datos[0].strip().strip('"')
                            apellido = datos[1].strip().strip('"')
                            telefono = datos[2].strip().strip('"')
                            carrera = datos[3].strip().strip('"')
                            
                            # Agregar contacto a la base de datos
                            conn = sqlite3.connect('numeros_whatsapp.db')
                            cursor = conn.cursor()
                            cursor.execute('''
                                INSERT OR REPLACE INTO numeros (nombre, apellido, telefono, carrera, activo)
                                VALUES (?, ?, ?, ?, ?)
                            ''', (nombre, apellido, telefono, carrera, 1))
                            conn.commit()
                            conn.close()
                            
                            contactos_importados += 1
                    except Exception as e:
                        logger.error(f"Error procesando línea {i}: {e}")
                        continue
                
                flash(f'Se importaron {contactos_importados} contactos desde CSV', 'success')
                
            else:
                # Procesar Excel
                try:
                    import pandas as pd
                    
                    # Leer archivo Excel
                    df = pd.read_excel(archivo)
                    
                    # Verificar columnas requeridas
                    columnas_requeridas = ['nombre', 'apellido', 'numero', 'carrera']
                    if not all(col in df.columns for col in columnas_requeridas):
                        flash('El archivo Excel debe contener las columnas: nombre, apellido, numero, carrera', 'error')
                        return redirect(url_for('index'))
                    
                    contactos_importados = 0
                    for _, fila in df.iterrows():
                        try:
                            nombre = str(fila['nombre']).strip()
                            apellido = str(fila['apellido']).strip()
                            telefono = str(fila['numero']).strip()
                            carrera = str(fila['carrera']).strip()
                            
                            # Agregar contacto a la base de datos
                            conn = sqlite3.connect('numeros_whatsapp.db')
                            cursor = conn.cursor()
                            cursor.execute('''
                                INSERT OR REPLACE INTO numeros (nombre, apellido, telefono, carrera, activo)
                                VALUES (?, ?, ?, ?, ?)
                            ''', (nombre, apellido, telefono, carrera, 1))
                            conn.commit()
                            conn.close()
                            
                            contactos_importados += 1
                        except Exception as e:
                            logger.error(f"Error procesando fila: {e}")
                            continue
                    
                    flash(f'Se importaron {contactos_importados} contactos desde Excel', 'success')
                    
                except ImportError:
                    flash('Error: pandas no está instalado. Instala con: pip install pandas openpyxl', 'error')
                    return redirect(url_for('index'))
                except Exception as e:
                    flash(f'Error procesando archivo Excel: {e}', 'error')
                    return redirect(url_for('index'))
            
            logger.info(f"Archivo importado exitosamente: {contactos_importados} contactos")
            return redirect(url_for('index'))
        else:
            flash('Formato de archivo no válido. Use .xlsx, .xls o .csv', 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        logger.error(f"Error importando archivo: {e}")
        flash(f'Error importando archivo: {e}', 'error')
        return redirect(url_for('index'))

@app.route('/exportar_contactos')
def exportar_contactos():
    """Exportar contactos a CSV"""
    csv_data = exportar_contactos_csv()
    
    output = io.BytesIO()
    output.write(csv_data.encode('utf-8'))
    output.seek(0)
    
    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'contactos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@app.route('/descargar_plantilla_excel')
def descargar_plantilla_excel():
    """Descargar plantilla de Excel"""
    try:
        plantilla = crear_plantilla_excel()
        if plantilla:
            output = io.BytesIO()
            output.write(plantilla)
            output.seek(0)
            
            # Detectar si es Excel o CSV basado en el contenido
            try:
                import pandas as pd
                # Si llegamos aquí, pandas está disponible y es Excel
                return send_file(
                    output,
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    as_attachment=True,
                    download_name='plantilla_contactos.xlsx'
                )
            except ImportError:
                # Si pandas no está disponible, es CSV
                return send_file(
                    output,
                    mimetype='text/csv',
                    as_attachment=True,
                    download_name='plantilla_contactos.csv'
                )
        else:
            flash('Error creando plantilla', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
