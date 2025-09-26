#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar la funcionalidad completa de grupos
"""

import sqlite3
import os
import sys

# Agregar el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_database_schema():
    """Probar el esquema de la base de datos"""
    print("🔍 Probando esquema de base de datos...")
    
    conn = sqlite3.connect('numeros_whatsapp.db')
    cursor = conn.cursor()
    
    # Verificar tabla de grupos
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='grupos'")
    if cursor.fetchone():
        print("✅ Tabla 'grupos' existe")
        
        # Verificar grupos por defecto
        cursor.execute("SELECT nombre FROM grupos")
        grupos = [row[0] for row in cursor.fetchall()]
        grupos_esperados = ['General', 'Ingeniería', 'Medicina', 'Derecho', 'Administración', 'Psicología']
        
        for grupo in grupos_esperados:
            if grupo in grupos:
                print(f"✅ Grupo '{grupo}' existe")
            else:
                print(f"❌ Grupo '{grupo}' NO existe")
    else:
        print("❌ Tabla 'grupos' NO existe")
    
    # Verificar tabla de números
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='numeros'")
    if cursor.fetchone():
        print("✅ Tabla 'numeros' existe")
        
        # Verificar columnas
        cursor.execute("PRAGMA table_info(numeros)")
        columnas = [row[1] for row in cursor.fetchall()]
        columnas_esperadas = ['id', 'nombre', 'apellido', 'telefono', 'carrera', 'grupo_id', 'activo', 'fecha_registro']
        
        for col in columnas_esperadas:
            if col in columnas:
                print(f"✅ Columna '{col}' existe")
            else:
                print(f"❌ Columna '{col}' NO existe")
    else:
        print("❌ Tabla 'numeros' NO existe")
    
    conn.close()

def test_agregar_contactos():
    """Probar agregar contactos con grupos"""
    print("\n🔍 Probando agregar contactos...")
    
    # Importar funciones del módulo principal
    try:
        from codchat import agregar_numero, get_numeros_activos, get_grupos
    except ImportError:
        print("❌ No se pudo importar codchat.py")
        return
    
    # Obtener grupos disponibles
    grupos = get_grupos()
    print(f"📋 Grupos disponibles: {[g[1] for g in grupos]}")
    
    # Agregar contactos de prueba
    contactos_prueba = [
        ('Juan', 'Pérez', '51987654321', 'Ingeniería de Sistemas', 'Ingeniería'),
        ('María', 'González', '51912345678', 'Medicina', 'Medicina'),
        ('Carlos', 'López', '51911223344', 'Derecho', 'Derecho'),
        ('Ana', 'Martínez', '51999887766', 'Psicología', 'Psicología'),
        ('Luis', 'Rodríguez', '51955443322', 'Administración', 'Administración')
    ]
    
    for nombre, apellido, telefono, carrera, grupo_nombre in contactos_prueba:
        # Buscar ID del grupo
        grupo_id = None
        for grupo in grupos:
            if grupo[1] == grupo_nombre:
                grupo_id = grupo[0]
                break
        
        if grupo_id:
            success = agregar_numero(nombre, apellido, telefono, carrera, grupo_id)
            if success:
                print(f"✅ {nombre} {apellido} agregado al grupo {grupo_nombre}")
            else:
                print(f"⚠️ {nombre} {apellido} ya existe")
        else:
            print(f"❌ Grupo '{grupo_nombre}' no encontrado")

def test_filtrado_grupos():
    """Probar filtrado por grupos"""
    print("\n🔍 Probando filtrado por grupos...")
    
    try:
        from codchat import get_numeros_activos, get_grupos
    except ImportError:
        print("❌ No se pudo importar codchat.py")
        return
    
    grupos = get_grupos()
    
    # Probar filtrado por cada grupo
    for grupo_id, grupo_nombre, descripcion in grupos:
        numeros = get_numeros_activos(grupo_id)
        print(f"📊 Grupo '{grupo_nombre}': {len(numeros)} contactos")
        
        for numero in numeros[:3]:  # Mostrar solo los primeros 3
            print(f"   - {numero[1]} {numero[2] or ''} ({numero[4] or 'Sin carrera'})")
    
    # Probar sin filtro (todos los contactos)
    todos_numeros = get_numeros_activos()
    print(f"📊 Total de contactos: {len(todos_numeros)}")

def test_importacion_excel():
    """Probar importación desde Excel"""
    print("\n🔍 Probando importación desde Excel...")
    
    if not os.path.exists('ejemplo_contactos.xlsx'):
        print("❌ Archivo 'ejemplo_contactos.xlsx' no encontrado")
        return
    
    try:
        from codchat import importar_desde_excel
    except ImportError:
        print("❌ No se pudo importar codchat.py")
        return
    
    # Simular archivo Excel
    class MockFile:
        def __init__(self, filename):
            self.filename = filename
    
    archivo = MockFile('ejemplo_contactos.xlsx')
    resultado = importar_desde_excel(archivo)
    
    if resultado['success']:
        res = resultado['resultados']
        print(f"✅ Importación exitosa: {res['exitosos']} contactos, {res['errores']} errores, {res['duplicados']} duplicados")
    else:
        print(f"❌ Error en importación: {resultado['message']}")

def main():
    """Función principal de prueba"""
    print("🚀 Iniciando pruebas de funcionalidad de grupos")
    print("=" * 50)
    
    # Inicializar base de datos
    try:
        from codchat import init_db
        init_db()
        print("✅ Base de datos inicializada")
    except Exception as e:
        print(f"❌ Error inicializando base de datos: {e}")
        return
    
    # Ejecutar pruebas
    test_database_schema()
    test_agregar_contactos()
    test_filtrado_grupos()
    test_importacion_excel()
    
    print("\n" + "=" * 50)
    print("✅ Pruebas completadas")

if __name__ == '__main__':
    main()
