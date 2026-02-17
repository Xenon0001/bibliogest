#!/usr/bin/env python3
"""
Script de ejecución para BiblioGest v1.1
Inicia la aplicación con el entorno virtual y logging configurado
"""
import os
import sys
import subprocess
from pathlib import Path

def check_environment():
    """Verifica que el entorno esté configurado correctamente"""
    # Verificar entorno virtual
    venv_path = Path("venv")
    if not venv_path.exists():
        print("❌ Error: No se encuentra el entorno virtual")
        print("   Ejecuta primero: python scripts/install.py")
        return False
    
    # Verificar requirements.txt
    if not Path("requirements.txt").exists():
        print("❌ Error: No se encuentra requirements.txt")
        return False
    
    # Verificar main.py
    if not Path("main.py").exists():
        print("❌ Error: No se encuentra main.py")
        return False
    
    print("✅ Entorno verificado")
    return True

def get_python_executable():
    """Obtiene el ejecutable de Python del entorno virtual"""
    if sys.platform == "win32":
        return os.path.join("venv", "Scripts", "python.exe")
    else:
        return os.path.join("venv", "bin", "python")

def run_application():
    """Inicia la aplicación BiblioGest"""
    python_executable = get_python_executable()
    
    print("🚀 Iniciando BiblioGest v1.1...")
    print("=" * 40)
    
    try:
        # Cargar variables de entorno si existe .env
        env_file = Path(".env")
        env = os.environ.copy()
        
        if env_file.exists():
            print("📝 Cargando variables de entorno desde .env...")
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        env[key] = value
            print("✅ Variables de entorno cargadas")
        
        # Iniciar la aplicación
        subprocess.run([python_executable, "main.py"], env=env, check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando la aplicación: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 Aplicación detenida por el usuario")
        return True
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    """Función principal"""
    print("🎯 Ejecutor BiblioGest v1.1")
    print("=" * 40)
    
    # Verificar entorno
    if not check_environment():
        sys.exit(1)
    
    # Ejecutar aplicación
    if not run_application():
        sys.exit(1)

if __name__ == "__main__":
    main()
