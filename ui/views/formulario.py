import customtkinter as ctk
import time
from threading import Thread

# Importamos la lógica de la base de datos
from db.database import autenticar_bibliotecario, registrar_bibliotecario, verificar_existencia_bibliotecarios

# Importamos el widget de mensaje
from ui.widgets.error import CustomMessage

# Importamos la validación de utilidades
from utils.validation import is_valid_email # <-- NUEVA IMPORTACIÓN

# Importamos la App principal (que aún vamos a crear en app.py)
# Necesitamos la clase para poder hacer la transición
from ui.views.app import App 

# ----------------------------------------------------------------------
# CLASE BASE PARA EL FRAME DE CARGA
# ----------------------------------------------------------------------

class CargaBienvenidaFrame(ctk.CTkFrame):
    """Frame que muestra la bienvenida y simula una carga antes de iniciar la App."""
    def __init__(self, master, username):
        super().__init__(master, corner_radius=10)
        self.master = master
        self.username = username
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        # 1. Título de bienvenida
        self.label_bienvenida = ctk.CTkLabel(
            self, 
            text=f"¡Bienvenido, {self.username}!", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#10B981" # Un verde agradable para éxito
        )
        self.label_bienvenida.grid(row=0, column=0, pady=(50, 10), sticky="nsew")

        # 2. Barra de progreso (simulación de carga)
        self.progress_bar = ctk.CTkProgressBar(self, orientation="horizontal")
        self.progress_bar.set(0)
        self.progress_bar.grid(row=1, column=0, pady=(10, 50), padx=40, sticky="ew")

        # Iniciamos la simulación de carga en un hilo
        Thread(target=self.simular_carga).start()

    def update_progress(self, i):
        """Actualiza la barra de progreso en el hilo principal de CTk."""
        self.progress_bar.set(i / 10)
        if i < 10:
            # Llama a sí misma después de 200ms para simular el progreso
            self.master.after(200, lambda: self.update_progress(i + 1))
        else:
            # Lanza la aplicación cuando la carga termina
            self.master.lanzar_app(self.username)

    def simular_carga(self):
        """Inicia la actualización de la interfaz de forma segura en el hilo principal."""
        # Solo iniciamos la cadena de llamadas 'after' en el hilo principal
        self.master.after(200, lambda: self.update_progress(1))


# ----------------------------------------------------------------------
# CLASE LOGIN
# ----------------------------------------------------------------------

class LoginFrame(ctk.CTkFrame):
    """Frame del formulario de inicio de sesión."""
    def __init__(self, master):
        super().__init__(master, corner_radius=10)
        self.master = master
        
        
        self.grid_columnconfigure(0, weight=1)
        
        # Título
        ctk.CTkLabel(
            self, 
            text="Iniciar Sesión", 
            font=ctk.CTkFont(size=24, weight="bold")
        ).grid(row=0, column=0, pady=20, padx=20, sticky="ew")

        # Entry de Email
        ctk.CTkLabel(self, text="Email:").grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")
        self.email_entry = ctk.CTkEntry(self, placeholder_text="bibliotecario@ejemplo.com")
        self.email_entry.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Entry de Contraseña
        ctk.CTkLabel(self, text="Contraseña:").grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")
        self.password_entry = ctk.CTkEntry(self, show="*", placeholder_text="Contraseña")
        self.password_entry.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Botón de Login
        self.login_button = ctk.CTkButton(self, text="Acceder", command=self.validar_login)
        self.login_button.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="ew")

    def validar_login(self):
        email = self.email_entry.get().strip()
        contrasena = self.password_entry.get().strip()

        # 1. Validación de campos vacíos
        if not email or not contrasena:
            CustomMessage(self.master, "Error de Validación", "Por favor, rellena todos los campos.", is_error=True)
            return
        
        # 2. Validación de formato de email (USANDO utils/validation.py)
        if not is_valid_email(email):
            CustomMessage(self.master, "Error de Validación", "El formato del correo electrónico no es válido.", is_error=True)
            return

        # 3. Autenticación en la DB
        nombre_usuario = autenticar_bibliotecario(email, contrasena)

        if nombre_usuario:
            # ÉXITO: Ocultamos el Login y mostramos la Carga/Bienvenida
            self.master.mostrar_carga_bienvenida(nombre_usuario)
        else:
            # ERROR: Credenciales inválidas
            CustomMessage(self.master, "Error de Autenticación", "Email o contraseña incorrectos.", is_error=True)


# ----------------------------------------------------------------------
# CLASE REGISTRO
# ----------------------------------------------------------------------

