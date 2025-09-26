#!/usr/bin/env python3
"""
Script de instalación y reparación automática
Instala dependencias y repara la base de datos de usuarios
"""

import subprocess
import sys
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def instalar_dependencias():
    """Instalar dependencias de Python"""
    try:
        print("📦 Instalando dependencias...")
        
        # Lista de dependencias principales
        dependencias = [
            'flask',
            'requests',
            'beautifulsoup4',
            'PyPDF2',
            'python-docx',
            'twilio'
        ]
        
        for dep in dependencias:
            try:
                print(f"  Instalando {dep}...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep], 
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"  ✅ {dep} instalado correctamente")
            except subprocess.CalledProcessError:
                print(f"  ⚠️  Error instalando {dep}, continuando...")
        
        print("✅ Dependencias instaladas")
        return True
        
    except Exception as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def reparar_base_datos():
    """Ejecutar script de reparación de base de datos"""
    try:
        print("🔧 Reparando base de datos de usuarios...")
        
        # Importar y ejecutar el script de reparación
        from reparar_base_datos_usuarios import main as reparar_main
        return reparar_main()
        
    except Exception as e:
        print(f"❌ Error reparando base de datos: {e}")
        return False

def verificar_instalacion():
    """Verificar que todo esté instalado correctamente"""
    try:
        print("🔍 Verificando instalación...")
        
        # Verificar archivos principales
        archivos_requeridos = [
            'SISTEMA_UNIFICADO_FINAL.py',
            'reparar_base_datos_usuarios.py',
            'requirements.txt'
        ]
        
        for archivo in archivos_requeridos:
            if not os.path.exists(archivo):
                print(f"  ❌ Archivo faltante: {archivo}")
                return False
            else:
                print(f"  ✅ {archivo} encontrado")
        
        # Verificar base de datos de usuarios
        if os.path.exists('data/database/users.db'):
            print("  ✅ Base de datos de usuarios encontrada")
        else:
            print("  ⚠️  Base de datos de usuarios no encontrada")
        
        print("✅ Verificación completada")
        return True
        
    except Exception as e:
        print(f"❌ Error en verificación: {e}")
        return False

def main():
    """Función principal de instalación"""
    print("=" * 70)
    print("🚀 INSTALADOR AUTOMÁTICO DEL SISTEMA UNIFICADO")
    print("=" * 70)
    print("Este script instalará las dependencias y reparará la base de datos")
    print()
    
    # Paso 1: Instalar dependencias
    if not instalar_dependencias():
        print("❌ Error en la instalación de dependencias")
        return False
    
    print()
    
    # Paso 2: Reparar base de datos
    if not reparar_base_datos():
        print("❌ Error reparando la base de datos")
        return False
    
    print()
    
    # Paso 3: Verificar instalación
    if not verificar_instalacion():
        print("❌ Error en la verificación")
        return False
    
    print()
    print("🎉 ¡INSTALACIÓN COMPLETADA EXITOSAMENTE!")
    print("=" * 70)
    print("Para iniciar el sistema:")
    print("  python SISTEMA_UNIFICADO_FINAL.py")
    print()
    print("Usuarios disponibles:")
    print("  👤 admin / admin123 (Administrador)")
    print("  👤 jperez / 123456 (Asesor)")
    print("  👤 carlos / 123456 (Programador)")
    print()
    print("Sistema disponible en: http://localhost:5000")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Instalación cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
