# src/ui/panel_right.py

import tkinter as tk
import customtkinter as ctk
from src.utils import i18n

class RightPanel:
    def __init__(self, parent, controller):
        self.controller = controller
        self.frame = ctk.CTkFrame(parent)

        self.title_label = ctk.CTkLabel(self.frame, text=i18n.t("generated_prompt"), font=("Segoe UI", 14, "bold"))
        self.title_label.pack(anchor='w', padx=10, pady=(10, 5))

        self.text_prompt_final = ctk.CTkTextbox(self.frame, height=400)
        self.text_prompt_final.pack(fill="both", expand=True, padx=10, pady=5)

        botones_frame = ctk.CTkFrame(self.frame)
        botones_frame.pack(pady=10, padx=10)

        self.btn_copiar = ctk.CTkButton(botones_frame, text=i18n.t("copy"), command=self.controller.copiar_prompt, width=150)
        self.btn_copiar.pack(side="left", padx=10)

        self.btn_limpiar = ctk.CTkButton(botones_frame, text=i18n.t("clear"), command=self.controller.limpiar_todo, width=150)
        self.btn_limpiar.pack(side="left", padx=10)

        self.widgets = [
            self.title_label, self.text_prompt_final, self.btn_copiar, self.btn_limpiar
        ]

    def mostrar_prompt_final(self, prompt):
        self.text_prompt_final.delete("1.0", tk.END)
        self.text_prompt_final.insert(tk.END, prompt)

    def construir_prompt_final(self, prompt_base, estructura, archivos):
        self.text_prompt_final.delete("1.0", tk.END)

        if prompt_base:
            self._insertar_separador_titulado(i18n.t("section_prompt_base"))
            self.text_prompt_final.insert(tk.END, prompt_base + "\n", "prompt")

        if estructura:
            self._insertar_separador_titulado(i18n.t("section_structure"))
            self.text_prompt_final.insert(tk.END, estructura + "\n", "estructura")

        if archivos:
            self._insertar_separador_titulado(i18n.t("section_file_contents"))
            self.text_prompt_final.insert(tk.END, archivos, "archivos")

        return self.text_prompt_final.get("1.0", tk.END).strip()

    def _insertar_separador_titulado(self, titulo):
        self.text_prompt_final.insert(tk.END, f"\n-------------------------------------------------------\n", "separador")
        self.text_prompt_final.insert(tk.END, f"\n-------- {titulo.upper()} --------\n", "separador")
        self.text_prompt_final.insert(tk.END, f"\n-------------------------------------------------------\n", "separador")

    def obtener_prompt_final(self):
        return self.text_prompt_final.get("1.0", tk.END).strip()

    def update_styles(self, estilos: dict):
        for widget in self.widgets:
            if isinstance(widget, (ctk.CTkLabel, ctk.CTkTextbox, ctk.CTkButton)):
                if "font" in estilos:
                    widget.configure(font=estilos["font"])
            try:
                if "fg_color" in estilos:
                    widget.configure(fg_color=estilos["bg_color"])
                if "text_color" in estilos:
                    widget.configure(text_color=estilos["fg_color"])
            except:
                pass
