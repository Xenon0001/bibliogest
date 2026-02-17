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

# La base de datos debe estar en la carpeta data/ para persistencia
def get_database_path():
    """
    Obtiene la ruta correcta para la base de datos persistente
    """
    try:
        # Si estamos en PyInstaller, usa la carpeta del ejecutable
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.abspath(".")
        
        # Crear carpeta data si no existe
        data_dir = os.path.join(base_dir, "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        return os.path.join(data_dir, "biblioteca.db")
    except Exception:
        # Fallback a carpeta actual
        return os.path.abspath("biblioteca.db")

DATABASE_PATH = get_database_path()