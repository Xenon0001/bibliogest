import sys
import os

def resource_path(relative_path):
    """
    Obtiene la ruta absoluta de un recurso, funcionando para
    desarrollo (directorio normal) y para PyInstaller (un archivo temporal).
    """
    try:
        # PyInstaller crea un atributo temporal en sys
        base_path = sys._MEIPASS
    except Exception:
        # En modo normal, usa el path del archivo actual
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# La base de datos debe estar en la carpeta raíz del proyecto
DATABASE_PATH = resource_path("biblioteca.db")