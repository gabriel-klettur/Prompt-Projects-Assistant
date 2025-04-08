# src/ui/panel_left.py

import tkinter as tk
from tkinter import ttk
from src.utils import i18n
import src.config as config


class LeftPanel:
    def __init__(self, parent, controller):
        self.controller = controller
        self.frame = tk.LabelFrame(parent, text=i18n.t("actions"), padx=10, pady=10)
        parent.add(self.frame, minsize=200)
        parent.paneconfig(self.frame, stretch="always")

        self.btn_select_prompt, self.status_prompt = self._crear_fila_boton_estado(
            i18n.t("select_prompt_base"), self.controller.seleccionar_prompt_base)

        # NUEVO: Input para carpetas/extensiones a ignorar
        self.label_ignore = tk.Label(self.frame, text=i18n.t("ignore_folders_extensions"))
        self.label_ignore.pack(anchor='w', pady=(10, 0))

        self.entry_ignore = tk.Text(self.frame, height=3, wrap='word')
        self.entry_ignore.pack(fill='x', padx=5, pady=(0, 10))
        self.entry_ignore.insert(tk.END, ", ".join(config.FOLDERS_TO_IGNORE))

        # 🚨 Trigger automático al salir del input
        self.entry_ignore.bind("<KeyRelease>", lambda e: self.controller.on_ignore_change())

        self.btn_select_project, self.status_project = self._crear_fila_boton_estado(
            i18n.t("select_project"), self.controller.seleccionar_proyecto)

        self.btn_select_files, self.status_files = self._crear_fila_boton_estado(
            i18n.t("select_files"), self.controller.seleccionar_archivos)
        self.btn_select_files.config(state='disabled')

        self.label_selected_files = tk.Label(self.frame, text=i18n.t("selected_files"))
        self.label_selected_files.pack(anchor='w', pady=(20, 0))

        listbox_frame = tk.Frame(self.frame)
        listbox_frame.pack(fill='both', expand=True)

        self.listbox_files = tk.Listbox(listbox_frame, height=10)
        self.listbox_files.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(listbox_frame, orient='vertical', command=self.listbox_files.yview)
        scrollbar.pack(side='right', fill='y')
        self.listbox_files.config(yscrollcommand=scrollbar.set)

    def _crear_fila_boton_estado(self, texto_boton, comando):
        frame = tk.Frame(self.frame)
        frame.pack(anchor='w', pady=5)
        boton = ttk.Button(frame, text=texto_boton, command=comando)
        boton.pack(side='left')
        estado = tk.Label(frame, text="❌", fg="red", width=2)
        estado.pack(side='left', padx=10)
        return boton, estado

    def set_prompt_base_estado(self, estado):
        self._set_estado(self.status_prompt, estado)
        self.btn_select_files['state'] = 'normal' if estado else 'disabled'

    def set_project_estado(self, estado):
        self._set_estado(self.status_project, estado)
        self.btn_select_files['state'] = 'normal' if estado else 'disabled'

    def set_archivos_estado(self, estado, cantidad=0):
        self._set_estado(self.status_files, estado)
        texto = f"{i18n.t('select_files')} ({cantidad})" if estado else i18n.t("select_files")
        self.btn_select_files.config(text=texto)

    def _set_estado(self, label, estado):
        icon = "✔️" if estado else "❌"
        color = "green" if estado else "red"
        label.config(text=icon, fg=color)

    def mostrar_lista_archivos(self, archivos):
        self.listbox_files.delete(0, tk.END)
        for archivo in archivos:
            self.listbox_files.insert(tk.END, archivo)
