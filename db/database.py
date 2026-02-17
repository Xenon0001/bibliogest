"""
    Implementa la conexión a SQLite, inicialización de tablas, migraciones y operaciones CRUD genéricas.
    Utiliza el patrón de funciones para el acceso a datos.
"""
import sqlite3
import datetime
import logging
# Importamos la ruta dinámica que resuelve PyInstaller o entorno de desarrollo
from utils.path_utils import DATABASE_PATH 
from utils.security import PasswordSecurity, log_security_event
from utils.validators_enhanced import EnhancedValidators 

# La variable DB_FILE ya no es necesaria, usamos DATABASE_PATH

def inicializar_db():
    """Crea la base de datos y las tablas si no existen."""
    conn = None

    try:
        # Usa la ruta dinámica para la conexión
        conn = sqlite3.connect(DATABASE_PATH) 
        cursor = conn.cursor()

        cursor.execute("PRAGMA foreign_keys = ON;")

        schema_sql = """
        -- 1. Tabla de BIBLIOTECARIOS (Quienes gestionan)
        CREATE TABLE IF NOT EXISTS bibliotecarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE,
            password_hash TEXT NOT NULL
        );
        -- 2. Tabla de USUARIOS (Quienes piden libros)
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            dni TEXT UNIQUE NOT NULL,
            telefono TEXT
        );
        -- 3. Tabla de LIBROS
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            isbn TEXT UNIQUE,
            categoria TEXT,
            editorial TEXT,
            fecha_publicacion DATE,
            disponible INTEGER DEFAULT 1 -- 1: Disponible, 0: Prestado
        );
        -- 4. Tabla de PRESTAMOS (Relaciona usuarios y libros)
        CREATE TABLE IF NOT EXISTS prestamos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            libro_id INTEGER,
            fecha_prestamo DATE DEFAULT CURRENT_DATE,
            fecha_devolucion DATE NULL, -- Es NULL si está activo
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY (libro_id) REFERENCES libros(id)
        );
        """
        cursor.executescript(schema_sql)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ocurrió un error al crear las tablas: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def verificar_existencia_bibliotecarios():
    """Verifica si existe al menos un registro en la tabla 'bibliotecarios'."""
    conn = None
    try:
        # Usa la ruta dinámica para la conexión
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM bibliotecarios")
        conteo = cursor.fetchone()[0]
        return conteo > 0
    except sqlite3.OperationalError:
        print("Error: La tabla 'bibliotecarios' no existe. Ejecute inicializar_db() primero.")
        return False
    except Exception as e:
        print(f"Error inesperado al verificar bibliotecarios: {e}")
        return False
    finally:
        if conn:
            conn.close()

def registrar_bibliotecario(nombre, email, contrasena):
    """Registra un nuevo bibliotecario con seguridad mejorada."""
    conn = None
    try:
        # Validar email y contraseña
        if not EnhancedValidators.is_valid_email(email):
            log_security_event('registro_fallo', f'Email inválido: {email}', email)
            return False, "Email inválido"
        
        is_valid, msg = PasswordSecurity.validate_password_strength(contrasena)
        if not is_valid:
            log_security_event('registro_fallo', f'Contraseña débil: {msg}', email)
            return False, msg
        
        # Generar hash seguro
        password_hash = PasswordSecurity.hash_password(contrasena)
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO bibliotecarios (nombre, email, password_hash) VALUES (?, ?, ?)",
            (nombre, email, password_hash)
        )
        conn.commit()
        
        log_security_event('registro', f'Bibliotecario registrado: {nombre}', email)
        return True, "Registro exitoso"
        
    except sqlite3.IntegrityError:
        log_security_event('registro_fallo', f'Email duplicado: {email}', email)
        return False, "El email ya está registrado"
    except Exception as e:
        log_security_event('error', f'Error registrando bibliotecario: {str(e)}', email)
        return False, f"Error al registrar: {str(e)}"
    finally:
        if conn:
            conn.close()

