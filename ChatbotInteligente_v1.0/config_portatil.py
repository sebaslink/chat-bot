#!/usr/bin/env python3
"""
Configuración Portátil para Chatbot Inteligente v1.0
Detecta automáticamente la configuración del sistema
"""

import os
import sys
import platform
import subprocess
import json
from pathlib import Path

class ConfiguracionPortatil:
    """Clase para manejar la configuración portátil del sistema"""
    
    def __init__(self):
        self.sistema_operativo = platform.system()
        self.arquitectura = platform.machine()
        self.python_version = sys.version_info
        self.python_path = sys.executable
        self.directorio_actual = os.path.dirname(os.path.abspath(__file__))
        self.config = {}
        
    def detectar_configuracion(self):
        """Detecta la configuración del sistema automáticamente"""
        print(f"[INFO] Detectando configuración del sistema...")
        print(f"[INFO] Sistema operativo: {self.sistema_operativo}")
        print(f"[INFO] Arquitectura: {self.arquitectura}")
        print(f"[INFO] Python: {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}")
        print(f"[INFO] Directorio: {self.directorio_actual}")
        
        # Configuración base
        self.config = {
            'sistema': {
                'os': self.sistema_operativo,
                'arquitectura': self.arquitectura,
                'python_version': f"{self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}",
                'python_path': self.python_path,
                'directorio_base': self.directorio_actual
            },
            'rutas': {
                'uploads': os.path.join(self.directorio_actual, 'uploads'),
                'static': os.path.join(self.directorio_actual, 'static'),
                'templates': os.path.join(self.directorio_actual, 'templates'),
                'data': os.path.join(self.directorio_actual, 'data'),
                'database': os.path.join(self.directorio_actual, 'data', 'database'),
                'logs': os.path.join(self.directorio_actual, 'logs'),
                'chatmasivo': os.path.join(self.directorio_actual, 'CHATMASIVO')
            },
            'servidor': {
                'host': '0.0.0.0',
                'puerto_principal': 5000,
                'puerto_chatmasivo': 5001,
                'debug': False
            },
            'base_datos': {
                'usuarios': os.path.join(self.directorio_actual, 'data', 'database', 'users.db'),
                'chatbot': os.path.join(self.directorio_actual, 'data', 'database', 'chatbot.db'),
                'contactos': os.path.join(self.directorio_actual, 'data', 'database', 'contactos.db'),
                'knowledge_base': os.path.join(self.directorio_actual, 'data', 'knowledge_base.json')
            }
        }
        
        return self.config
    
    def crear_directorios(self):
        """Crea los directorios necesarios si no existen"""
        print(f"[INFO] Creando directorios necesarios...")
        
        directorios = [
            self.config['rutas']['uploads'],
            self.config['rutas']['static'],
            self.config['rutas']['templates'],
            self.config['rutas']['data'],
            self.config['rutas']['database'],
            self.config['rutas']['logs'],
            os.path.join(self.config['rutas']['static'], 'uploads'),
            os.path.join(self.config['rutas']['chatmasivo'], 'static'),
            os.path.join(self.config['rutas']['chatmasivo'], 'static', 'uploads'),
            os.path.join(self.config['rutas']['chatmasivo'], 'templates'),
            os.path.join(self.config['rutas']['chatmasivo'], 'data'),
            os.path.join(self.config['rutas']['chatmasivo'], 'data', 'database')
        ]
        
        for directorio in directorios:
            try:
                os.makedirs(directorio, exist_ok=True)
                print(f"[OK] Directorio creado: {directorio}")
            except Exception as e:
                print(f"[ERROR] No se pudo crear directorio {directorio}: {e}")
    
    def verificar_dependencias(self):
        """Verifica que las dependencias estén instaladas"""
        print(f"[INFO] Verificando dependencias...")
        
        dependencias = [
            'flask',
            'werkzeug',
            'sqlite3',
            'json',
            'datetime',
            'threading',
            'subprocess',
            'webbrowser'
        ]
        
        dependencias_faltantes = []
        
        for dep in dependencias:
            try:
                if dep == 'sqlite3':
                    import sqlite3
                elif dep == 'json':
                    import json
                elif dep == 'datetime':
                    import datetime
                elif dep == 'threading':
                    import threading
                elif dep == 'subprocess':
                    import subprocess
                elif dep == 'webbrowser':
                    import webbrowser
                else:
                    __import__(dep)
                print(f"[OK] {dep} disponible")
            except ImportError:
                print(f"[ERROR] {dep} no disponible")
                dependencias_faltantes.append(dep)
        
        if dependencias_faltantes:
            print(f"[WARNING] Dependencias faltantes: {', '.join(dependencias_faltantes)}")
            return False
        else:
            print(f"[OK] Todas las dependencias están disponibles")
            return True
    
    def verificar_puertos(self):
        """Verifica que los puertos estén disponibles"""
        print(f"[INFO] Verificando puertos...")
        
        puertos = [5000, 5001]
        puertos_ocupados = []
        
        for puerto in puertos:
            try:
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex(('localhost', puerto))
                sock.close()
                
                if result == 0:
                    print(f"[WARNING] Puerto {puerto} está en uso")
                    puertos_ocupados.append(puerto)
                else:
                    print(f"[OK] Puerto {puerto} disponible")
            except Exception as e:
                print(f"[ERROR] Error verificando puerto {puerto}: {e}")
        
        return len(puertos_ocupados) == 0
    
    def crear_archivo_config(self):
        """Crea un archivo de configuración JSON"""
        config_file = os.path.join(self.directorio_actual, 'config_sistema.json')
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            print(f"[OK] Archivo de configuración creado: {config_file}")
            return True
        except Exception as e:
            print(f"[ERROR] No se pudo crear archivo de configuración: {e}")
            return False
    
    def cargar_config(self):
        """Carga la configuración desde archivo si existe"""
        config_file = os.path.join(self.directorio_actual, 'config_sistema.json')
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                print(f"[OK] Configuración cargada desde: {config_file}")
                return True
            except Exception as e:
                print(f"[ERROR] No se pudo cargar configuración: {e}")
                return False
        else:
            print(f"[INFO] No existe archivo de configuración, detectando automáticamente...")
            return False
    
    def obtener_ruta(self, tipo):
        """Obtiene una ruta específica de la configuración"""
        if tipo in self.config['rutas']:
            return self.config['rutas'][tipo]
        else:
            return None
    
    def obtener_puerto(self, tipo):
        """Obtiene un puerto específico de la configuración"""
        if tipo == 'principal':
            return self.config['servidor']['puerto_principal']
        elif tipo == 'chatmasivo':
            return self.config['servidor']['puerto_chatmasivo']
        else:
            return None
    
    def obtener_base_datos(self, tipo):
        """Obtiene la ruta de una base de datos específica"""
        if tipo in self.config['base_datos']:
            return self.config['base_datos'][tipo]
        else:
            return None

def inicializar_configuracion():
    """Función principal para inicializar la configuración portátil"""
    config = ConfiguracionPortatil()
    
    # Intentar cargar configuración existente
    if not config.cargar_config():
        # Si no existe, detectar y crear nueva configuración
        config.detectar_configuracion()
        config.crear_directorios()
        config.verificar_dependencias()
        config.verificar_puertos()
        config.crear_archivo_config()
    
    return config

if __name__ == "__main__":
    print("=" * 80)
    print("CONFIGURACIÓN PORTÁTIL - CHATBOT INTELIGENTE v1.0")
    print("=" * 80)
    
    config = inicializar_configuracion()
    
    print("\n" + "=" * 80)
    print("CONFIGURACIÓN DETECTADA:")
    print("=" * 80)
    print(f"Sistema operativo: {config.config['sistema']['os']}")
    print(f"Arquitectura: {config.config['sistema']['arquitectura']}")
    print(f"Python: {config.config['sistema']['python_version']}")
    print(f"Directorio base: {config.config['sistema']['directorio_base']}")
    print(f"Puerto principal: {config.config['servidor']['puerto_principal']}")
    print(f"Puerto Chat Masivo: {config.config['servidor']['puerto_chatmasivo']}")
    print("=" * 80)
