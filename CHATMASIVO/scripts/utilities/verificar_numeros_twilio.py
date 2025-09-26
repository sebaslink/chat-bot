#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para verificar y agregar números a la lista permitida de Twilio
"""

from twilio.rest import Client
from dotenv import load_dotenv
import os

def main():
    # Cargar configuración
    load_dotenv('Twilio.env')
    client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    
    print("=" * 60)
    print("🔍 VERIFICANDO NÚMEROS EN TWILIO")
    print("=" * 60)
    
    # Números que queremos verificar
    numeros = ['+51914649592', '+51970088333']
    
    # Verificar números existentes
    print("\n📋 NÚMEROS ACTUALMENTE PERMITIDOS:")
    try:
        caller_ids = client.outgoing_caller_ids.list()
        if caller_ids:
            for caller_id in caller_ids:
                print(f"✅ {caller_id.phone_number}")
        else:
            print("❌ No hay números permitidos")
    except Exception as e:
        print(f"❌ Error obteniendo números: {e}")
    
    # Intentar agregar números usando la API correcta
    print("\n➕ AGREGANDO NÚMEROS A LA LISTA PERMITIDA:")
    for numero in numeros:
        try:
            print(f"Intentando agregar {numero}...")
            caller_id = client.outgoing_caller_ids.create(phone_number=numero)
            print(f"✅ {numero} agregado exitosamente")
            print(f"   SID: {caller_id.sid}")
        except Exception as e:
            print(f"❌ Error agregando {numero}: {e}")
            if "already exists" in str(e).lower():
                print(f"   ℹ️ El número {numero} ya está en la lista")
            elif "not verified" in str(e).lower():
                print(f"   ⚠️ El número {numero} necesita verificación")
                print(f"   📱 Twilio enviará un código de verificación a {numero}")
    
    print("\n" + "=" * 60)
    print("💡 INSTRUCCIONES:")
    print("=" * 60)
    print("1. Si aparecen códigos de verificación, ingrésalos en:")
    print("   https://console.twilio.com/us1/develop/phone-numbers/manage/verified")
    print("2. Una vez verificados, los números podrán recibir mensajes")
    print("3. Para cuentas Trial, solo puedes enviar a números verificados")
    print("4. Para enviar a cualquier número, necesitas actualizar a cuenta paga")
    print("=" * 60)

if __name__ == "__main__":
    main()
