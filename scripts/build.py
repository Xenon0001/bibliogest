#!/usr/bin/env python3
"""
Script de build para crear ejecutable de BiblioGest v1.1
Usa PyInstaller para crear una distribución standalone
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """Verifica si PyInstaller está instalado"""
    try:
        subprocess.run(["pyinstaller", "--version"], capture_output=True, check=True)
        print("PyInstaller encontrado")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("PyInstaller no encontrado. Instalando...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
            print("PyInstaller instalado")
            return True
        except subprocess.CalledProcessError:
            print("Error instalando PyInstaller")
            return False

def create_spec_file():
    """Crea el archivo .spec para PyInstaller con configuración optimizada"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('ui', 'ui'),
        ('db', 'db'),
        ('utils', 'utils'),
        ('config', 'config'),
        ('.env.example', '.env.example'),
    ],
    hiddenimports=[
        'customtkinter',
        'tkinter',
        'sqlite3',
        'bcrypt',
        'validators',
        'smtplib',
        'ssl',
        'email.mime.text',
        'email.mime.multipart',
        'email.mime.base',
        'email.header',
        'email.utils',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BiblioGest',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
'''
    
    with open('bibliogest.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print("Archivo .spec creado")

def build_executable():
    """Construye el ejecutable con PyInstaller"""
    print("🔨 Construyendo ejecutable...")
    
    try:
        # Limpiar builds anteriores
        if Path("build").exists():
            shutil.rmtree("build")
        if Path("dist").exists():
            shutil.rmtree("dist")
        
        # Ejecutar PyInstaller
        subprocess.run(["pyinstaller", "bibliogest.spec", "--clean"], check=True)
        
        print("Ejecutable construido en dist/")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error construyendo ejecutable: {e}")
        return False

def create_portable_package():
    """Crea un paquete portable con todos los archivos necesarios"""
    print("Creando paquete portable...")
    
    portable_dir = Path("BiblioGest_v1.1_Portable")
    
    # Eliminar directorio anterior si existe
    if portable_dir.exists():
        shutil.rmtree(portable_dir)
    
    # Crear estructura del paquete
    portable_dir.mkdir()
    
    # Copiar ejecutable
    exe_source = Path("dist/BiblioGest.exe")
    if exe_source.exists():
        shutil.copy2(exe_source, portable_dir / "BiblioGest.exe")
    
    # Copiar archivos necesarios
    files_to_copy = [
        "README.md",
        ".env.example",
        "LICENSE",
    ]
    
    for file_name in files_to_copy:
        source = Path(file_name)
        if source.exists():
            shutil.copy2(source, portable_dir / file_name)
    
    # Crear directorios necesarios
    (portable_dir / "logs").mkdir(exist_ok=True)
    (portable_dir / "data").mkdir(exist_ok=True)
    
    # Crear script de inicio
    start_script = '''@echo off
title BiblioGest v1.1
echo Iniciando BiblioGest...
echo.
BiblioGest.exe
pause
'''
    
    with open(portable_dir / "Iniciar BiblioGest.bat", "w", encoding="utf-8") as f:
        f.write(start_script)
    
    print("Paquete portable creado en BiblioGest_v1.1_Portable/")

def main():
    """Función principal"""
    print("Build BiblioGest v1.1")
    print("=" * 40)
    
    # Verificar PyInstaller
    if not check_pyinstaller():
        sys.exit(1)
    
    # Crear archivo .spec
    create_spec_file()
    
    # Construir ejecutable
    if not build_executable():
        sys.exit(1)
    
    # Crear paquete portable
    create_portable_package()
    
    print("\n🎉 Build completado exitosamente!")
    print("\n📦 Archivos generados:")
    print("  - dist/BiblioGest.exe (ejecutable)")
    print("  - BiblioGest_v1.1_Portable/ (paquete completo)")
    print("\n🚀 Para distribuir, comprime la carpeta BiblioGest_v1.1_Portable")

if __name__ == "__main__":
    main()
