#!/usr/bin/env python3
"""
Script de configuración de credenciales de Twilio
Para instalación en nueva computadora
"""

import os
import sys
from pathlib import Path

def mostrar_banner():
    """Mostrar banner del script"""
    print("=" * 60)
    print("🔧 CONFIGURADOR DE CREDENCIALES TWILIO")
    print("=" * 60)
    print("Este script te ayudará a configurar las credenciales de Twilio")
    print("para el sistema de Chat Masivo WhatsApp.")
    print("=" * 60)

def obtener_credenciales():
    """Obtener credenciales del usuario"""
    print("\n📋 Necesitarás las siguientes credenciales de Twilio:")
    print("   1. Account SID (comienza con 'AC...')")
    print("   2. Auth Token (32 caracteres)")
    print("   3. Número de WhatsApp (formato: +1234567890)")
    print("\n   Puedes obtenerlas en: https://console.twilio.com/")
    print("   Ve a: Account > API keys & tokens")
    
    print("\n" + "=" * 40)
    print("🔑 INGRESA TUS CREDENCIALES")
    print("=" * 40)
    
    # Account SID
    while True:
        account_sid = input("\n1. Account SID: ").strip()
        if account_sid.startswith('AC') and len(account_sid) == 34:
            break
        print("❌ Account SID debe comenzar con 'AC' y tener 34 caracteres")
    
    # Auth Token
    while True:
        auth_token = input("2. Auth Token: ").strip()
        if len(auth_token) == 32 and auth_token.isalnum():
            break
        print("❌ Auth Token debe tener exactamente 32 caracteres alfanuméricos")
    
    # Número de WhatsApp
    while True:
        whatsapp_from = input("3. Número de WhatsApp (ej: +14155238886): ").strip()
        if whatsapp_from.startswith('+') and whatsapp_from[1:].isdigit() and len(whatsapp_from) >= 10:
            break
        print("❌ Número debe comenzar con '+' y contener solo dígitos")
    
    # Clave secreta de Flask
    flask_secret = input("4. Clave secreta Flask (opcional, se genera automática): ").strip()
    if not flask_secret:
        import secrets
        flask_secret = secrets.token_hex(32)
        print(f"   ✅ Clave generada automáticamente: {flask_secret[:16]}...")
    
    # Número de prueba
    numero_prueba = input("5. Número de prueba (opcional): ").strip()
    if not numero_prueba:
        numero_prueba = whatsapp_from
    
    return {
        'account_sid': account_sid,
        'auth_token': auth_token,
        'whatsapp_from': whatsapp_from,
        'flask_secret': flask_secret,
        'numero_prueba': numero_prueba
    }

def crear_archivo_env(credenciales):
    """Crear archivo .env principal"""
    print("\n📝 Creando archivo .env principal...")
    
    env_content = f"""# Configuración de Twilio - Chat Masivo WhatsApp
# Generado automáticamente el {os.popen('date /t' if os.name == 'nt' else 'date').read().strip()}

# Credenciales de Twilio
TWILIO_ACCOUNT_SID={credenciales['account_sid']}
TWILIO_AUTH_TOKEN={credenciales['auth_token']}
TWILIO_WHATSAPP_FROM={credenciales['whatsapp_from']}

# Flask
FLASK_SECRET_KEY={credenciales['flask_secret']}

# Número de prueba
NUMERO_PRUEBA={credenciales['numero_prueba']}
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("   ✅ Archivo .env creado correctamente")
        return True
    except Exception as e:
        print(f"   ❌ Error creando .env: {e}")
        return False

def crear_archivos_configuracion(credenciales):
    """Crear archivos de configuración en las carpetas correspondientes"""
    print("\n📁 Creando archivos de configuración...")
    
    # Configuración para CHATMASIVO
    configs = [
        {
            'path': 'CHATMASIVO/config/twilio/Twilio.env',
            'content': f"""# Configuración de Twilio
# Archivo de configuración para Chat Masivo WhatsApp

# Credenciales de Twilio (obténlas desde https://console.twilio.com/)
TWILIO_ACCOUNT_SID={credenciales['account_sid']}
TWILIO_AUTH_TOKEN={credenciales['auth_token']}

# Número de WhatsApp de Twilio (formato: whatsapp:+1234567890)
TWILIO_WHATSAPP_FROM={credenciales['whatsapp_from']}

# Clave secreta de Flask (genera una clave segura)
FLASK_SECRET_KEY={credenciales['flask_secret']}

# Número de prueba para testing (opcional)
NUMERO_PRUEBA={credenciales['numero_prueba']}
"""
        },
        {
            'path': 'CHATMASIVO/config/app/Twilio.env',
            'content': f"""# Twilio - Credenciales
TWILIO_ACCOUNT_SID={credenciales['account_sid']}
TWILIO_AUTH_TOKEN={credenciales['auth_token']}
TWILIO_WHATSAPP_FROM={credenciales['whatsapp_from']}

# Flask - Genera una clave secreta segura
FLASK_SECRET_KEY={credenciales['flask_secret']}
"""
        }
    ]
    
    for config in configs:
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(config['path']), exist_ok=True)
            
            with open(config['path'], 'w', encoding='utf-8') as f:
                f.write(config['content'])
            print(f"   ✅ {config['path']}")
        except Exception as e:
            print(f"   ❌ Error en {config['path']}: {e}")

def verificar_configuracion():
    """Verificar que la configuración sea correcta"""
    print("\n🔍 Verificando configuración...")
    
    archivos_verificar = [
        '.env',
        'CHATMASIVO/config/twilio/Twilio.env',
        'CHATMASIVO/config/app/Twilio.env'
    ]
    
    for archivo in archivos_verificar:
        if os.path.exists(archivo):
            print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ {archivo} - No encontrado")

def mostrar_instrucciones_finales():
    """Mostrar instrucciones finales"""
    print("\n" + "=" * 60)
    print("🎉 ¡CONFIGURACIÓN COMPLETADA!")
    print("=" * 60)
    
    print("\n📋 Próximos pasos:")
    print("   1. Ejecuta el sistema: python SISTEMA_UNIFICADO_FINAL.py")
    print("   2. Abre tu navegador en: http://localhost:5000")
    print("   3. Prueba enviando un mensaje de prueba")
    
    print("\n🔒 Seguridad:")
    print("   - Los archivos .env contienen credenciales sensibles")
    print("   - NO compartas estos archivos")
    print("   - Están protegidos por .gitignore")
    
    print("\n🆘 Si hay problemas:")
    print("   - Verifica que las credenciales sean correctas")
    print("   - Revisa los logs en: chatmasivo.log")
    print("   - Consulta la documentación en: README_GITLAB.md")

def main():
    """Función principal"""
    mostrar_banner()
    
    # Verificar si ya existe configuración
    if os.path.exists('.env'):
        respuesta = input("\n⚠️  Ya existe un archivo .env. ¿Sobrescribir? (s/n): ").lower()
        if respuesta != 's':
            print("❌ Configuración cancelada")
            return
    
    try:
        # Obtener credenciales
        credenciales = obtener_credenciales()
        
        # Crear archivos de configuración
        if not crear_archivo_env(credenciales):
            print("❌ Error creando archivo .env")
            return
        
        crear_archivos_configuracion(credenciales)
        
        # Verificar configuración
        verificar_configuracion()
        
        # Mostrar instrucciones finales
        mostrar_instrucciones_finales()
        
    except KeyboardInterrupt:
        print("\n\n❌ Configuración cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()