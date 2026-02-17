"""
Configuración centralizada para BiblioGest v1.1
"""
from .logging_config import setup_logging, app_logger, security_logger, email_logger

__all__ = ['setup_logging', 'app_logger', 'security_logger', 'email_logger']
