import pandas as pd

# Crear datos de ejemplo
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

# Guardar como Excel
df.to_excel('ejemplo_contactos.xlsx', index=False, sheet_name='Contactos')

print("✅ Archivo 'ejemplo_contactos.xlsx' creado exitosamente")
print("📋 Contiene 10 contactos de ejemplo con los campos requeridos")
print("🚀 Puedes usar este archivo para probar la importación")
