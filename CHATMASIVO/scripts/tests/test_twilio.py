#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de prueba para verificar las credenciales de Twilio
"""

import os
from dotenv import load_dotenv
from twilio.rest import Client

# Cargar variables de entorno
load_dotenv('Twilio.env')

# Obtener credenciales
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
whatsapp_from = os.getenv('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')

print("=" * 50)
print("PRUEBA DE CREDENCIALES TWILIO")
print("=" * 50)
print(f"Account SID: {account_sid}")
print(f"Auth Token: {auth_token[:10]}...")
print(f"WhatsApp From: {whatsapp_from}")
print("=" * 50)

try:
    # Crear cliente Twilio
    client = Client(account_sid, auth_token)
    
    # Obtener información de la cuenta
    account = client.api.accounts(account_sid).fetch()
    print(f"✅ Cuenta verificada: {account.friendly_name}")
    print(f"✅ Estado: {account.status}")
    print(f"✅ Tipo: {account.type}")
    
    # Probar envío de mensaje (opcional)
    print("\n¿Deseas enviar un mensaje de prueba? (y/n): ", end="")
    respuesta = input().lower()
    
    if respuesta == 'y':
        numero_prueba = input("Ingresa el número de WhatsApp (ej: 51914649592): ")
        
        try:
            message = client.messages.create(
                body="¡Hola! Este es un mensaje de prueba desde tu sistema de Chat Masivo WhatsApp. 🚀",
                from_=whatsapp_from,
                to=f'whatsapp:+{numero_prueba}'
            )
            print(f"✅ Mensaje enviado exitosamente!")
            print(f"✅ SID: {message.sid}")
            print(f"✅ Estado: {message.status}")
        except Exception as e:
            print(f"❌ Error enviando mensaje: {e}")
    
    print("\n✅ Las credenciales de Twilio están configuradas correctamente!")
    
except Exception as e:
    print(f"❌ Error verificando credenciales: {e}")
    print("Verifica que las credenciales sean correctas en el archivo Twilio.env")

print("=" * 50)
