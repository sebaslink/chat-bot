#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

# Crear datos de ejemplo con grupos
data = {
    'nombre': ['Juan', 'María', 'Carlos'],
    'apellido': ['Pérez', 'González', 'López'],
    'numero': ['51987654321', '51912345678', '51911223344'],
    'carrera': ['Ingeniería de Sistemas', 'Medicina', 'Derecho'],
    'grupo': ['Ingeniería', 'Medicina', 'Derecho']
}

# Crear DataFrame
df = pd.DataFrame(data)

# Guardar como Excel
df.to_excel('plantilla_verificacion.xlsx', index=False)

print("Archivo Excel creado con columnas:")
print(list(df.columns))

print("\nDatos:")
print(df)

print("\nGrupos incluidos:")
print(df['grupo'].unique())
