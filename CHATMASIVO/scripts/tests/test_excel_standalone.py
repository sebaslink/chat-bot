#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script independiente para probar la creación de archivos Excel
"""

def test_excel_creation():
    """Probar la creación de archivos Excel"""
    try:
        import pandas as pd
        import io
        import os
        
        print("=" * 60)
        print("PRUEBA DE CREACION DE ARCHIVO EXCEL")
        print("=" * 60)
        
        # Verificar dependencias
        print("1. Verificando dependencias...")
        try:
            import pandas as pd
            print("   ✅ pandas instalado")
        except ImportError:
            print("   ❌ pandas no instalado")
            return False
            
        try:
            import openpyxl
            print("   ✅ openpyxl instalado")
        except ImportError:
            print("   ❌ openpyxl no instalado")
            return False
        
        # Crear datos de ejemplo
        print("\n2. Creando datos de ejemplo...")
        data = {
            'nombre': ['Juan', 'María', 'Carlos', 'Ana', 'Luis'],
            'apellido': ['Pérez', 'González', 'López', 'Martínez', 'Rodríguez'],
            'numero': ['51987654321', '51912345678', '51911223344', '51999887766', '51955443322'],
            'carrera': ['Ingeniería', 'Medicina', 'Derecho', 'Arquitectura', 'Psicología']
        }
        
        df = pd.DataFrame(data)
        print(f"   ✅ DataFrame creado: {len(df)} filas, {len(df.columns)} columnas")
        print(f"   Columnas: {list(df.columns)}")
        
        # Crear archivo Excel
        print("\n3. Creando archivo Excel...")
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Contactos', index=False)
        
        output.seek(0)
        excel_content = output.getvalue()
        
        print(f"   ✅ Archivo Excel creado en memoria")
        print(f"   Tamaño: {len(excel_content)} bytes")
        
        # Guardar archivo
        print("\n4. Guardando archivo...")
        filename = 'plantilla_contactos_test.xlsx'
        
        with open(filename, 'wb') as f:
            f.write(excel_content)
        
        # Verificar archivo guardado
        if os.path.exists(filename):
            file_size = os.path.getsize(filename)
            print(f"   ✅ Archivo guardado: {filename}")
            print(f"   Tamaño: {file_size} bytes")
            
            if file_size > 0:
                print("\n" + "=" * 60)
                print("✅ ¡PRUEBA EXITOSA!")
                print("=" * 60)
                print("✅ El archivo Excel (.xlsx) se creó correctamente")
                print("✅ No es un archivo CSV, es un Excel real")
                print(f"✅ Archivo guardado como: {filename}")
                print("\n💡 Ahora puedes abrir el archivo con Excel o LibreOffice")
                return True
            else:
                print("   ❌ El archivo está vacío")
                return False
        else:
            print("   ❌ No se pudo guardar el archivo")
            return False
            
    except Exception as e:
        print(f"\n❌ Error durante la prueba: {e}")
        print("\n💡 Soluciones posibles:")
        print("   1. Instalar dependencias: pip install pandas openpyxl")
        print("   2. Verificar que Python esté funcionando correctamente")
        return False

if __name__ == "__main__":
    success = test_excel_creation()
    
    if not success:
        print("\n" + "=" * 60)
        print("❌ LA PRUEBA FALLÓ")
        print("=" * 60)
        print("Instala las dependencias necesarias:")
        print("pip install pandas openpyxl")
    else:
        print("\n🎉 ¡Todo funcionando correctamente!")
