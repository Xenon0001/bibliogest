# BiblioGest v1.1

> *Sistema de Gestión Bibliotecaria desarrollado en Python con CustomTkinter - Versión Mejorada.*

## Idiomas

- [🇪🇸 Español](#español)
- [🇬🇧 English](#english)

---

<a name="español"></a>
## 🇪🇸 Documentación en Español

### 💡 Sobre el Proyecto

BiblioGest nació como una iniciativa voluntaria para resolver un problema real en la biblioteca de la institución educativa. El objetivo fue crear una herramienta de escritorio robusta y fácil de usar, capaz de gestionar el inventario de libros, el estado actual de los préstamos y el registro de usuarios (bibliotecarios y lectores) de manera eficiente, sustituyendo los procesos manuales existentes.

Este proyecto fue desarrollado con la asistencia de herramientas de IA modernas.

### ✨ Características Principales v1.1

#### 🔒 **Seguridad Mejorada**
- **bcrypt**: Hashing de contraseñas con salt seguro
- **Validación Fortaleza**: Requisitos de contraseña (8+ chars, mayúscula, número, símbolo)
- **Auditoría Completa**: Logging de eventos de seguridad (login, registro, errores)
- **Validaciones Avanzadas**: DNI ecuatoguineano, ISBN-10/13, fechas, teléfonos

#### 📧 **Sistema de Notificaciones**
- **Email Automático**: Notificaciones de registro al administrador
- **Correo de Bienvenida**: Email personalizado para nuevos usuarios
- **HTML Profesional**: Correos con diseño moderno y responsive

#### 📚 **Gestión de Libros Mejorada**
- **Campos Adicionales**: Editorial y Fecha de Publicación
- **Validación ISBN**: Soporte completo para ISBN-10 e ISBN-13
- **Interfaz Expandida**: Tabla con nueva información visible

#### 🎨 **Mejoras de UX**
- **Cerrar Sesión**: Botón con confirmación y logging
- **Feedback Específico**: Mensajes de error detallados y útiles
- **Indicadores Visuales**: Requisitos de contraseña en el formulario

#### 🏗️ **Arquitectura Refactorizada**
- **Logging Estructurado**: Archivos separados para seguridad y email
- **Manejo de Errores**: Try/catch con logging específico
- **Validaciones Centralizadas**: Módulos dedicados y reutilizables

#### 🔄 **Funcionalidades Existentes**
- **Autenticación Segura**: Módulos de Login y Registro para bibliotecarios
- **Gestión Completa**: CRUD para libros y usuarios
- **Préstamos y Devoluciones**: Sistema completo de gestión
- **Interfaz Moderna**: CustomTkinter con experiencia de escritorio limpia

### ⚙️ Instalación

**1. Clonar el repositorio:**

```bash
git clone https://github.com/Xenon0001/bibliogest.git
cd bibliogest
```

**2. Crear y activar un entorno virtual:**

```bash
python -m venv venv
```

En Windows:
```bash
.\venv\Scripts\activate
```

En macOS/Linux:
```bash
source venv/bin/activate
```

**3. Configurar variables de entorno:**

```bash
# Copiar archivo de ejemplo
copy .env.example .env

# Editar .env con tu configuración de Gmail
BIBLIOGEST_EMAIL_PASSWORD=tu_contraseña_de_aplicacion_gmail
```

**4. Instalar dependencias:**

```bash
pip install -r requirements.txt
```

**5. Ejecutar la aplicación:**

```bash
python main.py
```

### 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

---

<a name="english"></a>
## 🇬🇧 English Documentation

### 💡 About the Project

BiblioGest was born as a voluntary initiative to solve a real problem in the educational institution's library. The goal was to create a robust and user-friendly desktop tool, capable of efficiently managing the book inventory, current loan status, and user registration (librarians and readers), replacing existing manual processes.

This project was developed with the assistance of modern AI tools.

### ✨ Key Features

- **Secure Authentication**: Login and Registration modules for librarians with email validation.
- **Inventory Management**: Forms to add, edit, and delete books.
- **User Management**: Forms to register and manage reader users.
- **Loans and Returns**: (Coming soon) Central module to register transactions.
- **Modern Interface**: Use of CustomTkinter for a clean desktop experience.

### ⚙️ Installation

**1. Clone the repository:**

```bash
git clone https://github.com/your-username/bibliogest.git
cd bibliogest
```

**2. Create and activate a virtual environment:**

```bash
python -m venv venv
```

On Windows:
```bash
.\venv\Scripts\activate
```

On macOS/Linux:
```bash
source venv/bin/activate
```

**3. Install dependencies:**

```bash
pip install -r requirements.txt
```

**4. Run the application:**

```bash
python main.py
```

### 📄 License

This project is under the MIT License. See the LICENSE file for more details.

---

# 📚 BiblioGest v1.1

> **Sistema de Gestión Bibliotecaria Profesional** - Desarrollado en Python con CustomTkinter

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.1.0-orange.svg)](VERSION)
[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen.svg)](DEPLOYMENT.md)

