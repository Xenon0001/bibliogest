import customtkinter as ctk

class CustomMessage(ctk.CTkToplevel):
    """
    Ventana modal para mostrar mensajes de éxito o error.
    Ahora es modal (siempre encima) y usa un callback para ejecutar 
    acciones (como continuar a la siguiente vista) después de la confirmación.
    """
    def __init__(self, master, title, message, is_error=False, callback=None):
        super().__init__(master)
        self.title(title)
        self.message = message
        self.is_error = is_error
        self.callback = callback
        
        # FIX: Configuración para hacer la ventana modal y siempre por encima
        self.grab_set() 
        self.attributes("-topmost", True)
        self.resizable(False, False)
        
        # Asegurar que la ventana se levante
        self.after(10, self.lift) 
        
        self.grid_columnconfigure(0, weight=1)
        
        # Color y texto del encabezado basado en el tipo de mensaje
        color = "#EF4444" if is_error else "#10B981"
        icon = "❗ ERROR" if is_error else "✅ ÉXITO"
        
        # Frame principal para contener todo
        main_frame = ctk.CTkFrame(self, fg_color=self.cget("fg_color"))
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        ctk.CTkLabel(
            main_frame,
            text=f"{icon} {title}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=color
        ).grid(row=0, column=0, padx=20, pady=(10, 5), sticky="ew")

        # Mensaje
        ctk.CTkLabel(
            main_frame,
            text=message,
            wraplength=350,
            justify="center"
        ).grid(row=1, column=0, padx=20, pady=(5, 15), sticky="ew")

        # Botón de Aceptar
        ctk.CTkButton(
            main_frame,
            text="Aceptar",
            command=self._confirm,
            fg_color=color
        ).grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")
        
        # Centrar la ventana
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = master.winfo_x() + (master.winfo_width() // 2) - (width // 2)
        y = master.winfo_y() + (master.winfo_height() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def _confirm(self):
        """Cierra la ventana y ejecuta el callback si existe."""
        # Primero ejecuta la acción de transición si existe
        if self.callback:
            self.callback()
        # Luego destruye la ventana modal
        self.destroy()