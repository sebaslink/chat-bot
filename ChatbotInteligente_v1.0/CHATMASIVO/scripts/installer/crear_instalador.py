#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear instalador.exe del sistema de Chat Masivo
Incluye PyInstaller para crear ejecutable y Inno Setup para el instalador
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def verificar_dependencias():
    """Verificar que las dependencias necesarias estén instaladas"""
    print("🔍 Verificando dependencias...")
    
    dependencias = ['pyinstaller', 'inno-setup']
    faltantes = []
    
    for dep in dependencias:
        try:
            if dep == 'inno-setup':
                # Verificar Inno Setup en ubicaciones comunes
                ubicaciones = [
                    r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
                    r"C:\Program Files\Inno Setup 6\ISCC.exe",
                    r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
                    r"C:\Program Files\Inno Setup 5\ISCC.exe"
                ]
                encontrado = False
                for ubicacion in ubicaciones:
                    if os.path.exists(ubicacion):
                        encontrado = True
                        break
                if not encontrado:
                    faltantes.append(dep)
            else:
                subprocess.run([sys.executable, '-m', 'pip', 'show', dep], 
                             check=True, capture_output=True)
        except subprocess.CalledProcessError:
            faltantes.append(dep)
    
    if faltantes:
        print(f"❌ Faltan dependencias: {', '.join(faltantes)}")
        print("\n📦 Instalando dependencias faltantes...")
        
        for dep in faltantes:
            if dep == 'inno-setup':
                print("⚠️  Inno Setup no encontrado. Descárgalo desde:")
                print("   https://jrsoftware.org/isinfo.php")
                print("   Instálalo y vuelve a ejecutar este script.")
                return False
            else:
                subprocess.run([sys.executable, '-m', 'pip', 'install', dep])
    
    print("✅ Todas las dependencias están disponibles")
    return True

def crear_ejecutable():
    """Crear ejecutable con PyInstaller"""
    print("\n🔨 Creando ejecutable con PyInstaller...")
    
    # Archivo principal
    archivo_principal = "app/codchat.py"
    if not os.path.exists(archivo_principal):
        archivo_principal = "codigo/codchat.py"
    
    if not os.path.exists(archivo_principal):
        print("❌ No se encontró el archivo principal codchat.py")
        return False
    
    # Comando PyInstaller
    comando = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',  # Un solo archivo ejecutable
        '--windowed',  # Sin consola (GUI)
        '--name=ChatMasivo',
        '--icon=imagen/icono.jpg' if os.path.exists('imagen/icono.jpg') else '',
        '--add-data=templates;templates',
        '--add-data=static;static',
        '--add-data=config;config',
        '--add-data=Twilio.env;.',
        '--hidden-import=flask',
        '--hidden-import=twilio',
        '--hidden-import=pandas',
        '--hidden-import=openpyxl',
        '--hidden-import=sqlite3',
        '--hidden-import=werkzeug',
        '--hidden-import=dotenv',
        archivo_principal
    ]
    
    # Filtrar elementos vacíos
    comando = [c for c in comando if c]
    
    try:
        subprocess.run(comando, check=True)
        print("✅ Ejecutable creado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creando ejecutable: {e}")
        return False

def crear_estructura_instalador():
    """Crear estructura de archivos para el instalador"""
    print("\n📁 Creando estructura del instalador...")
    
    # Directorio de instalador
    dir_instalador = "instalador_temp"
    if os.path.exists(dir_instalador):
        shutil.rmtree(dir_instalador)
    os.makedirs(dir_instalador)
    
    # Copiar archivos necesarios
    archivos_copiar = [
        ("dist/ChatMasivo.exe", "ChatMasivo.exe"),
        ("templates/", "templates/"),
        ("static/", "static/"),
        ("config/", "config/"),
        ("Twilio.env", "Twilio.env"),
        ("Twilio.env.example", "Twilio.env.example"),
        ("requirements.txt", "requirements.txt"),
        ("README.md", "README.md") if os.path.exists("README.md") else None,
        ("documentacion/", "documentacion/") if os.path.exists("documentacion/") else None
    ]
    
    for origen, destino in archivos_copiar:
        if origen and os.path.exists(origen):
            destino_path = os.path.join(dir_instalador, destino)
            if origen.endswith('/'):
                shutil.copytree(origen, destino_path)
            else:
                os.makedirs(os.path.dirname(destino_path), exist_ok=True)
                shutil.copy2(origen, destino_path)
            print(f"  ✓ Copiado: {origen} -> {destino}")
    
    # Crear archivo de configuración inicial
    config_inicial = os.path.join(dir_instalador, "config_inicial.txt")
    with open(config_inicial, 'w', encoding='utf-8') as f:
        f.write("""# Configuración inicial del Chat Masivo
# Edita este archivo con tus credenciales de Twilio

# Credenciales de Twilio (obligatorio)
TWILIO_ACCOUNT_SID=tu_account_sid_aqui
TWILIO_AUTH_TOKEN=tu_auth_token_aqui
TWILIO_WHATSAPP_FROM=+15005550009

# Número de prueba (opcional)
NUMERO_PRUEBA=+15005550009

# Clave secreta de Flask (opcional)
FLASK_SECRET_KEY=tu_clave_secreta_aqui
""")
    
    print(f"✅ Estructura creada en: {dir_instalador}")
    return dir_instalador