def autenticar_bibliotecario(email, contrasena):
    """Autentica un bibliotecario con seguridad mejorada."""
    conn = None
    try:
        # Validar email primero
        if not EnhancedValidators.is_valid_email(email):
            log_security_event('login_fallo', f'Email inválido: {email}', email)
            return None, "Email inválido"
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Obtener hash almacenado
        cursor.execute("SELECT nombre, password_hash FROM bibliotecarios WHERE email = ?", (email,))
        resultado = cursor.fetchone()
        
        if not resultado:
            log_security_event('login_fallo', f'Email no encontrado: {email}', email)
            return None, "Credenciales incorrectas"
        
        nombre, stored_hash = resultado
        
        # Verificar contraseña
        if PasswordSecurity.verify_password(contrasena, stored_hash):
            log_security_event('login', f'Login exitoso: {nombre}', email)
            return nombre, "Autenticación exitosa"
        else:
            log_security_event('login_fallo', f'Contraseña incorrecta: {email}', email)
            return None, "Credenciales incorrectas"
            
    except Exception as e:
        log_security_event('error', f'Error autenticando bibliotecario: {str(e)}', email)
        return None, f"Error de autenticación: {str(e)}"
    finally:
        if conn:
            conn.close()

# -------------------------------------------------------------
# Funciones de Gestión de Libros
# -------------------------------------------------------------

def obtener_todos_los_libros():
    """Obtiene todos los libros con el estado de disponibilidad."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT isbn, titulo, autor, categoria, editorial, fecha_publicacion, disponible, id 
            FROM libros 
            ORDER BY titulo
        """)
        return cursor.fetchall()
    except Exception as e:
        log_security_event('error', f'Error obteniendo libros: {str(e)}')
        return []
    finally:
        if conn:
            conn.close()

def obtener_libro_por_isbn(isbn):
    """Obtiene un libro por su ISBN."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, isbn, titulo, disponible FROM libros WHERE isbn = ?", (isbn,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error al obtener libro por ISBN: {e}")
        return None
    finally:
        if conn:
            conn.close()

def obtener_libros_prestados_count():
    """Obtiene el número de libros actualmente prestados (disponible = 0)."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM libros WHERE disponible = 0")
        return cursor.fetchone()[0]
    except Exception as e:
        print(f"Error al contar libros prestados: {e}")
        return 0
    finally:
        if conn:
            conn.close()

def insertar_libro(titulo, autor, isbn, categoria, editorial=None, fecha_publicacion=None):
    """Inserta un nuevo libro en la base de datos con validación mejorada."""
    conn = None
    try:
        # Validar ISBN si se proporciona
        if isbn:
            is_valid, msg = EnhancedValidators.is_valid_isbn(isbn)
            if not is_valid:
                log_security_event('error', f'ISBN inválido: {isbn} - {msg}')
                return False, f"ISBN inválido: {msg}"
        
        # Validar fecha de publicación si se proporciona
        if fecha_publicacion:
            is_valid, msg = EnhancedValidators.is_valid_date(fecha_publicacion)
            if not is_valid:
                log_security_event('error', f'Fecha inválida: {fecha_publicacion} - {msg}')
                return False, f"Fecha de publicación inválida: {msg}"
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO libros (titulo, autor, isbn, categoria, editorial, fecha_publicacion) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (titulo, autor, isbn, categoria, editorial, fecha_publicacion))
        
        conn.commit()
        log_security_event('info', f'Libro insertado: {titulo} - {autor}')
        return True, "Libro agregado exitosamente"
        
    except sqlite3.IntegrityError as e:
        log_security_event('error', f'ISBN duplicado: {isbn}')
        return False, "El ISBN ya está registrado"
    except Exception as e:
        log_security_event('error', f'Error insertando libro: {str(e)}')
        return False, f"Error al insertar libro: {str(e)}"
    finally:
        if conn:
            conn.close()

