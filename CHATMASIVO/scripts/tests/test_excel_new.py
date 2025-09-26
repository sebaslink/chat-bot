#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para probar la creación de Excel usando un enfoque diferente
"""

import sys
import os

def test_excel():
    """Probar la creación de Excel"""
    print("Iniciando prueba de Excel...")
    
    try:
        # Importar dependencias
        import pandas as pd
        import openpyxl
        
        print("Dependencias importadas correctamente")
        
        # Crear datos
        data = {
            'nombre': ['Juan', 'María', 'Carlos'],
            'apellido': ['Pérez', 'González', 'López'],
            'numero': ['51987654321', '51912345678', '51911223344'],
            'carrera': ['Ingeniería', 'Medicina', 'Derecho']
        }
        
        df = pd.DataFrame(data)
        print("DataFrame creado")
        
        # Crear archivo Excel
        filename = 'plantilla_contactos_test.xlsx'
        df.to_excel(filename, index=False, sheet_name='Contactos')
        print(f"Archivo Excel creado: {filename}")
        
        # Verificar archivo
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"Archivo verificado: {size} bytes")
            print("¡Archivo Excel creado exitosamente!")
            return True
        else:
            print("Error: Archivo no encontrado")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_excel()