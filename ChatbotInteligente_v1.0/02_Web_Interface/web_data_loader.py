#!/usr/bin/env python3
"""
Interfaz web para cargar datos en el chatbot
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
import json
from werkzeug.utils import secure_filename
import sys
import os
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '01_Core_Chatbot'))
from data_loader import DataLoader
from ultra_simple_chatbot import UltraSimpleChatbot
import tempfile
import shutil

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Cambia esto en producción

# Configuración de archivos
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB máximo

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Crear directorio de uploads si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_valid_pdf(filepath):
    """Verifica que el archivo es realmente un PDF válido"""
    try:
        import PyPDF2
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            # Intentar leer la primera página para verificar que es un PDF válido
            if len(pdf_reader.pages) > 0:
                pdf_reader.pages[0].extract_text()
                return True
            return False
    except Exception:
        return False

@app.route('/')
def index():
    """Página principal"""
    loader = DataLoader()
    stats = loader.get_stats()
    return render_template('index.html', stats=stats)

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    """Carga un archivo PDF"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No se seleccionó ningún archivo'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No se seleccionó ningún archivo'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            file.save(filepath)
            
            # Verificar que el archivo es realmente un PDF
            if not is_valid_pdf(filepath):
                os.remove(filepath)
                return jsonify({
                    'success': False, 
                    'message': f'El archivo {filename} no es un PDF válido. Verifica que sea un archivo PDF real.'
                })
            
            # Cargar el PDF usando DataLoader
            loader = DataLoader()
            success = loader.load_pdf(filepath)
            
            # Limpiar archivo temporal
            os.remove(filepath)
            
            if success:
                return jsonify({'success': True, 'message': f'PDF {filename} cargado exitosamente'})
            else:
                return jsonify({'success': False, 'message': f'Error al procesar el PDF {filename}. El archivo puede estar corrupto o protegido.'})
                
        except Exception as e:
            # Limpiar archivo en caso de error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({
                'success': False, 
                'message': f'Error procesando {filename}: {str(e)}'
            })
    
    return jsonify({'success': False, 'message': 'Tipo de archivo no permitido. Solo se permiten archivos PDF.'})

@app.route('/upload_multiple_pdfs', methods=['POST'])
def upload_multiple_pdfs():
    """Carga múltiples archivos PDF"""
    files = request.files.getlist('files')
    if not files or files[0].filename == '':
        return jsonify({'success': False, 'message': 'No se seleccionaron archivos'})
    
    loader = DataLoader()
    success_count = 0
    error_files = []
    invalid_files = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            try:
                file.save(filepath)
                
                # Verificar que el archivo es realmente un PDF
                if not is_valid_pdf(filepath):
                    invalid_files.append(filename)
                    os.remove(filepath)
                    continue
                
                if loader.load_pdf(filepath):
                    success_count += 1
                else:
                    error_files.append(filename)
                
                # Limpiar archivo temporal
                os.remove(filepath)
                
            except Exception as e:
                error_files.append(f"{filename} (Error: {str(e)})")
                if os.path.exists(filepath):
                    os.remove(filepath)
    
    # Construir mensaje de respuesta
    if success_count > 0:
        message = f'Se cargaron {success_count} PDFs exitosamente'
        if error_files:
            message += f'. Errores en: {", ".join(error_files[:3])}'
            if len(error_files) > 3:
                message += f' y {len(error_files) - 3} más'
        if invalid_files:
            message += f'. Archivos no válidos: {", ".join(invalid_files[:3])}'
            if len(invalid_files) > 3:
                message += f' y {len(invalid_files) - 3} más'
        return jsonify({'success': True, 'message': message})
    else:
        if invalid_files:
            return jsonify({'success': False, 'message': f'Ningún archivo era un PDF válido. Archivos rechazados: {", ".join(invalid_files)}'})
        else:
            return jsonify({'success': False, 'message': 'No se pudo cargar ningún PDF. Verifica que los archivos no estén corruptos.'})

@app.route('/add_url', methods=['POST'])
def add_url():
    """Añade contenido de una URL"""
    data = request.get_json()
    url = data.get('url', '').strip()
    title = data.get('title', '').strip()
    
    if not url:
        return jsonify({'success': False, 'message': 'URL es requerida'})
    
    loader = DataLoader()
    success = loader.load_url(url)
    
    if success:
        return jsonify({'success': True, 'message': f'URL cargada exitosamente'})
    else:
        return jsonify({'success': False, 'message': 'Error al cargar la URL'})

