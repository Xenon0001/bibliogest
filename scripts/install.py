#!/usr/bin/env python3
"""
Script de instalación para BiblioGest v1.1
Verifica dependencias, crea directorios necesarios y configura el entorno
"""
import os
import sys
import subprocess
import venv

def check_python_version():
    """Verifica la versión de Python"""
    if sys.version_info < (3, 8):
        print("❌ Error: BiblioGest requiere Python 3.8 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} verificado")
    return True

def create_virtual_environment():
    """Crea un entorno virtual si no existe"""
    venv_path = "venv"
    if not os.path.exists(venv_path):
        print("📦 Creando entorno virtual...")
        venv.create(venv_path, with_pip=True)
        print("✅ Entorno virtual creado")
    else:
        print("✅ Entorno virtual ya existe")

def install_dependencies():
    """Instala las dependencias desde requirements.txt"""
    if not os.path.exists("requirements.txt"):
        print("❌ Error: No se encuentra requirements.txt")
        return False
    
    print("📚 Instalando dependencias...")
    try:
        # Determinar el comando pip según el sistema operativo
        if sys.platform == "win32":
            pip_cmd = os.path.join("venv", "Scripts", "pip")
        else:
            pip_cmd = os.path.join("venv", "bin", "pip")
        
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def create_directories():
    """Crea directorios necesarios para la aplicación"""
    directories = ["logs", "data"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Directorio '{directory}' creado/verificado")

def setup_environment():
    """Configura el entorno de producción"""
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            print("📝 Creando archivo .env desde .env.example...")
            with open(".env.example", "r", encoding="utf-8") as f:
                content = f.read()
            with open(".env", "w", encoding="utf-8") as f:
                f.write(content)
            print("✅ Archivo .env creado. Por favor, configúralo con tus datos.")
        else:
            print("⚠️  No se encuentra .env.example. Creando .env básico...")
            basic_env = """# Variables de entorno para BiblioGest v1.1
# Configura estos valores según tu entorno

# Contraseña de aplicación para Gmail (opcional)
BIBLIOGEST_EMAIL_PASSWORD=

# Configuración SMTP (opcional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_FROM=bibliogest.notificaciones@gmail.com
EMAIL_ADMIN=xenonpy465@gmail.com
"""
            with open(".env", "w", encoding="utf-8") as f:
                f.write(basic_env)
            print("✅ Archivo .env básico creado")
    else:
        print("✅ Archivo .env ya existe")

def main():
    """Función principal de instalación"""
    print("🚀 Instalador BiblioGest v1.1")
    print("=" * 40)
    
    # Verificar Python
    if not check_python_version():
        sys.exit(1)
    
    # Crear entorno virtual
    create_virtual_environment()
    
    # Instalar dependencias
    if not install_dependencies():
        sys.exit(1)
    
    # Crear directorios
    create_directories()
    
    # Configurar entorno
    setup_environment()
    
    print("\n🎉 Instalación completada exitosamente!")
    print("\n📋 Próximos pasos:")
    print("1. Configura el archivo .env con tus datos")
    print("2. Ejecuta la aplicación:")
    print("   - Windows: venv\\Scripts\\python main.py")
    print("   - Linux/Mac: venv/bin/python main.py")
    print("3. O usa el script de ejecución: python scripts/run.py")

if __name__ == "__main__":
    main()
