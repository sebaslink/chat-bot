#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para reparar la base de datos y resolver problemas de bloqueo
"""

import os
import sqlite3
import shutil
from datetime import datetime

def reparar_base_datos():
    """Reparar la base de datos SQLite"""
    print("🔧 REPARANDO BASE DE DATOS")
    print("=" * 40)
    
    # Ruta de la base de datos
    db_path = "data/database/numeros_whatsapp.db"
    backup_path = f"data/database/numeros_whatsapp_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    
    try:
        # Verificar si existe la base de datos
        if not os.path.exists(db_path):
            print("❌ Base de datos no encontrada")
            return False
        
        # Crear respaldo
        print("📁 Creando respaldo de la base de datos...")
        shutil.copy2(db_path, backup_path)
        print(f"✅ Respaldo creado: {backup_path}")
        
        # Intentar conectar y verificar la base de datos
        print("🔍 Verificando integridad de la base de datos...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar integridad
        cursor.execute("PRAGMA integrity_check")
        result = cursor.fetchone()
        
        if result[0] == "ok":
            print("✅ Base de datos íntegra")
        else:
            print(f"⚠️  Problemas de integridad detectados: {result[0]}")
        
        # Verificar tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"📊 Tablas encontradas: {len(tables)}")
        
        for table in tables:
            print(f"  - {table[0]}")
        
        # Verificar datos
        cursor.execute("SELECT COUNT(*) FROM numeros")
        total_contactos = cursor.fetchone()[0]
        print(f"👥 Total contactos: {total_contactos}")
        
        cursor.execute("SELECT COUNT(*) FROM grupos")
        total_grupos = cursor.fetchone()[0]
        print(f"👥 Total grupos: {total_grupos}")
        
        # Cerrar conexión
        conn.close()
        
        print("✅ Base de datos reparada exitosamente")
        return True
        
    except sqlite3.OperationalError as e:
        if "database is locked" in str(e):
            print("❌ Base de datos bloqueada")
            print("💡 Solución: Cierra todas las aplicaciones que usen la base de datos")
            return False
        else:
            print(f"❌ Error de base de datos: {e}")
            return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def crear_base_datos_nueva():
    """Crear una nueva base de datos si es necesario"""
    print("\n🆕 CREANDO NUEVA BASE DE DATOS")
    print("=" * 40)
    
    try:
        # Importar la función de inicialización
        import sys
        sys.path.append('.')
        from main import init_db
        
        # Crear nueva base de datos
        init_db()
        print("✅ Nueva base de datos creada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error creando nueva base de datos: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 REPARADOR DE BASE DE DATOS - CHAT MASIVO")
    print("=" * 50)
    
    try:
        # Intentar reparar la base de datos existente
        if reparar_base_datos():
            print("\n🎉 ¡Base de datos reparada exitosamente!")
        else:
            print("\n⚠️  No se pudo reparar la base de datos existente")
            print("🆕 Creando nueva base de datos...")
            
            if crear_base_datos_nueva():
                print("🎉 ¡Nueva base de datos creada exitosamente!")
            else:
                print("❌ No se pudo crear nueva base de datos")
                return False
        
        print("\n📋 INSTRUCCIONES:")
        print("1. La base de datos está lista para usar")
        print("2. Ejecuta 'INICIAR_APLICACION.bat' para iniciar la app")
        print("3. Si hay problemas, revisa los logs")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error durante la reparación: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