@app.route('/add_text', methods=['POST'])
def add_text():
    """Añade texto manual"""
    data = request.get_json()
    content = data.get('content', '').strip()
    title = data.get('title', '').strip()
    source = data.get('source', 'manual').strip()
    
    if not content:
        return jsonify({'success': False, 'message': 'El contenido es requerido'})
    
    loader = DataLoader()
    success = loader.add_text_document(content, source, title)
    
    if success:
        return jsonify({'success': True, 'message': 'Texto añadido exitosamente'})
    else:
        return jsonify({'success': False, 'message': 'Error al añadir el texto'})

@app.route('/get_stats')
def get_stats():
    """Obtiene estadísticas actualizadas"""
    loader = DataLoader()
    stats = loader.get_stats()
    return jsonify(stats)

@app.route('/clear_data', methods=['POST'])
def clear_data():
    """Limpia todos los datos"""
    loader = DataLoader()
    loader.clear_data()
    return jsonify({'success': True, 'message': 'Base de datos limpiada exitosamente'})

@app.route('/chat', methods=['POST'])
def chat():
    """Maneja las conversaciones del chat"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'success': False, 'message': 'Mensaje vacío'})
        
        # Crear instancia del chatbot
        chatbot = UltraSimpleChatbot()
        
        # Generar respuesta
        response = chatbot.generate_response(message)
        
        return jsonify({
            'success': True, 
            'response': response
        })
        
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': f'Error procesando mensaje: {str(e)}'
        })

@app.route('/load_directory', methods=['POST'])
def load_directory():
    """Carga PDFs de un directorio"""
    data = request.get_json()
    directory_path = data.get('directory_path', '').strip()
    
    if not directory_path or not os.path.exists(directory_path):
        return jsonify({'success': False, 'message': 'Directorio no válido o no existe'})
    
    loader = DataLoader()
    count = loader.load_pdfs_from_directory(directory_path)
    
    if count > 0:
        return jsonify({'success': True, 'message': f'Se cargaron {count} PDFs del directorio'})
    else:
        return jsonify({'success': False, 'message': 'No se encontraron PDFs válidos en el directorio'})

@app.route('/upload_image', methods=['POST'])
def upload_image():
    """Carga una imagen y extrae texto usando OCR"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'No se seleccionó ninguna imagen'})
        
        file = request.files['file']
        title = request.form.get('title', '')
        
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No se seleccionó ninguna imagen'})
        
        if not title:
            title = file.filename
        
        # Verificar que es una imagen
        if not file.content_type.startswith('image/'):
            return jsonify({'success': False, 'message': 'El archivo debe ser una imagen'})
        
        # Guardar archivo temporalmente
        filename = secure_filename(file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(temp_path)
        
        try:
            # Procesar imagen con OCR
            loader = DataLoader()
            success = loader.load_image(temp_path, title)
            
            if success:
                return jsonify({
                    'success': True, 
                    'message': f'Imagen procesada exitosamente: {title}'
                })
            else:
                return jsonify({
                    'success': False, 
                    'message': 'No se pudo extraer texto de la imagen'
                })
        
        finally:
            # Limpiar archivo temporal
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': f'Error procesando imagen: {str(e)}'
        })

@app.route('/upload_multiple_images', methods=['POST'])
def upload_multiple_images():
    """Carga múltiples imágenes y extrae texto usando OCR"""
    try:
        files = request.files.getlist('files')
        if not files or files[0].filename == '':
            return jsonify({'success': False, 'message': 'No se seleccionaron imágenes'})
        
        # Verificar que todos son imágenes
        for file in files:
            if not file.content_type.startswith('image/'):
                return jsonify({'success': False, 'message': 'Todos los archivos deben ser imágenes'})
        
        temp_paths = []
        try:
            # Guardar archivos temporalmente
            for file in files:
                filename = secure_filename(file.filename)
                temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(temp_path)
                temp_paths.append(temp_path)
            
            # Procesar imágenes con OCR
            loader = DataLoader()
            success_count = loader.load_multiple_images(temp_paths)
            
            if success_count > 0:
                return jsonify({
                    'success': True, 
                    'message': f'Procesadas {success_count}/{len(files)} imágenes exitosamente'
                })
            else:
                return jsonify({
                    'success': False, 
                    'message': 'No se pudo extraer texto de ninguna imagen'
                })
        
        finally:
            # Limpiar archivos temporales
            for temp_path in temp_paths:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
    
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': f'Error procesando imágenes: {str(e)}'
        })

