#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para verificar números en cuenta Trial de Twilio
"""

from twilio.rest import Client
from dotenv import load_dotenv
import os
import webbrowser

def main():
    load_dotenv('Twilio.env')
    client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    
    print("=" * 70)
    print("🆓 VERIFICACIÓN DE NÚMEROS - CUENTA TRIAL TWILIO")
    print("=" * 70)
    
    # Verificar números actuales
    print("\n📋 NÚMEROS ACTUALMENTE PERMITIDOS:")
    try:
        caller_ids = client.outgoing_caller_ids.list()
        if caller_ids:
            for caller_id in caller_ids:
                print(f"✅ {caller_id.phone_number}")
        else:
            print("❌ No hay números permitidos")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("📱 INSTRUCCIONES PARA AGREGAR NÚMEROS:")
    print("=" * 70)
    print("1. 🌐 Abre tu navegador en:")
    print("   https://console.twilio.com/us1/develop/phone-numbers/manage/verified")
    print("\n2. 🔑 Inicia sesión con tu cuenta de Twilio")
    print("\n3. ➕ Haz clic en 'Add a new number'")
    print("\n4. 📞 Ingresa los números que quieres verificar:")
    print("   • +51914649592")
    print("   • +51970088333")
    print("\n5. 📱 Twilio enviará un código SMS a cada número")
    print("\n6. 🔢 Ingresa el código en la página web")
    print("\n7. ✅ Una vez verificados, podrás enviar mensajes")
    
    print("\n" + "=" * 70)
    print("🚀 ABRIENDO PÁGINA DE VERIFICACIÓN...")
    print("=" * 70)
    
    # Abrir la página de verificación
    try:
        webbrowser.open("https://console.twilio.com/us1/develop/phone-numbers/manage/verified")
        print("✅ Página abierta en tu navegador")
    except:
        print("❌ No se pudo abrir automáticamente")
        print("   Copia y pega este enlace:")
        print("   https://console.twilio.com/us1/develop/phone-numbers/manage/verified")
    
    print("\n" + "=" * 70)
    print("💡 INFORMACIÓN IMPORTANTE:")
    print("=" * 70)
    print("• 🆓 Cuenta Trial: Solo puede enviar a números verificados")
    print("• 📱 Verificación: Requiere código SMS enviado por Twilio")
    print("• ⏱️ Tiempo: El proceso toma 1-2 minutos por número")
    print("• 🔄 Una vez verificado, funciona inmediatamente")
    print("• 💰 Gratis: No cuesta nada verificar números")
    print("=" * 70)

if __name__ == "__main__":
    main()

