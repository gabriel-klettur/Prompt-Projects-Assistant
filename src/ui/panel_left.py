# src/ui/panel_left.py
import customtkinter as ctk
from src.utils import i18n
import src.config as config

class LeftPanel:
    def __init__(self, parent, controller):
        self.controller = controller
        # Contenedor moderno para acciones
        self.frame = ctk.CTkFrame(parent)
        self.frame.configure(height=600)  # Ajustar según sea necesario
        
        # Botón para seleccionar el prompt base
        self.btn_select_prompt = ctk.CTkButton(self.frame, text=i18n.t("select_prompt_base"),
                                               command=self.controller.seleccionar_prompt_base)
        self.btn_select_prompt.pack(pady=5, padx=10, fill="x")
        # Indicador de estado al lado (usaremos una etiqueta simple)
        self.status_prompt = ctk.CTkLabel(self.frame, text="❌", text_color="red", width=20)
        self.status_prompt.pack(pady=2, padx=10)
        
        # Área para especificar carpetas/extensiones a ignorar
        self.label_ignore = ctk.CTkLabel(self.frame, text=i18n.t("ignore_folders_extensions"))
        self.label_ignore.pack(anchor='w', padx=10, pady=(15, 5))
        self.entry_ignore = ctk.CTkTextbox(self.frame, height=60)
        self.entry_ignore.pack(fill='x', padx=10)
        self.entry_ignore.insert("0.0", ", ".join(config.FOLDERS_TO_IGNORE))
        self.entry_ignore.bind("<KeyRelease>", lambda e: self.controller.on_ignore_change())
        
        # Selector para "Only Extensions" (similar al anterior)
        self.label_only_ext = ctk.CTkLabel(self.frame, text=i18n.t("only_extensions"))
        self.label_only_ext.pack(anchor='w', padx=10, pady=(15, 5))
        self.entry_only_ext = ctk.CTkTextbox(self.frame, height=40)
        self.entry_only_ext.pack(fill='x', padx=10)
        self.entry_only_ext.bind("<KeyRelease>", lambda e: self.controller.on_ignore_change())
        
        # Botón para seleccionar carpeta del proyecto
        self.btn_select_project = ctk.CTkButton(self.frame, text=i18n.t("select_project"),
                                                command=self.controller.seleccionar_proyecto)
        self.btn_select_project.pack(pady=5, padx=10, fill="x")
        self.status_project = ctk.CTkLabel(self.frame, text="❌", text_color="red", width=20)
        self.status_project.pack(pady=2, padx=10)
        
        # Botón para seleccionar archivos
        self.btn_select_files = ctk.CTkButton(self.frame, text=i18n.t("select_files"),
                                              command=self.controller.seleccionar_archivos, state="disabled")
        self.btn_select_files.pack(pady=5, padx=10, fill="x")
        self.status_files = ctk.CTkLabel(self.frame, text="❌", text_color="red", width=20)
        self.status_files.pack(pady=2, padx=10)
        
        # ListBox moderno para mostrar archivos seleccionados
        self.label_selected_files = ctk.CTkLabel(self.frame, text=i18n.t("selected_files"))
        self.label_selected_files.pack(anchor='w', padx=10, pady=(20, 5))
        # CustomTkinter no ofrece directamente un widget Listbox; se puede usar CTkTextbox para mostrar listas
        self.listbox_files = ctk.CTkTextbox(self.frame, height=100)
        self.listbox_files.pack(fill="both", expand=False, padx=10, pady=(0,10))
    
    def set_prompt_base_estado(self, estado: bool):
        self._set_estado(self.status_prompt, estado)
        self.btn_select_files.configure(state="normal" if estado else "disabled")
    
    def set_project_estado(self, estado: bool):
        self._set_estado(self.status_project, estado)
        self.btn_select_files.configure(state="normal" if estado else "disabled")
    
    def set_archivos_estado(self, estado: bool, cantidad: int = 0):
        self._set_estado(self.status_files, estado)
        texto = f"{i18n.t('select_files')} ({cantidad})" if estado else i18n.t("select_files")
        self.btn_select_files.configure(text=texto)
    
    def _set_estado(self, label, estado: bool):
        icon = "✔️" if estado else "❌"
        text_color = "green" if estado else "red"
        label.configure(text=icon, text_color=text_color)
    
    def mostrar_lista_archivos(self, archivos: list):
        self.listbox_files.configure(state="normal")
        self.listbox_files.delete("0.0", "end")
        for archivo in archivos:
            self.listbox_files.insert("end", f"{archivo}\n")
        self.listbox_files.configure(state="disabled")
