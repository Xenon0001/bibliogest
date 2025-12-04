import customtkinter as ctk
from tkinter import ttk
from db.database import obtener_prestamos_activos, obtener_libro_por_isbn, obtener_usuario_por_dni, registrar_prestamo, registrar_devolucion
from ui.widgets.error import CustomMessage
from datetime import date
import sys

class HistorialView(ctk.CTkFrame):
    """Vista para la gestión de préstamos activos y registro de nuevas transacciones."""
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # Fila de préstamos activos
        self.grid_rowconfigure(2, weight=0) # Fila de nueva transacción
        
        self.active_loans_data = [] # Cache de datos de préstamos
        self._create_styles()
        self._create_active_loans_section()
        self._create_transaction_section()
        
        self.load_active_loans()

    def _create_styles(self):
        """Estilos personalizados para la tabla Treeview."""
        style = ttk.Style()
        style.theme_use("default")
        
        # Estilo para los encabezados de Historial (Naranja)
        style.configure("Historial.Heading", 
                        font=('Arial', 12, 'bold'), 
                        background="#F59E0B", 
                        foreground="white",
                        padding=5)
        
        style.configure("Historial.Treeview", 
                        font=('Arial', 10),
                        rowheight=25)
        
        style.map("Historial.Treeview",
                  background=[('selected', '#F59E0B')], 
                  foreground=[('selected', 'white')])

    def _create_active_loans_section(self):
        """Crea la sección superior para la tabla de préstamos activos."""
        active_loans_frame = ctk.CTkFrame(self, fg_color="transparent")
        active_loans_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")
        active_loans_frame.grid_columnconfigure(0, weight=1)
        active_loans_frame.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            active_loans_frame,
            text="PRÉSTAMOS ACTIVOS PENDIENTES DE DEVOLUCIÓN",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, pady=(0, 10), sticky="w")
        
        # Buscador
        search_frame = ctk.CTkFrame(active_loans_frame, fg_color="transparent")
        search_frame.grid(row=1, column=0, pady=(0, 10), sticky="ew")
        search_frame.grid_columnconfigure(0, weight=1)
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Buscar por Título o DNI del Usuario...")
        self.search_entry.grid(row=0, column=0, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self.filter_active_loans)

        # Tabla
        columns = ("ID", "Título del Libro", "Usuario", "DNI", "Fecha Préstamo", "Libro ID")
        self.tree = ttk.Treeview(active_loans_frame, columns=columns, show="headings", style="Historial.Treeview")
        
        self.tree.heading("ID", text="ID Préstamo", anchor="center")
        self.tree.heading("Título del Libro", text="Título del Libro", anchor="w")
        self.tree.heading("Usuario", text="Usuario", anchor="w")
        self.tree.heading("DNI", text="DNI Usuario", anchor="center")
        self.tree.heading("Fecha Préstamo", text="Fecha Préstamo", anchor="center")
        self.tree.heading("Libro ID", text="Libro ID", anchor="center")
        
        self.tree.column("ID", width=80, anchor="center")
        self.tree.column("Título del Libro", width=250, anchor="w")
        self.tree.column("Usuario", width=200, anchor="w")
        self.tree.column("DNI", width=120, anchor="center")
        self.tree.column("Fecha Préstamo", width=120, anchor="center")
        self.tree.column("Libro ID", width=0, stretch=False) # Columna oculta para referencia
        
        scrollbar = ctk.CTkScrollbar(active_loans_frame, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=2, column=0, sticky="nsew")
        scrollbar.grid(row=2, column=1, sticky="ns")

        # Acciones
        self.tree.bind("<Double-1>", self.on_double_click)
        
    def _create_transaction_section(self):
        """Crea la sección inferior para registrar nuevos préstamos."""
        transaction_frame = ctk.CTkFrame(self, fg_color="transparent")
        transaction_frame.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="ew")
        
        ctk.CTkLabel(
            transaction_frame,
            text="REGISTRAR NUEVO PRÉSTAMO",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=5, pady=(0, 15), sticky="w")
        
        # Campos de entrada
        ctk.CTkLabel(transaction_frame, text="ISBN del Libro:").grid(row=1, column=0, padx=(0, 10), sticky="w")
        self.isbn_entry = ctk.CTkEntry(transaction_frame, width=150)
        self.isbn_entry.grid(row=1, column=1, padx=(0, 20), sticky="ew")

        ctk.CTkLabel(transaction_frame, text="DNI del Usuario:").grid(row=1, column=2, padx=(0, 10), sticky="w")
        self.dni_entry = ctk.CTkEntry(transaction_frame, width=150)
        self.dni_entry.grid(row=1, column=3, padx=(0, 20), sticky="ew")

        # Botón de Préstamo
        ctk.CTkButton(
            transaction_frame,
            text="Registrar Préstamo",
            command=self.handle_new_loan,
            fg_color="#3B82F6",
            hover_color="#2563EB"
        ).grid(row=1, column=4, sticky="e")
        
        transaction_frame.grid_columnconfigure((1, 3), weight=1) # Expansión para entradas


    def load_active_loans(self):
        """Carga los datos de préstamos activos y actualiza la tabla."""
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        # Retorna: (prestamo_id, titulo, nombre_usuario, dni_usuario, fecha_prestamo, libro_id)
        self.active_loans_data = obtener_prestamos_activos()
        
        for row in self.active_loans_data:
            # Insertar los datos visibles (ID, Título, Usuario, DNI, Fecha Préstamo)
            self.tree.insert('', 'end', 
                             values=(row[0], row[1], row[2], row[3], row[4], row[5]))

    def filter_active_loans(self, event=None):
        """Filtra la tabla de préstamos activos por Título o DNI del usuario."""
        query = self.search_entry.get().strip().lower()
        
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not query:
            data_to_show = self.active_loans_data
        else:
            # Filtrar por Título (índice 1) o DNI (índice 3)
            data_to_show = [
                row for row in self.active_loans_data
                if query in row[1].lower() or query in row[3].lower()
            ]

        for row in data_to_show:
            self.tree.insert('', 'end', 
                             values=(row[0], row[1], row[2], row[3], row[4], row[5]))

    def on_double_click(self, event):
        """Maneja el doble clic para iniciar el proceso de Devolución."""
        item_id = self.tree.identify_row(event.y)
        if not item_id:
            return
            
        # Obtener los datos de la fila seleccionada (prestamo_id está en la columna 0)
        values = self.tree.item(item_id, 'values')
        prestamo_id = int(values[0])
        libro_id = int(values[5])
        titulo_libro = values[1]
        
        # Simular una confirmación de devolución
        self.confirm_devolution_modal(prestamo_id, libro_id, titulo_libro)


    def confirm_devolution_modal(self, prestamo_id, libro_id, titulo_libro):
        """Muestra un modal de confirmación para la devolución."""
        
        modal = ctk.CTkToplevel(self.master)
        modal.title("Confirmar Devolución")
        modal.geometry("350x150")
        modal.grab_set()

        ctk.CTkLabel(modal, text=f"¿Confirmas la devolución de:", font=ctk.CTkFont(size=14)).pack(pady=(15, 5))
        ctk.CTkLabel(modal, text=f"'{titulo_libro}'?", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

        button_frame = ctk.CTkFrame(modal, fg_color="transparent")
        button_frame.pack(pady=10)
        
        ctk.CTkButton(
            button_frame, 
            text="Confirmar", 
            command=lambda: self.handle_devolution(prestamo_id, libro_id, modal),
            fg_color="#10B981", 
            hover_color="#047857"
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame, 
            text="Cancelar", 
            command=modal.destroy,
            fg_color="gray",
            hover_color="darkgray"
        ).pack(side="right", padx=10)

    
    def handle_devolution(self, prestamo_id, libro_id, modal):
        """Ejecuta la lógica de devolución."""
        modal.destroy()
        
        if registrar_devolucion(prestamo_id, libro_id):
            CustomMessage(self.master, "Éxito", "Devolución registrada correctamente. Libro disponible.", is_error=False)
            self.load_active_loans() # Refrescar la tabla
            # Nota: Sería ideal refrescar también la BibliotecaView si estuviera visible
        else:
            CustomMessage(self.master, "Error", "No se pudo registrar la devolución.", is_error=True)

    
    def handle_new_loan(self):
        """Maneja el registro de un nuevo préstamo."""
        isbn = self.isbn_entry.get().strip()
        dni = self.dni_entry.get().strip()

        if not isbn or not dni:
            CustomMessage(self.master, "Error de Validación", "Ingrese el ISBN del libro y el DNI del usuario.", is_error=True)
            return

        # 1. Verificar Usuario
        user_info = obtener_usuario_por_dni(dni)
        if not user_info:
            CustomMessage(self.master, "Error", f"Usuario con DNI '{dni}' no encontrado.", is_error=True)
            return
        user_id = user_info[0]

        # 2. Verificar Libro
        # Retorna: (id, isbn, titulo, disponible)
        book_info = obtener_libro_por_isbn(isbn) 
        if not book_info:
            CustomMessage(self.master, "Error", f"Libro con ISBN '{isbn}' no encontrado.", is_error=True)
            return
        
        libro_id = book_info[0]
        disponible = book_info[3]
        
        if disponible == 0:
            CustomMessage(self.master, "Error", f"El libro '{book_info[2]}' no está disponible (ya prestado).", is_error=True)
            return

        # 3. Registrar Transacción
        if registrar_prestamo(user_id, libro_id):
            CustomMessage(self.master, "Éxito", "Préstamo registrado con éxito.", is_error=False)
            self.isbn_entry.delete(0, 'end')
            self.dni_entry.delete(0, 'end')
            self.load_active_loans() # Refrescar la tabla
            # Nota: Sería ideal refrescar también la BibliotecaView
        else:
            CustomMessage(self.master, "Error", "Error al registrar el préstamo.", is_error=True)