---

## 🎯 **Sobre BiblioGest**

BiblioGest es una solución **empresarial** para la gestión completa de bibliotecas, diseñada para reemplazar procesos manuales con una herramienta moderna, segura y eficiente. Nacida como iniciativa voluntaria para resolver problemas reales en instituciones educativas, ahora es una **solución de producción** con características de nivel profesional.

### 🏆 **Características Destacadas v1.1**

- 🔐 **Seguridad Empresarial** con bcrypt y auditoría completa
- 📧 **Notificaciones Automáticas** por email HTML
- 📊 **Gestión Completa** de libros, usuarios y préstamos
- 🎨 **Interfaz Moderna** con CustomTkinter
- 🚀 **Fácil Deployment** con scripts automatizados
- 📋 **Logging Profesional** para auditoría y debugging

---

## 🚀 **Instalación Rápida**

### **Método Recomendado: Automático**

```bash
# 1. Clonar repositorio
git clone https://github.com/Xenon0001/bibliogest.git
cd bibliogest

# 2. Instalación automática (verifica Python, crea venv, instala dependencias)
python scripts/install.py

# 3. Ejecutar aplicación
python scripts/run.py
```

### **Instalación Manual**

<details>
<summary>Ver instalación manual</summary>

```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
copy .env.example .env

# 5. Ejecutar
python main.py
```

</details>

---

## ✨ **Características Principales v1.1**

### 🔒 **Seguridad Mejorada**
- **🛡️ bcrypt**: Hashing de contraseñas con salt seguro (reemplaza MD5)
- **🔍 Validación Fortaleza**: Contraseñas con 8+ chars, mayúscula, número, símbolo
- **📊 Auditoría Completa**: Logging estructurado de eventos de seguridad
- **✅ Validaciones Avanzadas**: DNI español, ISBN-10/13, fechas, teléfonos

### 📧 **Sistema de Notificaciones**
- **📨 Email Automático**: ~~Notificaciones de registro al administrador~~ (Deshabilitado en v1.1)
- **🎉 Correo de Bienvenida**: ~~Email personalizado para nuevos usuarios~~ (Deshabilitado en v1.1)
- **🎨 HTML Profesional**: ~~Correos con diseño moderno y responsive~~ (Deshabilitado en v1.1)
- 🔐 **Configuración Segura**: ~~Variables de entorno para credenciales~~ (Deshabilitado en v1.1)

### 📚 **Gestión de Libros Mejorada**
- **📖 Campos Adicionales**: Editorial y Fecha de Publicación
- **🔢 Validación ISBN**: Soporte completo para ISBN-10 e ISBN-13
- **📋 Interfaz Expandida**: Tabla con 7 columnas informativas
- **📅 Formato Estandarizado**: YYYY-MM-DD para fechas

### 🎨 **Mejoras de UX**
- **🚪 Cerrar Sesión**: Botón con confirmación y logging
- **💬 Feedback Específico**: Mensajes de error detallados y útiles
- **👁️ Indicadores Visuales**: Requisitos de contraseña en el formulario
- **📐 Campos Alineados**: Formularios con diseño consistente

### 🏗️ **Arquitectura Empresarial**
- **📝 Logging Estructurado**: Archivos separados para seguridad y email
- **🔧 Validaciones Centralizadas**: Módulos dedicados y reutilizables
- **⚠️ Manejo de Errores**: Try/catch con logging específico
- **🎮 Inicialización Controlada**: Sin auto-ejecución al importar

---

## 📋 **Requisitos del Sistema**

### **Mínimos**
- **Python**: 3.8 o superior
- **Memoria RAM**: 4 GB
- **Espacio en Disco**: 500 MB
- **Sistema**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)

### **Recomendados**
- **Python**: 3.10 o superior
- **Memoria RAM**: 8 GB o más
- **Espacio en Disco**: 1 GB disponible
- **Pantalla**: 1920x1080 o superior

---

## ⚙️ **Configuración**

### **Variables de Entorno**

Copia `.env.example` a `.env` y configura:

```bash
# Configuración de Email (Opcional)
BIBLIOGEST_EMAIL_PASSWORD=tu_contraseña_de_aplicacion_gmail
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_FROM=bibliogest.notificaciones@outlook.com
EMAIL_ADMIN=xenonpy465@gmail.com
```

### **Configuración Outlook para Email**

