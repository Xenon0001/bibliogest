"""
Módulo de seguridad mejorado para BiblioGest v1.1
Implementa hashing de contraseñas con bcrypt y logging de auditoría
"""
import bcrypt
import logging
import hashlib
import re
from typing import Tuple, Optional
from datetime import datetime

# Configurar logging de seguridad
security_logger = logging.getLogger('security')
security_logger.setLevel(logging.INFO)

# Crear handler para archivo si no existe
if not security_logger.handlers:
    file_handler = logging.FileHandler('biblioteca_security.log', encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # Formato detallado para auditoría
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    file_handler.setFormatter(formatter)
    security_logger.addHandler(file_handler)

class PasswordSecurity:
    """Clase para manejo seguro de contraseñas con bcrypt"""
    
    @staticmethod
    def hash_password(password: str) -> bytes:
        """
        Genera un hash seguro de la contraseña usando bcrypt con salt automático
        
        Args:
            password: Contraseña en texto plano
            
        Returns:
            Hash de la contraseña como bytes
        """
        try:
            # Generar salt y hashear contraseña
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            
            security_logger.info(f"Contraseña hasheada exitosamente")
            return hashed
            
        except Exception as e:
            security_logger.error(f"Error al hashear contraseña: {str(e)}")
            raise
    
    @staticmethod
    def verify_password(password: str, hashed_password: bytes) -> bool:
        """
        Verifica si una contraseña coincide con el hash almacenado
        
        Args:
            password: Contraseña en texto plano a verificar
            hashed_password: Hash almacenado en la base de datos
            
        Returns:
            True si la contraseña es correcta, False en caso contrario
        """
        try:
            # Verificar contraseña
            password_bytes = password.encode('utf-8')
            result = bcrypt.checkpw(password_bytes, hashed_password)
            
            if result:
                security_logger.info("Verificación de contraseña exitosa")
            else:
                security_logger.warning("Intento de verificación de contraseña fallido")
                
            return result
            
        except Exception as e:
            security_logger.error(f"Error al verificar contraseña: {str(e)}")
            return False
    
    @staticmethod
    def validate_password_strength(password: str) -> Tuple[bool, str]:
        """
        Valida la fortaleza de una contraseña
        
        Args:
            password: Contraseña a validar
            
        Returns:
            Tuple[bool, str]: (es_valida, mensaje_error)
        """
        try:
            if len(password) < 8:
                return False, "La contraseña debe tener al menos 8 caracteres"
            
            if not re.search(r'[A-Z]', password):
                return False, "La contraseña debe contener al menos una mayúscula"
            
            if not re.search(r'[a-z]', password):
                return False, "La contraseña debe contener al menos una minúscula"
            
            if not re.search(r'\d', password):
                return False, "La contraseña debe contener al menos un número"
            
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                return False, "La contraseña debe contener al menos un carácter especial"
            
            security_logger.info("Validación de fortaleza de contraseña exitosa")
            return True, "Contraseña válida"
            
        except Exception as e:
            security_logger.error(f"Error en validación de contraseña: {str(e)}")
            return False, "Error al validar la contraseña"

def log_security_event(event_type: str, details: str, user_email: str = None):
    """
    Registra eventos de seguridad para auditoría
    
    Args:
        event_type: Tipo de evento (login, registro, error, etc.)
        details: Detalles del evento
        user_email: Email del usuario si aplica
    """
    try:
        user_info = f" - Usuario: {user_email}" if user_email else ""
        message = f"[{event_type.upper()}] {details}{user_info}"
        
        if event_type.lower() in ['login', 'registro']:
            security_logger.info(message)
        elif event_type.lower() in ['error', 'fallo']:
            security_logger.warning(message)
        else:
            security_logger.info(message)
            
    except Exception as e:
        print(f"Error al registrar evento de seguridad: {str(e)}")

def migrate_md5_to_bcrypt(md5_hash: str, new_password: str) -> bytes:
    """
    Función de migración para convertir hashes MD5 existentes a bcrypt
    
    Args:
        md5_hash: Hash MD5 existente
        new_password: Nueva contraseña en texto plano
        
    Returns:
        Nuevo hash bcrypt
    """
    try:
        # Verificar que el hash MD5 coincida con la contraseña actual
        current_md5 = hashlib.md5(new_password.encode('utf-8')).hexdigest()
        
        if current_md5 != md5_hash:
            security_logger.warning("Intento de migración con contraseña incorrecta")
            raise ValueError("La contraseña actual no coincide con el hash MD5")
        
        # Generar nuevo hash bcrypt
        new_hash = PasswordSecurity.hash_password(new_password)
        
        security_logger.info("Migración MD5 a bcrypt exitosa")
        return new_hash
        
    except Exception as e:
        security_logger.error(f"Error en migración MD5 a bcrypt: {str(e)}")
        raise
