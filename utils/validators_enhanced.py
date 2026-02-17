"""
Módulo de validaciones mejoradas para BiblioGest v1.1
Incluye validación de DNI español, ISBN-10/13 y otros formatos
"""
import re
import logging
from typing import Tuple, Optional

logger = logging.getLogger('validators')

class EnhancedValidators:
    """Clase con validaciones mejoradas para el sistema bibliotecario"""
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Valida formato de correo electrónico con regex mejorada
        
        Args:
            email: Correo electrónico a validar
            
        Returns:
            True si el formato es válido
        """
        try:
            # Regex más estricta para validación de email
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.fullmatch(email_regex, email):
                logger.info(f"Email válido: {email[:3]}***@{email.split('@')[1]}")
                return True
            else:
                logger.warning(f"Email inválido: {email}")
                return False
        except Exception as e:
            logger.error(f"Error validando email: {str(e)}")
            return False
    
    @staticmethod
    def is_valid_spanish_dni(dni: str) -> Tuple[bool, str]:
        """
        Valida DNI español (formato 8 dígitos + letra)
        
        Args:
            dni: DNI a validar
            
        Returns:
            Tuple[bool, str]: (es_valido, mensaje_error)
        """
        try:
            # Limpiar el DNI (quitar espacios, guiones, etc.)
            dni_clean = dni.upper().replace(' ', '').replace('-', '')
            
            # Verificar formato básico
            if not re.match(r'^\d{8}[A-Z]$', dni_clean):
                return False, "Formato inválido. Debe ser 8 dígitos seguidos de una letra (Ej: 12345678Z)"
            
            # Extraer números y letra
            numeros = int(dni_clean[:8])
            letra = dni_clean[8]
            
            # Calcular letra correcta
            letras = 'TRWAGMYFPDXBNJZSQVHLCKE'
            letra_correcta = letras[numeros % 23]
            
            if letra != letra_correcta:
                return False, f"Letra incorrecta. La letra correcta sería {letra_correcta}"
            
            logger.info(f"DNI válido: {dni_clean[:3]}***{dni_clean[-1]}")
            return True, "DNI válido"
            
        except ValueError:
            return False, "El DNI debe contener exactamente 8 números seguidos de una letra"
        except Exception as e:
            logger.error(f"Error validando DNI: {str(e)}")
            return False, "Error al validar DNI"
    
    @staticmethod
    def is_valid_isbn(isbn: str) -> Tuple[bool, str]:
        """
        Valida ISBN-10 o ISBN-13
        
        Args:
            isbn: ISBN a validar
            
        Returns:
            Tuple[bool, str]: (es_valido, mensaje_error)
        """
        try:
            # Limpiar ISBN (quitar guiones, espacios)
            isbn_clean = isbn.replace('-', '').replace(' ', '')
            
            # Validar ISBN-10
            if len(isbn_clean) == 10:
                return EnhancedValidators._validate_isbn10(isbn_clean)
            
            # Validar ISBN-13
            elif len(isbn_clean) == 13:
                return EnhancedValidators._validate_isbn13(isbn_clean)
            
            else:
                return False, "El ISBN debe tener 10 o 13 dígitos"
                
        except Exception as e:
            logger.error(f"Error validando ISBN: {str(e)}")
            return False, "Error al validar ISBN"
    
    @staticmethod
    def _validate_isbn10(isbn: str) -> Tuple[bool, str]:
        """Valida ISBN-10"""
        try:
            # Verificar que los primeros 9 caracteres sean dígitos
            if not re.match(r'^\d{9}[0-9X]$', isbn):
                return False, "ISBN-10 inválido. Debe ser 9 dígitos seguidos de un dígito o X"
            
            # Calcular checksum
            total = 0
            for i in range(9):
                total += int(isbn[i]) * (10 - i)
            
            # El último dígito puede ser X (valor 10)
            last_char = isbn[9]
            if last_char == 'X':
                total += 10
            else:
                total += int(last_char)
            
            if total % 11 == 0:
                logger.info(f"ISBN-10 válido: {isbn[:3]}***{isbn[-1]}")
                return True, "ISBN-10 válido"
            else:
                return False, "ISBN-10 inválido: checksum incorrecto"
                
        except Exception as e:
            logger.error(f"Error validando ISBN-10: {str(e)}")
            return False, "Error al validar ISBN-10"
    
    @staticmethod
    def _validate_isbn13(isbn: str) -> Tuple[bool, str]:
        """Valida ISBN-13"""
        try:
            # Verificar que todos los caracteres sean dígitos
            if not isbn.isdigit():
                return False, "ISBN-13 inválido. Debe contener solo dígitos"
            
            # Calcular checksum
            total = 0
            for i in range(12):
                digit = int(isbn[i])
                if i % 2 == 0:
                    total += digit
                else:
                    total += digit * 3
            
            checksum = (10 - (total % 10)) % 10
            
            if checksum == int(isbn[12]):
                logger.info(f"ISBN-13 válido: {isbn[:3]}***{isbn[-1]}")
                return True, "ISBN-13 válido"
            else:
                return False, f"ISBN-13 inválido: checksum incorrecto (esperado: {checksum})"
                
        except Exception as e:
            logger.error(f"Error validando ISBN-13: {str(e)}")
            return False, "Error al validar ISBN-13"
    
    @staticmethod
    def is_valid_phone(phone: str) -> Tuple[bool, str]:
        """
        Valida número de teléfono español
        
        Args:
            phone: Teléfono a validar
            
        Returns:
            Tuple[bool, str]: (es_valido, mensaje_error)
        """
        try:
            # Limpiar teléfono
            phone_clean = phone.replace(' ', '').replace('-', '').replace('+', '')
            
            # Validar formato español (9 dígitos empezando por 6, 7, 8 o 9)
            if re.match(r'^[6789]\d{8}$', phone_clean):
                logger.info(f"Teléfono válido: {phone_clean[:3]}***{phone_clean[-2:]}")
                return True, "Teléfono válido"
            else:
                return False, "Teléfono inválido. Debe empezar por 6, 7, 8 o 9 y tener 9 dígitos"
                
        except Exception as e:
            logger.error(f"Error validando teléfono: {str(e)}")
            return False, "Error al validar teléfono"
    
    @staticmethod
    def is_valid_date(date_str: str) -> Tuple[bool, str]:
        """
        Valida formato de fecha YYYY-MM-DD
        
        Args:
            date_str: Fecha a validar
            
        Returns:
            Tuple[bool, str]: (es_valida, mensaje_error)
        """
        try:
            from datetime import datetime
            
            # Intentar parsear la fecha
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            
            # Verificar que la fecha no sea futura (para fecha de publicación)
            current_date = datetime.now()
            if date_obj > current_date:
                return False, "La fecha no puede ser futura"
            
            # Verificar que la fecha no sea muy antigua (libros muy antiguos)
            if date_obj.year < 1450:  # Invención de la imprenta
                return False, "La fecha de publicación no puede ser anterior a 1450"
            
            logger.info(f"Fecha válida: {date_str}")
            return True, "Fecha válida"
            
        except ValueError:
            return False, "Formato de fecha inválido. Use YYYY-MM-DD"
        except Exception as e:
            logger.error(f"Error validando fecha: {str(e)}")
            return False, "Error al validar fecha"

# Funciones de compatibilidad con el código existente
def is_valid_email(email: str) -> bool:
    """Función de compatibilidad para el código existente"""
    return EnhancedValidators.is_valid_email(email)

def is_valid_dni(dni: str) -> bool:
    """Función de compatibilidad mejorada para DNI"""
    is_valid, _ = EnhancedValidators.is_valid_spanish_dni(dni)
    return is_valid
