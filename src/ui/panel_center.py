# src/ui/panel_center.py

import tkinter as tk
from tkinter import ttk
from src.utils import i18n
import customtkinter as ctk

class CenterPanel:
    def __init__(self, parent):
        # Contenedor moderno para la vista de contexto
        self.frame = ctk.CTkFrame(parent)
        # Etiqueta para título
        self.title_label = ctk.CTkLabel(self.frame, text=i18n.t("context_view"), font=("Segoe UI", 14, "bold"))
        self.title_label.pack(anchor='w', padx=10, pady=(10, 5))
        
        # Área de texto para el prompt base
        self.label_prompt_base = ctk.CTkLabel(self.frame, text=i18n.t("prompt_base"))
        self.label_prompt_base.pack(anchor='w', padx=10)
        self.text_prompt_base = ctk.CTkTextbox(self.frame, height=150)
        self.text_prompt_base.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Área de texto para la estructura de carpetas
        self.label_estructura = ctk.CTkLabel(self.frame, text=i18n.t("folder_structure"))
        self.label_estructura.pack(anchor='w', padx=10)
        self.text_directorio = ctk.CTkTextbox(self.frame, height=100)
        self.text_directorio.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Área de texto para el contenido de archivos
        self.label_archivos = ctk.CTkLabel(self.frame, text=i18n.t("file_content"))
        self.label_archivos.pack(anchor='w', padx=10)
        self.text_archivos = ctk.CTkTextbox(self.frame, height=150)
        self.text_archivos.pack(fill="both", expand=True, padx=10, pady=5)

    def _crear_text_area(self, etiqueta):
        label = tk.Label(self.frame, text=i18n.t(etiqueta))
        label.pack(anchor='w')
        frame = tk.Frame(self.frame)
        frame.pack(fill='both', expand=True, pady=(0, 10))
        text_widget = tk.Text(frame, wrap='word', height=10)
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=text_widget.yview)
        scrollbar.pack(side='right', fill='y')
        text_widget.config(yscrollcommand=scrollbar.set)
        return text_widget

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
