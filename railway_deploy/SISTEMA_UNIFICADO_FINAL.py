#!/usr/bin/env python3
"""
Sistema Unificado Final - Chatbot y Chat Masivo Integrados
Ejecutable único que combina todas las funcionalidades
"""

import os
import sys
import subprocess
import time
import threading
import webbrowser
import json
import sqlite3
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file, session
from werkzeug.utils import secure_filename
import tempfile
import shutil

# Configurar logging sin emojis para evitar errores de codificación
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sistema_unificado.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuración de la aplicación Flask unificada
app = Flask(__name__)
app.secret_key = 'sistema_unificado_secret_key_2024'

# Configuración de archivos
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'pptx', 'xlsx', 'xls', 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB máximo

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Crear directorios necesarios
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('data/database', exist_ok=True)
os.makedirs('static/uploads', exist_ok=True)

# Crear usuarios por defecto
def create_default_users():
    """Crear usuarios por defecto si no existen"""
    try:
        conn = sqlite3.connect('data/database/users.db')
        cursor = conn.cursor()
        
        # Verificar si ya existe un administrador
        cursor.execute('SELECT COUNT(*) FROM users WHERE role = ?', ('administrativo',))
        admin_count = cursor.fetchone()[0]
        
        if admin_count == 0:
            # Crear usuario administrador por defecto
            cursor.execute('''
                INSERT INTO users (name, lastname, dni, role, username, password)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                'Administrador',
                'Sistema',
                '00000000',
                'administrativo',
                'admin',
                'admin123'
            ))
            logger.info("Usuario administrador por defecto creado: admin/admin123")
        
        # Verificar si ya existe un asesor
        cursor.execute('SELECT COUNT(*) FROM users WHERE role = ?', ('asesor',))
        asesor_count = cursor.fetchone()[0]
        
        if asesor_count == 0:
            # Crear usuario asesor por defecto
            cursor.execute('''
                INSERT INTO users (name, lastname, dni, role, username, password)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                'Juan',
                'Pérez',
                '12345678',
                'asesor',
                'jperez',
                '123456'
            ))
            logger.info("Usuario asesor por defecto creado: jperez/123456")
        
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Error creando usuarios por defecto: {e}")

# ==================== DECORADORES DE AUTENTICACIÓN ====================