def actualizar_libro(libro_id, titulo, autor, isbn, categoria, editorial=None, fecha_publicacion=None):
    """Actualiza la información de un libro existente."""
    conn = None
    try:
        # Validar ISBN si se proporciona
        if isbn:
            is_valid, msg = EnhancedValidators.is_valid_isbn(isbn)
            if not is_valid:
                log_security_event('error', f'ISBN inválido: {isbn} - {msg}')
                return False, f"ISBN inválido: {msg}"
        
        # Validar fecha de publicación si se proporciona
        if fecha_publicacion:
            is_valid, msg = EnhancedValidators.is_valid_date(fecha_publicacion)
            if not is_valid:
                log_security_event('error', f'Fecha inválida: {fecha_publicacion} - {msg}')
                return False, f"Fecha de publicación inválida: {msg}"
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE libros 
            SET titulo = ?, autor = ?, isbn = ?, categoria = ?, editorial = ?, fecha_publicacion = ? 
            WHERE id = ?
        """, (titulo, autor, isbn, categoria, editorial, fecha_publicacion, libro_id))
        
        conn.commit()
        log_security_event('info', f'Libro actualizado ID {libro_id}: {titulo}')
        return True, "Libro actualizado exitosamente"
        
    except sqlite3.IntegrityError as e:
        log_security_event('error', f'ISBN duplicado al actualizar: {isbn}')
        return False, "El ISBN ya está registrado en otro libro"
    except Exception as e:
        log_security_event('error', f'Error actualizando libro ID {libro_id}: {str(e)}')
        return False, f"Error al actualizar libro: {str(e)}"
    finally:
        if conn:
            conn.close()

def eliminar_libro(libro_id):
    """Elimina un libro de la base de datos. Solo si no está prestado activamente."""
    conn = None
    try:
        # Usa la ruta dinámica para la conexión
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Verificar si el libro está prestado activamente
        cursor.execute("SELECT disponible FROM libros WHERE id = ?", (libro_id,))
        is_available = cursor.fetchone()
        
        # Si no existe o está prestado (disponible == 0), no se elimina
        if is_available is None or is_available[0] == 0:
            return False 

        cursor.execute("DELETE FROM libros WHERE id = ?", (libro_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al eliminar libro ID {libro_id}: {e}")
        return False
    finally:
        if conn:
            conn.close()
            
# -------------------------------------------------------------
# Funciones de Gestión de Usuarios (Lectores)
# -------------------------------------------------------------

def obtener_todos_los_usuarios():
    """Obtiene todos los usuarios y el conteo de libros prestados activamente por cada uno."""
    conn = None
    try:
        # Usa la ruta dinámica para la conexión
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        query = """
        SELECT 
            u.id, 
            u.nombre, 
            u.dni, 
            u.telefono,
            COUNT(p.libro_id) AS libros_prestados_activos
        FROM usuarios u
        LEFT JOIN prestamos p ON u.id = p.usuario_id AND p.fecha_devolucion IS NULL
        GROUP BY u.id, u.nombre, u.dni, u.telefono
        ORDER BY u.nombre
        """
        cursor.execute(query)
        # Retorna: (id, nombre, dni, telefono, libros_prestados_activos)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return []
    finally:
        if conn:
            conn.close()

def obtener_usuario_por_dni(dni):
    """Obtiene un usuario por su DNI. Retorna (id, nombre, dni, telefono) o None."""
    conn = None
    try:
        # Usa la ruta dinámica para la conexión
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, dni, telefono FROM usuarios WHERE dni = ?", (dni,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error al obtener usuario por DNI: {e}")
        return None
    finally:
        if conn:
            conn.close()

def obtener_usuario_por_id(user_id):
    """Obtiene un usuario por su ID. Retorna (id, nombre, dni, telefono) o None."""
    conn = None
    try:
        # Usa la ruta dinámica para la conexión
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, dni, telefono FROM usuarios WHERE id = ?", (user_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error al obtener usuario por ID: {e}")
        return None
    finally:
        if conn:
            conn.close()
            
def insertar_usuario(nombre, dni, telefono):
    """Inserta un nuevo usuario (lector)."""
    conn = None
    try:
        # Usa la ruta dinámica para la conexión
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, dni, telefono) VALUES (?, ?, ?)",
            (nombre, dni, telefono)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False # DNI duplicado
    except Exception as e:
        print(f"Error al insertar usuario: {e}")
        return False
    finally:
        if conn:
            conn.close()

def actualizar_usuario(user_id, nombre, telefono):
    """Actualiza la información de un usuario existente."""
    conn = None
    try:
        # Usa la ruta dinámica para la conexión
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE usuarios SET nombre = ?, telefono = ? WHERE id = ?",
            (nombre, telefono, user_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al actualizar usuario ID {user_id}: {e}")
        return False
    finally:
        if conn:
            conn.close()

def eliminar_usuario(user_id):
    """Elimina un usuario. Solo si no tiene libros prestados activamente."""
    conn = None
    try:
        # Usa la ruta dinámica para la conexión
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # 1. Contar préstamos activos
        cursor.execute("SELECT COUNT(*) FROM prestamos WHERE usuario_id = ? AND fecha_devolucion IS NULL", (user_id,))
        active_loans = cursor.fetchone()[0]

        if active_loans > 0:
            return False # No se puede eliminar si tiene préstamos activos

        # 2. Eliminar usuario
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al eliminar usuario ID {user_id}: {e}")
        return False
    finally:
        if conn:
            conn.close()
            
# -------------------------------------------------------------
# Funciones de Gestión de Préstamos
# -------------------------------------------------------------

def registrar_prestamo(usuario_id, libro_id):
    """Registra un nuevo préstamo y actualiza el estado del libro."""
    conn = None
    try:
        # Usa la ruta dinámica para la conexión
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # 1. Registrar el préstamo
        fecha_prestamo = datetime.date.today().strftime("%Y-%m-%d")
        cursor.execute(
            "INSERT INTO prestamos (usuario_id, libro_id, fecha_prestamo) VALUES (?, ?, ?)",
            (usuario_id, libro_id, fecha_prestamo)
        )
        
        # 2. Actualizar el estado del libro a NO DISPONIBLE (0)
        cursor.execute(
            "UPDATE libros SET disponible = 0 WHERE id = ?",
            (libro_id,)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al registrar préstamo: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def registrar_devolucion(prestamo_id, libro_id):
    """Registra la devolución de un libro y actualiza su estado."""
    conn = None
    try:
        # Usa la ruta dinámica para la conexión
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # 1. Registrar la fecha de devolución en la tabla de préstamos
        fecha_devolucion = datetime.date.today().strftime("%Y-%m-%d")
        cursor.execute(
            "UPDATE prestamos SET fecha_devolucion = ? WHERE id = ?",
            (fecha_devolucion, prestamo_id)
        )

        # 2. Actualizar el estado del libro a DISPONIBLE (1)
        cursor.execute(
            "UPDATE libros SET disponible = 1 WHERE id = ?",
            (libro_id,)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al registrar devolución: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def obtener_prestamos_activos():
    """Obtiene una lista de todos los préstamos que aún no tienen fecha_devolucion."""
    conn = None
    try:
        # Usa la ruta dinámica para la conexión
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        query = """
        SELECT 
            p.id, 
            l.titulo, 
            u.nombre, 
            u.dni, 
            p.fecha_prestamo,
            l.id as libro_id
        FROM prestamos p
        JOIN libros l ON p.libro_id = l.id
        JOIN usuarios u ON p.usuario_id = u.id
        WHERE p.fecha_devolucion IS NULL
        ORDER BY p.fecha_prestamo DESC
        """
        cursor.execute(query)
        # Retorna: (prestamo_id, titulo, nombre_usuario, dni_usuario, fecha_prestamo, libro_id)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener préstamos activos: {e}")
        return []
    finally:
        if conn:
            conn.close()
    
# NOTA: La inicialización de la base de datos ahora se maneja explícitamente en main.py
# para evitar inicializaciones automáticas al importar el módulo.