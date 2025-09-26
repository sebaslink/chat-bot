#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para verificar números en cuenta Trial de Twilio (GRATUITA)
"""

from twilio.rest import Client
from dotenv import load_dotenv
import os
import time

def main():
    load_dotenv('Twilio.env')
    client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    
    print("=" * 60)
    print("🆓 VERIFICACIÓN DE NÚMEROS - CUENTA TRIAL GRATUITA")
    print("=" * 60)
    
    # Números que queremos verificar
    numeros = ['+51914649592', '+51970088333']
    
    print("\n📋 NÚMEROS ACTUALMENTE VERIFICADOS:")
    try:
        caller_ids = client.outgoing_caller_ids.list()
        if caller_ids:
            for caller_id in caller_ids:
                print(f"✅ {caller_id.phone_number}")
        else:
            print("❌ No hay números verificados")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n➕ AGREGANDO NÚMEROS A VERIFICAR:")
    for numero in numeros:
        try:
            print(f"\n📱 Procesando {numero}...")
            
            # Intentar agregar el número
            caller_id = client.outgoing_caller_ids.create(phone_number=numero)
            print(f"✅ {numero} agregado para verificación")
            print(f"   SID: {caller_id.sid}")
            
            # Esperar un poco
            time.sleep(2)
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error con {numero}: {error_msg}")
            
            if "already exists" in error_msg.lower():
                print(f"   ℹ️ {numero} ya está en la lista")
            elif "not verified" in error_msg.lower():
                print(f"   ⚠️ {numero} necesita verificación")
                print(f"   📱 Twilio enviará un código a {numero}")
            elif "invalid" in error_msg.lower():
                print(f"   ❌ {numero} no es un número válido")
            else:
                print(f"   ❌ Error desconocido: {error_msg}")
    
    print("\n" + "=" * 60)
    print("📱 INSTRUCCIONES PARA VERIFICAR NÚMEROS:")
    print("=" * 60)
    print("1. Ve a: https://console.twilio.com/us1/develop/phone-numbers/manage/verified")
    print("2. Busca los números que agregamos arriba")
    print("3. Para cada número:")
    print("   - Haz clic en 'Verify'")
    print("   - Twilio enviará un código SMS al número")
    print("   - Ingresa el código que recibas")
    print("   - El número quedará verificado")
    print("\n4. Una vez verificados, podrás enviar mensajes a esos números")
    print("5. Con cuenta Trial solo puedes enviar a números verificados")
    print("=" * 60)
    
    print("\n💡 ALTERNATIVA - USAR NÚMEROS MÁGICOS DE TWILIO:")
    print("Para pruebas, puedes usar estos números mágicos que siempre funcionan:")
    numeros_magicos = [
        "+15005550006",
        "+15005550001", 
        "+15005550002",
        "+15005550003",
        "+15005550004",
        "+15005550005"
    ]
    
    for num in numeros_magicos:
        print(f"   📱 {num}")
    
    print("\n¿Quieres que agregue estos números mágicos a tu base de datos?")
    respuesta = input("Escribe 'si' para agregarlos: ").lower().strip()
    
    if respuesta == 'si':
        agregar_numeros_magicos()

def agregar_numeros_magicos():
    """Agregar números mágicos de Twilio a la base de datos"""
    import sqlite3
    
    print("\n🔮 AGREGANDO NÚMEROS MÁGICOS DE TWILIO...")
    
    numeros_magicos = [
        ("Twilio", "Magic", "15005550006", "Prueba"),
        ("Twilio", "Magic2", "15005550001", "Prueba"),
        ("Twilio", "Magic3", "15005550002", "Prueba")
    ]
    
    try:
        conn = sqlite3.connect('numeros_whatsapp.db')
        cursor = conn.cursor()
        
        for nombre, apellido, telefono, carrera in numeros_magicos:
            cursor.execute('''
                INSERT OR REPLACE INTO numeros (nombre, apellido, telefono, carrera, activo)
                VALUES (?, ?, ?, ?, ?)
            ''', (nombre, apellido, telefono, carrera, 1))
            print(f"✅ {nombre} {apellido} ({telefono}) agregado")
        
        conn.commit()
        conn.close()
        print("\n🎉 Números mágicos agregados exitosamente!")
        print("Ahora puedes enviar mensajes de prueba a estos números")
        
    except Exception as e:
        print(f"❌ Error agregando números mágicos: {e}")

if __name__ == "__main__":
    main()


