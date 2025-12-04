# Importación de la lógica de la DB
from db.database import inicializar_db, verificar_existencia_bibliotecarios 

# Importación de la función de arranque de la UI
from ui.views.formulario import iniciar_formulario

def iniciar_aplicacion():
    # 1. Asegurar que la DB y las tablas existan
    inicializar_db()

    # 2. Verificar el estado de la autenticación
    hay_bibliotecario = verificar_existencia_bibliotecarios()

    if hay_bibliotecario:
        # A. Hay bibliotecario, iniciamos la ventana de LOGIN
        iniciar_formulario(debe_registrar=False)
    else:
        # B. No hay bibliotecario, iniciamos la ventana de REGISTRO inicial
        iniciar_formulario(debe_registrar=True)


if __name__ == "__main__":
    # Importar customtkinter para la configuración de apariencia (Opcional pero recomendado)
    import customtkinter as ctk
    ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
    ctk.set_default_color_theme("blue") # Themes: "blue" (default), "green", "dark-blue"
    
    iniciar_aplicacion()