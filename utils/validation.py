import re

# Expresión regular estándar para la validación de correos electrónicos
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def is_valid_email(email: str) -> bool:
    """
    Verifica si una cadena de texto es un formato de correo electrónico válido.

    Args:
        email: La cadena de texto a validar.

    Returns:
        True si la cadena coincide con el formato de correo electrónico, False en caso contrario.
    """
    if re.fullmatch(EMAIL_REGEX, email):
        return True
    return False

def is_valid_dni(dni: str) -> bool:
    """
    Función de marcador de posición para validar DNI/identificación.
    Debe implementarse según el formato específico del país (por ejemplo, longitud, dígito de control).
    Por ahora, solo verifica que no esté vacío.
    """
    return bool(dni.strip())

# Se pueden agregar más funciones de validación aquí (contraseñas, números de teléfono, etc.)