# src/ui/main_window.py

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from src.utils import i18n
from src.config import FOLDERS_TO_IGNORE
from src.controller.prompt_controller import PromptController
from src.ui import PromptAssistantGUI
from src.ui.themes.theme_manager import ThemeManager

class MainWindow:
    def __init__(self, design_mode="Moderno"):
        self.theme_name = design_mode  # "Clasico", "Moderno" o "Light"

        # Crear ventana principal
        self.root = ctk.CTk()
        self.root.title(i18n.t("title"))
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)

        # Aplicar tema seleccionado
        self.theme_manager = ThemeManager(self.root, self.theme_name)
        self.theme_manager.apply_theme()

        # Crear menú de idioma y diseño
        self._crear_seleccion_idioma_y_diseno()

        # Inicializar GUI helper y controlador
        self.gui_helper = PromptAssistantGUI(self.root, FOLDERS_TO_IGNORE)
        self.controller = PromptController(self.gui_helper, self)

        # Crear contenedor de paneles
        container = ctk.CTkFrame(self.root)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Importar y crear los paneles
        from src.ui.panel_left import LeftPanel
        from src.ui.panel_center import CenterPanel
        from src.ui.panel_right import RightPanel

        self.left_panel = LeftPanel(container, self.controller)
        self.center_panel = CenterPanel(container)
        self.right_panel = RightPanel(container, self.controller)

        self.left_panel.frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.center_panel.frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.right_panel.frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=2)
        container.grid_columnconfigure(2, weight=1)
        container.grid_rowconfigure(0, weight=1)

    def _crear_seleccion_idioma_y_diseno(self):
        top_frame = ctk.CTkFrame(self.root, height=50)
        top_frame.pack(fill="x", padx=10, pady=(10, 0))

        idioma_label = ctk.CTkLabel(top_frame, text=f"{i18n.t('language')}:", font=("Segoe UI", 12))
        idioma_label.pack(side="left", padx=(10, 5))

        self.language_var = ctk.StringVar(value=i18n.current_language)
        idioma_selector = ctk.CTkComboBox(top_frame,
                                        values=list(i18n.AVAILABLE_LANGUAGES.keys()),
                                        variable=self.language_var,
                                        width=80,
                                        command=self._on_language_change)
        idioma_selector.pack(side="left", padx=5)

        diseno_label = ctk.CTkLabel(top_frame, text="Diseño:", font=("Segoe UI", 12))
        diseno_label.pack(side="left", padx=(20, 5))

        self.design_var = ctk.StringVar(value=self.theme_name)
        diseno_selector = ctk.CTkComboBox(top_frame,
                                        values=["Clasico", "Moderno", "Light"],
                                        variable=self.design_var,
                                        width=100,
                                        command=self._on_design_change)
        diseno_selector.pack(side="left", padx=5)

        # 🔧 Guarda widgets para actualizar luego
        self.top_widgets = [top_frame, idioma_label, idioma_selector, diseno_label, diseno_selector]

    def _on_language_change(self, nuevo_idioma):
        print(f"[Idioma] Cambiado a: {nuevo_idioma}")
        if nuevo_idioma != i18n.current_language:
            i18n.set_language(nuevo_idioma)
            self.root.destroy()
            self.__init__(design_mode=self.theme_name)
            self.run()

    def _on_design_change(self, nuevo_diseno):
        print(f"[Diseño] Cambiado a: {nuevo_diseno}")
        if nuevo_diseno != self.theme_name:
            self.root.destroy()
            self.__init__(design_mode=nuevo_diseno)
            self.run()

    def _crear_main_paned(self):
        main_paned = tk.PanedWindow(self.root, orient='horizontal',
                                    sashrelief='raised', showhandle=True)
        main_paned.pack(fill='both', expand=True)
        return main_paned

    def _crear_left_panel(self, paned):
        from src.ui.panel_left import LeftPanel
        return LeftPanel(paned, self.controller)

    def _crear_center_panel(self, paned):
        from src.ui.panel_center import CenterPanel
        return CenterPanel(paned)

    def _crear_right_panel(self, paned):
        from src.ui.panel_right import RightPanel
        return RightPanel(paned, self.controller)

    def run(self):
        self.root.mainloop()

    def _update_top_styles(self, estilos: dict):
        for widget in self.top_widgets:
            if isinstance(widget, (ctk.CTkLabel, ctk.CTkComboBox)):
                if "font" in estilos:
                    widget.configure(font=estilos["font"])
            try:
                if "fg_color" in estilos:
                    widget.configure(fg_color=estilos["bg_color"])
                if "text_color" in estilos:
                    widget.configure(text_color=estilos["fg_color"])
            except:
                pass
