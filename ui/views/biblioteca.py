import customtkinter as ctk
from tkinter import ttk # Usamos ttk para la tabla (Treeview)
from db.database import obtener_todos_los_libros, obtener_libros_prestados_count
from ui.forms.form_biblioteca import FormBiblioteca
from ui.widgets.error import CustomMessage # Para los mensajes de éxito/error

class BibliotecaView(ctk.CTkFrame):
    """Vista principal para la gestión y listado de libros."""
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # La fila de la tabla necesita expandirse

        self.libros_data = [] # Cache de datos de libros
        self._create_styles()
        self._create_header_frame()
        self._create_search_frame()
        self._create_table_frame()
        
        # Cargar datos iniciales
        self.load_books_data()
        
    def _create_styles(self):
        """Estilos personalizados para la tabla Treeview de Tkinter."""
        style = ttk.Style()
        # Configurar tema (basado en el tema actual de ctk)
        style.theme_use("default")
        
        # Estilo para los encabezados
        style.configure("Treeview.Heading", 
                        font=('Arial', 12, 'bold'), 
                        background="#3B82F6", # Color de cabecera
                        foreground="white",
                        padding=5)
        
        # Estilo para las filas
        style.configure("Treeview", 
                        font=('Arial', 10),
                        rowheight=25)
        
        # Mapeo de colores para filas alternas (opcional)
        style.map("Treeview",
                  background=[('selected', '#10B981')], # Color al seleccionar
                  foreground=[('selected', 'white')])


    def _create_header_frame(self):
        """Crea el encabezado con el contador y el botón Agregar."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1) # Contador
        header_frame.grid_columnconfigure(1, weight=0) # Botón

        # Contador de Libros Prestados
        self.borrowed_count_label = ctk.CTkLabel(
            header_frame,
            text="Libros Prestados: 0",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#EF4444" # Rojo para destacar
        )
        self.borrowed_count_label.grid(row=0, column=0, sticky="w")

        # Botón Agregar Libros
        ctk.CTkButton(
            header_frame,
            text="➕ Agregar Libro",
            command=lambda: self.open_book_form(),
            fg_color="#10B981", # Verde para Agregar
            hover_color="#047857"
        ).grid(row=0, column=1, sticky="e")

    def _create_search_frame(self):
        """Crea el campo de búsqueda en tiempo real."""
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        search_frame.grid_columnconfigure(0, weight=1)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Buscar por Título o Autor...",
            font=ctk.CTkFont(size=14)
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        # Vincula el evento de pulsación de tecla para la búsqueda en tiempo real
        self.search_entry.bind("<KeyRelease>", self.filter_books)

        ctk.CTkButton(search_frame, text="🔍", width=40, command=self.filter_books).grid(row=0, column=1, sticky="e")


    def _create_table_frame(self):
        """Crea la tabla Treeview y la barra de desplazamiento."""
        table_frame = ctk.CTkFrame(self, fg_color="transparent")
        table_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        
        # 1. Definición de la tabla
        columns = ("ISBN", "Título", "Autor", "Categoría", "Editorial", "Fecha Pub.", "Disponible")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # 2. Encabezados de la tabla
        self.tree.heading("ISBN", text="ISBN", anchor="center")
        self.tree.heading("Título", text="Título", anchor="w")
        self.tree.heading("Autor", text="Autor", anchor="w")
        self.tree.heading("Categoría", text="Categoría", anchor="center")
        self.tree.heading("Editorial", text="Editorial", anchor="center")
        self.tree.heading("Fecha Pub.", text="Fecha Pub.", anchor="center")
        self.tree.heading("Disponible", text="Disponible", anchor="center")
        
        # 3. Ancho de columnas
        self.tree.column("ISBN", width=100, anchor="center")
        self.tree.column("Título", width=250, anchor="w")
        self.tree.column("Autor", width=200, anchor="w")
        self.tree.column("Categoría", width=80, anchor="center")
        self.tree.column("Editorial", width=120, anchor="center")
        self.tree.column("Fecha Pub.", width=90, anchor="center")
        self.tree.column("Disponible", width=70, anchor="center")

        # 4. Scrollbar
        scrollbar = ctk.CTkScrollbar(table_frame, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Posicionamiento del Treeview y Scrollbar
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # 5. Click Actions (Doble clic)
        self.tree.bind("<Double-1>", self.on_double_click)


    def load_books_data(self):
        """Carga los datos de la base de datos y actualiza la tabla."""
        # Limpiar la tabla
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        # Cargar los datos desde la DB
        self.libros_data = obtener_todos_los_libros()
        
        for row in self.libros_data:
            # row: (isbn, titulo, autor, categoria, editorial, fecha_publicacion, disponible, id)
            status = "Sí" if row[6] == 1 else "No"
            # Insertar los datos visibles
            self.tree.insert('', 'end', 
                             values=(row[0], row[1], row[2], row[3], row[4] or "", row[5] or "", status),
                             tags=("disponible" if row[6] == 1 else "prestado",))

        # Actualizar contador de prestados
        count = obtener_libros_prestados_count()
        self.borrowed_count_label.configure(text=f"Libros Prestados: {count}")
        
        # Aplicar tags de color
        self.tree.tag_configure("prestado", foreground="#EF4444")
        self.tree.tag_configure("disponible", foreground="#10B981")


    def filter_books(self, event=None):
        """Filtra la tabla de libros basándose en el Entry de búsqueda."""
        query = self.search_entry.get().strip().lower()
        
        # Limpiar la tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not query:
            # Si la búsqueda está vacía, mostrar todos los datos
            data_to_show = self.libros_data
        else:
            # Filtrar por Título o Autor (índices 1 y 2 en self.libros_data)
            data_to_show = [
                row for row in self.libros_data
                if query in row[1].lower() or query in row[2].lower()
            ]

        for row in data_to_show:
            # row: (isbn, titulo, autor, categoria, editorial, fecha_publicacion, disponible, id)
            status = "Sí" if row[6] == 1 else "No"
            self.tree.insert('', 'end', 
                             values=(row[0], row[1], row[2], row[3], row[4] or "", row[5] or "", status),
                             tags=("disponible" if row[6] == 1 else "prestado",))


    def on_double_click(self, event):
        """Maneja el doble clic en una fila para abrir el formulario de edición/eliminación."""
        item_id = self.tree.identify_row(event.y)
        if not item_id:
            return
            
        # Obtener el ISBN del libro seleccionado
        selected_isbn = self.tree.item(item_id, 'values')[0]
        
        # Buscar los datos completos del libro usando el ISBN
        book_data = next((row for row in self.libros_data if row[0] == selected_isbn), None)

        if book_data:
            self.open_book_form(book_data)
        else:
            CustomMessage(self.master, "Error de Datos", "No se encontraron los datos completos del libro.", is_error=True)


    def open_book_form(self, book_data=None):
        """Abre la ventana Toplevel FormBiblioteca en modo Agregar o Editar."""
        # Se pasa la función load_books_data como callback para refrescar la tabla
        FormBiblioteca(self.master, self.load_books_data, book_data)