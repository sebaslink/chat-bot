#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SCRIPT DE PRUEBA COMPLETA DEL SISTEMA CHAT MASIVO
Verifica todas las funcionalidades del sistema
"""

import requests
import json
import time
import sqlite3
from datetime import datetime

def test_servidor():
    """Probar que el servidor esté funcionando"""
    print("🔍 Probando servidor...")
    try:
        response = requests.get("http://localhost:5000/api/estadisticas", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor funcionando correctamente")
            return True
        else:
            print(f"❌ Servidor respondió con código: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error conectando al servidor: {e}")
        return False

def test_base_datos():
    """Probar la base de datos"""
    print("\n🔍 Probando base de datos...")
    try:
        conn = sqlite3.connect('numeros_whatsapp.db')
        cursor = conn.cursor()
        
        # Verificar tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas = [row[0] for row in cursor.fetchall()]
        print(f"✅ Tablas encontradas: {tablas}")
        
        # Verificar contactos
        cursor.execute("SELECT COUNT(*) FROM numeros WHERE activo = 1")
        contactos = cursor.fetchone()[0]
        print(f"✅ Contactos activos: {contactos}")
        
        # Verificar estructura
        cursor.execute("PRAGMA table_info(numeros)")
        columnas_numeros = [col[1] for col in cursor.fetchall()]
        print(f"✅ Columnas tabla numeros: {columnas_numeros}")
        
        cursor.execute("PRAGMA table_info(mensajes_log)")
        columnas_log = [col[1] for col in cursor.fetchall()]
        print(f"✅ Columnas tabla mensajes_log: {columnas_log}")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error en base de datos: {e}")
        return False

def test_api_endpoints():
    """Probar endpoints de la API"""
    print("\n🔍 Probando endpoints de la API...")
    
    endpoints = [
        ("/", "Página principal"),
        ("/api/estadisticas", "Estadísticas"),
        ("/descargar_plantilla_excel", "Descarga plantilla Excel")
    ]
    
    for endpoint, descripcion in endpoints:
        try:
            response = requests.get(f"http://localhost:5000{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {descripcion}: OK")
            else:
                print(f"⚠️ {descripcion}: Código {response.status_code}")
        except Exception as e:
            print(f"❌ {descripcion}: Error - {e}")

def test_envio_prueba():
    """Probar envío de mensaje de prueba"""
    print("\n🔍 Probando envío de mensaje de prueba...")
    try:
        response = requests.post("http://localhost:5000/api/enviar_prueba", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Mensaje de prueba enviado exitosamente")
                print(f"   SID: {data.get('sid', 'N/A')}")
                return True
            else:
                print(f"⚠️ Mensaje de prueba falló: {data.get('message', 'Error desconocido')}")
                return False
        else:
            print(f"❌ Error en envío de prueba: Código {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en envío de prueba: {e}")
        return False

def test_envio_masivo():
    """Probar envío masivo"""
    print("\n🔍 Probando envío masivo...")
    try:
        # Datos de prueba para envío masivo
        data = {
            'intro': 'Hola',
            'texto_random': 'Mensaje de prueba del sistema',
            'texto_fijo': 'Este es un mensaje de prueba del sistema de chat masivo.'
        }
        
        response = requests.post("http://localhost:5000/enviar_masivo", data=data, timeout=30)
        if response.status_code == 302:  # Redirect después del envío
            print("✅ Envío masivo procesado correctamente")
            return True
        else:
            print(f"⚠️ Envío masivo falló: Código {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en envío masivo: {e}")
        return False

def test_importar_excel():
    """Probar importación de Excel"""
    print("\n🔍 Probando importación de Excel...")
    try:
        # Crear archivo CSV de prueba
        csv_content = "nombre,apellido,numero,carrera\nTest,Usuario,123456789,Prueba"
        
        files = {'archivo': ('test.csv', csv_content, 'text/csv')}
        response = requests.post("http://localhost:5000/importar_excel", files=files, timeout=10)
        
        if response.status_code == 302:  # Redirect después de importar
            print("✅ Importación de Excel procesada correctamente")
            return True
        else:
            print(f"⚠️ Importación de Excel falló: Código {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en importación de Excel: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("=" * 60)
    print("🧪 PRUEBA COMPLETA DEL SISTEMA CHAT MASIVO WHATSAPP")
    print("=" * 60)
    
    resultados = []
    
    # Ejecutar todas las pruebas
    resultados.append(("Servidor", test_servidor()))
    resultados.append(("Base de Datos", test_base_datos()))
    test_api_endpoints()
    resultados.append(("Envío Prueba", test_envio_prueba()))
    resultados.append(("Envío Masivo", test_envio_masivo()))
    resultados.append(("Importar Excel", test_importar_excel()))
    
    # Resumen de resultados
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    exitosos = 0
    total = len(resultados)
    
    for prueba, resultado in resultados:
        estado = "✅ EXITOSO" if resultado else "❌ FALLÓ"
        print(f"{prueba:20} : {estado}")
        if resultado:
            exitosos += 1
    
    print(f"\nResultado: {exitosos}/{total} pruebas exitosas")
    
    if exitosos == total:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON! El sistema está funcionando correctamente.")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa los errores arriba.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()


