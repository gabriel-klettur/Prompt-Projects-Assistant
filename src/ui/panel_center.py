# src/ui/panel_center.py

import tkinter as tk
from tkinter import ttk
from src.utils import i18n

class CenterPanel:
    def __init__(self, parent):
        self.frame = tk.LabelFrame(parent, text=i18n.t("context_view"), padx=10, pady=10)
        parent.add(self.frame, minsize=200)
        parent.paneconfig(self.frame, stretch="always")

        self.text_prompt_base = self._crear_text_area("prompt_base")
        self.text_directorio = self._crear_text_area("folder_structure")
        self.text_archivos = self._crear_text_area("file_content")

        self.text_prompt_base.tag_configure("prompt", foreground="blue")
        self.text_directorio.tag_configure("estructura", foreground="green")
        self.text_archivos.tag_configure("archivos", foreground="purple")

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
