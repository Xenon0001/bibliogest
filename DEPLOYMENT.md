# 🚀 Guía de Deployment - BiblioGest v1.1

## 📋 Tabla de Contenidos

- [Requisitos del Sistema](#requisitos-del-sistema)
- [Instalación Automática](#instalación-automática)
- [Instalación Manual](#instalación-manual)
- [Configuración](#configuración)
- [Ejecución](#ejecución)
- [Build para Producción](#build-para-producción)
- [Troubleshooting](#troubleshooting)

---

## 🔧 Requisitos del Sistema

### **Mínimos**
- **Python**: 3.8 o superior
- **Sistema Operativo**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Memoria RAM**: 4 GB mínimo
- **Espacio en Disco**: 500 MB disponibles
- **Pantalla**: Resolución mínima 1024x768

### **Recomendados**
- **Python**: 3.10 o superior
- **Memoria RAM**: 8 GB o más
- **Espacio en Disco**: 1 GB disponible
- **Pantalla**: Resolución 1920x1080 o superior

---

## 🚀 Instalación Automática

### **Método 1: Usando el Script de Instalación**

```bash
# 1. Clonar el repositorio
git clone https://github.com/Xenon0001/bibliogest.git
cd bibliogest

# 2. Ejecutar instalación automática
python scripts/install.py
```

El script realizará automáticamente:
- ✅ Verificación de versión de Python
- ✅ Creación de entorno virtual
- ✅ Instalación de dependencias
- ✅ Creación de directorios necesarios
- ✅ Configuración inicial del entorno

### **Método 2: Instalación con un Comando**

```bash
# Descargar y ejecutar en un paso
curl -sSL https://raw.githubusercontent.com/Xenon0001/bibliogest/main/scripts/install.py | python
```

---

## 🔨 Instalación Manual

### **Paso 1: Clonar el Repositorio**

```bash
git clone https://github.com/Xenon0001/bibliogest.git
cd bibliogest
```

### **Paso 2: Crear Entorno Virtual**

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\\Scripts\\activate
# Linux/macOS:
source venv/bin/activate
```

### **Paso 3: Instalar Dependencias**

```bash
pip install -r requirements.txt
```

### **Paso 4: Configurar Variables de Entorno**

```bash
# Copiar archivo de configuración
copy .env.example .env

# Editar .env con tu configuración
notepad .env  # Windows
nano .env      # Linux/macOS
```

### **Paso 5: Crear Directorios Necesarios**

```bash
mkdir logs
mkdir data
```

---

## Configuración

### Variables de Entorno

Copia `.env.example` a `.env` y configura:

```bash
# Configuración de Email (Opcional)
BIBLIOGEST_EMAIL_PASSWORD=tu_contraseña_de_outlook
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
EMAIL_FROM=bibliogest.notificaciones@outlook.com
EMAIL_ADMIN=xenonpy465@gmail.com
```

### Configuración de Outlook para Email

1. **Crear cuenta Outlook**:
   - Ve a [outlook.com](https://outlook.com)
   - Registra `bibliogest.notificaciones@outlook.com`
   - Verifica el email de confirmación

2. **Configurar en .env**:
   ```bash
   BIBLIOGEST_EMAIL_PASSWORD=la_contraseña_normal_de_outlook
   ```

---

## Ejecución
## 🎯 Ejecución

### **Método 1: Script de Ejecución**

```bash
python scripts/run.py
```

### **Método 2: Ejecución Manual**

```bash
# Windows
venv\\Scripts\\python main.py

# Linux/macOS
venv/bin/python main.py
```

### **Método 3: Ejecutable (Después del Build)**

```bash
# Windows
dist\\BiblioGest.exe

# Linux/macOS
./dist/BiblioGest
```

---

## 🏗️ Build para Producción

### **Crear Ejecutable Standalone**

```bash
# Ejecutar script de build
python scripts/build.py
```

Este script creará:
- `dist/BiblioGest.exe` - Ejecutable standalone
- `BiblioGest_v1.1_Portable/` - Paquete completo para distribución

### **Build Manual con PyInstaller**

```bash
# Instalar PyInstaller
pip install pyinstaller

# Crear ejecutable
pyinstaller --onefile --windowed --name=BiblioGest main.py
```

---

## 📁 Estructura de Archivos

```
bibliogest/
├── main.py                 # Punto de entrada
├── requirements.txt        # Dependencias
├── .env.example           # Plantilla de configuración
├── README.md              # Documentación principal
├── DEPLOYMENT.md          # Esta guía
├── LICENSE                # Licencia
├── config/                # Configuración de logging
│   ├── __init__.py
│   └── logging_config.py
├── db/                    # Base de datos y lógica
│   ├── __init__.py
│   └── database.py
├── ui/                    # Interfaz de usuario
│   ├── views/
│   ├── forms/
│   └── widgets/
├── utils/                 # Utilidades
│   ├── security.py
│   ├── validators_enhanced.py
│   └── email_service.py
├── scripts/               # Scripts de automatización
│   ├── install.py
│   ├── run.py
│   └── build.py
├── logs/                  # Logs de la aplicación
├── data/                  # Datos y base de datos
└── venv/                  # Entorno virtual
```

---

## 🔍 Troubleshooting

### **Problemas Comunes**

#### **1. Error: "No module named 'customtkinter'"**
```bash
# Solución: Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

#### **2. Error: "Database locked"**
```bash
# Solución: Eliminar archivo de base de datos corrupto
rm data/biblioteca.db
# Reiniciar la aplicación
```

#### **3. Error: "Email authentication failed"**
```bash
# Solución: Verificar configuración de Gmail
# 1. Generar nueva contraseña de aplicación
# 2. Actualizar .env con la nueva contraseña
```

#### **4. Error: "Permission denied" (Linux/macOS)**
```bash
# Solución: Dar permisos de ejecución
chmod +x scripts/*.py
chmod +x dist/BiblioGest
```

#### **5. Error: "Tkinter not available"**
```bash
# Solución: Instalar Tkinter
# Ubuntu/Debian:
sudo apt-get install python3-tk
# Fedora:
sudo dnf install python3-tkinter
# macOS (si usamos Homebrew Python):
brew install python-tk
```

### **Logs y Diagnóstico**

Los logs se guardan en el directorio `logs/`:

- `bibliogest_YYYYMMDD.log` - Logs generales de la aplicación
- `bibliogest_security.log` - Eventos de seguridad
- `bibliogest_email.log` - Eventos de envío de correos

### **Soporte**

Si encuentras problemas no documentados:

1. Revisa los logs en `logs/`
2. Verifica que todos los requisitos del sistema estén cumplidos
3. Intenta una instalación limpia
4. Reporta el issue en: https://github.com/Xenon0001/bibliogest/issues

---

## 📝 Notas de Versión

### **v1.1 - Características de Producción**
- ✅ bcrypt para seguridad de contraseñas
- ✅ Logging estructurado
- ✅ Validaciones mejoradas
- ✅ Sistema de notificaciones por email
- ✅ Campos adicionales en libros
- ✅ Scripts de automatización
- ✅ Build para distribución

### **Requisitos de Producción**
- Python 3.8+ requerido
- 500 MB de espacio en disco
- Conexión a internet opcional (para email)

---

## 🎉 ¡Listo para Producción!

Una vez completada la instalación y configuración, BiblioGest v1.1 está listo para uso en producción con:

- 🔐 **Seguridad empresarial** con bcrypt
- 📊 **Auditoría completa** con logging estructurado
- 📧 **Notificaciones automáticas** por email
- 🎨 **Interfaz profesional** y moderna
- 🚀 **Distribución fácil** con ejecutable standalone

**¡Gracias por usar BiblioGest!** 📚
