#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os

print("🔍 PROBANDO IMPORTACIÓN EXCEL")
print("=" * 40)

# Crear datos de prueba
datos = {
    'nombre': ['Juan', 'María', 'Carlos'],
    'apellido': ['Pérez', 'García', 'López'],
    'numero': ['51987654321', '51987654322', '51987654323'],
    'carrera': ['Ingeniería', 'Medicina', 'Derecho'],
    'grupo': ['Grupo A', 'Grupo B', 'Grupo A']
}

print("📝 Creando DataFrame...")
df = pd.DataFrame(datos)
print(f"✅ DataFrame creado: {len(df)} filas")

print("📋 Columnas:", list(df.columns))

print("💾 Guardando Excel...")
archivo = 'test_simple.xlsx'
df.to_excel(archivo, index=False)
print(f"✅ Archivo guardado: {archivo}")

print("📖 Leyendo Excel...")
df_leido = pd.read_excel(archivo)
print(f"✅ Archivo leído: {len(df_leido)} filas")

print("📋 Primeras filas:")
print(df_leido.head())

# Limpiar
if os.path.exists(archivo):
    os.remove(archivo)
    print(f"🧹 Archivo eliminado: {archivo}")

print("🎉 ¡Prueba completada!")

