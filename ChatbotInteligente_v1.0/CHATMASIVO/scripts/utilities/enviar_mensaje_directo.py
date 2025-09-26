#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para enviar mensaje directamente usando Twilio
"""

from twilio.rest import Client
from dotenv import load_dotenv
import os
import sqlite3

def main():
    print("=" * 60)
    print("📱 ENVIANDO MENSAJE DIRECTO A NÚMERO VERIFICADO")
    print("=" * 60)
    
    # Cargar configuración
    load_dotenv('Twilio.env')
    client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    
    # Obtener número verificado
    try:
        caller_ids = client.outgoing_caller_ids.list()
        numeros_verificados = [caller_id.phone_number for caller_id in caller_ids]
        
        if not numeros_verificados:
            print("❌ No hay números verificados")
            return
        
        print(f"✅ Números verificados encontrados: {len(numeros_verificados)}")
        for numero in numeros_verificados:
            print(f"   📱 {numero}")
        
        # Usar el primer número verificado
        numero_destino = numeros_verificados[0]
        print(f"\n🎯 Enviando a: {numero_destino}")
        
    except Exception as e:
        print(f"❌ Error obteniendo números: {e}")
        return
    
    # Crear mensaje personalizado
    mensaje = f"""¡Hola! 👋

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
Este es un mensaje de prueba del sistema de chat masivo."""
    
    try:
        print(f"\n📝 Enviando mensaje...")
        print(f"   Destino: {numero_destino}")
        print(f"   Desde: {os.getenv('TWILIO_WHATSAPP_FROM')}")
        
        # Enviar mensaje
        message = client.messages.create(
            body=mensaje,
            from_=os.getenv('TWILIO_WHATSAPP_FROM'),
            to=f"whatsapp:{numero_destino}"
        )
        
        print(f"✅ Mensaje enviado exitosamente!")
        print(f"   SID: {message.sid}")
        print(f"   Status: {message.status}")
        
        # Guardar en base de datos
        try:
            conn = sqlite3.connect('numeros_whatsapp.db')
            cursor = conn.cursor()
            
            # Obtener nombre del contacto
            cursor.execute('SELECT nombre, apellido FROM numeros WHERE telefono = ?', (numero_destino.replace('+', ''),))
            contacto = cursor.fetchone()
            
            if contacto:
                nombre_completo = f"{contacto[0]} {contacto[1]}"
            else:
                nombre_completo = "Usuario"
            
            # Registrar en log
            cursor.execute('''
                INSERT INTO mensajes_log (telefono, nombre, mensaje, estado, fecha_envio, sid_twilio)
                VALUES (?, ?, ?, ?, datetime('now'), ?)
            ''', (numero_destino.replace('+', ''), nombre_completo, mensaje, 'enviado', message.sid))
            
            conn.commit()
            conn.close()
            
            print(f"✅ Mensaje registrado en base de datos")
            
        except Exception as e:
            print(f"⚠️ Error registrando en BD: {e}")
        
    except Exception as e:
        print(f"❌ Error enviando mensaje: {e}")
        if "not verified" in str(e).lower():
            print("   ⚠️ El número no está verificado")
        elif "trial" in str(e).lower():
            print("   ⚠️ Restricción de cuenta Trial")
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN:")
    print("=" * 60)
    print("✅ Mensaje enviado a número verificado")
    print("📱 Revisa tu WhatsApp para ver el mensaje")
    print("🔄 Para agregar más números:")
    print("   • Ve a: https://console.twilio.com/us1/develop/phone-numbers/manage/verified")
    print("   • Agrega el número +51970088333")
    print("   • Verifica con el código SMS")
    print("=" * 60)

if __name__ == "__main__":
    main()
