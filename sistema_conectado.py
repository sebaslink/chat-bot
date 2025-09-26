#!/usr/bin/env python3
"""
Sistema Conectado - Versión que permite sincronización entre computadoras
Permite crear usuarios desde una computadora y acceder desde otras
"""

import os
import sys
import sqlite3
import requests
import json
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SistemaConectado:
    def __init__(self):
        self.servidor_central = "https://tu-app.onrender.com"  # URL de tu app en Render
        self.base_datos_local = "data/database/users.db"
        self.modo_conectado = True  # Cambiar a False para modo local
        
    def verificar_conexion_servidor(self):
        """Verificar si el servidor central está disponible"""
        try:
            response = requests.get(f"{self.servidor_central}/api/auth/check", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def sincronizar_usuarios_desde_servidor(self):
        """Sincronizar usuarios desde el servidor central"""
        try:
            if not self.verificar_conexion_servidor():
                logger.warning("Servidor central no disponible, usando modo local")
                return False
            
            # Obtener usuarios del servidor central
            response = requests.get(f"{self.servidor_central}/api/users/list")
            if response.status_code == 200:
                usuarios_servidor = response.json().get('users', [])
                
                # Sincronizar con base de datos local
                conn = sqlite3.connect(self.base_datos_local)
                cursor = conn.cursor()
                
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
                        logger.info(f"Usuario sincronizado: {usuario['username']}")
                
                conn.commit()
                conn.close()
                return True
                
        except Exception as e:
            logger.error(f"Error sincronizando usuarios: {e}")
            return False
    
    def crear_usuario_en_servidor(self, datos_usuario):
        """Crear usuario en el servidor central"""
        try:
            if not self.verificar_conexion_servidor():
                logger.warning("Servidor central no disponible, creando solo localmente")
                return self.crear_usuario_local(datos_usuario)
            
            # Crear usuario en servidor central
            response = requests.post(
                f"{self.servidor_central}/api/users/create",
                json=datos_usuario,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                logger.info(f"Usuario creado en servidor central: {datos_usuario['username']}")
                # También crear localmente
                self.crear_usuario_local(datos_usuario)
                return True
            else:
                logger.error(f"Error creando usuario en servidor: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error creando usuario en servidor: {e}")
            return False
    
    def crear_usuario_local(self, datos_usuario):
        """Crear usuario solo localmente"""
        try:
            conn = sqlite3.connect(self.base_datos_local)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO users (name, lastname, dni, role, username, password)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                datos_usuario['name'],
                datos_usuario['lastname'],
                datos_usuario['dni'],
                datos_usuario['role'],
                datos_usuario['username'],
                datos_usuario['password']
            ))
            
            conn.commit()
            conn.close()
            logger.info(f"Usuario creado localmente: {datos_usuario['username']}")
            return True
            
        except Exception as e:
            logger.error(f"Error creando usuario local: {e}")
            return False
    
    def inicializar_sistema(self):
        """Inicializar el sistema conectado"""
        print("=" * 60)
        print("🌐 SISTEMA CONECTADO - INICIALIZACIÓN")
        print("=" * 60)
        
        # Crear directorios
        os.makedirs('data/database', exist_ok=True)
        
        # Inicializar base de datos local
        self.init_database_local()
        
        # Sincronizar con servidor central si está disponible
        if self.modo_conectado:
            print("🔄 Sincronizando con servidor central...")
            if self.sincronizar_usuarios_desde_servidor():
                print("✅ Sincronización exitosa")
            else:
                print("⚠️  Modo local activado (servidor no disponible)")
                self.modo_conectado = False
        
        # Crear usuarios por defecto si no hay usuarios
        if self.contar_usuarios() == 0:
            print("👤 Creando usuarios por defecto...")
            self.crear_usuarios_por_defecto()
        
        print("✅ Sistema inicializado correctamente")
        return True
    
    def init_database_local(self):
        """Inicializar base de datos local"""
        try:
            conn = sqlite3.connect(self.base_datos_local)
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
            
        except Exception as e:
            logger.error(f"Error inicializando base de datos local: {e}")
    
    def contar_usuarios(self):
        """Contar usuarios en la base de datos local"""
        try:
            conn = sqlite3.connect(self.base_datos_local)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM users')
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def crear_usuarios_por_defecto(self):
        """Crear usuarios por defecto"""
        usuarios_default = [
            {
                'name': 'Administrador',
                'lastname': 'Sistema',
                'dni': '00000000',
                'role': 'administrativo',
                'username': 'admin',
                'password': 'admin123'
            },
            {
                'name': 'Juan',
                'lastname': 'Pérez',
                'dni': '12345678',
                'role': 'asesor',
                'username': 'jperez',
                'password': '123456'
            }
        ]
        
        for usuario in usuarios_default:
            if self.modo_conectado:
                self.crear_usuario_en_servidor(usuario)
            else:
                self.crear_usuario_local(usuario)
    
    def crear_nuevo_usuario(self):
        """Interfaz para crear nuevo usuario"""
        print("\n" + "=" * 40)
        print("👤 CREAR NUEVO USUARIO")
        print("=" * 40)
        
        try:
            name = input("Nombre: ").strip()
            lastname = input("Apellido: ").strip()
            dni = input("DNI (8 dígitos): ").strip()
            role = input("Rol (administrativo/asesor/programador): ").strip()
            username = input("Usuario: ").strip()
            password = input("Contraseña: ").strip()
            
            # Validaciones
            if not all([name, lastname, dni, role, username, password]):
                print("❌ Todos los campos son requeridos")
                return False
            
            if not dni.isdigit() or len(dni) != 8:
                print("❌ DNI debe tener 8 dígitos")
                return False
            
            if role not in ['administrativo', 'asesor', 'programador']:
                print("❌ Rol inválido")
                return False
            
            datos_usuario = {
                'name': name,
                'lastname': lastname,
                'dni': dni,
                'role': role,
                'username': username,
                'password': password
            }
            
            if self.modo_conectado:
                if self.crear_usuario_en_servidor(datos_usuario):
                    print("✅ Usuario creado y sincronizado")
                    return True
                else:
                    print("❌ Error creando usuario")
                    return False
            else:
                if self.crear_usuario_local(datos_usuario):
                    print("✅ Usuario creado localmente")
                    return True
                else:
                    print("❌ Error creando usuario")
                    return False
                    
        except KeyboardInterrupt:
            print("\n❌ Operación cancelada")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def listar_usuarios(self):
        """Listar usuarios disponibles"""
        try:
            conn = sqlite3.connect(self.base_datos_local)
            cursor = conn.cursor()
            
            cursor.execute('SELECT username, name, lastname, role FROM users ORDER BY created_at DESC')
            usuarios = cursor.fetchall()
            
            conn.close()
            
            print("\n" + "=" * 60)
            print("👥 USUARIOS DISPONIBLES")
            print("=" * 60)
            
            if usuarios:
                for username, name, lastname, role in usuarios:
                    print(f"👤 {username} - {name} {lastname} ({role})")
            else:
                print("❌ No hay usuarios disponibles")
            
            print("=" * 60)
            
        except Exception as e:
            print(f"❌ Error listando usuarios: {e}")

def main():
    """Función principal"""
    sistema = SistemaConectado()
    
    # Inicializar sistema
    if not sistema.inicializar_sistema():
        print("❌ Error inicializando sistema")
        return
    
    while True:
        print("\n" + "=" * 40)
        print("🌐 SISTEMA CONECTADO")
        print("=" * 40)
        print("1. Listar usuarios")
        print("2. Crear nuevo usuario")
        print("3. Sincronizar con servidor")
        print("4. Salir")
        print("=" * 40)
        
        try:
            opcion = input("Selecciona una opción: ").strip()
            
            if opcion == '1':
                sistema.listar_usuarios()
            elif opcion == '2':
                sistema.crear_nuevo_usuario()
            elif opcion == '3':
                print("🔄 Sincronizando...")
                if sistema.sincronizar_usuarios_desde_servidor():
                    print("✅ Sincronización exitosa")
                else:
                    print("❌ Error en sincronización")
            elif opcion == '4':
                print("👋 ¡Hasta luego!")
                break
            else:
                print("❌ Opción inválida")
                
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