def require_auth(f):
    """Decorador para requerir autenticación"""
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return jsonify({'success': False, 'message': 'Acceso no autorizado'}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def require_role(required_role):
    """Decorador para requerir rol específico"""
    def decorator(f):
        def decorated_function(*args, **kwargs):
            if not session.get('logged_in'):
                return jsonify({'success': False, 'message': 'Acceso no autorizado'}), 401
            if session.get('role') != required_role:
                return jsonify({'success': False, 'message': 'Permisos insuficientes'}), 403
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function
    return decorator

def allowed_file(filename):
    """Verificar si el archivo tiene una extensión permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Variables globales
chatbot_data = []
contactos_db = 'data/database/contactos.db'
knowledge_base = 'data/knowledge_base.json'

def init_databases():
    """Inicializar todas las bases de datos necesarias"""
    try:
        # Base de datos de contactos
        conn = sqlite3.connect(contactos_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contactos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT,
                telefono TEXT NOT NULL UNIQUE,
                carrera TEXT,
                grupo TEXT,
                activo BOOLEAN DEFAULT 1,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS grupos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                descripcion TEXT,
                activo BOOLEAN DEFAULT 1,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insertar grupos por defecto
        grupos_default = [
            ('General', 'Grupo por defecto'),
            ('Ingeniería', 'Estudiantes de ingeniería'),
            ('Medicina', 'Estudiantes de medicina'),
            ('Derecho', 'Estudiantes de derecho'),
            ('Administración', 'Estudiantes de administración'),
            ('Psicología', 'Estudiantes de psicología')
        ]
        
        for nombre, descripcion in grupos_default:
            cursor.execute('SELECT COUNT(*) FROM grupos WHERE nombre = ?', (nombre,))
            if cursor.fetchone()[0] == 0:
                cursor.execute('INSERT INTO grupos (nombre, descripcion) VALUES (?, ?)', (nombre, descripcion))
        
        conn.commit()
        conn.close()
        
        # Inicializar base de datos de usuarios
        init_users_db()
        
        # Inicializar base de conocimientos
        if not os.path.exists(knowledge_base):
            with open(knowledge_base, 'w', encoding='utf-8') as f:
                json.dump({'documents': [], 'total_documents': 0}, f, ensure_ascii=False, indent=2)
        
        logger.info("Bases de datos inicializadas correctamente")
        return True
        
    except Exception as e:
        logger.error(f"Error inicializando bases de datos: {e}")
        return False

def load_knowledge_base():
    """Cargar base de conocimientos"""
    global chatbot_data
    try:
        if os.path.exists(knowledge_base):
            with open(knowledge_base, 'r', encoding='utf-8') as f:
                data = json.load(f)
                chatbot_data = data.get('documents', [])
                logger.info(f"Cargados {len(chatbot_data)} documentos de la base de conocimientos")
        else:
            chatbot_data = []
    except Exception as e:
        logger.error(f"Error cargando base de conocimientos: {e}")
        chatbot_data = []

def save_knowledge_base():
    """Guardar base de conocimientos"""
    try:
        data = {
            'documents': chatbot_data,
            'total_documents': len(chatbot_data),
            'last_updated': str(datetime.now())
        }
        with open(knowledge_base, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info("Base de conocimientos guardada")
    except Exception as e:
        logger.error(f"Error guardando base de conocimientos: {e}")

def search_documents(query, n_results=5):
    """Buscar documentos en la base de conocimientos"""
    if not chatbot_data:
        return []
    
    query_lower = query.lower()
    query_words = set(query_lower.split())
    scored_docs = []
    
    for doc in chatbot_data:
        content_lower = doc.get('content', '').lower()
        content_words = set(content_lower.split())
        
        # Calcular similitud
        score = 0
        
        # Coincidencia exacta de palabras
        common_words = query_words.intersection(content_words)
        if common_words:
            score += len(common_words) / len(query_words) * 0.5
        
        # Coincidencia de frases
        if len(query_lower) > 3 and query_lower in content_lower:
            score += 0.8
        
        # Bonus por título
        if doc.get('title'):
            title_lower = doc['title'].lower()
            if query_lower in title_lower:
                score += 0.5
        
        if score > 0:
            scored_docs.append((doc, score))
    
    # Ordenar por puntuación
    scored_docs.sort(key=lambda x: x[1], reverse=True)
    return [doc for doc, score in scored_docs[:n_results]]

def generate_chatbot_response(user_query):
    """Generar respuesta del chatbot"""
    try:
        # Buscar documentos relevantes
        similar_docs = search_documents(user_query, n_results=3)
        
        if not similar_docs:
            return "No encontré información específica sobre tu consulta. ¿Podrías ser más específico o cargar algunos documentos primero?"
        
        # Generar respuesta basada en los documentos encontrados
        response_parts = []
        
        for i, doc in enumerate(similar_docs[:2], 1):
            content = doc.get('content', '')
            title = doc.get('title', 'Documento')
            
            # Extraer información relevante
            sentences = [s.strip() for s in content.split('.') if s.strip()]
            relevant_sentences = []
            
            for sentence in sentences:
                if any(word in sentence.lower() for word in user_query.lower().split()):
                    relevant_sentences.append(sentence)
            
            if relevant_sentences:
                response_parts.append(f"**{title}:**\n" + '. '.join(relevant_sentences[:2]) + '.')
            else:
                response_parts.append(f"**{title}:**\n" + content[:200] + '...')
        
        if response_parts:
            return '\n\n'.join(response_parts)
        else:
            return "Encontré información relacionada pero no pude generar una respuesta específica. ¿Podrías reformular tu pregunta?"
            
    except Exception as e:
        logger.error(f"Error generando respuesta: {e}")
        return "Lo siento, hubo un error procesando tu consulta. Intenta de nuevo."

def get_contactos():
    """Obtener lista de contactos"""
    try:
        conn = sqlite3.connect(contactos_db)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.id, c.nombre, c.apellido, c.telefono, c.carrera, g.nombre as grupo_nombre
            FROM contactos c
            LEFT JOIN grupos g ON c.grupo = g.nombre
            WHERE c.activo = 1
        ''')
        contactos = cursor.fetchall()
        conn.close()
        return contactos
    except Exception as e:
        logger.error(f"Error obteniendo contactos: {e}")
        return []

def get_grupos():
    """Obtener lista de grupos"""
    try:
        conn = sqlite3.connect(contactos_db)
        cursor = conn.cursor()
        cursor.execute('SELECT id, nombre, descripcion FROM grupos WHERE activo = 1')
        grupos = cursor.fetchall()
        conn.close()
        return grupos
    except Exception as e:
        logger.error(f"Error obteniendo grupos: {e}")
        return []

def agregar_contacto(nombre, apellido, telefono, carrera, grupo):
    """Agregar nuevo contacto"""
    try:
        conn = sqlite3.connect(contactos_db)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO contactos (nombre, apellido, telefono, carrera, grupo)
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, apellido, telefono, carrera, grupo))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error agregando contacto: {e}")
        return False

def eliminar_contacto(contacto_id):
    """Eliminar contacto"""
    try:
        conn = sqlite3.connect(contactos_db)
        cursor = conn.cursor()
        cursor.execute('UPDATE contactos SET activo = 0 WHERE id = ?', (contacto_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error eliminando contacto: {e}")
        return False

# Rutas de la aplicación Flask
@app.route('/')
def index():
    """Página principal - redirige según autenticación y rol"""
    if not session.get('logged_in'):
        return redirect('/login')
    
    # Redirigir según el rol del usuario
    role = session.get('role')
    if role == 'asesor':
        # Asesor va directamente al Chat Masivo original
        return redirect('http://localhost:5001')
    elif role in ['administrativo', 'programador']:
        # Administrador y programador van al chatbot completo
        stats = {
            'total_documentos': len(chatbot_data)
        }
        return render_template('chatbot_principal.html', stats=stats)
    else:
        # Si no tiene rol válido, mostrar página principal del chatbot
        stats = {
            'total_documentos': len(chatbot_data)
        }
        return render_template('chatbot_principal.html', stats=stats)

@app.route('/chatbot')
def chatbot():
    """Página principal del chatbot para administradores y programadores"""
    if not session.get('logged_in'):
        return redirect('/login')
    
    role = session.get('role')
    if role not in ['administrativo', 'programador']:
        return redirect('/abrir_chatmasivo')
    
    stats = {
        'total_documentos': len(chatbot_data)
    }
    return render_template('chatbot_principal.html', stats=stats)

@app.route('/abrir_chatmasivo')
def abrir_chatmasivo():
    """Abrir el chat masivo - redirige al Chat Masivo original"""
    try:
        # Siempre devolver JSON para peticiones del botón
        return jsonify({
            'success': True, 
            'message': 'Redirigiendo al Chat Masivo...',
            'redirect_url': 'http://localhost:5001'
        })
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': f'Error abriendo Chat Masivo: {str(e)}'
        })

@app.route('/chatmasivo')
def chatmasivo():
    """Página del Chat Masivo"""
    try:
        # Verificar si existe la interfaz original del Chat Masivo
        chatmasivo_template = os.path.join('templates', 'chatmasivo_original.html')
        
        if os.path.exists(chatmasivo_template):
            # Preparar datos para la plantilla
            estadisticas = {
                'total_contactos': len(get_contactos()),
                'mensajes_hoy': 0,  # Por ahora en 0, se puede implementar después
                'mensajes_semana': 0,  # Por ahora en 0, se puede implementar después
                'errores_recientes': 0  # Por ahora en 0, se puede implementar después
            }
            
            numero_prueba = "123456789"  # Número de prueba por defecto
            
            # Renderizar la interfaz original del Chat Masivo con datos
            return render_template('chatmasivo_original.html', 
                                 estadisticas=estadisticas, 
                                 numero_prueba=numero_prueba)
        else:
            return "Interfaz del Chat Masivo no encontrada", 404
    except Exception as e:
        return f"Error cargando Chat Masivo: {str(e)}", 500

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint para chat del chatbot"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'success': False, 'message': 'Mensaje vacío'})
        
        response = generate_chatbot_response(message)
        return jsonify({'success': True, 'response': response})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/upload_document', methods=['POST'])
def upload_document():
    """Subir documento"""
    try:
        # Determinar si es JSON o FormData
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        doc_type = data.get('type', '')
        title = data.get('title', '')
        
        # Debug: imprimir datos recibidos
        print(f"DEBUG - Datos recibidos: {data}")
        print(f"DEBUG - Tipo de documento: '{doc_type}'")
        print(f"DEBUG - Request files: {list(request.files.keys())}")
        print(f"DEBUG - Request form: {dict(request.form)}")
        logger.info(f"Datos recibidos: {data}")
        logger.info(f"Tipo de documento: '{doc_type}'")
        logger.info(f"Request files: {list(request.files.keys())}")
        logger.info(f"Request form: {dict(request.form)}")
        
        if not title:
            return jsonify({'success': False, 'message': 'Título requerido'})
        
        content = ""
        doc_id = f"doc_{len(chatbot_data)}"
        
        print(f"DEBUG - Validando tipo: '{doc_type}'")
        print(f"DEBUG - Es 'file'? {doc_type == 'file'}")
        print(f"DEBUG - Está en lista? {doc_type in ['pdf', 'docx', 'txt', 'file']}")
        
        if doc_type == 'url':
            url = data.get('url', '')
            if not url:
                return jsonify({'success': False, 'message': 'URL requerida'})
            
            try:
                content = extract_url_content(url)
                if not content:
                    return jsonify({'success': False, 'message': 'No se pudo extraer contenido de la URL'})
            except Exception as e:
                return jsonify({'success': False, 'message': f'Error procesando URL: {str(e)}'})
                
        elif doc_type == 'text':
            content = data.get('text', '')
            if not content:
                return jsonify({'success': False, 'message': 'Contenido de texto requerido'})
                
        else:  # Cualquier otro tipo se trata como archivo
            print(f"DEBUG - Procesando archivo con tipo: '{doc_type}'")
            if 'file' not in request.files:
                print("DEBUG - No hay archivo en request.files")
                return jsonify({'success': False, 'message': 'No se seleccionó archivo'})
            
            file = request.files['file']
            if file.filename == '':
                return jsonify({'success': False, 'message': 'No se seleccionó archivo'})
            
            # Verificar que el archivo tenga una extensión permitida
            if not allowed_file(file.filename):
                return jsonify({'success': False, 'message': f'Tipo de archivo no permitido. Tipos permitidos: {", ".join(ALLOWED_EXTENSIONS)}'})
            
            # Guardar archivo temporalmente
            filename = secure_filename(file.filename)
            temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(temp_path)
            
            try:
                # Procesar archivo según su tipo
                if filename.lower().endswith('.pdf'):
                    content = extract_pdf_text(temp_path)
                elif filename.lower().endswith(('.docx', '.doc')):
                    content = extract_docx_text(temp_path)
                elif filename.lower().endswith(('.txt', '.md')):
                    with open(temp_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                elif filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')):
                    # Para imágenes, guardar la ruta del archivo y crear descripción
                    content = f"Imagen: {filename}\nTipo: {filename.split('.')[-1].upper()}\nRuta: {temp_path}\nDescripción: Imagen cargada por el usuario"
                    # Mover archivo a carpeta permanente
                    permanent_path = os.path.join('static/uploads', filename)
                    shutil.move(temp_path, permanent_path)
                    temp_path = permanent_path  # Actualizar ruta para no eliminar
                else:
                    # Para otros tipos de archivo, crear descripción básica
                    content = f"Archivo: {filename}\nTipo: {filename.split('.')[-1].upper()}\nRuta: {temp_path}\nDescripción: Archivo cargado por el usuario"
                
                if not content:
                    return jsonify({'success': False, 'message': 'No se pudo procesar el archivo'})
                    
            finally:
                # Limpiar archivo temporal solo si no se movió a carpeta permanente
                if os.path.exists(temp_path) and not temp_path.startswith('static/uploads'):
                    os.remove(temp_path)
        
        # Agregar a la base de conocimientos
        doc = {
            'id': doc_id,
            'title': title,
            'content': content,
            'source': doc_type,
            'filename': data.get('url', '') if doc_type == 'url' else data.get('filename', ''),
            'date_added': str(datetime.now())
        }
        chatbot_data.append(doc)
        save_knowledge_base()
        
        return jsonify({
            'success': True, 
            'message': f'Documento "{title}" cargado exitosamente',
            'document_id': doc_id
        })
                
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/documents', methods=['GET'])
def get_documents():
    """Obtener lista de documentos"""
    try:
        documents = []
        for doc in chatbot_data:
            documents.append({
                'id': doc['id'],
                'title': doc['title'],
                'source': doc['source'],
                'filename': doc.get('filename', ''),
                'date_added': doc.get('date_added', ''),
                'content_preview': doc['content'][:200] + '...' if len(doc['content']) > 200 else doc['content']
            })
        
        return jsonify({
            'success': True,
            'documents': documents
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/delete_document/<document_id>', methods=['DELETE'])
def delete_document(document_id):
    """Eliminar documento"""
    try:
        global chatbot_data
        
        # Buscar y eliminar documento
        original_length = len(chatbot_data)
        chatbot_data = [doc for doc in chatbot_data if doc['id'] != document_id]
        
        if len(chatbot_data) < original_length:
            save_knowledge_base()
            return jsonify({
                'success': True,
                'message': 'Documento eliminado exitosamente'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Documento no encontrado'
            })
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/estadisticas', methods=['GET'])
def get_estadisticas():
    """Obtener estadísticas del sistema"""
    try:
        total_docs = len(chatbot_data)
        
        # Calcular tamaño aproximado de la base de conocimientos
        total_chars = sum(len(doc.get('content', '')) for doc in chatbot_data)
        size_mb = round(total_chars / (1024 * 1024), 2)
        
        return jsonify({
            'success': True,
            'total_documentos': total_docs,
            'tamaño_base_conocimientos': f'{size_mb} MB',
            'tipos_documentos': {
                'pdf': len([d for d in chatbot_data if d.get('source') == 'pdf']),
                'docx': len([d for d in chatbot_data if d.get('source') == 'docx']),
                'txt': len([d for d in chatbot_data if d.get('source') == 'txt']),
                'url': len([d for d in chatbot_data if d.get('source') == 'url']),
                'text': len([d for d in chatbot_data if d.get('source') == 'text'])
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

# ================================================================================
# RUTAS DE BASE DE DATOS
# ================================================================================

@app.route('/api/database/stats', methods=['GET'])
@require_auth
def get_database_stats():
    """Obtener estadísticas de la base de datos"""
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('data/database/chatbot.db')
        cursor = conn.cursor()
        
        # Obtener información de las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        total_tables = len(tables)
        total_records = 0
        
        # Contar registros en cada tabla
        for table in tables:
            table_name = table[0]
            if table_name != 'sqlite_sequence':
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                total_records += count
        
        # Obtener tamaño de la base de datos
        import os
        db_path = 'data/database/chatbot.db'
        size_bytes = os.path.getsize(db_path) if os.path.exists(db_path) else 0
        size_mb = round(size_bytes / (1024 * 1024), 2)
        
        # Obtener última modificación
        last_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        conn.close()
        
        return jsonify({
            'success': True,
            'total_records': total_records,
            'total_tables': total_tables,
            'size_mb': size_mb,
            'last_update': last_update
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/database/tables', methods=['GET'])
@require_auth
def get_database_tables():
    """Obtener lista de tablas de la base de datos"""
    try:
        conn = sqlite3.connect('data/database/chatbot.db')
        cursor = conn.cursor()
        
        # Obtener tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        tables_info = []
        for table in tables:
            table_name = table[0]
            if table_name != 'sqlite_sequence':
                # Contar registros en la tabla
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                records = cursor.fetchone()[0]
                
                tables_info.append({
                    'name': table_name,
                    'records': records
                })
        
        conn.close()
        
        return jsonify({
            'success': True,
            'tables': tables_info
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/database/table/<table_name>', methods=['GET'])
@require_auth
def get_table_content(table_name):
    """Obtener contenido de una tabla específica"""
    try:
        conn = sqlite3.connect('data/database/chatbot.db')
        cursor = conn.cursor()
        
        # Verificar que la tabla existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if not cursor.fetchone():
            return jsonify({'success': False, 'message': 'Tabla no encontrada'})
        
        # Obtener datos de la tabla (limitado a 100 registros para rendimiento)
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 100")
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        
        # Convertir a diccionarios
        records = []
        for row in rows:
            record = {}
            for i, value in enumerate(row):
                record[columns[i]] = value
            records.append(record)
        
        conn.close()
        
        return jsonify({
            'success': True,
            'records': records,
            'columns': columns
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/database/search', methods=['GET'])
@require_auth
def search_database():
    """Buscar en toda la base de datos"""
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({'success': False, 'message': 'Query vacía'})
        
        conn = sqlite3.connect('data/database/chatbot.db')
        cursor = conn.cursor()
        
        # Obtener todas las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        all_results = []
        
        for table in tables:
            table_name = table[0]
            if table_name != 'sqlite_sequence':
                # Obtener columnas de la tabla
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [col[1] for col in cursor.fetchall()]
                
                # Buscar en todas las columnas de texto
                search_conditions = []
                for col in columns:
                    search_conditions.append(f"{col} LIKE ?")
                
                if search_conditions:
                    search_query = f"SELECT * FROM {table_name} WHERE {' OR '.join(search_conditions)} LIMIT 50"
                    search_params = [f'%{query}%'] * len(search_conditions)
                    
                    cursor.execute(search_query, search_params)
                    rows = cursor.fetchall()
                    
                    for row in rows:
                        record = {}
                        for i, value in enumerate(row):
                            record[columns[i]] = value
                        record['_table'] = table_name
                        all_results.append(record)
        
        conn.close()
        
        return jsonify({
            'success': True,
            'results': all_results[:100]  # Limitar a 100 resultados
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/database/export', methods=['GET'])
@require_auth
def export_database():
    """Exportar base de datos completa"""
    try:
        conn = sqlite3.connect('data/database/chatbot.db')
        cursor = conn.cursor()
        
        # Obtener todas las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        export_data = {}
        
        for table in tables:
            table_name = table[0]
            if table_name != 'sqlite_sequence':
                cursor.execute(f"SELECT * FROM {table_name}")
                columns = [description[0] for description in cursor.description]
                rows = cursor.fetchall()
                
                records = []
                for row in rows:
                    record = {}
                    for i, value in enumerate(row):
                        record[columns[i]] = value
                    records.append(record)
                
                export_data[table_name] = {
                    'columns': columns,
                    'records': records
                }
        
        conn.close()
        
        # Crear respuesta JSON
        import json
        response_data = json.dumps(export_data, indent=2, ensure_ascii=False)
        
        return app.response_class(
            response_data,
            mimetype='application/json',
            headers={'Content-Disposition': f'attachment; filename=database_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'}
        )
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/database/clear', methods=['POST'])
@require_auth
def clear_database():
    """Limpiar toda la base de datos"""
    try:
        conn = sqlite3.connect('data/database/chatbot.db')
        cursor = conn.cursor()
        
        # Obtener todas las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        # Limpiar cada tabla
        for table in tables:
            table_name = table[0]
            if table_name != 'sqlite_sequence':
                cursor.execute(f"DELETE FROM {table_name}")
        
        conn.commit()
        conn.close()
        
        # Limpiar también la base de conocimientos en memoria
        global chatbot_data
        chatbot_data.clear()
        
        return jsonify({
            'success': True,
            'message': 'Base de datos limpiada exitosamente'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

# ================================================================================
# RUTAS DE BASE DE DATOS DEL CHAT MASIVO
# ================================================================================

@app.route('/api/chatmasivo/database/stats', methods=['GET'])
@require_auth
def get_chatmasivo_database_stats():
    """Obtener estadísticas de la base de datos del Chat Masivo"""
    try:
        # Conectar a la base de datos del Chat Masivo
        chatmasivo_db = 'CHATMASIVO/data/database/numeros_whatsapp.db'
        
        if not os.path.exists(chatmasivo_db):
            return jsonify({'success': False, 'message': 'Base de datos del Chat Masivo no encontrada'})
        
        conn = sqlite3.connect(chatmasivo_db)
        cursor = conn.cursor()
        
        # Obtener información de las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        total_tables = len(tables)
        total_records = 0
        
        # Contar registros en cada tabla
        for table in tables:
            table_name = table[0]
            if table_name != 'sqlite_sequence':
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                total_records += count
        
        # Obtener tamaño de la base de datos
        size_bytes = os.path.getsize(chatmasivo_db) if os.path.exists(chatmasivo_db) else 0
        size_mb = round(size_bytes / (1024 * 1024), 2)
        
        # Obtener última modificación
        last_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        conn.close()
        
        return jsonify({
            'success': True,
            'total_records': total_records,
            'total_tables': total_tables,
            'size_mb': size_mb,
            'last_update': last_update
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/chatmasivo/database/tables', methods=['GET'])
@require_auth
def get_chatmasivo_database_tables():
    """Obtener lista de tablas de la base de datos del Chat Masivo"""
    try:
        chatmasivo_db = 'CHATMASIVO/data/database/numeros_whatsapp.db'
        
        if not os.path.exists(chatmasivo_db):
            return jsonify({'success': False, 'message': 'Base de datos del Chat Masivo no encontrada'})
        
        conn = sqlite3.connect(chatmasivo_db)
        cursor = conn.cursor()
        
        # Obtener tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        tables_info = []
        for table in tables:
            table_name = table[0]
            if table_name != 'sqlite_sequence':
                # Contar registros en la tabla
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                records = cursor.fetchone()[0]
                
                tables_info.append({
                    'name': table_name,
                    'records': records
                })
        
        conn.close()
        
        return jsonify({
            'success': True,
            'tables': tables_info
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/chatmasivo/database/table/<table_name>', methods=['GET'])
def get_chatmasivo_table_content(table_name):
    """Obtener contenido de una tabla específica del Chat Masivo"""
    try:
        chatmasivo_db = 'CHATMASIVO/data/database/numeros_whatsapp.db'
        
        if not os.path.exists(chatmasivo_db):
            return jsonify({'success': False, 'message': 'Base de datos del Chat Masivo no encontrada'})
        
        conn = sqlite3.connect(chatmasivo_db)
        cursor = conn.cursor()
        
        # Verificar que la tabla existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if not cursor.fetchone():
            return jsonify({'success': False, 'message': 'Tabla no encontrada'})
        
        # Obtener datos de la tabla (limitado a 100 registros para rendimiento)
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 100")
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        
        # Convertir a diccionarios
        records = []
        for row in rows:
            record = {}
            for i, value in enumerate(row):
                record[columns[i]] = value
            records.append(record)
        
        conn.close()
        
        return jsonify({
            'success': True,
            'records': records,
            'columns': columns
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/chatmasivo/database/search', methods=['GET'])
def search_chatmasivo_database():
    """Buscar en toda la base de datos del Chat Masivo"""
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({'success': False, 'message': 'Query vacía'})
        
        chatmasivo_db = 'CHATMASIVO/data/database/numeros_whatsapp.db'
        
        if not os.path.exists(chatmasivo_db):
            return jsonify({'success': False, 'message': 'Base de datos del Chat Masivo no encontrada'})
        
        conn = sqlite3.connect(chatmasivo_db)
        cursor = conn.cursor()
        
        # Obtener todas las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        all_results = []
        
        for table in tables:
            table_name = table[0]
            if table_name != 'sqlite_sequence':
                # Obtener columnas de la tabla
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [col[1] for col in cursor.fetchall()]
                
                # Buscar en todas las columnas de texto
                search_conditions = []
                for col in columns:
                    search_conditions.append(f"{col} LIKE ?")
                
                if search_conditions:
                    search_query = f"SELECT * FROM {table_name} WHERE {' OR '.join(search_conditions)} LIMIT 50"
                    search_params = [f'%{query}%'] * len(search_conditions)
                    
                    cursor.execute(search_query, search_params)
                    rows = cursor.fetchall()
                    
                    for row in rows:
                        record = {}
                        for i, value in enumerate(row):
                            record[columns[i]] = value
                        record['_table'] = table_name
                        all_results.append(record)
        
        conn.close()
        
        return jsonify({
            'success': True,
            'results': all_results[:100]  # Limitar a 100 resultados
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/chatmasivo/database/export', methods=['GET'])
def export_chatmasivo_database():
    """Exportar base de datos completa del Chat Masivo"""
    try:
        chatmasivo_db = 'CHATMASIVO/data/database/numeros_whatsapp.db'
        
        if not os.path.exists(chatmasivo_db):
            return jsonify({'success': False, 'message': 'Base de datos del Chat Masivo no encontrada'})
        
        conn = sqlite3.connect(chatmasivo_db)
        cursor = conn.cursor()
        
        # Obtener todas las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        export_data = {}
        
        for table in tables:
            table_name = table[0]
            if table_name != 'sqlite_sequence':
                cursor.execute(f"SELECT * FROM {table_name}")
                columns = [description[0] for description in cursor.description]
                rows = cursor.fetchall()
                
                records = []
                for row in rows:
                    record = {}
                    for i, value in enumerate(row):
                        record[columns[i]] = value
                    records.append(record)
                
                export_data[table_name] = {
                    'columns': columns,
                    'records': records
                }
        
        conn.close()
        
        # Crear respuesta JSON
        response_data = json.dumps(export_data, indent=2, ensure_ascii=False)
        
        return app.response_class(
            response_data,
            mimetype='application/json',
            headers={'Content-Disposition': f'attachment; filename=chatmasivo_database_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'}
        )
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/chatmasivo/database/clear', methods=['POST'])
def clear_chatmasivo_database():
    """Limpiar toda la base de datos del Chat Masivo"""
    try:
        chatmasivo_db = 'CHATMASIVO/data/database/numeros_whatsapp.db'
        
        if not os.path.exists(chatmasivo_db):
            return jsonify({'success': False, 'message': 'Base de datos del Chat Masivo no encontrada'})
        
        conn = sqlite3.connect(chatmasivo_db)
        cursor = conn.cursor()
        
        # Obtener todas las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        # Limpiar cada tabla
        for table in tables:
            table_name = table[0]
            if table_name != 'sqlite_sequence':
                cursor.execute(f"DELETE FROM {table_name}")
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Base de datos del Chat Masivo limpiada exitosamente'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/chatmasivo/database/backup', methods=['POST'])
def backup_chatmasivo_database():
    """Crear backup de la base de datos del Chat Masivo"""
    try:
        chatmasivo_db = 'CHATMASIVO/data/database/numeros_whatsapp.db'
        
        if not os.path.exists(chatmasivo_db):
            return jsonify({'success': False, 'message': 'Base de datos del Chat Masivo no encontrada'})
        
        # Crear directorio de backups si no existe
        backup_dir = 'backups/chatmasivo'
        os.makedirs(backup_dir, exist_ok=True)
        
        # Crear nombre de archivo con timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_dir, f'chatmasivo_backup_{timestamp}.db')
        
        # Copiar archivo de base de datos
        shutil.copy2(chatmasivo_db, backup_file)
        
        return jsonify({
            'success': True,
            'message': f'Backup creado exitosamente: {backup_file}'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/database/backup', methods=['POST'])
@require_auth
def backup_database():
    """Crear backup de la base de datos del Chatbot"""
    try:
        chatbot_db = 'data/database/chatbot.db'
        
        if not os.path.exists(chatbot_db):
            return jsonify({'success': False, 'message': 'Base de datos del Chatbot no encontrada'})
        
        # Crear directorio de backups si no existe
        backup_dir = 'backups/chatbot'
        os.makedirs(backup_dir, exist_ok=True)
        
        # Crear nombre de archivo con timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_dir, f'chatbot_backup_{timestamp}.db')
        
        # Copiar archivo de base de datos
        shutil.copy2(chatbot_db, backup_file)
        
        return jsonify({
            'success': True,
            'message': f'Backup creado exitosamente: {backup_file}'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

# ==================== RUTAS API PARA GESTIÓN DE USUARIOS ====================

def init_users_db():
    """Inicializar base de datos de usuarios"""
    try:
        conn = sqlite3.connect('data/database/users.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                lastname TEXT NOT NULL,
                dni TEXT UNIQUE NOT NULL,
                role TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Base de datos de usuarios inicializada correctamente")
        
    except Exception as e:
        logger.error(f"Error inicializando base de datos de usuarios: {e}")

@app.route('/api/users/create', methods=['POST'])
@require_auth
def create_user():
    """Crear nuevo usuario"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['name', 'lastname', 'dni', 'role', 'username', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'Campo requerido: {field}'})
        
        # Validar DNI (8 dígitos)
        if not data['dni'].isdigit() or len(data['dni']) != 8:
            return jsonify({'success': False, 'message': 'El DNI debe contener exactamente 8 dígitos'})
        
        # Validar rol
        if data['role'] not in ['administrativo', 'programador', 'asesor']:
            return jsonify({'success': False, 'message': 'Rol inválido'})
        
        # Validar formato de username (UC + 5 dígitos)
        if not data['username'].startswith('UC') or len(data['username']) != 7:
            return jsonify({'success': False, 'message': 'Formato de usuario inválido'})
        
        conn = sqlite3.connect('data/database/users.db')
        cursor = conn.cursor()
        
        # Verificar si el DNI ya existe
        cursor.execute('SELECT id FROM users WHERE dni = ?', (data['dni'],))
        if cursor.fetchone():
            conn.close()
            return jsonify({'success': False, 'message': 'Ya existe un usuario con este DNI'})
        
        # Verificar si el username ya existe
        cursor.execute('SELECT id FROM users WHERE username = ?', (data['username'],))
        if cursor.fetchone():
            conn.close()
            return jsonify({'success': False, 'message': 'Ya existe un usuario con este nombre de usuario'})
        
        # Insertar nuevo usuario
        cursor.execute('''
            INSERT INTO users (name, lastname, dni, role, username, password)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['lastname'],
            data['dni'],
            data['role'],
            data['username'],
            data['password']
        ))
        
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        logger.info(f"Usuario creado: {data['name']} {data['lastname']} ({data['username']})")
        
        return jsonify({
            'success': True,
            'message': 'Usuario creado exitosamente',
            'user_id': user_id
        })
        
    except Exception as e:
        logger.error(f"Error creando usuario: {e}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/users/list', methods=['GET'])
@require_auth
def list_users():
    """Listar todos los usuarios"""
    try:
        conn = sqlite3.connect('data/database/users.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, lastname, dni, role, username, password, created_at
            FROM users
            ORDER BY created_at DESC
        ''')
        
        users = []
        for row in cursor.fetchall():
            users.append({
                'id': row[0],
                'name': row[1],
                'lastname': row[2],
                'dni': row[3],
                'role': row[4],
                'username': row[5],
                'password': row[6],
                'created_at': row[7]
            })
        
        conn.close()
        
        return jsonify({
            'success': True,
            'users': users
        })
        
    except Exception as e:
        logger.error(f"Error listando usuarios: {e}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/users/delete/<int:user_id>', methods=['DELETE'])
@require_auth
def delete_user(user_id):
    """Eliminar usuario"""
    try:
        conn = sqlite3.connect('data/database/users.db')
        cursor = conn.cursor()
        
        # Verificar si el usuario existe
        cursor.execute('SELECT name, lastname FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return jsonify({'success': False, 'message': 'Usuario no encontrado'})
        
        # Eliminar usuario
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        
        logger.info(f"Usuario eliminado: {user[0]} {user[1]} (ID: {user_id})")
        
        return jsonify({
            'success': True,
            'message': 'Usuario eliminado exitosamente'
        })
        
    except Exception as e:
        logger.error(f"Error eliminando usuario: {e}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

# ==================== RUTAS DE AUTENTICACIÓN ====================

@app.route('/login')
def login_page():
    """Página de inicio de sesión"""
    return render_template('login.html')

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Autenticar usuario"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Usuario y contraseña son requeridos'})
        
        conn = sqlite3.connect('data/database/users.db')
        cursor = conn.cursor()
        
        # Buscar usuario por username
        cursor.execute('''
            SELECT id, name, lastname, dni, role, username, password
            FROM users WHERE username = ?
        ''', (username,))
        
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return jsonify({'success': False, 'message': 'Usuario no encontrado'})
        
        # Verificar contraseña (en un sistema real, usar hash)
        if user[6] != password:
            return jsonify({'success': False, 'message': 'Contraseña incorrecta'})
        
        # Crear sesión
        session['user_id'] = user[0]
        session['username'] = user[5]
        session['name'] = user[1]
        session['lastname'] = user[2]
        session['role'] = user[4]
        session['logged_in'] = True
        
        logger.info(f"Usuario autenticado: {user[1]} {user[2]} ({user[5]}) - Rol: {user[4]}")
        
        return jsonify({
            'success': True,
            'message': 'Inicio de sesión exitoso',
            'user': {
                'id': user[0],
                'name': user[1],
                'lastname': user[2],
                'username': user[5],
                'role': user[4]
            },
            'role': user[4]
        })
        
    except Exception as e:
        logger.error(f"Error en autenticación: {e}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Cerrar sesión"""
    try:
        session.clear()
        return jsonify({'success': True, 'message': 'Sesión cerrada exitosamente'})
    except Exception as e:
        logger.error(f"Error cerrando sesión: {e}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/auth/check', methods=['GET'])
def check_auth():
    """Verificar estado de autenticación"""
    try:
        if session.get('logged_in'):
            return jsonify({
                'success': True,
                'authenticated': True,
                'user': {
                    'id': session.get('user_id'),
                    'username': session.get('username'),
                    'name': session.get('name'),
                    'lastname': session.get('lastname'),
                    'role': session.get('role')
                }
            })
        else:
            return jsonify({
                'success': True,
                'authenticated': False
            })
    except Exception as e:
        logger.error(f"Error verificando autenticación: {e}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

def require_auth(f):
    """Decorador para requerir autenticación"""
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return jsonify({'success': False, 'message': 'Acceso no autorizado'}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def require_role(required_role):
    """Decorador para requerir rol específico"""
    def decorator(f):
        def decorated_function(*args, **kwargs):
            if not session.get('logged_in'):
                return jsonify({'success': False, 'message': 'Acceso no autorizado'}), 401
            if session.get('role') != required_role:
                return jsonify({'success': False, 'message': 'Permisos insuficientes'}), 403
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorator
    return decorator

# ==================== RUTAS DE GESTIÓN DE USUARIOS EN BD ====================

@app.route('/api/database/users-table', methods=['GET'])
@require_auth
def get_users_table():
    """Obtener información de la tabla de usuarios para la base de datos"""
    try:
        conn = sqlite3.connect('data/database/users.db')
        cursor = conn.cursor()
        
        # Obtener información de la tabla
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            return jsonify({'success': False, 'message': 'Tabla de usuarios no encontrada'})
        
        # Obtener estructura de la tabla
        cursor.execute("PRAGMA table_info(users)")
        columns = [{'name': col[1], 'type': col[2], 'notnull': col[3], 'pk': col[5]} for col in cursor.fetchall()]
        
        # Obtener estadísticas
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        # Obtener usuarios por rol
        cursor.execute("SELECT role, COUNT(*) FROM users GROUP BY role")
        users_by_role = dict(cursor.fetchall())
        
        # Obtener usuarios recientes
        cursor.execute("SELECT name, lastname, role, created_at FROM users ORDER BY created_at DESC LIMIT 5")
        recent_users = [{'name': row[0], 'lastname': row[1], 'role': row[2], 'created_at': row[3]} for row in cursor.fetchall()]
        
        conn.close()
        
        return jsonify({
            'success': True,
            'table_info': {
                'name': 'users',
                'columns': columns,
                'total_records': total_users,
                'users_by_role': users_by_role,
                'recent_users': recent_users
            }
        })
        
    except Exception as e:
        logger.error(f"Error obteniendo información de tabla de usuarios: {e}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

# ==================== RUTAS DE PÁGINAS POR ROL ====================

@app.route('/admin')
def admin_page():
    """Página de administrador"""
    if not session.get('logged_in') or session.get('role') != 'administrativo':
        return redirect('/login')
    return render_template('admin.html')

@app.route('/programmer')
def programmer_page():
    """Página de programador"""
    if not session.get('logged_in') or session.get('role') != 'programador':
        return redirect('/login')
    return render_template('programmer.html')

@app.route('/advisor')
def advisor_page():
    """Página de asesor"""
    if not session.get('logged_in') or session.get('role') != 'asesor':
        return redirect('/login')
    return render_template('advisor.html')

def extract_pdf_text(filepath):
    """Extraer texto de PDF"""
    try:
        import PyPDF2
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        logger.error(f"Error extrayendo PDF: {e}")
        return ""

def extract_docx_text(filepath):
    """Extraer texto de DOCX"""
    try:
        from docx import Document
        doc = Document(filepath)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        logger.error(f"Error extrayendo DOCX: {e}")
        return ""

def extract_url_content(url):
    """Extraer contenido de una URL"""
    try:
        import requests
        from bs4 import BeautifulSoup
        
        # Headers para simular un navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Hacer petición a la URL
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parsear HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remover scripts y estilos
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Extraer texto
        text = soup.get_text()
        
        # Limpiar texto
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Limitar tamaño del contenido
        if len(text) > 50000:
            text = text[:50000] + "... [contenido truncado]"
        
        return text
        
    except Exception as e:
        logger.error(f"Error extrayendo URL {url}: {e}")
        return ""

def start_chatmasivo():
    """Iniciar el Chat Masivo original en puerto 5001"""
    try:
        chatmasivo_path = os.path.join(os.path.dirname(__file__), 'CHATMASIVO', 'main.py')
        if os.path.exists(chatmasivo_path):
            print("Iniciando Chat Masivo original...")
            subprocess.Popen([
                'C:\\Program Files\\Python313\\python.exe', 
                chatmasivo_path
            ], cwd=os.path.dirname(chatmasivo_path))
            print("Chat Masivo iniciado en: http://localhost:5001")
            return True
        else:
            print("ERROR: No se encontró el Chat Masivo original")
            return False
    except Exception as e:
        print(f"Error iniciando Chat Masivo: {e}")
        return False

def main():
    """Función principal del sistema unificado"""
    print("=" * 80)
    print("SISTEMA UNIFICADO FINAL - CHATBOT Y CHAT MASIVO")
    print("=" * 80)
    print("Iniciando sistema...")
    print()
    
    # Inicializar bases de datos
    if not init_databases():
        print("ERROR: No se pudieron inicializar las bases de datos")
        return
    
    # Crear usuarios por defecto después de inicializar las bases de datos
    create_default_users()
    
    # Cargar base de conocimientos
    load_knowledge_base()
    
    # Solo iniciar Chat Masivo en desarrollo local
    if os.getenv('RAILWAY_ENVIRONMENT') is None:
        start_chatmasivo()
    
    print("Sistema inicializado correctamente")
    
    # Solo abrir navegador en desarrollo local
    if os.getenv('RAILWAY_ENVIRONMENT') is None:
        print("Abriendo navegador...")
        print()
        
        # Abrir navegador después de un breve delay
        def open_browser():
            time.sleep(3)  # Esperar un poco más para que el Chat Masivo se inicie
            webbrowser.open('http://localhost:5000')
        
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        print("Sistema disponible en: http://localhost:5000")
        print("Chat Masivo disponible en: http://localhost:5001")
        print("Presiona Ctrl+C para detener el servidor")
        print()
    else:
        print("Sistema desplegado en la nube")
        print("Sistema disponible en: https://tu-app.railway.app")
        print()
    
    try:
        # Obtener puerto de la variable de entorno o usar 5000 por defecto
        port = int(os.getenv('PORT', 5000))
        # Ejecutar servidor Flask
        app.run(debug=False, host='0.0.0.0', port=port)
    except KeyboardInterrupt:
        print("\nSistema detenido!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
