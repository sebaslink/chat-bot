#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para enviar mensajes solo a números verificados
"""

import requests
import time

def main():
    print("=" * 60)
    print("📱 ENVIANDO MENSAJES A NÚMEROS VERIFICADOS")
    print("=" * 60)
    
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get('http://localhost:5000', timeout=5)
        if response.status_code == 200:
            print("✅ Servidor funcionando correctamente")
        else:
            print("❌ Servidor no responde correctamente")
            return
    except:
        print("❌ Servidor no está corriendo")
        print("   Ejecuta: .\\ABRIR_CHAT_MASIVO.bat")
        return
    
    # Datos del mensaje
    mensaje_data = {
        'intro': 'Hola',
        'texto_random': 'Mensaje de prueba del sistema',
        'texto_fijo': 'Este es un mensaje de prueba del sistema de chat masivo.'
    }
    
    print(f"\n📝 Enviando mensaje personalizado...")
    print(f"   Intro: {mensaje_data['intro']}")
    print(f"   Texto: {mensaje_data['texto_random']}")
    print(f"   Fijo: {mensaje_data['texto_fijo']}")
    
    try:
        # Enviar mensaje
        response = requests.post(
            'http://localhost:5000/enviar_masivo', 
            data=mensaje_data, 
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Mensaje enviado exitosamente")
            print(f"   Respuesta: {response.status_code}")
        else:
            print(f"❌ Error enviando mensaje: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("📋 PRÓXIMOS PASOS:")
    print("=" * 60)
    print("1. ✅ El mensaje se envió solo a números verificados")
    print("2. 📱 Revisa tu WhatsApp para ver el mensaje")
    print("3. 🔄 Para agregar más números:")
    print("   • Ve a: https://console.twilio.com/us1/develop/phone-numbers/manage/verified")
    print("   • Agrega el número +51970088333")
    print("   • Verifica con el código SMS")
    print("4. 🚀 Una vez verificado, podrás enviar a ambos números")
    print("=" * 60)

if __name__ == "__main__":
    main()

