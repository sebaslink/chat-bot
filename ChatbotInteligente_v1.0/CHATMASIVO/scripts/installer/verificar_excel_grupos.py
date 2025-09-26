#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar que el archivo Excel contiene la columna de grupos
"""

import pandas as pd
import os

def verificar_excel():
    """Verificar que el archivo Excel tiene la columna de grupos"""
    archivo = 'ejemplo_contactos.xlsx'
    
    if not os.path.exists(archivo):
        print(f"❌ El archivo '{archivo}' no existe")
        return False
    
    try:
        # Leer el archivo Excel
        df = pd.read_excel(archivo)
        
        print("🔍 Verificando estructura del archivo Excel...")
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
            print("\n🎉 ¡Todas las columnas requeridas están presentes!")
            
            # Mostrar algunos datos de ejemplo
            print("\n📋 Datos de ejemplo:")
            print(df.head().to_string(index=False))
            
            # Verificar grupos únicos
            if 'grupo' in df.columns:
                grupos_unicos = df['grupo'].unique()
                print(f"\n🏷️ Grupos encontrados: {list(grupos_unicos)}")
                
                # Contar contactos por grupo
                print("\n📊 Distribución por grupos:")
                conteo_grupos = df['grupo'].value_counts()
                for grupo, cantidad in conteo_grupos.items():
                    print(f"   {grupo}: {cantidad} contactos")
            
            return True
        else:
            print("\n❌ Faltan columnas requeridas")
            return False
            
    except Exception as e:
        print(f"❌ Error leyendo el archivo: {e}")
        return False

def main():
    """Función principal"""
    print("🔍 Verificando archivo Excel con grupos...")
    print("=" * 50)
    
    if verificar_excel():
        print("\n✅ Verificación completada exitosamente")
        print("🚀 El archivo está listo para importar contactos con grupos")
    else:
        print("\n❌ La verificación falló")
        print("🔧 Revisa la estructura del archivo Excel")

if __name__ == '__main__':
    main()
