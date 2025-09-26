#!/usr/bin/env python3
"""
Configurador de Computadora Cliente
Configura una computadora para conectarse al servidor central
"""

import os
import requests
import json
import sqlite3
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def configurar_computadora_cliente():
    """Configurar computadora como cliente del servidor central"""
    print("=" * 60)
    print("💻 CONFIGURADOR DE COMPUTADORA CLIENTE")
    print("=" * 60)
    print("Este script configurará tu computadora para conectarse")
    print("al servidor central y sincronizar usuarios.")
    print()
    
    # Obtener URL del servidor central
    url_servidor = input("Ingresa la URL del servidor central (ej: https://tu-app.onrender.com): ").strip()
    
    if not url_servidor:
        print("❌ URL del servidor es requerida")
        return False
    
    # Verificar conexión al servidor
    if not verificar_conexion_servidor(url_servidor):
        print("❌ No se puede conectar al servidor central")
        return False
    
    # Crear directorios
    os.makedirs('data/database', exist_ok=True)
    
    # Inicializar base de datos local
    if not init_database_local():
        print("❌ Error inicializando base de datos local")
        return False
    
    # Sincronizar usuarios desde servidor
    if not sincronizar_usuarios_desde_servidor(url_servidor):
        print("❌ Error sincronizando usuarios")
        return False
    
    # Crear archivo de configuración
    if not crear_configuracion_cliente(url_servidor):
        print("❌ Error creando configuración")
        return False
    
    print("✅ Computadora cliente configurada correctamente")
    print()
    print("📋 INSTRUCCIONES:")
    print("1. Ejecuta: python sistema_conectado.py")
    print("2. Los usuarios se sincronizarán automáticamente")
    print("3. Puedes crear usuarios que se sincronizarán con el servidor")
    print()
    print("🔗 Servidor central: " + url_servidor)
    print("=" * 60)
    
    return True

def verificar_conexion_servidor(url_servidor):
    """Verificar conexión al servidor central"""
    try:
        print("🔄 Verificando conexión al servidor...")
        response = requests.get(f"{url_servidor}/api/auth/check", timeout=10)
        
        if response.status_code == 200:
            print("✅ Conexión exitosa al servidor central")
            return True
        else:
            print(f"❌ Error del servidor: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def init_database_local():
    """Inicializar base de datos local"""
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
        logger.info("Base de datos local inicializada")
        return True
        
    except Exception as e:
        logger.error(f"Error inicializando base de datos local: {e}")
        return False

def sincronizar_usuarios_desde_servidor(url_servidor):
    """Sincronizar usuarios desde el servidor central"""
    try:
        print("🔄 Sincronizando usuarios desde servidor...")
        
        # Obtener usuarios del servidor
        response = requests.get(f"{url_servidor}/api/users/list")
        if response.status_code != 200:
            print("❌ Error obteniendo usuarios del servidor")
            return False
        
        usuarios_servidor = response.json().get('users', [])
        
        if not usuarios_servidor:
            print("⚠️  No hay usuarios en el servidor central")
            return True
        
        # Sincronizar con base de datos local
        conn = sqlite3.connect('data/database/users.db')
        cursor = conn.cursor()
        
        usuarios_sincronizados = 0
        for usuario in usuarios_servidor:
            # Verificar si el usuario ya existe localmente
            cursor.execute('SELECT id FROM users WHERE username = ?', (usuario['username'],))
            if not cursor.fetchone():
                # Insertar usuario desde servidor
                cursor.execute('''
                    INSERT INTO users (name, lastname, dni, role, username, password, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    usuario['name'],
                    usuario['lastname'],
                    usuario['dni'],
                    usuario['role'],
                    usuario['username'],
                    usuario['password'],
                    usuario['created_at']
                ))
                usuarios_sincronizados += 1
                logger.info(f"Usuario sincronizado: {usuario['username']}")
        
        conn.commit()
        conn.close()
        
        print(f"✅ {usuarios_sincronizados} usuarios sincronizados")
        return True
        
    except Exception as e:
        logger.error(f"Error sincronizando usuarios: {e}")
        return False

def crear_configuracion_cliente(url_servidor):
    """Crear archivo de configuración del cliente"""
    try:
        config = {
            "cliente": {
                "servidor_central": url_servidor,
                "modo": "cliente",
                "descripcion": "Computadora cliente conectada al servidor central"
            },
            "sincronizacion": {
                "automatica": True,
                "intervalo_minutos": 5
            }
        }
        
        with open('config_cliente.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        logger.info("Configuración del cliente creada")
        return True
        
    except Exception as e:
        logger.error(f"Error creando configuración: {e}")
        return False

def main():
    """Función principal"""
    try:
        configurar_computadora_cliente()
    except KeyboardInterrupt:
        print("\n❌ Configuración cancelada")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
