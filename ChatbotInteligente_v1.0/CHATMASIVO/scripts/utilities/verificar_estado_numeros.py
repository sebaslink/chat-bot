#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para verificar el estado de los números en Twilio
"""

from twilio.rest import Client
from dotenv import load_dotenv
import os

def main():
    load_dotenv('Twilio.env')
    client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    
    print("=" * 60)
    print("🔍 VERIFICANDO ESTADO DE NÚMEROS")
    print("=" * 60)
    
    # Números que queremos verificar
    numeros_deseados = ['+51914649592', '+51970088333']
    
    try:
        # Obtener números permitidos
        caller_ids = client.outgoing_caller_ids.list()
        numeros_permitidos = [caller_id.phone_number for caller_id in caller_ids]
        
        print(f"\n📋 NÚMEROS PERMITIDOS EN TWILIO ({len(numeros_permitidos)}):")
        for numero in numeros_permitidos:
            print(f"✅ {numero}")
        
        print(f"\n🎯 NÚMEROS QUE NECESITAS VERIFICAR:")
        for numero in numeros_deseados:
            if numero in numeros_permitidos:
                print(f"✅ {numero} - YA VERIFICADO")
            else:
                print(f"❌ {numero} - NECESITA VERIFICACIÓN")
        
        # Verificar si podemos enviar mensajes
        numeros_listos = [n for n in numeros_deseados if n in numeros_permitidos]
        
        if numeros_listos:
            print(f"\n🚀 NÚMEROS LISTOS PARA ENVÍO ({len(numeros_listos)}):")
            for numero in numeros_listos:
                print(f"✅ {numero}")
            
            print(f"\n💡 PUEDES ENVIAR MENSAJES A {len(numeros_listos)} NÚMERO(S)")
        else:
            print(f"\n⚠️ NO HAY NÚMEROS LISTOS PARA ENVÍO")
            print("   Necesitas verificar al menos un número")
        
    except Exception as e:
        print(f"❌ Error verificando números: {e}")
    
    print("\n" + "=" * 60)
    print("📱 PARA AGREGAR NÚMEROS:")
    print("=" * 60)
    print("1. Ve a: https://console.twilio.com/us1/develop/phone-numbers/manage/verified")
    print("2. Haz clic en 'Add a new number'")
    print("3. Ingresa el número que quieres verificar")
    print("4. Twilio enviará un código SMS")
    print("5. Ingresa el código para verificar")
    print("6. Ejecuta este script nuevamente para verificar")
    print("=" * 60)

if __name__ == "__main__":
    main()

