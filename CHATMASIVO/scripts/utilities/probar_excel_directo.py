#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para probar la función de creación de Excel directamente
"""

import sys
import os

# Agregar el directorio actual al path para importar el módulo
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def probar_creacion_excel():
    """Probar la creación de archivo Excel directamente"""
    try:
        import pandas as pd
        import io
        
        print("=" * 50)
        print("PROBANDO CREACION DE ARCHIVO EXCEL")
        print("=" * 50)
        
        # Crear DataFrame con ejemplo
        data = {
            'nombre': ['Juan', 'María', 'Carlos'],
            'apellido': ['Pérez', 'González', 'López'],
            'numero': ['51987654321', '51912345678', '51911223344'],
            'carrera': ['Ingeniería', 'Medicina', 'Derecho']
        }
        
        df = pd.DataFrame(data)
        print("✅ DataFrame creado correctamente")
        print(f"Columnas: {list(df.columns)}")
        print(f"Filas: {len(df)}")
        
        # Crear archivo Excel en memoria
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Contactos', index=False)
        
        output.seek(0)
        excel_content = output.getvalue()
        
        print(f"✅ Archivo Excel creado en memoria")
        print(f"Tamaño: {len(excel_content)} bytes")
        
        # Guardar archivo para verificación
        with open('plantilla_prueba.xlsx', 'wb') as f:
            f.write(excel_content)
        
        print("✅ Archivo guardado como: plantilla_prueba.xlsx")
        
        # Verificar que el archivo se creó correctamente
        if os.path.exists('plantilla_prueba.xlsx'):
            file_size = os.path.getsize('plantilla_prueba.xlsx')
            print(f"✅ Archivo guardado correctamente")
            print(f"Tamaño del archivo: {file_size} bytes")
            
            if file_size > 0:
                print("✅ ¡Archivo Excel creado exitosamente!")
                print("✅ Es un archivo .xlsx real, no CSV")
            else:
                print("❌ El archivo está vacío")
        else:
            print("❌ No se pudo guardar el archivo")
            
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("Instala las dependencias con: pip install pandas openpyxl")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    probar_creacion_excel()
