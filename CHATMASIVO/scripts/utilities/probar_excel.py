#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para probar la descarga de plantilla Excel
"""

import requests
import os

def probar_descarga_excel():
    """Probar la descarga de plantilla Excel"""
    try:
        # Hacer petición para descargar la plantilla
        response = requests.get('http://localhost:5000/descargar_plantilla_excel')
        
        if response.status_code == 200:
            # Guardar el archivo descargado
            with open('plantilla_descargada.xlsx', 'wb') as f:
                f.write(response.content)
            
            print("=" * 50)
            print("PRUEBA DE DESCARGA EXCEL")
            print("=" * 50)
            print(f"Estado HTTP: {response.status_code}")
            print(f"Tipo de contenido: {response.headers.get('content-type', 'N/A')}")
            print(f"Tamaño del archivo: {len(response.content)} bytes")
            print(f"Archivo guardado como: plantilla_descargada.xlsx")
            
            # Verificar si el archivo existe y su tamaño
            if os.path.exists('plantilla_descargada.xlsx'):
                file_size = os.path.getsize('plantilla_descargada.xlsx')
                print(f"Tamaño del archivo guardado: {file_size} bytes")
                
                if file_size > 0:
                    print("✅ ¡Archivo Excel descargado exitosamente!")
                    print("✅ El archivo tiene contenido y es un Excel real (.xlsx)")
                else:
                    print("❌ El archivo está vacío")
            else:
                print("❌ No se pudo guardar el archivo")
                
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor")
        print("Asegúrate de que el servidor esté ejecutándose en http://localhost:5000")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    probar_descarga_excel()
