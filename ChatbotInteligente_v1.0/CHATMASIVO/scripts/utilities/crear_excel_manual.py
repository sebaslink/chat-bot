#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para crear manualmente un archivo Excel de prueba
"""

import subprocess
import sys

def crear_excel_manual():
    """Crear archivo Excel manualmente"""
    try:
        print("Creando archivo Excel de prueba...")
        
        # Crear script temporal
        script_content = '''
import pandas as pd
import os

# Crear datos
data = {
    'nombre': ['Juan', 'María', 'Carlos'],
    'apellido': ['Pérez', 'González', 'López'],
    'numero': ['51987654321', '51912345678', '51911223344'],
    'carrera': ['Ingeniería', 'Medicina', 'Derecho']
}

df = pd.DataFrame(data)

# Crear archivo Excel
df.to_excel('plantilla_contactos_manual.xlsx', index=False, sheet_name='Contactos')

print("Archivo Excel creado: plantilla_contactos_manual.xlsx")
print(f"Tamaño: {os.path.getsize('plantilla_contactos_manual.xlsx')} bytes")
'''
        
        # Escribir script temporal
        with open('temp_excel.py', 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Ejecutar script
        result = subprocess.run([sys.executable, 'temp_excel.py'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Archivo Excel creado exitosamente")
            print(result.stdout)
            
            # Verificar archivo
            import os
            if os.path.exists('plantilla_contactos_manual.xlsx'):
                size = os.path.getsize('plantilla_contactos_manual.xlsx')
                print(f"✅ Archivo verificado: {size} bytes")
                return True
            else:
                print("❌ Archivo no encontrado")
                return False
        else:
            print("❌ Error ejecutando script:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        # Limpiar archivo temporal
        try:
            import os
            if os.path.exists('temp_excel.py'):
                os.remove('temp_excel.py')
        except:
            pass

if __name__ == "__main__":
    crear_excel_manual()
