import os

# --- Directorios y Rutas ---
# La ruta del directorio base de la aplicación.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta a la base de datos SQLite.
# Se guarda en la carpeta principal del proyecto.
DATABASE_PATH = os.path.join(BASE_DIR, 'biblioteca.db')


# --- Constantes de la Aplicación ---
APP_TITLE = "Sistema de Gestión Bibliotecaria"
APP_VERSION = "1.0.0"

# --- Configuración de UI (Opcional, pero útil) ---
DEFAULT_THEME = "dark" # "light" o "dark"
DEFAULT_COLOR_THEME = "blue" # Colores de CTK

# Mínimo de caracteres requerido para una contraseña
MIN_PASSWORD_LENGTH = 6