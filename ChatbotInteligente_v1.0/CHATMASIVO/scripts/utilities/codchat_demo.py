from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
import sqlite3
import os
import logging
from dotenv import load_dotenv
import random
from datetime import datetime, timedelta
import csv
import io
import pandas as pd
from werkzeug.utils import secure_filename

load_dotenv('Twilio.env')

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'tu_clave_secreta_aqui')

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chatmasivo.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuración Twilio (modo demo)
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_FROM = os.getenv('TWILIO_WHATSAPP_FROM', 'whatsapp:+TU_NUMERO_TWILIO')

# Número de prueba
NUMERO_PRUEBA = "+TU_NUMERO_PRUEBA"

# Modo demo (sin Twilio real)
MODO_DEMO = True

def init_db():
    """Crear base de datos y tablas si no existen"""
    conn = sqlite3.connect('numeros_whatsapp.db')
    cursor = conn.cursor()
    
    # Tabla de grupos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS grupos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            descripcion TEXT,
            activo BOOLEAN DEFAULT 1,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de números (actualizada)
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
    
    # Tabla de logs de mensajes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mensajes_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_id INTEGER,
            mensaje TEXT,
            status TEXT,
            twilio_sid TEXT,
            error_message TEXT,
            fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (numero_id) REFERENCES numeros (id)
        )
    ''')
    
    # Tabla de plantillas de mensajes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plantillas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            intro TEXT,
            texto_random TEXT,
            texto_fijo TEXT,
            activa BOOLEAN DEFAULT 1,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insertar grupo por defecto
    cursor.execute('SELECT COUNT(*) FROM grupos WHERE nombre = ?', ('General',))
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO grupos (nombre, descripcion) VALUES (?, ?)', 
                      ('General', 'Grupo por defecto para todos los contactos'))
    
    conn.commit()
    conn.close()
    logger.info("Base de datos inicializada correctamente")

def get_numeros_activos(grupo_id=None):
    """Obtener todos los números activos, opcionalmente filtrados por grupo"""
    conn = sqlite3.connect('numeros_whatsapp.db')
    cursor = conn.cursor()
    
    if grupo_id:
        cursor.execute('''
            SELECT n.id, n.nombre, n.apellido, n.telefono, n.carrera, g.nombre as grupo_nombre 
            FROM numeros n 
            LEFT JOIN grupos g ON n.grupo_id = g.id 
            WHERE n.activo = 1 AND n.grupo_id = ?
        ''', (grupo_id,))
    else:
        cursor.execute('''
            SELECT n.id, n.nombre, n.apellido, n.telefono, n.carrera, g.nombre as grupo_nombre 
            FROM numeros n 
            LEFT JOIN grupos g ON n.grupo_id = g.id 
            WHERE n.activo = 1
        ''')
    
    numeros = cursor.fetchall()
    conn.close()
    return numeros

def get_grupos():
    """Obtener todos los grupos activos"""
    conn = sqlite3.connect('numeros_whatsapp.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre, descripcion FROM grupos WHERE activo = 1')
    grupos = cursor.fetchall()
    conn.close()
    return grupos

def crear_grupo(nombre, descripcion=""):
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
        logger.warning(f"Grupo '{nombre}' ya existe")
        return False

def guardar_plantilla(nombre, intro, texto_random, texto_fijo):
    """Guardar plantilla de mensaje"""
    try:
        conn = sqlite3.connect('numeros_whatsapp.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO plantillas (nombre, intro, texto_random, texto_fijo) 
            VALUES (?, ?, ?, ?)
        ''', (nombre, intro, texto_random, texto_fijo))
        conn.commit()
        conn.close()
        logger.info(f"Plantilla '{nombre}' guardada exitosamente")
        return True
    except Exception as e:
        logger.error(f"Error al guardar plantilla: {e}")
        return False

def get_plantillas():
    """Obtener todas las plantillas activas"""
    conn = sqlite3.connect('numeros_whatsapp.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre, intro, texto_random, texto_fijo FROM plantillas WHERE activa = 1')
    plantillas = cursor.fetchall()
    conn.close()
    return plantillas

