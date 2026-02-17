import customtkinter as ctk
from db.database import insertar_libro, actualizar_libro, eliminar_libro
from ui.widgets.error import CustomMessage

class FormBiblioteca(ctk.CTkToplevel):
    """
    Ventana Toplevel para Agregar, Editar o Eliminar Libros.
    """
    def __init__(self, master, refresh_callback, book_data=None):
        super().__init__(master)
        self.title("Gestión de Libro")
        self.geometry("460x450")
        
        # Configuración modal
        self.transient(master) 
        self.grab_set()
        
        self.refresh_callback = refresh_callback
        self.book_data = book_data 
        
        # CORRECCIÓN: Los índices correctos según database.py línea 184-188
        # SELECT isbn, titulo, autor, categoria, editorial, fecha_publicacion, disponible, id
        # [0]=isbn, [1]=titulo, [2]=autor, [3]=categoria, [4]=editorial, [5]=fecha_publicacion, [6]=disponible, [7]=id
        self.book_id = book_data[7] if book_data else None  # id está en [7]
        self.is_available = book_data[6] if book_data else 1  # disponible está en [6]
        
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(8, weight=1)
        
        self._create_header()
        self._create_form_fields()
        self._create_action_buttons()
        self._load_data()
        
        # Foco inicial seguro
        self.after(200, self._safe_focus)
        
        # Centrar la ventana en la pantalla
        self._center_window()

    def _center_window(self):
        """Calcula las coordenadas para centrar la ventana Toplevel en la pantalla."""
        self.update_idletasks() # Asegura que las dimensiones estén calculadas
        
        # Dimensiones de la ventana
        win_w = self.winfo_width()
        win_h = self.winfo_height()
        
        # Dimensiones de la pantalla
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        
        # Calcular posición para centrar
        start_x = (screen_w // 2) - (win_w // 2)
        start_y = (screen_h // 2) - (win_h // 2)
        
        self.geometry(f'{win_w}x{win_h}+{start_x}+{start_y}')

    def _safe_focus(self):
        """Establece el foco solo si el widget y la ventana existen."""
        try:
            if self.winfo_exists() and "titulo" in self.fields:
                self.fields["titulo"].focus_set()
        except Exception:
            pass

    def _clean_close(self):
        """Cierra la ventana de forma limpia para evitar errores de Tcl/Tk."""
        try:
            self.focus()
            self.grab_release()
            self.withdraw()
            self.update_idletasks()
            self.destroy()
        except Exception:
            pass

    def _on_success(self):
        """Callback que se ejecuta al dar click en Aceptar del mensaje de éxito."""
        self.refresh_callback()
        self._clean_close()

    def _create_header(self):
        title_text = "Editar | Eliminar" if self.book_data else "Agregar Nuevo Libro"
        ctk.CTkLabel(
            self,
            text=title_text,
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

    def _create_form_fields(self):
        self.fields = {}
        field_configs = [
            ("Título:", "titulo"),
            ("Autor:", "autor"), 
            ("ISBN:", "isbn"),
            ("Categoría:", "categoria"),
            ("Editorial:", "editorial"),
            ("Fecha Publicación:", "fecha_publicacion")
        ]
        
        for i, (label_text, field_key) in enumerate(field_configs):
            ctk.CTkLabel(self, text=label_text).grid(row=i+1, column=0, padx=(20, 10), pady=(10, 0), sticky="w")
            
            # Configuración especial para fecha de publicación
            if label_text == "Fecha Publicación:":
                entry = ctk.CTkEntry(self, placeholder_text="YYYY-MM-DD")
            else:
                entry = ctk.CTkEntry(self)
                
            entry.grid(row=i+1, column=1, padx=(0, 20), pady=(0, 10), sticky="ew")
            self.fields[field_key] = entry
            
            if self.book_data and label_text == "ISBN:":
                entry.configure(state="disabled")

    def _create_action_buttons(self):
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=7, column=0, columnspan=2, padx=20, pady=(10, 20), sticky="ew")
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)

        action_text = "Guardar Cambios" if self.book_data else "Agregar Libro"
        self.save_button = ctk.CTkButton(
            button_frame, 
            text=action_text, 
            command=self._save_action,
            fg_color="#10B981",
            hover_color="#047857"
        )
        self.save_button.grid(row=0, column=0, padx=5, sticky="ew")
        
        if self.book_data:
            delete_text = "Eliminar"
            if self.is_available == 0:
                delete_text = "Eliminar (Prestado)"
            self.delete_button = ctk.CTkButton(
                button_frame, 
                text=delete_text, 
                command=self._confirm_delete,
                fg_color="#EF4444", 
                hover_color="#B91C1C",
                state="disabled" if self.is_available == 0 else "normal"
            )
            self.delete_button.grid(row=0, column=1, padx=5, sticky="ew")

        ctk.CTkButton(
            button_frame, 
            text="Cancelar", 
            command=self._clean_close,
            fg_color="gray",
            hover_color="darkgray"
        ).grid(row=0, column=2 if self.book_data else 1, padx=5, sticky="ew")

    def _load_data(self):
        if self.book_data:
            # CORRECCIÓN: Usar los índices correctos según database.py
            # book_data = [isbn, titulo, autor, categoria, editorial, fecha_publicacion, disponible, id]
            self.fields["titulo"].insert(0, self.book_data[1])       # titulo está en [1]
            self.fields["autor"].insert(0, self.book_data[2])        # autor está en [2]

            self.fields["isbn"].configure(state="normal")
            self.fields["isbn"].insert(0, self.book_data[0])         # isbn está en [0]
            self.fields["isbn"].configure(state="disabled")
            
            self.fields["categoria"].insert(0, self.book_data[3])    # categoria está en [3]
            self.fields["editorial"].insert(0, self.book_data[4])    # editorial está en [4]
            self.fields["fecha_publicacion"].insert(0, self.book_data[5])  # fecha_publicacion está en [5]

    def _save_action(self):
        titulo = self.fields["titulo"].get().strip()
        autor = self.fields["autor"].get().strip()
        isbn = self.fields["isbn"].get().strip()
        categoria = self.fields["categoria"].get().strip()
        editorial = self.fields["editorial"].get().strip()
        fecha_publicacion = self.fields["fecha_publicacion"].get().strip()

        if not all([titulo, autor, isbn, categoria]):
            CustomMessage(self.master, "Error de Validación", "Los campos Título, Autor, ISBN y Categoría son obligatorios.", is_error=True)
            return

        success = False
        message = ""
        
        if self.book_data:
            resultado = actualizar_libro(self.book_id, titulo, autor, isbn, categoria, editorial, fecha_publicacion)
            if resultado and resultado[0]:
                success = True
                message = resultado[1]
            else:
                mensaje_error = resultado[1] if resultado and resultado[1] else "No se pudo actualizar el libro."
                CustomMessage(self.master, "Error", mensaje_error, is_error=True)
                return
        else:
            resultado = insertar_libro(titulo, autor, isbn, categoria, editorial, fecha_publicacion)
            if resultado and resultado[0]:
                success = True
                message = resultado[1]
            else:
                mensaje_error = resultado[1] if resultado and resultado[1] else "No se pudo agregar el libro."
                CustomMessage(self.master, "Error", mensaje_error, is_error=True)
                return
        
        if success:
            CustomMessage(self.master, "Éxito", message, is_error=False, callback=self._on_success)

    def _confirm_delete(self):
        if self.is_available == 0:
            CustomMessage(self.master, "Error", "No se puede eliminar un libro prestado.", is_error=True)
            return

        if eliminar_libro(self.book_id):
            CustomMessage(self.master, "Éxito", "Libro eliminado correctamente.", is_error=False, callback=self._on_success)
        else:
            CustomMessage(self.master, "Error", "No se pudo eliminar el libro.", is_error=True)