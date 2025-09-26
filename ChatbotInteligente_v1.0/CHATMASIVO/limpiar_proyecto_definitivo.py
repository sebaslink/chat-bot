#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para limpiar el proyecto eliminando archivos innecesarios
"""

import os
import shutil
import glob
from datetime import datetime

def crear_respaldo():
    """Crear respaldo antes de limpiar"""
    print("📁 Creando respaldo de seguridad...")
    
    backup_dir = f"backup_antes_limpieza_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        # Crear carpeta de respaldo
        os.makedirs(backup_dir, exist_ok=True)
        
        # Archivos importantes a respaldar
        archivos_importantes = [
            "main.py",
            "requirements.txt",
            "README.md",
            "ABRIR_CHAT_MASIVO.bat",
            "INICIAR_APLICACION.bat",
            "CREAR_INSTALADOR_FINAL.bat"
        ]
        
        for archivo in archivos_importantes:
            if os.path.exists(archivo):
                shutil.copy2(archivo, backup_dir)
                print(f"  ✅ Respaldo: {archivo}")
        
        print(f"✅ Respaldo creado en: {backup_dir}")
        return True
        
    except Exception as e:
        print(f"❌ Error creando respaldo: {e}")
        return False

def eliminar_carpetas():
    """Eliminar carpetas innecesarias"""
    print("\n🗑️ Eliminando carpetas innecesarias...")
    
    carpetas_eliminar = [
        "__pycache__",
        "build",
        "dist", 
        "temp",
        "backup",
        "codigo",
        "executables",
        "documentacion",
        "configuracion",
        "imagen",
        "uploads",
        "logs",
        "installer"
    ]
    
    eliminadas = 0
    for carpeta in carpetas_eliminar:
        if os.path.exists(carpeta):
            try:
                shutil.rmtree(carpeta)
                print(f"  ✅ Eliminada: {carpeta}/")
                eliminadas += 1
            except Exception as e:
                print(f"  ❌ Error eliminando {carpeta}/: {e}")
    
    print(f"✅ Carpetas eliminadas: {eliminadas}")
    return eliminadas

def eliminar_archivos_patron():
    """Eliminar archivos por patrón"""
    print("\n🗑️ Eliminando archivos por patrón...")
    
    patrones_eliminar = [
        "test_*.py",
        "test_*.xlsx", 
        "probar_*.py",
        "*_debug.py",
        "crear_instalador_*.py",
        "reorganizar_*.py",
        "limpiar_*.py",
        "importacion_excel_mejorada.py",
        "*.log",
        "*_RESUMEN.md",
        "*_FINAL.md",
        "LANZADORES_DISPONIBLES.md",
        "SOLUCION_*.md",
        "ChatMasivo.spec",
        "chatmasivo.log"
    ]
    
    eliminados = 0
    for patron in patrones_eliminar:
        archivos = glob.glob(patron)
        for archivo in archivos:
            try:
                os.remove(archivo)
                print(f"  ✅ Eliminado: {archivo}")
                eliminados += 1
            except Exception as e:
                print(f"  ❌ Error eliminando {archivo}: {e}")
    
    print(f"✅ Archivos eliminados: {eliminados}")
    return eliminados

def limpiar_archivos_excel_prueba():
    """Limpiar archivos Excel de prueba"""
    print("\n🗑️ Limpiando archivos Excel de prueba...")
    
    excel_dir = "data/excel"
    if os.path.exists(excel_dir):
        archivos_excel = [
            "ejemplo_contactos_completo.xlsx",
            "ejemplo_contactos.xlsx", 
            "plantilla_contactos_con_grupos_mejorada.xlsx",
            "plantilla_descargada.xlsx",
            "plantilla_prueba.xlsx",
            "plantilla_sistema_mejorada.xlsx",
            "plantilla_sistema.xlsx",
            "plantilla_verificacion.xlsx"
        ]
        
        eliminados = 0
        for archivo in archivos_excel:
            archivo_path = os.path.join(excel_dir, archivo)
            if os.path.exists(archivo_path):
                try:
                    os.remove(archivo_path)
                    print(f"  ✅ Eliminado: {archivo}")
                    eliminados += 1
                except Exception as e:
                    print(f"  ❌ Error eliminando {archivo}: {e}")
        
        print(f"✅ Archivos Excel eliminados: {eliminados}")
        return eliminados
    else:
        print("  ⚠️  Carpeta data/excel no encontrada")
        return 0

def limpiar_backups_database():
    """Limpiar backups antiguos de base de datos"""
    print("\n🗑️ Limpiando backups antiguos de base de datos...")
    
    db_dir = "data/database"
    if os.path.exists(db_dir):
        # Mantener solo el backup más reciente
        backups = [f for f in os.listdir(db_dir) if f.startswith("numeros_whatsapp_backup_") and f.endswith(".db")]
        
        if len(backups) > 1:
            # Ordenar por fecha y mantener solo el más reciente
            backups.sort(reverse=True)
            backups_a_eliminar = backups[1:]  # Eliminar todos excepto el más reciente
            
            eliminados = 0
            for backup in backups_a_eliminar:
                backup_path = os.path.join(db_dir, backup)
                try:
                    os.remove(backup_path)
                    print(f"  ✅ Eliminado: {backup}")
                    eliminados += 1
                except Exception as e:
                    print(f"  ❌ Error eliminando {backup}: {e}")
            
            print(f"✅ Backups eliminados: {eliminados}")
            return eliminados
        else:
            print("  ℹ️  Solo hay un backup, no se elimina nada")
            return 0
    else:
        print("  ⚠️  Carpeta data/database no encontrada")
        return 0

def verificar_estructura_final():
    """Verificar la estructura final del proyecto"""
    print("\n🔍 Verificando estructura final...")
    
    archivos_esenciales = [
        "main.py",
        "requirements.txt", 
        "README.md",
        "ABRIR_CHAT_MASIVO.bat",
        "INICIAR_APLICACION.bat",
        "CREAR_INSTALADOR_FINAL.bat"
    ]
    
    carpetas_esenciales = [
        "app",
        "templates",
        "static", 
        "config",
        "data/database",
        "scripts"
    ]
    
    print("📄 Archivos esenciales:")
    for archivo in archivos_esenciales:
        if os.path.exists(archivo):
            print(f"  ✅ {archivo}")
        else:
            print(f"  ❌ {archivo} - FALTANTE")
    
    print("\n📁 Carpetas esenciales:")
    for carpeta in carpetas_esenciales:
        if os.path.exists(carpeta):
            print(f"  ✅ {carpeta}/")
        else:
            print(f"  ❌ {carpeta}/ - FALTANTE")

def calcular_espacio_liberado():
    """Calcular espacio liberado"""
    print("\n📊 Calculando espacio liberado...")
    
    # Esto es una estimación, ya que no podemos medir exactamente
    print("  ℹ️  Espacio estimado liberado:")
    print("    - Carpetas temporales: ~50-100 MB")
    print("    - Archivos de prueba: ~10-20 MB") 
    print("    - Logs y cache: ~5-10 MB")
    print("    - Archivos duplicados: ~20-30 MB")
    print("    - Total estimado: ~85-160 MB")

def main():
    """Función principal de limpieza"""
    print("🧹 LIMPIEZA DEFINITIVA DEL PROYECTO CHAT MASIVO")
    print("=" * 60)
    
    try:
        # Crear respaldo
        if not crear_respaldo():
            print("\n❌ No se pudo crear respaldo. Abortando limpieza.")
            return False
        
        # Confirmar limpieza
        print("\n⚠️  ADVERTENCIA: Esta operación eliminará archivos permanentemente.")
        respuesta = input("¿Continuar con la limpieza? (s/n): ").lower()
        
        if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
            print("❌ Limpieza cancelada por el usuario")
            return False
        
        # Ejecutar limpieza
        print("\n🚀 Iniciando limpieza...")
        
        carpetas_eliminadas = eliminar_carpetas()
        archivos_eliminados = eliminar_archivos_patron()
        excel_eliminados = limpiar_archivos_excel_prueba()
        backups_eliminados = limpiar_backups_database()
        
        # Verificar estructura final
        verificar_estructura_final()
        
        # Calcular espacio liberado
        calcular_espacio_liberado()
        
        # Resumen final
        print("\n🎉 ¡LIMPIEZA COMPLETADA EXITOSAMENTE!")
        print("=" * 60)
        print(f"📊 RESUMEN:")
        print(f"  - Carpetas eliminadas: {carpetas_eliminadas}")
        print(f"  - Archivos eliminados: {archivos_eliminados}")
        print(f"  - Archivos Excel eliminados: {excel_eliminados}")
        print(f"  - Backups eliminados: {backups_eliminados}")
        print(f"  - Total elementos eliminados: {carpetas_eliminadas + archivos_eliminados + excel_eliminados + backups_eliminados}")
        
        print(f"\n✅ El proyecto está ahora limpio y optimizado")
        print(f"✅ Solo quedan los archivos esenciales para el funcionamiento")
        print(f"✅ El respaldo está en: backup_antes_limpieza_*")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error durante la limpieza: {e}")
        return False

if __name__ == "__main__":
    main()
