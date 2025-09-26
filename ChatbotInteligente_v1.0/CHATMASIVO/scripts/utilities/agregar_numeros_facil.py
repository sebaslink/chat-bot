#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para agregar números fácilmente a la lista de verificación
"""

import webbrowser
import time

def main():
    print("=" * 70)
    print("📱 AGREGAR NÚMEROS FÁCILMENTE - CUENTA TRIAL")
    print("=" * 70)
    
    # Números que quieres agregar
    numeros_para_agregar = [
        '+51970088333',  # Número que quieres verificar
        # Agrega más números aquí
    ]
    
    print(f"📋 NÚMEROS A AGREGAR: {len(numeros_para_agregar)}")
    for i, numero in enumerate(numeros_para_agregar, 1):
        print(f"   {i}. {numero}")
    
    print(f"\n" + "=" * 70)
    print(f"📱 PROCESO PASO A PASO")
    print(f"=" * 70)
    print(f"1. 🌐 Se abrirá la página de verificación de Twilio")
    print(f"2. 🔑 Inicia sesión con tu cuenta de Twilio")
    print(f"3. ➕ Haz clic en 'Add a new number'")
    print(f"4. 📞 Ingresa cada número de la lista")
    print(f"5. 📱 Twilio enviará un código SMS a cada número")
    print(f"6. 🔢 Ingresa el código en la página web")
    print(f"7. ✅ Repite para cada número")
    print(f"8. 🎉 ¡Listo! Los números podrán recibir mensajes")
    
    print(f"\n⏱️ TIEMPO ESTIMADO:")
    print(f"   • Por número: 1-2 minutos")
    print(f"   • Total: {len(numeros_para_agregar) * 2} minutos")
    
    print(f"\n💰 COSTO:")
    print(f"   • Verificación: GRATIS")
    print(f"   • Envío de mensajes: GRATIS (cuenta Trial)")
    
    print(f"\n⚠️ IMPORTANTE:")
    print(f"   • Necesitas acceso físico a cada número")
    print(f"   • Los códigos SMS llegan en 1-2 minutos")
    print(f"   • Una vez verificado, funciona inmediatamente")
    
    print(f"\n🚀 ¿CONTINUAR?")
    print(f"   Presiona Enter para abrir la página o Ctrl+C para cancelar")
    
    try:
        input()
    except KeyboardInterrupt:
        print(f"\n❌ Proceso cancelado")
        return
    
    # Abrir página de verificación
    print(f"\n🌐 Abriendo página de verificación...")
    try:
        webbrowser.open("https://console.twilio.com/us1/develop/phone-numbers/manage/verified")
        print(f"✅ Página abierta en tu navegador")
    except:
        print(f"❌ No se pudo abrir automáticamente")
        print(f"   Copia y pega este enlace:")
        print(f"   https://console.twilio.com/us1/develop/phone-numbers/manage/verified")
    
    print(f"\n" + "=" * 70)
    print(f"📋 LISTA DE NÚMEROS PARA COPIAR")
    print(f"=" * 70)
    for i, numero in enumerate(numeros_para_agregar, 1):
        print(f"{i}. {numero}")
    
    print(f"\n💡 CONSEJOS:")
    print(f"   • Copia y pega los números para evitar errores")
    print(f"   • Verifica un número a la vez")
    print(f"   • Mantén este terminal abierto para referencia")
    print(f"   • Una vez terminado, ejecuta: python verificar_estado_numeros.py")
    
    print(f"\n🔄 VERIFICAR PROGRESO:")
    print(f"   Ejecuta este comando para ver qué números ya están listos:")
    print(f"   python verificar_estado_numeros.py")
    
    print(f"=" * 70)

if __name__ == "__main__":
    main()

