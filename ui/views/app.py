import customtkinter as ctk
import sys
import datetime

# Importación de las vistas dinámicas (Asegurada)
from ui.views.biblioteca import BibliotecaView
from ui.views.usuarios import UsuariosView
from ui.views.historial import HistorialView

class TopFrame(ctk.CTkFrame):
    """Frame superior que contiene el nombre de usuario, el menú y la hora/fecha."""
    def __init__(self, master, username, change_view_callback):
        super().__init__(master, height=80, corner_radius=0)
        self.username = username
        self.change_view_callback = change_view_callback
        
        # Grid Configuration: 3 Columnas (Usuario, Menú, Hora)
        self.grid_columnconfigure(0, weight=1) # Usuario a la izquierda
        self.grid_columnconfigure(1, weight=3) # Menú central
        self.grid_columnconfigure(2, weight=1) # Hora a la derecha
        self.grid_rowconfigure(0, weight=1)

        self._create_user_label()
        self._create_navigation_menu()
        self._create_time_widget()

        # Inicia la actualización de la hora
        self.update_time()

    def _create_user_label(self):
        """Etiqueta del nombre del usuario (Izquierda)."""
        ctk.CTkLabel(
            self,
            text=f"Bienvenido: {self.username}",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).grid(row=0, column=0, padx=20, pady=10, sticky="w")

    def _create_navigation_menu(self):
        """Menú de navegación (Centro)."""
        menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        menu_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        views = ["Biblioteca", "Usuarios", "Historial"]
        
        for i, view_name in enumerate(views):
            menu_frame.grid_columnconfigure(i, weight=1)
            
            button = ctk.CTkButton(
                menu_frame,
                text=view_name,
                # La callback se llama con el nombre de la vista
                command=lambda name=view_name: self.change_view_callback(name),
                corner_radius=8,
                fg_color="#3B82F6",
                hover_color="#2563EB"
            )
            button.grid(row=0, column=i, padx=10, sticky="ew")

    def _create_time_widget(self):
        """Widget de fecha y hora (Derecha)."""
        time_frame = ctk.CTkFrame(self, fg_color="transparent")
        time_frame.grid(row=0, column=2, padx=20, pady=5, sticky="e")
        
        # Fecha
        self.date_label = ctk.CTkLabel(
            time_frame, 
            text="", 
            font=ctk.CTkFont(size=12)
        )
        self.date_label.pack(side="top", anchor="e")

        # Hora (más destacada)
        self.time_label = ctk.CTkLabel(
            time_frame, 
            text="", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.time_label.pack(side="top", anchor="e")

    def update_time(self):
        """Actualiza la hora y fecha cada segundo."""
        now = datetime.datetime.now()
        
        fecha_str = now.strftime("%d/%m/%Y")
        hora_str = now.strftime("%H:%M:%S")

        self.date_label.configure(text=fecha_str)
        self.time_label.configure(text=hora_str)

        # Llama a esta función de nuevo después de 1000ms (1 segundo)
        self.after(1000, self.update_time)


class App(ctk.CTk):
    """
    Ventana principal de la aplicación de biblioteca.
    Actúa como contenedor y router de las vistas.
    """
    VIEW_MAP = {
        "Biblioteca": BibliotecaView,
        "Usuarios": UsuariosView,
        "Historial": HistorialView,
    }

    def __init__(self, username):
        super().__init__()
        self.title(f"Sistema Bibliotecario - Sesión de {username}")
        self.geometry("1000x700")
        self.username = username

        # ** Estructura de la aplicación: 2 filas **
        self.grid_rowconfigure(0, weight=0) # Fila TOP fija
        self.grid_rowconfigure(1, weight=1) # Fila DYNAMIC expandible
        self.grid_columnconfigure(0, weight=1)

        # 1. TOP FRAME (Fijo)
        self.top_frame = TopFrame(self, self.username, self.change_view)
        self.top_frame.grid(row=0, column=0, sticky="ew")

        # 2. DYNAMIC FRAME (Contenedor de Vistas)
        self.dynamic_container = ctk.CTkFrame(self, fg_color="transparent")
        self.dynamic_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.dynamic_container.grid_columnconfigure(0, weight=1)
        self.dynamic_container.grid_rowconfigure(0, weight=1)
        
        self.current_view = None
        
        # Iniciar con la vista por defecto (Biblioteca)
        self.change_view("Biblioteca")

        # Configuración de protocolo de cierre
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def change_view(self, view_name):
        """Cambia la vista dinámica en el contenedor central."""
        view_class = self.VIEW_MAP.get(view_name)
        if not view_class:
            print(f"Error: Vista '{view_name}' no encontrada.")
            return

        # Destruir la vista anterior si existe
        if self.current_view:
            self.current_view.destroy()
            
        # Crear e insertar la nueva vista
        new_view = view_class(self.dynamic_container)
        new_view.grid(row=0, column=0, sticky="nsew")
        self.current_view = new_view

    def on_closing(self):
        """Maneja el cierre de la ventana principal y termina la aplicación."""
        import sys
        self.destroy()
        sys.exit() # Esto asegura que el proceso termine completamente