#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para mostrar opciones de envío masivo
"""

from twilio.rest import Client
from dotenv import load_dotenv
import os
import webbrowser

def main():
    print("=" * 70)
    print("📱 OPCIONES PARA ENVÍO MASIVO DE WHATSAPP")
    print("=" * 70)
    
    # Cargar configuración
    load_dotenv('Twilio.env')
    client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    
    # Verificar tipo de cuenta
    try:
        account = client.api.accounts(os.getenv('TWILIO_ACCOUNT_SID')).fetch()
        print(f"📊 TIPO DE CUENTA: {account.type.upper()}")
        print(f"💰 Estado: {account.status}")
        print(f"🏢 Nombre: {account.friendly_name}")
        
        if account.type == 'Trial':
            print("\n" + "=" * 70)
            print("🆓 OPCIÓN 1: MANTENER CUENTA GRATUITA")
            print("=" * 70)
            print("✅ Ventajas:")
            print("   • Completamente gratis")
            print("   • No requiere tarjeta de crédito")
            print("   • Ideal para pruebas y desarrollo")
            
            print("\n❌ Limitaciones:")
            print("   • Solo puede enviar a números verificados")
            print("   • Máximo 1 número verificado por defecto")
            print("   • Proceso manual para cada número")
            
            print("\n📱 Cómo agregar números:")
            print("   1. Ve a: https://console.twilio.com/us1/develop/phone-numbers/manage/verified")
            print("   2. Haz clic en 'Add a new number'")
            print("   3. Ingresa el número")
            print("   4. Twilio envía código SMS")
            print("   5. Ingresa el código")
            print("   6. ¡Listo! El número puede recibir mensajes")
            
            print("\n" + "=" * 70)
            print("💳 OPCIÓN 2: ACTUALIZAR A CUENTA PAGA")
            print("=" * 70)
            print("✅ Ventajas:")
            print("   • Enviar a CUALQUIER número")
            print("   • Sin restricciones de verificación")
            print("   • Envío masivo ilimitado")
            print("   • Mejor para uso comercial")
            
            print("\n💰 Costos:")
            print("   • WhatsApp: ~$0.005 por mensaje")
            print("   • SMS: ~$0.0075 por mensaje")
            print("   • Llamadas: ~$0.013 por minuto")
            print("   • Solo pagas por lo que usas")
            
            print("\n📊 Ejemplo de costos:")
            print("   • 100 mensajes WhatsApp = $0.50")
            print("   • 1000 mensajes WhatsApp = $5.00")
            print("   • 10000 mensajes WhatsApp = $50.00")
            
            print("\n🔧 Cómo actualizar:")
            print("   1. Ve a: https://console.twilio.com/us1/account/billing")
            print("   2. Haz clic en 'Add Payment Method'")
            print("   3. Agrega tu tarjeta de crédito")
            print("   4. ¡Listo! Tu cuenta se actualiza automáticamente")
            
        else:
            print("\n✅ ¡Ya tienes cuenta paga!")
            print("   Puedes enviar a cualquier número sin restricciones")
            
    except Exception as e:
        print(f"❌ Error verificando cuenta: {e}")
    
    print("\n" + "=" * 70)
    print("🎯 RECOMENDACIÓN")
    print("=" * 70)
    print("Para envío masivo comercial:")
    print("1. 💳 Actualiza a cuenta paga (recomendado)")
    print("2. 📱 Usa el sistema actual sin restricciones")
    print("3. 💰 Los costos son muy bajos")
    
    print("\nPara pruebas y desarrollo:")
    print("1. 🆓 Mantén cuenta gratuita")
    print("2. 📱 Verifica números manualmente")
    print("3. 🔄 Ideal para pocos contactos")
    
    print("\n" + "=" * 70)
    print("🚀 ACCIONES RÁPIDAS")
    print("=" * 70)
    print("¿Qué quieres hacer?")
    print("1. 🌐 Abrir página de verificación de números")
    print("2. 💳 Abrir página de facturación para actualizar cuenta")
    print("3. 📊 Ver estado actual de números")
    print("4. 📱 Enviar mensaje de prueba")
    
    # Abrir páginas relevantes
    try:
        print("\n🌐 Abriendo páginas relevantes...")
        webbrowser.open("https://console.twilio.com/us1/develop/phone-numbers/manage/verified")
        webbrowser.open("https://console.twilio.com/us1/account/billing")
        print("✅ Páginas abiertas en tu navegador")
    except:
        print("❌ No se pudieron abrir las páginas automáticamente")
        print("   Copia y pega estos enlaces:")
        print("   • Verificación: https://console.twilio.com/us1/develop/phone-numbers/manage/verified")
        print("   • Facturación: https://console.twilio.com/us1/account/billing")
    
    print("\n" + "=" * 70)
    print("💡 INFORMACIÓN ADICIONAL")
    print("=" * 70)
    print("• 🆓 Cuenta Trial: Ideal para desarrollo y pruebas")
    print("• 💳 Cuenta Paga: Necesaria para uso comercial")
    print("• 📱 WhatsApp: Requiere número de Twilio aprobado")
    print("• 🔒 Seguridad: Twilio es muy seguro y confiable")
    print("• 🌍 Global: Funciona en todo el mundo")
    print("=" * 70)

if __name__ == "__main__":
    main()