def log_mensaje(numero_id, mensaje, status, twilio_sid=None, error_message=None):
    """Registrar envío de mensaje en el log"""
    conn = sqlite3.connect('numeros_whatsapp.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO mensajes_log (numero_id, mensaje, status, twilio_sid, error_message) 
        VALUES (?, ?, ?, ?, ?)
    ''', (numero_id, mensaje, status, twilio_sid, error_message))
    conn.commit()
    conn.close()
    logger.info(f"Mensaje loggeado: {status} para número ID {numero_id}")

def get_estadisticas():
    """Obtener estadísticas de envíos"""
    conn = sqlite3.connect('numeros_whatsapp.db')
    cursor = conn.cursor()
    
    # Total de contactos
    cursor.execute('SELECT COUNT(*) FROM numeros WHERE activo = 1')
    total_contactos = cursor.fetchone()[0]
    
    # Mensajes enviados hoy
    cursor.execute('''
        SELECT COUNT(*) FROM mensajes_log 
        WHERE status = 'enviado' AND DATE(fecha_envio) = DATE('now')
    ''')
    mensajes_hoy = cursor.fetchone()[0]
    
    # Mensajes enviados esta semana
    cursor.execute('''
        SELECT COUNT(*) FROM mensajes_log 
        WHERE status = 'enviado' AND fecha_envio >= datetime('now', '-7 days')
    ''')
    mensajes_semana = cursor.fetchone()[0]
    
    # Errores recientes
    cursor.execute('''
        SELECT COUNT(*) FROM mensajes_log 
        WHERE status = 'error' AND fecha_envio >= datetime('now', '-24 hours')
    ''')
    errores_recientes = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'total_contactos': total_contactos,
        'mensajes_hoy': mensajes_hoy,
        'mensajes_semana': mensajes_semana,
        'errores_recientes': errores_recientes
    }

def importar_desde_excel(archivo_excel, grupo_id=None):
    """Importar contactos desde archivo Excel con límite de 5000"""
    try:
        # Leer el archivo Excel
        df = pd.read_excel(archivo_excel)
        
        # Verificar límite antes de procesar
        contactos_actuales = contar_contactos_activos()
        if contactos_actuales >= 5000:
            return {
                'success': False,
                'message': f'Límite de 5000 contactos alcanzado. Contactos actuales: {contactos_actuales}'
            }
        
        # Verificar que tenga las columnas necesarias
        columnas_requeridas = ['nombre', 'apellido', 'numero', 'carrera', 'grupo']
        columnas_disponibles = [col.lower().strip() for col in df.columns]
        
        # Mapear columnas (case insensitive)
        mapeo_columnas = {}
        for col_req in columnas_requeridas:
            for col_disp in columnas_disponibles:
                if col_req in col_disp or col_disp in col_req:
                    mapeo_columnas[col_req] = df.columns[columnas_disponibles.index(col_disp)]
                    break
        
        # Verificar que se encontraron todas las columnas
        if len(mapeo_columnas) < 5:
            return {
                'success': False, 
                'message': f'Faltan columnas requeridas. Se encontraron: {list(mapeo_columnas.keys())}'
            }
        
        # Procesar cada fila
        resultados = {
            'exitosos': 0,
            'errores': 0,
            'duplicados': 0,
            'limite_alcanzado': False,
            'detalles': []
        }
        
        for index, row in df.iterrows():
            # Verificar límite en cada iteración
            if contar_contactos_activos() >= 5000:
                resultados['limite_alcanzado'] = True
                resultados['detalles'].append(f"Límite de 5000 contactos alcanzado en fila {index + 2}")
                break
                
            try:
                nombre = str(row[mapeo_columnas['nombre']]).strip()
                apellido = str(row[mapeo_columnas['apellido']]).strip()
                numero = str(row[mapeo_columnas['numero']]).strip()
                carrera = str(row[mapeo_columnas['carrera']]).strip()
                grupo_nombre = str(row[mapeo_columnas['grupo']]).strip()
                
                # Limpiar número (solo dígitos)
                numero_limpio = ''.join(filter(str.isdigit, numero))
                
                if not nombre or not numero_limpio:
                    resultados['errores'] += 1
                    resultados['detalles'].append(f"Fila {index + 2}: Faltan datos obligatorios")
                    continue
                
                # Obtener ID del grupo por nombre
                grupo_id_final = grupo_id  # Usar el grupo_id pasado como parámetro si existe
                if not grupo_id_final and grupo_nombre:
                    # Buscar el grupo por nombre
                    conn = sqlite3.connect('numeros_whatsapp.db')
                    cursor = conn.cursor()
                    cursor.execute('SELECT id FROM grupos WHERE nombre = ?', (grupo_nombre,))
                    grupo_result = cursor.fetchone()
                    conn.close()
                    if grupo_result:
                        grupo_id_final = grupo_result[0]
                
                # Intentar agregar el contacto
                success, message = agregar_numero(nombre, apellido, numero_limpio, carrera, grupo_id_final)
                if success:
                    resultados['exitosos'] += 1
                    resultados['detalles'].append(f"Fila {index + 2}: {nombre} {apellido} - Agregado exitosamente")
                elif "Límite" in message:
                    resultados['limite_alcanzado'] = True
                    resultados['detalles'].append(f"Fila {index + 2}: Límite de 5000 contactos alcanzado")
                    break
                else:
                    resultados['duplicados'] += 1
                    resultados['detalles'].append(f"Fila {index + 2}: {nombre} {apellido} - Número duplicado")
                    
            except Exception as e:
                resultados['errores'] += 1
                resultados['detalles'].append(f"Fila {index + 2}: Error - {str(e)}")
        
        logger.info(f"Importación desde Excel completada: {resultados['exitosos']} exitosos, {resultados['errores']} errores, {resultados['duplicados']} duplicados")
        
        return {
            'success': True,
            'resultados': resultados
        }
        
    except Exception as e:
        logger.error(f"Error importando desde Excel: {e}")
        return {
            'success': False,
            'message': f'Error procesando archivo Excel: {str(e)}'
        }

def crear_plantilla_excel():
    """Crear plantilla de Excel para importar contactos"""
    try:
        # Crear DataFrame con ejemplo
        data = {
            'nombre': ['Juan', 'María', 'Carlos'],
            'apellido': ['Pérez', 'González', 'López'],
            'numero': ['51987654321', '51912345678', '51911223344'],
            'carrera': ['Ingeniería', 'Medicina', 'Derecho']
        }
        
        df = pd.DataFrame(data)
        
        # Crear archivo en memoria
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Contactos', index=False)
        
        output.seek(0)
        
        return output.getvalue()
        
    except Exception as e:
        logger.error(f"Error creando plantilla Excel: {e}")
        return None

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

def generar_mensaje(nombre, intro="mane", texto_random=None, texto_fijo="Este es el mensaje predeterminado."):
    """Generar mensaje personalizado"""
    opciones_random = [
        "Tenemos una novedad que podría interesarte.",
        "Te comparto una actualización rápida.",
        "Solo paso a dejarte este aviso importante.",
        "Gracias por tu atención, aquí va la info."
    ]
    
    if not texto_random:
        texto_random = random.choice(opciones_random)
    
    partes = [
        intro.strip(),
        f"Hola {nombre},".strip(),
        texto_random.strip(),
        texto_fijo.strip()
    ]
    return "\n\n".join(p for p in partes if p)

def enviar_whatsapp_masivo(intro="mane", texto_fijo="Este es el mensaje predeterminado.", 
                          texto_random=None, grupo_id=None):
    """Enviar mensajes masivos por WhatsApp (modo demo)"""
    numeros = get_numeros_activos(grupo_id)
    resultados = []
    
    logger.info(f"Iniciando envío masivo a {len(numeros)} contactos (MODO DEMO)")
    
    for numero_id, nombre, apellido, telefono, carrera, grupo_nombre in numeros:
        try:
            mensaje = generar_mensaje(nombre, intro, texto_random, texto_fijo)
            
            # Simular envío exitoso en modo demo
            if MODO_DEMO:
                logger.info(f"[DEMO] Mensaje simulado enviado a {nombre} ({telefono})")
                logger.info(f"[DEMO] Contenido: {mensaje[:100]}...")
                
                # Log del mensaje simulado
                log_mensaje(numero_id, mensaje, "enviado", f"DEMO_{numero_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}")
                
                resultados.append({
                    "nombre": nombre,
                    "telefono": telefono,
                    "grupo": grupo_nombre,
                    "status": "enviado",
                    "sid": f"DEMO_{numero_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                })
            else:
                # Código real de Twilio aquí (cuando tengas credenciales válidas)
                pass
            
        except Exception as e:
            logger.error(f"Error en modo demo: {e}")
            resultados.append({
                "nombre": nombre,
                "telefono": telefono,
                "grupo": grupo_nombre,
                "status": "error",
                "error": str(e)
            })
    
    logger.info(f"Envío masivo completado (MODO DEMO). Exitosos: {len([r for r in resultados if r['status'] == 'enviado'])}, Errores: {len([r for r in resultados if r['status'] == 'error'])}")
    return {"success": True, "resultados": resultados}

@app.route('/')
def index():
    """Página principal"""
    numeros = get_numeros_activos()
    grupos = get_grupos()
    plantillas = get_plantillas()
    estadisticas = get_estadisticas()
    return render_template('interface_simple.html', 
                         numeros=numeros, 
                         grupos=grupos,
                         plantillas=plantillas,
                         estadisticas=estadisticas,
                         numero_prueba=NUMERO_PRUEBA)

@app.route('/agregar', methods=['POST'])
def agregar():
    """Agregar nuevo número"""
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido', '')
    telefono = request.form.get('telefono')
    carrera = request.form.get('carrera', '')
    grupo_id = request.form.get('grupo_id')
    
    if not nombre or not telefono:
        flash('Nombre y teléfono son requeridos', 'error')
        return redirect(url_for('index'))
    
    # Limpiar número (quitar espacios, guiones, etc.)
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
    texto_fijo = request.form.get('texto_fijo', 'Este es el mensaje predeterminado.')
    texto_random = request.form.get('texto_random', '')
    grupo_id = request.form.get('grupo_id', '')
    
    if not texto_random:
        texto_random = None
    
    # Convertir grupo_id a int si existe
    grupo_id = int(grupo_id) if grupo_id and grupo_id != '' else None
    
    resultado = enviar_whatsapp_masivo(intro, texto_fijo, texto_random, grupo_id)
    
    if resultado['success']:
        enviados = len([r for r in resultado['resultados'] if r['status'] == 'enviado'])
        errores = len([r for r in resultado['resultados'] if r['status'] == 'error'])
        flash(f'[MODO DEMO] Mensajes simulados: {enviados}, Errores: {errores}', 'success')
    else:
        flash(f'Error: {resultado["message"]}', 'error')
    
    return redirect(url_for('index'))

@app.route('/api/enviar_prueba', methods=['POST'])
def enviar_prueba():
    """API para enviar mensaje de prueba (modo demo)"""
    try:
        mensaje = generar_mensaje("Usuario de Prueba", "mane", None, "Mensaje de prueba desde el sistema (MODO DEMO).")
        
        if MODO_DEMO:
            logger.info(f"[DEMO] Mensaje de prueba simulado: {mensaje[:100]}...")
            return jsonify({
                "success": True, 
                "message": "Mensaje de prueba simulado (MODO DEMO)",
                "sid": f"DEMO_PRUEBA_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            })
        else:
            # Código real de Twilio aquí
            return jsonify({"success": False, "message": "Modo demo desactivado"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/crear_grupo', methods=['POST'])
def crear_grupo_route():
    """Crear nuevo grupo"""
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion', '')
    
    if not nombre:
        flash('Nombre del grupo es requerido', 'error')
        return redirect(url_for('index'))
    
    if crear_grupo(nombre, descripcion):
        flash(f'Grupo "{nombre}" creado exitosamente', 'success')
    else:
        flash(f'El grupo "{nombre}" ya existe', 'error')
    
    return redirect(url_for('index'))

@app.route('/guardar_plantilla', methods=['POST'])
def guardar_plantilla_route():
    """Guardar plantilla de mensaje"""
    nombre = request.form.get('nombre')
    intro = request.form.get('intro', 'mane')
    texto_random = request.form.get('texto_random', '')
    texto_fijo = request.form.get('texto_fijo', '')
    
    if not nombre or not texto_fijo:
        flash('Nombre y texto fijo son requeridos', 'error')
        return redirect(url_for('index'))
    
    if guardar_plantilla(nombre, intro, texto_random, texto_fijo):
        flash(f'Plantilla "{nombre}" guardada exitosamente', 'success')
    else:
        flash(f'Error al guardar plantilla', 'error')
    
    return redirect(url_for('index'))

@app.route('/exportar_contactos')
def exportar_contactos():
    """Exportar contactos a CSV"""
    numeros = get_numeros_activos()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Nombre', 'Teléfono', 'Grupo'])
    
    for numero in numeros:
        writer.writerow([numero[0], numero[1], numero[2], numero[3] or 'Sin grupo'])
    
    output.seek(0)
    
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'contactos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@app.route('/api/estadisticas')
def api_estadisticas():
    """API para obtener estadísticas"""
    return jsonify(get_estadisticas())

@app.route('/descargar_plantilla_excel')
def descargar_plantilla_excel():
    """Descargar plantilla de Excel"""
    try:
        plantilla = crear_plantilla_excel()
        if plantilla:
            return send_file(
                io.BytesIO(plantilla),
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name='plantilla_contactos.xlsx'
            )
        else:
            flash('Error creando plantilla', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/importar_excel', methods=['POST'])
def importar_excel():
    """Importar contactos desde Excel"""
    try:
        if 'archivo_excel' not in request.files:
            flash('No se seleccionó archivo', 'error')
            return redirect(url_for('index'))
        
        archivo = request.files['archivo_excel']
        grupo_id = request.form.get('grupo_importar', '')
        
        if archivo.filename == '':
            flash('No se seleccionó archivo', 'error')
            return redirect(url_for('index'))
        
        if archivo and archivo.filename.endswith(('.xlsx', '.xls')):
            # Convertir grupo_id a int si existe
            grupo_id = int(grupo_id) if grupo_id and grupo_id != '' else None
            
            # Procesar archivo
            resultado = importar_desde_excel(archivo, grupo_id)
            
            if resultado['success']:
                res = resultado['resultados']
                mensaje = f'Importación completada: {res["exitosos"]} exitosos, {res["errores"]} errores, {res["duplicados"]} duplicados'
                if res.get('limite_alcanzado'):
                    mensaje += ' (Límite de 5000 contactos alcanzado)'
                flash(mensaje, 'success')
                
                # Mostrar detalles en logs
                for detalle in res['detalles'][:10]:  # Mostrar solo los primeros 10
                    logger.info(detalle)
            else:
                flash(f'Error: {resultado["message"]}', 'error')
        else:
            flash('Formato de archivo no válido. Use .xlsx o .xls', 'error')
            
    except Exception as e:
        logger.error(f"Error en importación: {e}")
        flash(f'Error procesando archivo: {str(e)}', 'error')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    print("=" * 50)
    print("🚀 CHAT MASIVO WHATSAPP - MODO DEMO")
    print("=" * 50)
    print("✅ El sistema funciona sin credenciales de Twilio")
    print("✅ Los mensajes se simulan en los logs")
    print("✅ Todas las funciones están disponibles")
    print("=" * 50)
    print("🌐 Accede a: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