1. **Crear cuenta Outlook**:
   - Ve a [outlook.com](https://outlook.com)
   - Registra `bibliogest.notificaciones@outlook.com`
   - Verifica el email de confirmación

2. **Configurar en .env**:
   ```bash
   BIBLIOGEST_EMAIL_PASSWORD=la_contraseña_normal_de_outlook
   ```

...

## 🚀 **Ejecución y Deployment**

...

```bash
# 1. Script automatizado (recomendado)
python scripts/run.py

# 2. Ejecución manual
venv/Scripts/python main.py  # Windows
venv/bin/python main.py      # Linux/macOS

# 3. Ejecutable (después del build)
dist/BiblioGest.exe
```

### **Build para Producción**

```bash
# Crear ejecutable standalone
python scripts/build.py

# Resultados:
# - dist/BiblioGest.exe (ejecutable)
# - BiblioGest_v1.1_Portable/ (paquete completo)
```

---

## 📁 **Estructura del Proyecto**

```
bibliogest/
├── 📄 main.py                 # Punto de entrada
├── 📋 requirements.txt        # Dependencias
├── 🔧 .env.example           # Configuración
├── 📚 README.md              # Documentación
├── 🚀 DEPLOYMENT.md          # Guía de deployment
├── 📝 CHANGELOG.md           # Historial de cambios
├── 🏷️  VERSION                # Versión actual
├── 
├── 📁 config/                # Configuración centralizada
│   ├── logging_config.py     # Logging profesional
│   └── __init__.py
├── 
├── 📁 db/                    # Base de datos y lógica
│   └── database.py           # SQLite + seguridad
├── 
├── 📁 ui/                    # Interfaz de usuario
│   ├── views/                # Vistas principales
│   ├── forms/                # Formularios
│   └── widgets/              # Componentes UI
├── 
├── 📁 utils/                 # Utilidades
│   ├── security.py           # bcrypt + logging
│   ├── validators_enhanced.py # Validaciones avanzadas
│   └── email_service.py      # Email HTML
├── 
├── 📁 scripts/               # Automatización
│   ├── install.py            # Instalación automática
│   ├── run.py                # Ejecución con entorno
│   └── build.py              # Build para producción
├── 
├── 📁 logs/                  # Logs de aplicación
└── 📁 data/                  # Datos y base de datos
```

---

## 🔍 **Troubleshooting**

### **Problemas Comunes**

<details>
<summary>🔧 Error: "No module found"</summary>

```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

</details>

<details>
<summary>📧 Error: "Email authentication failed"</summary>

1. Generar nueva contraseña de aplicación Gmail
2. Actualizar `.env` con la nueva contraseña
3. Verificar 2FA esté habilitada

</details>

<details>
<summary>🗄️ Error: "Database locked"</summary>

```bash
# Eliminar base de datos corrupta
rm data/biblioteca.db
# Reiniciar aplicación
```

</details>

### **Logs y Soporte**

- **Logs generales**: `logs/bibliogest_YYYYMMDD.log`
- **Seguridad**: `logs/bibliogest_security.log`
- **Email**: `logs/bibliogest_email.log`

Para más ayuda, consulta [DEPLOYMENT.md](DEPLOYMENT.md) o reporta issues en GitHub.

---

## 📊 **Comparación de Versiones**

| Característica | v1.0 | v1.1 |
|----------------|------|------|
| 🔐 Seguridad | MD5 (básico) | bcrypt (empresarial) |
| 📧 Notificaciones | ❌ | ✅ Email HTML |
| 📋 Validaciones | Básicas | Avanzadas (DNI, ISBN) |
| 📊 Logging | ❌ | ✅ Estructurado |
| 🚀 Deployment | Manual | Automatizado |
| 📚 Campos Libros | 4 | 6 (+editorial, fecha) |
| 🎨 UX/UX | Funcional | Profesional |

---

## 🤝 **Contribución**

BiblioGest es un proyecto **open source**. Contribuciones son bienvenidas:

1. **Fork** el repositorio
2. **Crea** una rama para tu feature (`git checkout -b feature/amazing-feature`)
3. **Commit** tus cambios (`git commit -m 'Add amazing feature'`)
4. **Push** a la rama (`git push origin feature/amazing-feature`)
5. **Abre** un Pull Request

---

## 📜 **Licencia**

Este proyecto está bajo la **Licencia MIT**. Ver [LICENSE](LICENSE) para más detalles.

---

## 🙏 **Agradecimientos**

- **CustomTkinter** - Framework UI moderno
- **bcrypt** - Seguridad de contraseñas
- **Python Community** - Soporte y herramientas

---

## 📞 **Contacto y Soporte**

- **GitHub**: https://github.com/Xenon0001/bibliogest
- **Issues**: https://github.com/Xenon0001/bibliogest/issues
- **Email**: xenonpy465@gmail.com

---

## 🎉 **¡Gracias por usar BiblioGest!**

**BiblioGest v1.1** está listo para producción con seguridad empresarial, auditoría completa y experiencia de usuario profesional. 📚✨

---

*Última actualización: 2024-02-10 | Versión: 1.1.0 | Status: Production Ready*