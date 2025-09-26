#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para enviar mensajes a cualquier número (requiere cuenta paga)
"""

from twilio.rest import Client
from dotenv import load_dotenv
import os
import sqlite3

def main():
    print("=" * 70)
    print("📱 ENVÍO A CUALQUIER NÚMERO - CUENTA PAGA REQUERIDA")
    print("=" * 70)
    
    # Cargar configuración
    load_dotenv('Twilio.env')
    client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    
    # Verificar tipo de cuenta
    try:
        account = client.api.accounts(os.getenv('TWILIO_ACCOUNT_SID')).fetch()
        print(f"📊 TIPO DE CUENTA: {account.type.upper()}")
        
        if account.type == 'Trial':
            print("\n❌ CUENTA TRIAL DETECTADA")
            print("=" * 70)
            print("Para enviar a cualquier número necesitas:")
            print("1. 💳 Actualizar a cuenta paga")
            print("2. 🌐 Ve a: https://console.twilio.com/us1/account/billing")
            print("3. 🔑 Agrega tu tarjeta de crédito")
            print("4. ✅ Tu cuenta se actualiza automáticamente")
            print("\n💰 Costos muy bajos:")
            print("   • WhatsApp: ~$0.005 por mensaje")
            print("   • 1000 mensajes = $5.00")
            print("   • 10000 mensajes = $50.00")
            return
        
        print("✅ Cuenta paga detectada - Puedes enviar a cualquier número")
        
    except Exception as e:
        print(f"❌ Error verificando cuenta: {e}")
        return
    
    # Lista de números para enviar
    numeros_destino = [
        '+51914649592',  # Número verificado
        '+51970088333',  # Número no verificado
        # Agrega más números aquí
    ]
    
    print(f"\n📋 NÚMEROS A ENVIAR: {len(numeros_destino)}")
    for i, numero in enumerate(numeros_destino, 1):
        print(f"   {i}. {numero}")
    
    # Crear mensaje personalizado
    mensaje_base = """¡Hola! 👋

🎓 ¡Descubre tu futuro profesional con nosotros!

✨ Te invitamos a conocer nuestros programas académicos y las oportunidades que tenemos para ti.

📚 Programas disponibles:
• Ingeniería de Sistemas
• Administración de Empresas
• Psicología
• Y muchos más...

🏫 Universidad Continental
📍 Ubicación: Lima, Perú

¿Te interesa conocer más? ¡Contáctanos!

---
Este es un mensaje del sistema de chat masivo."""
    
    print(f"\n📝 MENSAJE A ENVIAR:")
    print(f"   {mensaje_base[:100]}...")
    
    # Confirmar envío
    print(f"\n⚠️ ¿CONFIRMAR ENVÍO?")
    print(f"   • Números: {len(numeros_destino)}")
    print(f"   • Costo estimado: ${len(numeros_destino) * 0.005:.3f}")
    print(f"   • Presiona Enter para continuar o Ctrl+C para cancelar")
    
    try:
        input()
    except KeyboardInterrupt:
        print("\n❌ Envío cancelado")
        return
    
    # Enviar mensajes
    print(f"\n🚀 ENVIANDO MENSAJES...")
    exitosos = 0
    fallidos = 0
    
    for i, numero in enumerate(numeros_destino, 1):
        try:
            print(f"\n📱 [{i}/{len(numeros_destino)}] Enviando a {numero}...")
            
            # Personalizar mensaje
            mensaje_personalizado = mensaje_base.replace("¡Hola!", f"¡Hola! {numero}")
            
            # Enviar mensaje
            message = client.messages.create(
                body=mensaje_personalizado,
                from_=os.getenv('TWILIO_WHATSAPP_FROM'),
                to=f"whatsapp:{numero}"
            )
            
            print(f"✅ Enviado exitosamente")
            print(f"   SID: {message.sid}")
            print(f"   Status: {message.status}")
            
            # Registrar en base de datos
            try:
                conn = sqlite3.connect('numeros_whatsapp.db')
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO mensajes_log (telefono, mensaje, estado, fecha_envio, sid_twilio)
                    VALUES (?, ?, ?, datetime('now'), ?)
                ''', (numero.replace('+', ''), mensaje_personalizado, 'enviado', message.sid))
                
                conn.commit()
                conn.close()
                
            except Exception as e:
                print(f"⚠️ Error registrando en BD: {e}")
            
            exitosos += 1
            
        except Exception as e:
            print(f"❌ Error enviando a {numero}: {e}")
            fallidos += 1
    
    # Resumen final
    print(f"\n" + "=" * 70)
    print(f"📊 RESUMEN DEL ENVÍO")
    print(f"=" * 70)
    print(f"✅ Exitosos: {exitosos}")
    print(f"❌ Fallidos: {fallidos}")
    print(f"📱 Total: {len(numeros_destino)}")
    print(f"💰 Costo estimado: ${exitosos * 0.005:.3f}")
    
    if exitosos > 0:
        print(f"\n🎉 ¡Mensajes enviados exitosamente!")
        print(f"📱 Revisa los WhatsApps para ver los mensajes")
    
    print(f"=" * 70)

if __name__ == "__main__":
    main()

