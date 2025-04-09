# src/ui/panel_center.py

import tkinter as tk
import customtkinter as ctk
from src.utils import i18n

class CenterPanel:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent)

        self.title_label = ctk.CTkLabel(self.frame, text=i18n.t("context_view"), font=("Segoe UI", 14, "bold"))
        self.title_label.pack(anchor='w', padx=10, pady=(10, 5))

        self.label_prompt_base = ctk.CTkLabel(self.frame, text=i18n.t("prompt_base"))
        self.label_prompt_base.pack(anchor='w', padx=10)

        self.text_prompt_base = ctk.CTkTextbox(self.frame, height=150)
        self.text_prompt_base.pack(fill="both", expand=True, padx=10, pady=5)

        self.label_estructura = ctk.CTkLabel(self.frame, text=i18n.t("folder_structure"))
        self.label_estructura.pack(anchor='w', padx=10)

        self.text_directorio = ctk.CTkTextbox(self.frame, height=100)
        self.text_directorio.pack(fill="both", expand=True, padx=10, pady=5)

        self.label_archivos = ctk.CTkLabel(self.frame, text=i18n.t("file_content"))
        self.label_archivos.pack(anchor='w', padx=10)

        self.text_archivos = ctk.CTkTextbox(self.frame, height=150)
        self.text_archivos.pack(fill="both", expand=True, padx=10, pady=5)

        self.widgets = [
            self.title_label, self.label_prompt_base, self.text_prompt_base,
            self.label_estructura, self.text_directorio,
            self.label_archivos, self.text_archivos
        ]

    def mostrar_prompt_base(self, texto):
        self.text_prompt_base.delete("1.0", tk.END)
        self.text_prompt_base.insert(tk.END, texto, "prompt")

    def mostrar_estructura(self, estructura):
        self.text_directorio.delete("1.0", tk.END)
        self.text_directorio.insert(tk.END, estructura, "estructura")

    def mostrar_contenido_archivos(self, contenido):
        self.text_archivos.delete("1.0", tk.END)
        self.text_archivos.insert(tk.END, contenido, "archivos")

    def obtener_prompt_base(self):
        return self.text_prompt_base.get("1.0", tk.END).strip()

    def update_styles(self, estilos: dict):
        for widget in self.widgets:
            if isinstance(widget, (ctk.CTkLabel, ctk.CTkTextbox)):
                if "font" in estilos:
                    widget.configure(font=estilos["font"])
            try:
                if "fg_color" in estilos:
                    widget.configure(fg_color=estilos["bg_color"])
                if "text_color" in estilos:
                    widget.configure(text_color=estilos["fg_color"])
            except:
                pass
