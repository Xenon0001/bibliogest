"""
    Implementa la conexión a SQLite, inicialización de tablas, migraciones y operaciones CRUD genéricas.
    Utiliza el patrón Repository para desacoplar la lógica de acceso a datos.
"""
import sqlite3
import os
import hashlib
import datetime

DB_FILE = "biblioteca.db"

def obtener_hash(contrasena):
    """Genera el hash MD5 de una contraseña."""
    return hashlib.md5(contrasena.encode('utf-8')).hexdigest()

def inicializar_db():
    """Crea la base de datos y las tablas si no existen."""
    conn = None

    try:
        conn = sqlite3.connect(DB_FILE)
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
        conn = sqlite3.connect(DB_FILE)
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
    """Registra un nuevo bibliotecario y devuelve True si tiene éxito."""
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        password_hash = obtener_hash(contrasena)
        
        cursor.execute(
            "INSERT INTO bibliotecarios (nombre, email, password_hash) VALUES (?, ?, ?)",
            (nombre, email, password_hash)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception as e:
        print(f"Error al registrar bibliotecario: {e}")
        return False
    finally:
        if conn:
            conn.close()

def autenticar_bibliotecario(email, contrasena):
    """Autentica un bibliotecario y devuelve su nombre si tiene éxito."""
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        password_hash = obtener_hash(contrasena)

        cursor.execute(
            "SELECT nombre FROM bibliotecarios WHERE email = ? AND password_hash = ?",
            (email, password_hash)
        )
        resultado = cursor.fetchone()
        
        if resultado:
            return resultado[0] # Retorna el nombre del bibliotecario
        else:
            return None # Credenciales inválidas
            
    except Exception as e:
        print(f"Error al autenticar bibliotecario: {e}")
        return None
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
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT isbn, titulo, autor, categoria, disponible, id FROM libros")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener libros: {e}")
        return []
    finally:
        if conn:
            conn.close()

def obtener_libro_por_isbn(isbn):
    """Obtiene un libro por su ISBN."""
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
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
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM libros WHERE disponible = 0")
        return cursor.fetchone()[0]
    except Exception as e:
        print(f"Error al contar libros prestados: {e}")
        return 0
    finally:
        if conn:
            conn.close()

def insertar_libro(titulo, autor, isbn, categoria):
    """Inserta un nuevo libro en la base de datos."""
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO libros (titulo, autor, isbn, categoria) VALUES (?, ?, ?, ?)",
            (titulo, autor, isbn, categoria)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception as e:
        print(f"Error al insertar libro: {e}")
        return False
    finally:
        if conn:
            conn.close()

def actualizar_libro(libro_id, titulo, autor, isbn, categoria):
    """Actualiza la información de un libro existente."""
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE libros SET titulo = ?, autor = ?, isbn = ?, categoria = ? WHERE id = ?",
            (titulo, autor, isbn, categoria, libro_id)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception as e:
        print(f"Error al actualizar libro ID {libro_id}: {e}")
        return False
    finally:
        if conn:
            conn.close()

def eliminar_libro(libro_id):
    """Elimina un libro de la base de datos. Solo si no tiene prestamos activos."""
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Verificar si el libro está prestado activamente
        cursor.execute("SELECT disponible FROM libros WHERE id = ?", (libro_id,))
        is_available = cursor.fetchone()
        
        if is_available is None or is_available[0] == 0:
            return False # No existe o está prestado

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
        conn = sqlite3.connect(DB_FILE)
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
        conn = sqlite3.connect(DB_FILE)
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
        conn = sqlite3.connect(DB_FILE)
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
        conn = sqlite3.connect(DB_FILE)
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
        conn = sqlite3.connect(DB_FILE)
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
        conn = sqlite3.connect(DB_FILE)
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
        conn = sqlite3.connect(DB_FILE)
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
        conn = sqlite3.connect(DB_FILE)
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
        conn = sqlite3.connect(DB_FILE)
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
    
# Llamamos a la función
# if __name__ == "__main__":
#     inicializar_db()