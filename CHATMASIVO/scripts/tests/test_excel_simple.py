#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script simple para probar la creación de Excel
"""

def main():
    print("=" * 50)
    print("PRUEBA DE CREACION DE EXCEL")
    print("=" * 50)
    
    try:
        import pandas as pd
        print("✅ pandas importado correctamente")
        
        import openpyxl
        print("✅ openpyxl importado correctamente")
        
        # Crear datos
        data = {
            'nombre': ['Juan', 'María', 'Carlos'],
            'apellido': ['Pérez', 'González', 'López'],
            'numero': ['51987654321', '51912345678', '51911223344'],
            'carrera': ['Ingeniería', 'Medicina', 'Derecho']
        }
        
        df = pd.DataFrame(data)
        print("✅ DataFrame creado")
        
        # Crear archivo Excel
        df.to_excel('plantilla_contactos_final.xlsx', index=False, sheet_name='Contactos')
        print("✅ Archivo Excel creado: plantilla_contactos_final.xlsx")
        
        # Verificar archivo
        import os
        if os.path.exists('plantilla_contactos_final.xlsx'):
            size = os.path.getsize('plantilla_contactos_final.xlsx')
            print(f"✅ Archivo verificado: {size} bytes")
            print("✅ ¡Es un archivo Excel real (.xlsx)!")
        else:
            print("❌ Archivo no encontrado")
            
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("Instala las dependencias: pip install pandas openpyxl")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
