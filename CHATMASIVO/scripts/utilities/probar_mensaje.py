#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para probar el envío de mensajes con números mágicos de Twilio
"""

import requests
import json

def probar_mensaje():
    """Probar el envío de mensaje de prueba"""
    try:
        # Hacer petición a la API de envío de prueba
        response = requests.post('http://localhost:5000/api/enviar_prueba')
        
        if response.status_code == 200:
            data = response.json()
            print("=" * 50)
            print("RESULTADO DE LA PRUEBA")
            print("=" * 50)
            print(f"Éxito: {data.get('success', False)}")
            print(f"Mensaje: {data.get('message', 'Sin mensaje')}")
            
            if data.get('success'):
                print(f"SID: {data.get('sid', 'N/A')}")
                print(f"Número usado: {data.get('numero_usado', 'N/A')}")
                print("✅ ¡Mensaje enviado exitosamente!")
            else:
                print(f"Código de error: {data.get('error_code', 'N/A')}")
                print(f"Sugerencia: {data.get('sugerencia', 'N/A')}")
                print("❌ Error en el envío")
        else:
            print(f"Error HTTP: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor")
        print("Asegúrate de que el servidor esté ejecutándose en http://localhost:5000")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    probar_mensaje()
