#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para diagnosticar problemas de importación de Excel
"""

import os
import sys
import pandas as pd
import sqlite3
from datetime import datetime

def verificar_dependencias():
    """Verificar que las dependencias estén instaladas"""
    print("🔍 VERIFICANDO DEPENDENCIAS")
    print("=" * 40)
    
    try:
        import pandas
        print("✅ pandas instalado")
    except ImportError:
        print("❌ pandas no instalado")
        return False
    
    try:
        import openpyxl
        print("✅ openpyxl instalado")
    except ImportError:
        print("❌ openpyxl no instalado")
        return False
    
    try:
        import xlrd
        print("✅ xlrd instalado")
    except ImportError:
        print("⚠️  xlrd no instalado (opcional para .xls)")
    
    return True

def crear_archivo_excel_prueba():
    """Crear un archivo Excel de prueba"""
    print("\n📝 CREANDO ARCHIVO EXCEL DE PRUEBA")
    print("=" * 40)
    
    # Datos de prueba
    datos = {
        'nombre': ['Juan', 'María', 'Carlos', 'Ana', 'Luis'],
        'apellido': ['Pérez', 'García', 'López', 'Martín', 'Rodríguez'],
        'numero': ['51987654321', '51987654322', '51987654323', '51987654324', '51987654325'],
        'carrera': ['Ingeniería', 'Medicina', 'Derecho', 'Psicología', 'Administración'],
        'grupo': ['Grupo A', 'Grupo B', 'Grupo A', 'Grupo C', 'Grupo B']
    }
    
    df = pd.DataFrame(datos)
    archivo_prueba = 'test_importacion.xlsx'
    
    try:
        df.to_excel(archivo_prueba, index=False)
        print(f"✅ Archivo de prueba creado: {archivo_prueba}")
        print(f"📊 Filas: {len(df)}")
        print(f"📋 Columnas: {list(df.columns)}")
        return archivo_prueba
    except Exception as e:
        print(f"❌ Error creando archivo: {e}")
        return None

def probar_lectura_excel(archivo):
    """Probar la lectura del archivo Excel"""
    print(f"\n📖 PROBANDO LECTURA DE {archivo}")
    print("=" * 40)
    
    try:
        # Leer archivo
        df = pd.read_excel(archivo)
        print(f"✅ Archivo leído exitosamente")
        print(f"📊 Filas: {len(df)}")
        print(f"📋 Columnas: {list(df.columns)}")
        print(f"📋 Tipos de datos:")
        for col in df.columns:
            print(f"  - {col}: {df[col].dtype}")
        
        # Mostrar primeras filas
        print(f"\n📋 Primeras 3 filas:")
        print(df.head(3).to_string())
        
        return True
        
    except Exception as e:
        print(f"❌ Error leyendo archivo: {e}")
        import traceback
        traceback.print_exc()
        return False

def probar_mapeo_columnas(archivo):
    """Probar el mapeo de columnas"""
    print(f"\n🗺️  PROBANDO MAPEO DE COLUMNAS")
    print("=" * 40)
    
    try:
        df = pd.read_excel(archivo)
        
        # Columnas requeridas
        columnas_requeridas = ['nombre', 'apellido', 'numero', 'carrera', 'grupo']
        columnas_disponibles = [col.lower().strip() for col in df.columns]
        
        print(f"📋 Columnas requeridas: {columnas_requeridas}")
        print(f"📋 Columnas disponibles: {columnas_disponibles}")
        
        # Mapear columnas (case insensitive)
        mapeo_columnas = {}
        for col_req in columnas_requeridas:
            for col_disp in columnas_disponibles:
                if col_req in col_disp or col_disp in col_req:
                    mapeo_columnas[col_req] = df.columns[columnas_disponibles.index(col_disp)]
                    break
        
        print(f"🗺️  Mapeo encontrado: {mapeo_columnas}")
        
        # Verificar que se encontraron todas las columnas
        if len(mapeo_columnas) < 5:
            print(f"❌ Faltan columnas requeridas. Se encontraron: {list(mapeo_columnas.keys())}")
            return False
        else:
            print(f"✅ Todas las columnas requeridas encontradas")
            return True
            
    except Exception as e:
        print(f"❌ Error en mapeo: {e}")
        return False

def probar_procesamiento_filas(archivo):
    """Probar el procesamiento de filas"""
    print(f"\n⚙️  PROBANDO PROCESAMIENTO DE FILAS")
    print("=" * 40)
    
    try:
        df = pd.read_excel(archivo)
        
        # Mapear columnas
        columnas_requeridas = ['nombre', 'apellido', 'numero', 'carrera', 'grupo']
        columnas_disponibles = [col.lower().strip() for col in df.columns]
        
        mapeo_columnas = {}
        for col_req in columnas_requeridas:
            for col_disp in columnas_disponibles:
                if col_req in col_disp or col_disp in col_req:
                    mapeo_columnas[col_req] = df.columns[columnas_disponibles.index(col_disp)]
                    break
        
        # Procesar primeras 3 filas
        for index, row in df.head(3).iterrows():
            print(f"\n📋 Procesando fila {index + 1}:")
            
            try:
                nombre = str(row[mapeo_columnas['nombre']]).strip()
                apellido = str(row[mapeo_columnas['apellido']]).strip()
                numero = str(row[mapeo_columnas['numero']]).strip()
                carrera = str(row[mapeo_columnas['carrera']]).strip()
                grupo_nombre = str(row[mapeo_columnas['grupo']]).strip()
                
                print(f"  - Nombre: '{nombre}'")
                print(f"  - Apellido: '{apellido}'")
                print(f"  - Número: '{numero}'")
                print(f"  - Carrera: '{carrera}'")
                print(f"  - Grupo: '{grupo_nombre}'")
                
                # Limpiar número
                numero_limpio = ''.join(filter(str.isdigit, numero))
                print(f"  - Número limpio: '{numero_limpio}'")
                
                if not nombre or not numero_limpio:
                    print(f"  ❌ Faltan datos obligatorios")
                else:
                    print(f"  ✅ Datos válidos")
                    
            except Exception as e:
                print(f"  ❌ Error procesando fila: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en procesamiento: {e}")
        return False

def verificar_base_datos():
    """Verificar la base de datos"""
    print(f"\n🗄️  VERIFICANDO BASE DE DATOS")
    print("=" * 40)
    
    try:
        conn = sqlite3.connect('data/database/numeros_whatsapp.db')
        cursor = conn.cursor()
        
        # Verificar tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas = cursor.fetchall()
        print(f"📊 Tablas encontradas: {[t[0] for t in tablas]}")
        
        # Verificar tabla numeros
        cursor.execute("SELECT COUNT(*) FROM numeros")
        total_contactos = cursor.fetchone()[0]
        print(f"👥 Total contactos: {total_contactos}")
        
        # Verificar tabla grupos
        cursor.execute("SELECT COUNT(*) FROM grupos")
        total_grupos = cursor.fetchone()[0]
        print(f"👥 Total grupos: {total_grupos}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 DIAGNÓSTICO DE IMPORTACIÓN EXCEL - CHAT MASIVO")
    print("=" * 60)
    
    try:
        # Verificar dependencias
        if not verificar_dependencias():
            print("\n❌ Faltan dependencias necesarias")
            return False
        
        # Crear archivo de prueba
        archivo_prueba = crear_archivo_excel_prueba()
        if not archivo_prueba:
            print("\n❌ No se pudo crear archivo de prueba")
            return False
        
        # Probar lectura
        if not probar_lectura_excel(archivo_prueba):
            print("\n❌ Error en lectura de Excel")
            return False
        
        # Probar mapeo
        if not probar_mapeo_columnas(archivo_prueba):
            print("\n❌ Error en mapeo de columnas")
            return False
        
        # Probar procesamiento
        if not probar_procesamiento_filas(archivo_prueba):
            print("\n❌ Error en procesamiento de filas")
            return False
        
        # Verificar base de datos
        if not verificar_base_datos():
            print("\n❌ Error en base de datos")
            return False
        
        print("\n🎉 ¡DIAGNÓSTICO COMPLETADO EXITOSAMENTE!")
        print("=" * 60)
        print("✅ Todas las funciones de importación están funcionando")
        print("✅ El problema puede estar en la interfaz web o en el archivo específico")
        print("\n💡 RECOMENDACIONES:")
        print("1. Verifica que el archivo Excel tenga las columnas correctas")
        print("2. Asegúrate de que no haya caracteres especiales en los datos")
        print("3. Revisa los logs de la aplicación para más detalles")
        
        # Limpiar archivo de prueba
        if os.path.exists(archivo_prueba):
            os.remove(archivo_prueba)
            print(f"\n🧹 Archivo de prueba eliminado: {archivo_prueba}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error durante el diagnóstico: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()

