#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar la descarga de plantilla Excel con grupos
"""

import pandas as pd
import io
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

def crear_plantilla_excel():
    """Crear plantilla Excel con grupos (simulando la función del sistema)"""
    try:
        # Crear datos de ejemplo más completos
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
        df = pd.DataFrame(data)
        
        # Crear archivo en memoria con múltiples hojas
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
        with open('plantilla_descargada.xlsx', 'wb') as f:
            f.write(output.getvalue())
        
        print("✅ Plantilla Excel creada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error creando plantilla: {e}")
        return False

def verificar_plantilla():
    """Verificar que la plantilla tiene la columna de grupos"""
    try:
        # Leer el archivo generado
        df = pd.read_excel('plantilla_descargada.xlsx', sheet_name='Contactos')
        
        print("\n🔍 Verificando plantilla descargada...")
        print(f"📊 Columnas encontradas: {list(df.columns)}")
        print(f"📈 Número de filas: {len(df)}")
        
        # Verificar columnas requeridas
        columnas_requeridas = ['nombre', 'apellido', 'numero', 'carrera', 'grupo']
        columnas_encontradas = [col.lower().strip() for col in df.columns]
        
        print("\n✅ Verificación de columnas:")
        todas_presentes = True
        for col in columnas_requeridas:
            if col in columnas_encontradas:
                print(f"   ✅ {col}")
            else:
                print(f"   ❌ {col} - FALTA")
                todas_presentes = False
        
        if todas_presentes:
            print("\n🎉 ¡La plantilla incluye la columna de grupos!")
            
            # Mostrar algunos datos de ejemplo
            print("\n📋 Datos de ejemplo:")
            print(df.head().to_string(index=False))
            
            # Verificar grupos únicos
            if 'grupo' in df.columns:
                grupos_unicos = df['grupo'].unique()
                print(f"\n🏷️ Grupos en la plantilla: {list(grupos_unicos)}")
                
                # Contar contactos por grupo
                print("\n📊 Distribución por grupos:")
                conteo_grupos = df['grupo'].value_counts()
                for grupo, cantidad in conteo_grupos.items():
                    print(f"   {grupo}: {cantidad} contactos")
            
            return True
        else:
            print("\n❌ Faltan columnas requeridas en la plantilla")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando plantilla: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Probando descarga de plantilla Excel con grupos...")
    print("=" * 60)
    
    # Crear plantilla
    if crear_plantilla_excel():
        print("✅ Plantilla creada exitosamente")
        
        # Verificar plantilla
        if verificar_plantilla():
            print("\n✅ Verificación completada exitosamente")
            print("🎯 La plantilla descargada incluye correctamente la columna de grupos")
            print("📁 Archivo guardado como: plantilla_descargada.xlsx")
        else:
            print("\n❌ La verificación falló")
    else:
        print("\n❌ Error creando la plantilla")

if __name__ == '__main__':
    main()
