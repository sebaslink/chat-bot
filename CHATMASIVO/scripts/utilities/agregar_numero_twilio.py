#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para agregar un número específico a la lista permitida de Twilio
"""

from twilio.rest import Client
from dotenv import load_dotenv
import os

def main():
    # Cargar configuración
    load_dotenv('Twilio.env')
    client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    
    print("=" * 60)
    print("📱 AGREGANDO NÚMERO A TWILIO")
    print("=" * 60)
    
    # Número a agregar
    numero = '+51970088333'
    
    try:
        print(f"Agregando {numero} a la lista permitida...")
        
        # Usar la API correcta para agregar números
        caller_id = client.outgoing_caller_ids.create(phone_number=numero)
        
        print(f"✅ {numero} agregado exitosamente!")
        print(f"   SID: {caller_id.sid}")
        print(f"   Status: {getattr(caller_id, 'status', 'Pendiente de verificación')}")
        
        print("\n📱 VERIFICACIÓN REQUERIDA:")
        print(f"Twilio enviará un código de verificación a {numero}")
        print("Ingresa el código en: https://console.twilio.com/us1/develop/phone-numbers/manage/verified")
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error: {error_msg}")
        
        if "already exists" in error_msg.lower():
            print(f"ℹ️ El número {numero} ya está en la lista")
        elif "not verified" in error_msg.lower():
            print(f"⚠️ El número {numero} necesita verificación")
            print(f"📱 Twilio enviará un código de verificación a {numero}")
        elif "invalid" in error_msg.lower():
            print(f"❌ El número {numero} no es válido")
        else:
            print(f"❌ Error desconocido: {error_msg}")
    
    print("\n" + "=" * 60)
    print("💡 INFORMACIÓN IMPORTANTE:")
    print("=" * 60)
    print("• Las cuentas Trial de Twilio solo pueden enviar a números verificados")
    print("• Una vez verificado, el número podrá recibir mensajes")
    print("• Para enviar a cualquier número, actualiza a cuenta paga")
    print("=" * 60)

if __name__ == "__main__":
    main()
