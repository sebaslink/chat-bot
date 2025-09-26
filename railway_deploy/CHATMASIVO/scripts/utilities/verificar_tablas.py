import sqlite3

conn = sqlite3.connect('numeros_whatsapp.db')
cursor = conn.cursor()

# Verificar tablas existentes
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tablas existentes:", tables)

# Verificar estructura de numeros
cursor.execute("PRAGMA table_info(numeros)")
columns = cursor.fetchall()
print("Columnas en numeros:", columns)

# Verificar estructura de mensajes_log
cursor.execute("PRAGMA table_info(mensajes_log)")
columns = cursor.fetchall()
print("Columnas en mensajes_log:", columns)

conn.close()
