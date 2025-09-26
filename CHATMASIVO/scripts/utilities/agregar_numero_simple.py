#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script simple para agregar número a Twilio
"""

from twilio.rest import Client
from dotenv import load_dotenv
import os

def main():
    load_dotenv('Twilio.env')
    client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    
    print("Agregando número +51970088333...")
    
    try:
        # Método directo
        caller_id = client.outgoing_caller_ids.create(phone_number='+51970088333')
        print(f"✅ Número agregado: {caller_id.sid}")
    except Exception as e:
        print(f"❌ Error: {e}")
        
        # Intentar método alternativo
        try:
            print("Intentando método alternativo...")
            caller_id = client.api.outgoing_caller_ids.create(phone_number='+51970088333')
            print(f"✅ Número agregado (método alternativo): {caller_id.sid}")
        except Exception as e2:
            print(f"❌ Error método alternativo: {e2}")
            
            # Mostrar instrucciones manuales
            print("\n📱 INSTRUCCIONES MANUALES:")
            print("1. Ve a: https://console.twilio.com/us1/develop/phone-numbers/manage/verified")
            print("2. Haz clic en 'Add a new number'")
            print("3. Ingresa: +51970088333")
            print("4. Twilio enviará un código de verificación")
            print("5. Ingresa el código para verificar el número")

if __name__ == "__main__":
    main()


