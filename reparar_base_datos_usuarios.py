#!/usr/bin/env python3
"""
Script para reparar la base de datos de usuarios
Soluciona el problema de "no hay usuario" al iniciar sesión
"""

import sqlite3
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def crear_directorios():
    """Crear directorios necesarios"""
    directorios = [
        'data',
        'data/database'
    ]
    
    for directorio in directorios:
        os.makedirs(directorio, exist_ok=True)
        logger.info(f"Directorio creado/verificado: {directorio}")

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
        return True
        
    except Exception as e:
        logger.error(f"Error inicializando base de datos de usuarios: {e}")
        return False

def crear_usuarios_por_defecto():
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
        
        # Verificar si ya existe un programador
        cursor.execute('SELECT COUNT(*) FROM users WHERE role = ?', ('programador',))
        programador_count = cursor.fetchone()[0]
        
        if programador_count == 0:
            # Crear usuario programador por defecto
            cursor.execute('''
                INSERT INTO users (name, lastname, dni, role, username, password)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                'Carlos',
                'Desarrollador',
                '87654321',
                'programador',
                'carlos',
                '123456'
            ))
            logger.info("Usuario programador por defecto creado: carlos/123456")
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Error creando usuarios por defecto: {e}")
        return False

def verificar_usuarios():
    """Verificar que los usuarios existen"""
    try:
        conn = sqlite3.connect('data/database/users.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
        
        cursor.execute('SELECT username, role FROM users')
        usuarios = cursor.fetchall()
        
        conn.close()
        
        logger.info(f"Total de usuarios en la base de datos: {total_users}")
        for username, role in usuarios:
            logger.info(f"  - {username} ({role})")
        
        return total_users > 0
        
    except Exception as e:
        logger.error(f"Error verificando usuarios: {e}")
        return False

def main():
    """Función principal de reparación"""
    print("=" * 60)
    print("🔧 REPARADOR DE BASE DE DATOS DE USUARIOS")
    print("=" * 60)
    print("Solucionando problema de 'no hay usuario'...")
    print()
    
    # Crear directorios
    crear_directorios()
    
    # Inicializar base de datos
    if not init_users_db():
        print("❌ Error inicializando base de datos")
        return False
    
    # Crear usuarios por defecto
    if not crear_usuarios_por_defecto():
        print("❌ Error creando usuarios por defecto")
        return False
    
    # Verificar usuarios
    if not verificar_usuarios():
        print("❌ No se encontraron usuarios en la base de datos")
        return False
    
    print()
    print("✅ ¡REPARACIÓN COMPLETADA!")
    print("=" * 60)
    print("Usuarios disponibles:")
    print("  👤 Administrador: admin / admin123")
    print("  👤 Asesor: jperez / 123456")
    print("  👤 Programador: carlos / 123456")
    print()
    print("Ahora puedes iniciar sesión en el sistema.")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Reparación cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
