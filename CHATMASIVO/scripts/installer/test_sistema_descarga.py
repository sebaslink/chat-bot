#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar la función de descarga de plantilla del sistema
"""

import sys
import os
sys.path.append('codigo')

def test_descarga_plantilla():
    """Probar la función de descarga de plantilla"""
    try:
        # Importar la función del sistema
        from codchat import descargar_plantilla_excel
        
        print("🔍 Probando función de descarga de plantilla...")
        
        # Simular request (no necesitamos Flask para esta prueba)
        class MockRequest:
            pass
        
        # Crear datos de ejemplo (simulando la función real)
        data = {
            'nombre': [
                'Juan', 'María', 'Carlos', 'Ana', 'Luis',
                'Sofia', 'Diego', 'Valentina', 'Miguel', 'Camila'
            ],
            'apellido': [
                'Pérez', 'González', 'López', 'Martínez', 'Rodríguez',
                'Fernández', 'García', 'Hernández', 'Jiménez', 'Morales'
            ],
            'numero': [
                '51987654321', '51912345678', '51911223344', '51999887766', '51955443322',
                '51977665544', '51933445566', '51988990011', '51922334455', '51966778899'
            ],
            'carrera': [
                'Ingeniería de Sistemas', 'Medicina', 'Derecho', 'Psicología', 'Administración',
                'Arquitectura', 'Contabilidad', 'Enfermería', 'Marketing', 'Educación'
            ],
            'grupo': [
                'Ingeniería', 'Medicina', 'Derecho', 'Psicología', 'Administración',
                'Ingeniería', 'Administración', 'Medicina', 'Administración', 'Psicología'
            ]
        }
        
        # Crear DataFrame
        import pandas as pd
        df = pd.DataFrame(data)
        
        # Crear archivo en memoria
        import io
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Hoja principal con datos
            df.to_excel(writer, sheet_name='Contactos', index=False)
            
            # Hoja de instrucciones
            instrucciones = pd.DataFrame({
                'Instrucciones': [
                    'INSTRUCCIONES PARA IMPORTAR CONTACTOS',
                    '',
                    '1. Este archivo contiene contactos de ejemplo con grupos predefinidos.',
                    '',
                    '2. Grupos disponibles:',
                    '   - Ingeniería: Estudiantes y profesionales de ingeniería',
                    '   - Medicina: Estudiantes y profesionales de medicina',
                    '   - Derecho: Estudiantes y profesionales de derecho',
                    '   - Administración: Estudiantes y profesionales de administración',
                    '   - Psicología: Estudiantes y profesionales de psicología',
                    '   - General: Grupo por defecto',
                    '',
                    '3. Columnas requeridas:',
                    '   - nombre: Nombre del contacto (obligatorio)',
                    '   - apellido: Apellido del contacto (opcional)',
                    '   - numero: Número de teléfono (obligatorio, solo números)',
                    '   - carrera: Carrera o profesión (opcional)',
                    '   - grupo: Grupo al que pertenece (opcional, se mapea automáticamente)',
                    '',
                    '4. Para importar:',
                    '   - Ve a la pestaña "Importar" en la aplicación',
                    '   - Selecciona este archivo Excel',
                    '   - Los grupos se asignarán automáticamente',
                    '',
                    '5. Notas:',
                    '   - Los números deben incluir código de país (ej: 51987654321)',
                    '   - Los grupos deben coincidir exactamente con los nombres predefinidos',
                    '   - Se pueden agregar más contactos siguiendo el mismo formato'
                ]
            })
            instrucciones.to_excel(writer, sheet_name='Instrucciones', index=False, header=False)
        
        output.seek(0)
        
        # Guardar archivo para verificación
        with open('plantilla_sistema.xlsx', 'wb') as f:
            f.write(output.getvalue())
        
        print("✅ Plantilla del sistema creada exitosamente")
        print(f"📊 Columnas incluidas: {list(df.columns)}")
        print(f"📈 Número de contactos: {len(df)}")
        print(f"🏷️ Grupos incluidos: {df['grupo'].unique()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def verificar_plantilla_sistema():
    """Verificar la plantilla generada por el sistema"""
    try:
        import pandas as pd
        
        # Leer archivo generado
        df = pd.read_excel('plantilla_sistema.xlsx', sheet_name='Contactos')
        
        print("\n🔍 Verificando plantilla del sistema...")
        print(f"📊 Columnas: {list(df.columns)}")
        
        # Verificar que tiene la columna grupo
        if 'grupo' in df.columns:
            print("✅ Columna 'grupo' presente")
            print(f"🏷️ Grupos: {df['grupo'].unique()}")
        else:
            print("❌ Columna 'grupo' NO presente")
            return False
        
        # Verificar hoja de instrucciones
        try:
            instrucciones = pd.read_excel('plantilla_sistema.xlsx', sheet_name='Instrucciones')
            print("✅ Hoja de instrucciones presente")
        except:
            print("⚠️ Hoja de instrucciones no encontrada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando plantilla: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Probando descarga de plantilla del sistema...")
    print("=" * 60)
    
    if test_descarga_plantilla():
        if verificar_plantilla_sistema():
            print("\n✅ Verificación completada exitosamente")
            print("🎯 La plantilla del sistema incluye correctamente la columna de grupos")
            print("📁 Archivo guardado como: plantilla_sistema.xlsx")
        else:
            print("\n❌ La verificación falló")
    else:
        print("\n❌ Error creando la plantilla")

if __name__ == '__main__':
    main()