class RegistroFrame(ctk.CTkFrame):
    """Frame del formulario de Registro (usado para el primer bibliotecario)."""
    def __init__(self, master):
        super().__init__(master, corner_radius=10)
        self.master = master
        
        self.grid_columnconfigure(0, weight=1)
        
        # Título
        ctk.CTkLabel(
            self, 
            text="Registro (Primer Bibliotecario)", 
            font=ctk.CTkFont(size=24, weight="bold")
        ).grid(row=0, column=0, pady=20, padx=20, sticky="ew")

        # Entry de Nombre
        ctk.CTkLabel(self, text="Nombre:").grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")
        self.nombre_entry = ctk.CTkEntry(self, placeholder_text="Tu Nombre Completo")
        self.nombre_entry.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Entry de Email
        ctk.CTkLabel(self, text="Email (Será tu usuario):").grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")
        self.email_entry = ctk.CTkEntry(self, placeholder_text="bibliotecario@ejemplo.com")
        self.email_entry.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Entry de Contraseña
        ctk.CTkLabel(self, text="Contraseña:").grid(row=5, column=0, padx=20, pady=(10, 0), sticky="w")
        self.password_entry = ctk.CTkEntry(self, show="*", placeholder_text="Contraseña Segura")
        self.password_entry.grid(row=6, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Botón de Registro
        self.registro_button = ctk.CTkButton(self, text="Registrar y Continuar", command=self.validar_registro)
        self.registro_button.grid(row=7, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        # FIX TclError: Implementar enfoque seguro y retardado al primer campo
        self.after(100, self._safe_focus)

    def _safe_focus(self):
        """Intenta establecer el foco en el campo Nombre de forma segura."""
        try:
            self.nombre_entry.focus_set()
        except Exception as e:
            # Ignoramos la excepción si el widget ya fue destruido.
            pass

    def validar_registro(self):
        nombre = self.nombre_entry.get().strip()
        email = self.email_entry.get().strip()
        contrasena = self.password_entry.get().strip()

        # 1. Validación de campos vacíos
        if not nombre or not email or not contrasena:
            CustomMessage(self.master, "Error de Validación", "Debes rellenar todos los campos.", is_error=True)
            return
        
        # 2. Validación de formato de email (USANDO utils/validation.py)
        if not is_valid_email(email):
            CustomMessage(self.master, "Error de Validación", "El formato del correo electrónico no es válido.", is_error=True)
            return
        
        # 3. Validación de contraseña mínima
        if len(contrasena) < 6:
             CustomMessage(self.master, "Error de Validación", "La contraseña debe tener al menos 6 caracteres.", is_error=True)
             return

        # 4. Registro en la DB
        if registrar_bibliotecario(nombre, email, contrasena):
            
            # Definimos el callback para la transición, que solo se ejecuta al presionar Aceptar
            def on_registro_success():
                # Esta función se ejecutará DESPUÉS de cerrar el CustomMessage
                self.master.mostrar_carga_bienvenida(nombre)
            
            # ÉXITO: El usuario fue registrado.
            CustomMessage(
                self.master, 
                "Registro Exitoso", 
                f"Bienvenido, {nombre}. Iniciando aplicación.", 
                is_error=False, 
                callback=on_registro_success
            )
            
        else:
            # ERROR: Generalmente por email duplicado
            CustomMessage(self.master, "Error de Registro", "El email ya está registrado o hubo un error interno.", is_error=True)

# ----------------------------------------------------------------------
# CLASE MAINWINDOW (Contenedor de Vistas)
# ----------------------------------------------------------------------

class FormularioMainWindow(ctk.CTk):
    """
    Ventana principal que gestiona la vista actual (Login, Registro o Carga).
    """
    def __init__(self, debe_registrar):
        super().__init__()
        self.title("Sistema de Gestión Bibliotecaria")
        self.geometry("400x500")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.current_frame = None
        self.debe_registrar = debe_registrar
        
        # Inicializar la primera vista
        if self.debe_registrar:
            self.mostrar_registro()
        else:
            self.mostrar_login()

    def mostrar_frame(self, frame_class):
        """Función genérica para cambiar el frame actual."""
        # Destruir el frame anterior si existe
        if self.current_frame:
            self.current_frame.destroy()
            
        # Crear el nuevo frame
        new_frame = frame_class(self)
        new_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.current_frame = new_frame

    def mostrar_login(self):
        """Muestra la vista de Login."""
        self.mostrar_frame(LoginFrame)

    def mostrar_registro(self):
        """Muestra la vista de Registro."""
        self.mostrar_frame(RegistroFrame)
        
    def mostrar_carga_bienvenida(self, username):
        """Muestra la interfaz de carga y bienvenida."""
        self.mostrar_frame(lambda master: CargaBienvenidaFrame(master, username))

    def lanzar_app(self, username):
        """
        Lanza la aplicación principal (App.py).
        
        CORRECCIÓN: Usamos 'withdraw' para ocultar la ventana actual antes de 
        lanzar la nueva App. Esto previene el error TclError al intentar 
        destruir la ventana mientras hay callbacks pendientes (como el foco).
        """
        
        # 1. Ocultamos la ventana actual inmediatamente
        self.withdraw()
        
        # 2. Abrimos la ventana de la aplicación principal
        app = App(username=username) # Creamos la nueva ventana
        app.mainloop() # La App principal toma el control y se bloquea aquí

        # 3. Después de que app.mainloop() retorna (es decir, el usuario cerró la App principal), 
        # cerramos completamente la ventana de formulario.
        # Ya que la App principal tiene el sys.exit() en su on_closing, 
        # esta línea solo se ejecutaría si se cerrara sin usar la "X" del sistema, 
        # pero la mantenemos para asegurar la limpieza del objeto.
        self.destroy()

# ----------------------------------------------------------------------
# FUNCIONES DE ARRANQUE PARA MAIN.PY
# ----------------------------------------------------------------------

def iniciar_formulario(debe_registrar):
    """
    Función llamada desde main.py para iniciar la ventana.
    :param debe_registrar: True si se debe mostrar el Registro, False para Login.
    """
    app = FormularioMainWindow(debe_registrar)
    app.mainloop()