# Importar ambas librerías
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from src.utils import i18n
from src.config import FOLDERS_TO_IGNORE
from src.controller.prompt_controller import PromptController
from src.ui import PromptAssistantGUI

class MainWindow:
    def __init__(self, design_mode="Moderno"):
        self.design_mode = design_mode  # "Clásico" o "Moderno"
        # Para el diseño moderno, usaremos CustomTkinter siempre.
        ctk.set_appearance_mode("Dark")  # Opcional: "Light", "Dark" o "System"
        self.root = ctk.CTk()
        self.root.title(i18n.t("title"))
        self.root.geometry("1200x800")  # Dimensión inicial
        self.root.minsize(800, 600)
        
        # Crear la parte superior de la ventana con selectores de idioma y diseño
        self._crear_seleccion_idioma_y_diseno()

        # Inicializamos la lógica auxiliar y el controlador
        self.gui_helper = PromptAssistantGUI(self.root, FOLDERS_TO_IGNORE)
        self.controller = PromptController(self.gui_helper, self)
        
        # Contenedor principal para los paneles
        container = ctk.CTkFrame(self.root)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Crear los tres paneles y organizarlos en grid
        from src.ui.panel_left import LeftPanel
        from src.ui.panel_center import CenterPanel
        from src.ui.panel_right import RightPanel
        self.left_panel = LeftPanel(container, self.controller)
        self.center_panel = CenterPanel(container)
        self.right_panel = RightPanel(container, self.controller)
        
        self.left_panel.frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.center_panel.frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.right_panel.frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        
        # Configurar la grilla para que los paneles se expandan
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=2)
        container.grid_columnconfigure(2, weight=1)
        container.grid_rowconfigure(0, weight=1)
        
    def _center_window(self, width, height):
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _crear_seleccion_idioma_y_diseno(self):
        top_frame = ctk.CTkFrame(self.root, height=50)
        top_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        # Selector de idioma usando CTkLabel y CTkComboBox
        idioma_label = ctk.CTkLabel(top_frame, text=f"{i18n.t('language')}:",
                                    font=("Segoe UI", 12))
        idioma_label.pack(side="left", padx=(10, 5))
        self.language_var = ctk.StringVar(value=i18n.current_language)
        idioma_selector = ctk.CTkComboBox(top_frame, 
                                          values=list(i18n.AVAILABLE_LANGUAGES.keys()),
                                          variable=self.language_var, width=80)
        idioma_selector.pack(side="left", padx=5)
        idioma_selector.bind("<<CTkComboBoxSelected>>", self._on_language_change)
        
        # Selector de diseño (Clásico vs Moderno)
        diseno_label = ctk.CTkLabel(top_frame, text="Diseño:", font=("Segoe UI", 12))
        diseno_label.pack(side="left", padx=(20, 5))
        self.design_var = ctk.StringVar(value=self.design_mode)
        diseno_selector = ctk.CTkComboBox(top_frame,
                                          values=["Clásico", "Moderno"],
                                          variable=self.design_var, width=100)
        diseno_selector.pack(side="left", padx=5)
        diseno_selector.bind("<<CTkComboBoxSelected>>", self._on_design_change)

    def _on_language_change(self, event):
        i18n.set_language(self.language_var.get())
        self.root.destroy()  # Se reinicia la interfaz para actualizar idioma
        # Se crea una nueva instancia conservando el diseño actual.
        self.__init__(design_mode=self.diseno_var.get())
        self.run()

    def _on_design_change(self, event):
        nuevo_diseno = self.design_var.get()
        if nuevo_diseno != self.design_mode:
            self.design_mode = nuevo_diseno
            self.root.destroy()
            self.__init__(design_mode=self.design_mode)
            self.run()
            
    def _crear_main_paned(self):
        # Se puede extraer a un método para la creación del paned window
        main_paned = tk.PanedWindow(self.root, orient='horizontal',
                                    sashrelief='raised', showhandle=True)
        main_paned.pack(fill='both', expand=True)
        return main_paned

    def _crear_left_panel(self, paned):
        from src.ui.panel_left import LeftPanel
        left_panel = LeftPanel(paned, self.controller)
        return left_panel

    def _crear_center_panel(self, paned):
        from src.ui.panel_center import CenterPanel
        center_panel = CenterPanel(paned)
        return center_panel

    def _crear_right_panel(self, paned):
        from src.ui.panel_right import RightPanel
        right_panel = RightPanel(paned, self.controller)
        return right_panel

    def run(self):
        self.root.mainloop()
