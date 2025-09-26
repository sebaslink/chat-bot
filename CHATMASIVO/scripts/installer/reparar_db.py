import sqlite3
import os

print("Reparando base de datos...")

# Conectar a la base de datos
conn = sqlite3.connect('numeros_whatsapp.db')
cursor = conn.cursor()

# Crear tabla numeros si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS numeros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT DEFAULT "",
        numero TEXT NOT NULL UNIQUE,
        carrera TEXT DEFAULT "",
        activo BOOLEAN DEFAULT 1,
        fecha_agregado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Crear tabla mensajes_log si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS mensajes_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero TEXT NOT NULL,
        mensaje TEXT NOT NULL,
        status TEXT DEFAULT 'pendiente',
        fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        error_msg TEXT DEFAULT NULL
    )
''')

# Verificar y agregar columnas faltantes
print("Verificando columnas...")

# Verificar columnas de numeros
cursor.execute("PRAGMA table_info(numeros)")
columns = [column[1] for column in cursor.fetchall()]

if 'apellido' not in columns:
    cursor.execute('ALTER TABLE numeros ADD COLUMN apellido TEXT DEFAULT ""')   
    print("Columna apellido agregada")

if 'carrera' not in columns:
    cursor.execute('ALTER TABLE numeros ADD COLUMN carrera TEXT DEFAULT ""')    
    print("Columna carrera agregada")

# Verificar columnas de mensajes_log
cursor.execute("PRAGMA table_info(mensajes_log)")
columns = [column[1] for column in cursor.fetchall()]

if 'status' not in columns:
    cursor.execute('ALTER TABLE mensajes_log ADD COLUMN status TEXT DEFAULT "pendiente"')
    print("Columna status agregada")

if 'error_msg' not in columns:
    cursor.execute('ALTER TABLE mensajes_log ADD COLUMN error_msg TEXT DEFAULT NULL')
    print("Columna error_msg agregada")

# Confirmar cambios
conn.commit()
conn.close()

print("Base de datos reparada exitosamente")