import customtkinter as ctk
from tkinter import ttk
from db.database import obtener_todos_los_usuarios
from ui.forms.form_usuario import FormUsuario
from ui.widgets.error import CustomMessage

class UsuariosView(ctk.CTkFrame):
    """Vista para la gestión y listado de usuarios (lectores)."""
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Fila de la tabla

        self.users_data = [] # Cache de datos de usuarios
        self._create_styles()
        self._create_header_frame()
        self._create_search_frame()
        self._create_table_frame()
        
        self.load_users_data()
        
    def _create_styles(self):
        """Estilos personalizados para la tabla Treeview de Tkinter."""
        style = ttk.Style()
        style.theme_use("default")
        
        style.configure("Treeview.Heading", 
                        font=('Arial', 12, 'bold'), 
                        background="#3B82F6", 
                        foreground="white",
                        padding=5)
        
        style.configure("Treeview", 
                        font=('Arial', 10),
                        rowheight=25)
        
        style.map("Treeview",
                  background=[('selected', '#3B82F6')], 
                  foreground=[('selected', 'white')])


    def _create_header_frame(self):
        """Crea el encabezado con el contador y el botón Agregar."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=0)

        # Contador de Usuarios Activos
        self.active_users_label = ctk.CTkLabel(
            header_frame,
            text="Usuarios Registrados: 0",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#3B82F6" 
        )
        self.active_users_label.grid(row=0, column=0, sticky="w")

        # Botón Agregar Usuario
        ctk.CTkButton(
            header_frame,
            text="➕ Agregar Usuario",
            command=lambda: self.open_user_form(),
            fg_color="#10B981", 
            hover_color="#047857"
        ).grid(row=0, column=1, sticky="e")

    def _create_search_frame(self):
        """Crea el campo de búsqueda en tiempo real."""
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        search_frame.grid_columnconfigure(0, weight=1)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Buscar por Nombre o DNI...",
            font=ctk.CTkFont(size=14)
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.filter_users)

        ctk.CTkButton(search_frame, text="🔍", width=40, command=self.filter_users).grid(row=0, column=1, sticky="e")


    def _create_table_frame(self):
        """Crea la tabla Treeview y la barra de desplazamiento."""
        table_frame = ctk.CTkFrame(self, fg_color="transparent")
        table_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        
        # 1. Definición de la tabla
        columns = ("Nombre", "DNI", "Teléfono", "Libros Prestados")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # 2. Encabezados de la tabla
        self.tree.heading("Nombre", text="Nombre", anchor="w")
        self.tree.heading("DNI", text="DNI", anchor="center")
        self.tree.heading("Teléfono", text="Teléfono", anchor="center")
        self.tree.heading("Libros Prestados", text="Libros Prestados", anchor="center")
        
        # 3. Ancho de columnas
        self.tree.column("Nombre", width=300, anchor="w")
        self.tree.column("DNI", width=150, anchor="center")
        self.tree.column("Teléfono", width=150, anchor="center")
        self.tree.column("Libros Prestados", width=120, anchor="center")

        # 4. Scrollbar
        scrollbar = ctk.CTkScrollbar(table_frame, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # 5. Click Actions (Doble clic)
        self.tree.bind("<Double-1>", self.on_double_click)


    def load_users_data(self):
        """Carga los datos de la base de datos y actualiza la tabla."""
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        # Cargar los datos desde la DB: (id, nombre, dni, telefono, libros_prestados_activos)
        self.users_data = obtener_todos_los_usuarios()
        
        for row in self.users_data:
            loans_count = row[4]
            
            # Insertar los datos visibles (Nombre, DNI, Teléfono, Libros Prestados)
            self.tree.insert('', 'end', 
                             values=(row[1], row[2], row[3], loans_count),
                             tags=("active" if loans_count > 0 else "inactive",))

        # Actualizar contador
        self.active_users_label.configure(text=f"Usuarios Registrados: {len(self.users_data)}")
        
        # Aplicar tags de color
        self.tree.tag_configure("active", foreground="#EF4444") # Rojo si tiene préstamos
        self.tree.tag_configure("inactive", foreground="gray")


    def filter_users(self, event=None):
        """Filtra la tabla de usuarios basándose en el Entry de búsqueda por Nombre o DNI."""
        query = self.search_entry.get().strip().lower()
        
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not query:
            data_to_show = self.users_data
        else:
            # Filtrar por Nombre (índice 1) o DNI (índice 2)
            data_to_show = [
                row for row in self.users_data
                if query in row[1].lower() or query in row[2].lower()
            ]

        for row in data_to_show:
            loans_count = row[4]
            self.tree.insert('', 'end', 
                             values=(row[1], row[2], row[3], loans_count),
                             tags=("active" if loans_count > 0 else "inactive",))


    def on_double_click(self, event):
        """Maneja el doble clic en una fila para abrir el formulario de edición/eliminación."""
        item_id = self.tree.identify_row(event.y)
        if not item_id:
            return
            
        # Obtener el DNI del usuario seleccionado (columna 1 de la vista)
        selected_dni = self.tree.item(item_id, 'values')[1]
        
        # Buscar los datos completos del usuario usando el DNI
        user_data = next((row for row in self.users_data if row[2] == selected_dni), None)

        if user_data:
            self.open_user_form(user_data)
        else:
            CustomMessage(self.master, "Error de Datos", "No se encontraron los datos completos del usuario.", is_error=True)


    def open_user_form(self, user_data=None):
        """Abre la ventana Toplevel FormUsuario en modo Agregar o Editar."""
        FormUsuario(self.master, self.load_users_data, user_data)