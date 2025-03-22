# src/ui/main_window.py

import tkinter as tk
from tkinter import ttk
from src.ui.panel_left import LeftPanel
from src.ui.panel_center import CenterPanel
from src.ui.panel_right import RightPanel
from src.controller.prompt_controller import PromptController
from src.ui import PromptAssistantGUI
from src.utils import i18n
from src.config import FOLDERS_TO_IGNORE

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(i18n.t("title"))
        self.root.state('zoomed')
        self._center_window(500, 500)
        self.root.minsize(800, 600)

        self.language_var = tk.StringVar(value=i18n.current_language)
        self._crear_selector_idioma()

        self.gui_helper = PromptAssistantGUI(self.root, FOLDERS_TO_IGNORE)
        self.controller = PromptController(self.gui_helper, self)

        main_paned = tk.PanedWindow(self.root, orient='horizontal', sashrelief='raised', showhandle=True)
        main_paned.pack(fill='both', expand=True)

        self.left_panel = LeftPanel(main_paned, self.controller)
        self.center_panel = CenterPanel(main_paned)
        self.right_panel = RightPanel(main_paned, self.controller)

    def _center_window(self, width, height):
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _crear_selector_idioma(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill='x', padx=10, pady=(5, 0))
        tk.Label(top_frame, text=i18n.t("language") + ":", font=("Segoe UI", 10)).pack(side='left')
        language_selector = ttk.Combobox(
            top_frame,
            textvariable=self.language_var,
            values=list(i18n.AVAILABLE_LANGUAGES.keys()),
            state="readonly", width=5
        )
        language_selector.pack(side='left', padx=5)
        language_selector.bind("<<ComboboxSelected>>", self._on_language_change)

    def _on_language_change(self, event):
        i18n.set_language(self.language_var.get())
        self.root.destroy()
        self.__init__()
        self.run()

    def run(self):
        self.root.mainloop()
