"""
Configuración centralizada de logging para BiblioGest v1.1
"""
import logging
import os
import sys
from datetime import datetime

def get_log_directory():
    """Obtiene el directorio correcto para logs persistentes"""
    try:
        # Si estamos en PyInstaller, usa la carpeta del ejecutable
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.abspath(".")
        
        # Crear carpeta logs si no existe
        log_dir = os.path.join(base_dir, "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        return log_dir
    except Exception:
        # Fallback a carpeta actual
        return "logs"
 
def setup_logging():
    """Configura el sistema de logging para producción"""
 
    # Crear directorio de logs si no existe
    log_dir = get_log_directory()
 
    # Configurar formato de logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
 
    # Logger principal de la aplicación
    app_logger = logging.getLogger('bibliogest')
    app_logger.setLevel(logging.INFO)
 
    # Handler para archivo general
    file_handler = logging.FileHandler(
        os.path.join(log_dir, f'bibliogest_{datetime.now().strftime("%Y%m%d")}.log'),
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    app_logger.addHandler(file_handler)
 
    # Logger de seguridad
    security_logger = logging.getLogger('bibliogest.security')
    security_logger.setLevel(logging.INFO)
 
    security_handler = logging.FileHandler(
        os.path.join(log_dir, 'bibliogest_security.log'),
        encoding='utf-8'
    )
    security_handler.setFormatter(formatter)
    security_logger.addHandler(security_handler)
 
    # Logger de email
    email_logger = logging.getLogger('bibliogest.email')
    email_logger.setLevel(logging.INFO)
 
    email_handler = logging.FileHandler(
        os.path.join(log_dir, 'bibliogest_email.log'),
        encoding='utf-8'
    )
    email_handler.setFormatter(formatter)
    email_logger.addHandler(email_handler)
 
    # Evitar duplicación de logs
    app_logger.propagate = False
    security_logger.propagate = False
    email_logger.propagate = False
 
    return app_logger, security_logger, email_logger
 
# Inicializar logging al importar
app_logger, security_logger, email_logger = setup_logging()