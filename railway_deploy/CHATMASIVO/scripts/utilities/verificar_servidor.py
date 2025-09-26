#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para verificar que el servidor esté funcionando
"""

import requests
import time

def verificar_servidor():
    """Verificar que el servidor esté funcionando"""
    try:
        # Verificar que el servidor responda
        response = requests.get('http://localhost:5000/', timeout=5)
        
        if response.status_code == 200:
            print("✅ Servidor funcionando correctamente")
            print(f"Estado: {response.status_code}")
            print("✅ Puedes acceder a: http://localhost:5000")
            return True
        else:
            print(f"❌ Servidor respondió con error: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor")
        print("El servidor no está ejecutándose en http://localhost:5000")
        return False
    except requests.exceptions.Timeout:
        print("❌ Timeout al conectar con el servidor")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def probar_descarga_excel():
    """Probar la descarga de plantilla Excel"""
    try:
        print("\n" + "=" * 50)
        print("PROBANDO DESCARGA DE PLANTILLA EXCEL")
        print("=" * 50)
        
        response = requests.get('http://localhost:5000/descargar_plantilla_excel', timeout=10)
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            content_length = len(response.content)
            
            print(f"✅ Descarga exitosa")
            print(f"Tipo de contenido: {content_type}")
            print(f"Tamaño: {content_length} bytes")
            
            # Verificar si es realmente un Excel
            if 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in content_type:
                print("✅ Es un archivo Excel (.xlsx) real")
            elif 'application/octet-stream' in content_type:
                print("✅ Es un archivo binario (probablemente Excel)")
            else:
                print(f"⚠️  Tipo de contenido inesperado: {content_type}")
            
            # Guardar archivo para verificación
            with open('plantilla_verificacion.xlsx', 'wb') as f:
                f.write(response.content)
            print("✅ Archivo guardado como: plantilla_verificacion.xlsx")
            
        else:
            print(f"❌ Error en descarga: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error probando descarga: {e}")

if __name__ == "__main__":
    print("VERIFICANDO SERVIDOR CHAT MASIVO")
    print("=" * 50)
    
    if verificar_servidor():
        probar_descarga_excel()
    else:
        print("\n💡 Para iniciar el servidor, ejecuta:")
        print("   python codchat_simple.py")
        print("   o")
        print("   .\\INICIAR_CHAT_MASIVO.bat")