@app.route('/upload_document', methods=['POST'])
def upload_document():
    """Carga un documento y extrae texto según su tipo"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'No se seleccionó ningún documento'})
        
        file = request.files['file']
        title = request.form.get('title', '')
        
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No se seleccionó ningún documento'})
        
        if not title:
            title = file.filename
        
        # Guardar archivo temporalmente
        filename = secure_filename(file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(temp_path)
        
        try:
            # Procesar documento según su tipo
            loader = DataLoader()
            success = loader.load_document_by_type(temp_path, title)
            
            if success:
                return jsonify({
                    'success': True, 
                    'message': f'Documento procesado exitosamente: {title}'
                })
            else:
                return jsonify({
                    'success': False, 
                    'message': 'No se pudo procesar el documento'
                })
        
        finally:
            # Limpiar archivo temporal
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': f'Error procesando documento: {str(e)}'
        })

@app.route('/upload_multiple_documents', methods=['POST'])
def upload_multiple_documents():
    """Carga múltiples documentos y extrae texto según su tipo"""
    try:
        files = request.files.getlist('files')
        if not files or files[0].filename == '':
            return jsonify({'success': False, 'message': 'No se seleccionaron documentos'})
        
        temp_paths = []
        try:
            # Guardar archivos temporalmente
            for file in files:
                filename = secure_filename(file.filename)
                temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(temp_path)
                temp_paths.append(temp_path)
            
            # Procesar documentos según su tipo
            loader = DataLoader()
            success_count = 0
            
            for temp_path in temp_paths:
                if loader.load_document_by_type(temp_path):
                    success_count += 1
            
            if success_count > 0:
                return jsonify({
                    'success': True, 
                    'message': f'Procesados {success_count}/{len(files)} documentos exitosamente'
                })
            else:
                return jsonify({
                    'success': False, 
                    'message': 'No se pudo procesar ningún documento'
                })
        
        finally:
            # Limpiar archivos temporales
            for temp_path in temp_paths:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
    
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': f'Error procesando documentos: {str(e)}'
        })

# Rutas API para integración con Chat Masivo
@app.route('/api/masivo_stats')
def masivo_stats():
    """Obtiene estadísticas del chat masivo"""
    try:
        # Intentar conectar con el chat masivo
        import requests
        response = requests.get('http://localhost:5001/api/estadisticas', timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return jsonify({
                'success': True,
                'contactos': data.get('total_contactos', 0),
                'mensajes_hoy': data.get('mensajes_hoy', 0),
                'grupos': 6,  # Grupos por defecto
                'estado': 'Conectado'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Chat Masivo no disponible'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error conectando con Chat Masivo: {str(e)}',
            'contactos': 0,
            'mensajes_hoy': 0,
            'grupos': 0,
            'estado': 'Desconectado'
        })

@app.route('/api/masivo_test')
def masivo_test():
    """Prueba la conexión con el chat masivo"""
    try:
        import requests
        response = requests.get('http://localhost:5001/api/estadisticas', timeout=5)
        
        if response.status_code == 200:
            return jsonify({
                'success': True,
                'message': 'Conexión exitosa con Chat Masivo'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Chat Masivo no responde correctamente'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error de conexión: {str(e)}'
        })

@app.route('/api/sync_resources', methods=['POST'])
def sync_resources():
    """Sincroniza recursos entre chatbot y chat masivo"""
    try:
        # Obtener estadísticas actuales
        loader = DataLoader()
        stats = loader.get_stats()
        
        # Crear archivo de sincronización
        sync_data = {
            'timestamp': str(datetime.now()),
            'total_documents': stats.get('total_documents', 0),
            'sources': stats.get('sources', {}),
            'data_file': stats.get('data_file', 'knowledge_base.json')
        }
        
        # Guardar archivo de sincronización
        sync_file = os.path.join(os.path.dirname(__file__), '..', 'CHATMASIVO', 'data', 'sync_status.json')
        os.makedirs(os.path.dirname(sync_file), exist_ok=True)
        
        with open(sync_file, 'w', encoding='utf-8') as f:
            json.dump(sync_data, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            'success': True,
            'message': f'Recursos sincronizados: {stats.get("total_documents", 0)} documentos disponibles'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error sincronizando recursos: {str(e)}'
        })

if __name__ == '__main__':
    print("🌐 Iniciando interfaz web para cargar datos...")
    print("📱 Abre tu navegador en: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