def crear_script_inno_setup():
    """Crear script de Inno Setup"""
    print("\n📝 Creando script de Inno Setup...")
    
    script_inno = """[Setup]
AppName=Chat Masivo WhatsApp
AppVersion=1.0
AppPublisher=Tu Empresa
AppPublisherURL=https://tu-empresa.com
AppSupportURL=https://tu-empresa.com/soporte
AppUpdatesURL=https://tu-empresa.com/actualizaciones
DefaultDirName={autopf}\\ChatMasivo
DefaultGroupName=Chat Masivo
AllowNoIcons=yes
LicenseFile=
OutputDir=dist_instalador
OutputBaseFilename=ChatMasivo_Instalador
SetupIconFile=imagen\\icono.jpg
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "Crear icono en el escritorio"; GroupDescription: "Iconos adicionales:"
Name: "quicklaunchicon"; Description: "Crear icono en la barra de inicio rápido"; GroupDescription: "Iconos adicionales:"

[Files]
Source: "instalador_temp\\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "instalador_temp\\ChatMasivo.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\\Chat Masivo"; Filename: "{app}\\ChatMasivo.exe"; WorkingDir: "{app}"
Name: "{group}\\Configuración"; Filename: "{app}\\config_inicial.txt"
Name: "{group}\\Documentación"; Filename: "{app}\\documentacion"
Name: "{group}\\Desinstalar Chat Masivo"; Filename: "{uninstallexe}"
Name: "{autodesktop}\\Chat Masivo"; Filename: "{app}\\ChatMasivo.exe"; WorkingDir: "{app}"; Tasks: desktopicon
Name: "{userappdata}\\Microsoft\\Internet Explorer\\Quick Launch\\Chat Masivo"; Filename: "{app}\\ChatMasivo.exe"; WorkingDir: "{app}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\\ChatMasivo.exe"; Description: "Ejecutar Chat Masivo"; Flags: nowait postinstall skipifsilent
Filename: "{app}\\config_inicial.txt"; Description: "Abrir configuración inicial"; Flags: postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
  // Verificar si Python está instalado (opcional)
  // if not RegKeyExists(HKEY_LOCAL_MACHINE, 'SOFTWARE\\Python\\PythonCore') then
  // begin
  //   MsgBox('Python no está instalado. Por favor instala Python 3.8 o superior.', mbError, MB_OK);
  //   Result := False;
  // end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Crear directorio de datos si no existe
    ForceDirectories(ExpandConstant('{app}\\data'));
    ForceDirectories(ExpandConstant('{app}\\logs'));
  end;
end;
"""
    
    with open("instalador.iss", 'w', encoding='utf-8') as f:
        f.write(script_inno)
    
    print("✅ Script de Inno Setup creado: instalador.iss")
    return True

def compilar_instalador():
    """Compilar el instalador con Inno Setup"""
    print("\n🔨 Compilando instalador con Inno Setup...")
    
    # Buscar Inno Setup
    ubicaciones_iscc = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
        r"C:\Program Files\Inno Setup 5\ISCC.exe"
    ]
    
    iscc_path = None
    for ubicacion in ubicaciones_iscc:
        if os.path.exists(ubicacion):
            iscc_path = ubicacion
            break
    
    if not iscc_path:
        print("❌ Inno Setup no encontrado. Instálalo desde:")
        print("   https://jrsoftware.org/isinfo.php")
        return False
    
    try:
        comando = [iscc_path, "instalador.iss"]
        subprocess.run(comando, check=True)
        print("✅ Instalador compilado exitosamente")
        print("📁 El instalador se encuentra en: dist_instalador/")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error compilando instalador: {e}")
        return False

def limpiar_archivos_temporales():
    """Limpiar archivos temporales"""
    print("\n🧹 Limpiando archivos temporales...")
    
    directorios_limpiar = [
        "build",
        "dist",
        "instalador_temp",
        "__pycache__"
    ]
    
    for directorio in directorios_limpiar:
        if os.path.exists(directorio):
            shutil.rmtree(directorio)
            print(f"  ✓ Eliminado: {directorio}")
    
    archivos_limpiar = [
        "ChatMasivo.spec",
        "instalador.iss"
    ]
    
    for archivo in archivos_limpiar:
        if os.path.exists(archivo):
            os.remove(archivo)
            print(f"  ✓ Eliminado: {archivo}")

def main():
    """Función principal"""
    print("🚀 CREADOR DE INSTALADOR - CHAT MASIVO")
    print("=" * 50)
    
    # Verificar dependencias
    if not verificar_dependencias():
        return False
    
    # Crear ejecutable
    if not crear_ejecutable():
        return False
    
    # Crear estructura del instalador
    dir_instalador = crear_estructura_instalador()
    if not dir_instalador:
        return False
    
    # Crear script de Inno Setup
    if not crear_script_inno_setup():
        return False
    
    # Compilar instalador
    if not compilar_instalador():
        return False
    
    print("\n🎉 ¡INSTALADOR CREADO EXITOSAMENTE!")
    print("=" * 50)
    print("📁 Ubicación del instalador: dist_instalador/ChatMasivo_Instalador.exe")
    print("\n📋 INSTRUCCIONES:")
    print("1. El instalador está listo para distribuir")
    print("2. Los usuarios pueden ejecutarlo en cualquier Windows")
    print("3. Se instalará automáticamente con todas las dependencias")
    print("4. Incluye configuración inicial para Twilio")
    
    # Preguntar si limpiar archivos temporales
    respuesta = input("\n¿Limpiar archivos temporales? (s/n): ").lower()
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        limpiar_archivos_temporales()
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Proceso cancelado por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
