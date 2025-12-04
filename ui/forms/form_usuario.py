import customtkinter as ctk
from db.database import insertar_usuario, actualizar_usuario, eliminar_usuario
from ui.widgets.error import CustomMessage

class FormUsuario(ctk.CTkToplevel):
    """
    Ventana Toplevel para Agregar, Editar o Eliminar Usuarios.
    """
    def __init__(self, master, refresh_callback, user_data=None):
        super().__init__(master)
        self.title("Gestión de Usuario")
        self.geometry("450x450")
        
        # Configuración modal
        self.transient(master)
        self.grab_set() 
        
        self.refresh_callback = refresh_callback
        self.user_data = user_data 
        self.user_id = user_data[0] if user_data else None
        self.active_loans = user_data[4] if user_data and len(user_data) > 4 else 0
        
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(5, weight=1) 
        
        self._create_header()
        self._create_form_fields()
        self._create_action_buttons()
        self._load_data()

        # FIX: Foco inicial solo si la ventana existe
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
            if self.winfo_exists() and "Nombre" in self.fields:
                self.fields["Nombre"].focus_set()
        except Exception:
            pass

    def _clean_close(self):
        """Cierra la ventana de forma limpia cuando el usuario confirma."""
        try:
            # Quitamos el foco de cualquier entry y lo pasamos a la ventana
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
        title_text = "Editar/Eliminar Usuario" if self.user_data else "Agregar Nuevo Usuario"
        ctk.CTkLabel(
            self,
            text=title_text,
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="ew")

    def _create_form_fields(self):
        self.fields = {}
        labels = ["Nombre:", "DNI:", "Teléfono:"]
        
        for i, label_text in enumerate(labels):
            ctk.CTkLabel(self, text=label_text).grid(row=i+1, column=0, padx=(20, 10), pady=(10, 0), sticky="w")
            entry = ctk.CTkEntry(self)
            entry.grid(row=i+1, column=1, padx=(0, 20), pady=(0, 10), sticky="ew")
            self.fields[label_text.split(':')[0]] = entry
            
            if self.user_data and label_text == "DNI:":
                entry.configure(state="disabled")

    def _create_action_buttons(self):
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=4, column=0, columnspan=2, padx=20, pady=(10, 20), sticky="ew")
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)

        action_text = "Guardar Cambios" if self.user_data else "Agregar Usuario"
        self.save_button = ctk.CTkButton(
            button_frame, 
            text=action_text, 
            command=self._save_action,
            fg_color="#10B981",
            hover_color="#047857"
        )
        self.save_button.grid(row=0, column=0, padx=5, sticky="ew")
        
        if self.user_data:
            delete_text = "Eliminar"
            if self.active_loans > 0:
                delete_text = f"Eliminar ({self.active_loans} activos)"
                
            self.delete_button = ctk.CTkButton(
                button_frame, 
                text=delete_text, 
                command=self._confirm_delete,
                fg_color="#EF4444", 
                hover_color="#B91C1C",
                state="disabled" if self.active_loans > 0 else "normal"
            )
            self.delete_button.grid(row=0, column=1, padx=5, sticky="ew")

        ctk.CTkButton(
            button_frame, 
            text="Cancelar", 
            command=self._clean_close, # Usar cierre limpio
            fg_color="gray",
            hover_color="darkgray"
        ).grid(row=0, column=2 if self.user_data else 1, padx=5, sticky="ew")

    def _load_data(self):
        if self.user_data:
            data = {
                "Nombre": self.user_data[1],
                "DNI": self.user_data[2], 
                "Teléfono": self.user_data[3]
            }
            self.fields["Nombre"].insert(0, data["Nombre"])
            self.fields["DNI"].configure(state="normal")
            self.fields["DNI"].insert(0, data["DNI"])
            self.fields["DNI"].configure(state="disabled")
            self.fields["Teléfono"].insert(0, data["Teléfono"])

    def _save_action(self):
        nombre = self.fields["Nombre"].get().strip()
        telefono = self.fields["Teléfono"].get().strip()
        dni = self.user_data[2] if self.user_data else self.fields["DNI"].get().strip()

        if not all([nombre, dni, telefono]):
            CustomMessage(self.master, "Error de Validación", "Todos los campos deben estar rellenos.", is_error=True)
            return

        success = False
        message = ""

        if self.user_data:
            if actualizar_usuario(self.user_id, nombre, telefono):
                success = True
                message = "Usuario actualizado."
            else:
                CustomMessage(self.master, "Error", "No se pudo actualizar.", is_error=True)
                return
        else:
            if insertar_usuario(nombre, dni, telefono):
                success = True
                message = "Usuario agregado."
            else:
                CustomMessage(self.master, "Error", "No se pudo agregar (DNI duplicado).", is_error=True)
                return
        
        if success:
            # FIX: Pasamos _on_success como callback. La ventana NO se cierra hasta dar OK.
            CustomMessage(self.master, "Éxito", message, is_error=False, callback=self._on_success)

    def _confirm_delete(self):
        if self.active_loans > 0:
            CustomMessage(self.master, "Error", "Usuario tiene préstamos activos.", is_error=True)
            return

        if eliminar_usuario(self.user_id):
            # FIX: Igual aquí, cierre controlado vía callback
            CustomMessage(self.master, "Éxito", "Usuario eliminado.", is_error=False, callback=self._on_success)
        else:
            CustomMessage(self.master, "Error", "No se pudo eliminar el usuario.", is_error=True)