#!/usr/bin/env python3
"""
Configurador del Servidor Central
Configura el sistema para que funcione como servidor central
"""

import os
import sqlite3
import json
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def configurar_servidor_central():
    """Configurar el sistema como servidor central"""
    print("=" * 60)
    print("🌐 CONFIGURADOR DE SERVIDOR CENTRAL")
    print("=" * 60)
    print("Este script configurará tu sistema como servidor central")
    print("para que otras computadoras puedan conectarse y sincronizar usuarios.")
    print()
    
    # Crear directorios
    os.makedirs('data/database', exist_ok=True)
    
    # Inicializar base de datos
    if not init_database_central():
        print("❌ Error inicializando base de datos")
        return False
    
    # Crear usuarios por defecto
    if not crear_usuarios_por_defecto():
        print("❌ Error creando usuarios por defecto")
        return False
    
    # Crear archivo de configuración
    if not crear_configuracion():
        print("❌ Error creando configuración")
        return False
    
    print("✅ Servidor central configurado correctamente")
    print()
    print("📋 INSTRUCCIONES:")
    print("1. Despliega este sistema en Render")
    print("2. Obtén la URL de tu aplicación")
    print("3. Actualiza la URL en sistema_conectado.py")
    print("4. Distribuye sistema_conectado.py a otras computadoras")
    print()
    print("🔗 URL de ejemplo: https://tu-app.onrender.com")
    print("=" * 60)
    
    return True

def init_database_central():
    """Inicializar base de datos del servidor central"""
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
        logger.info("Base de datos del servidor central inicializada")
        return True
        
    except Exception as e:
        logger.error(f"Error inicializando base de datos: {e}")
        return False

def crear_usuarios_por_defecto():
    """Crear usuarios por defecto en el servidor central"""
    try:
        conn = sqlite3.connect('data/database/users.db')
        cursor = conn.cursor()
        
        # Verificar si ya existen usuarios
        cursor.execute('SELECT COUNT(*) FROM users')
        count = cursor.fetchone()[0]
        
        if count > 0:
            print("✅ Usuarios ya existen en el servidor central")
            conn.close()
            return True
        
        # Crear usuarios por defecto
        usuarios_default = [
            ('Administrador', 'Sistema', '00000000', 'administrativo', 'admin', 'admin123'),
            ('Juan', 'Pérez', '12345678', 'asesor', 'jperez', '123456'),
            ('Carlos', 'Desarrollador', '87654321', 'programador', 'carlos', '123456')
        ]
        
        for usuario in usuarios_default:
            cursor.execute('''
                INSERT INTO users (name, lastname, dni, role, username, password)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', usuario)
            logger.info(f"Usuario creado: {usuario[4]}")
        
        conn.commit()
        conn.close()
        
        print("✅ Usuarios por defecto creados en el servidor central")
        return True
        
    except Exception as e:
        logger.error(f"Error creando usuarios por defecto: {e}")
        return False

def crear_configuracion():
    """Crear archivo de configuración del servidor central"""
    try:
        config = {
            "servidor_central": {
                "url": "https://tu-app.onrender.com",
                "modo": "central",
                "descripcion": "Servidor central para sincronización de usuarios"
            },
            "usuarios_por_defecto": {
                "admin": "admin123",
                "jperez": "123456",
                "carlos": "123456"
            },
            "roles_disponibles": [
                "administrativo",
                "asesor", 
                "programador"
            ]
        }
        
        with open('config_servidor_central.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        logger.info("Configuración del servidor central creada")
        return True
        
    except Exception as e:
        logger.error(f"Error creando configuración: {e}")
        return False

def main():
    """Función principal"""
    try:
        configurar_servidor_central()
    except KeyboardInterrupt:
        print("\n❌ Configuración cancelada")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
