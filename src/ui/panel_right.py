# src/ui/panel_right.py

import tkinter as tk
from tkinter import ttk
from src.utils import i18n


class RightPanel:
    def __init__(self, parent, controller):
        self.controller = controller
        self.frame = tk.LabelFrame(parent, text=i18n.t("generated_prompt"), padx=10, pady=10)
        parent.add(self.frame, minsize=200)
        parent.paneconfig(self.frame, stretch="always")

        self.label_final_prompt = tk.Label(self.frame, text=i18n.t("final_prompt"))
        self.label_final_prompt.pack(anchor='w')

        prompt_final_frame = tk.Frame(self.frame)
        prompt_final_frame.pack(fill='both', expand=True)

        self.text_prompt_final = tk.Text(prompt_final_frame, wrap='word')
        self.text_prompt_final.pack(side='left', fill='both', expand=True)

        scrollbar_final = ttk.Scrollbar(prompt_final_frame, orient='vertical', command=self.text_prompt_final.yview)
        scrollbar_final.pack(side='right', fill='y')
        self.text_prompt_final.config(yscrollcommand=scrollbar_final.set)

        # Colores de las secciones
        self.text_prompt_final.tag_configure("prompt", foreground="blue")
        self.text_prompt_final.tag_configure("estructura", foreground="green")
        self.text_prompt_final.tag_configure("archivos", foreground="purple")
        self.text_prompt_final.tag_configure("separador", foreground="orange")

        # Botones Copiar y Limpiar
        frame_botones = tk.Frame(self.frame)
        frame_botones.pack(pady=10, anchor='s')

        self.btn_copiar = tk.Button(
            frame_botones,
            text=i18n.t("copy"),
            bg="#4CAF50", fg="white",
            font=("Segoe UI", 10, "bold"),
            width=20,
            command=self.controller.copiar_prompt
        )
        self.btn_copiar.pack(side='left', padx=10)

        self.btn_limpiar = tk.Button(
            frame_botones,
            text=i18n.t("clear"),
            bg="#F44336", fg="white",
            font=("Segoe UI", 10, "bold"),
            width=20,
            command=self.controller.limpiar_todo
        )
        self.btn_limpiar.pack(side='left', padx=10)

    def mostrar_prompt_final(self, prompt):
        self.text_prompt_final.delete("1.0", tk.END)
        self.text_prompt_final.insert(tk.END, prompt)

    def construir_prompt_final(self, prompt_base, estructura, archivos):
        self.text_prompt_final.delete("1.0", tk.END)

        if prompt_base:
            self._insertar_separador_titulado("PROMPT BASE")
            self.text_prompt_final.insert(tk.END, prompt_base + "\n", "prompt")

        if estructura:
            self._insertar_separador_titulado("ESTRUCTURA DE CARPETAS")
            self.text_prompt_final.insert(tk.END, estructura + "\n", "estructura")

        if archivos:
            self._insertar_separador_titulado("CONTENIDO DE LOS ARCHIVOS SELECCIONADOS")
            self.text_prompt_final.insert(tk.END, archivos, "archivos")

        return self.text_prompt_final.get("1.0", tk.END).strip()

    def _insertar_separador_titulado(self, titulo):
        self.text_prompt_final.insert(tk.END, f"\n-------------------------------------------------------\n", "separador")
        self.text_prompt_final.insert(tk.END, f"\n-------- {titulo.upper()} --------\n", "separador")
        self.text_prompt_final.insert(tk.END, f"\n-------------------------------------------------------\n", "separador")

    def obtener_prompt_final(self):
        return self.text_prompt_final.get("1.0", tk.END).strip()