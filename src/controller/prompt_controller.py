# src/controller/prompt_controller.py

from tkinter import messagebox
from src.core import FileManager
from src.config import FOLDERS_TO_IGNORE

class PromptController:
    def __init__(self, gui_helper, view):
        self.view = view
        self.gui_helper = gui_helper
        self.file_manager = FileManager(FOLDERS_TO_IGNORE)
        self.prompt_base_path = None
        self.project_folder = None
        self.selected_files = []
        self.estructura = ''
        self.contenido_archivos = ''
        self.prompt_final = ''

    def seleccionar_prompt_base(self):
        path = self.gui_helper.seleccionar_ruta(tipo="archivo")
        if path:
            self.prompt_base_path = path
            self.view.set_prompt_base_estado(True, path)
            with open(path, 'r', encoding='utf-8') as f:
                contenido = f.read()
                self.view.mostrar_prompt_base(contenido)
            self.actualizar_prompt_final()
        else:
            messagebox.showwarning("Advertencia", "No se seleccionó ningún archivo.")

    def seleccionar_proyecto(self):
        path = self.gui_helper.seleccionar_ruta(tipo="carpeta")
        if path:
            self.project_folder = path
            self.view.set_project_estado(True, path)
            self.estructura = self.file_manager.genera_estructura_de_carpetas(path)
            self.view.mostrar_estructura(self.estructura)
            self.actualizar_prompt_final()
        else:
            messagebox.showwarning("Advertencia", "No se seleccionó ninguna carpeta.")

    def seleccionar_archivos(self):
        if not self.project_folder:
            messagebox.showerror("Error", "Primero seleccione una carpeta de proyecto.")
            return

        self.selected_files = self.gui_helper.mostrar_arbol_directorios(self.project_folder)
        if self.selected_files:
            self.view.set_archivos_estado(True, len(self.selected_files))
            self.view.mostrar_lista_archivos(self.selected_files)
            self.contenido_archivos = self.file_manager.extrae_contenido_archivos(self.selected_files)
            self.view.mostrar_contenido_archivos(self.contenido_archivos)
            self.actualizar_prompt_final()
        else:
            messagebox.showwarning("Advertencia", "No se seleccionaron archivos.")
            self.view.set_archivos_estado(False)

    def actualizar_prompt_final(self):
        prompt_base = self.view.obtener_prompt_base()
        if not prompt_base:
            return
        self.prompt_final = self.view.construir_prompt_final(prompt_base, self.estructura, self.contenido_archivos)


    def copiar_prompt(self):
        if self.prompt_final:
            self.gui_helper.copiar_al_portapapeles(self.prompt_final)
        else:
            messagebox.showwarning("Advertencia", "El prompt final está vacío.")
    
    def limpiar_todo(self):
        self.prompt_base_path = None
        self.project_folder = None
        self.selected_files = []
        self.estructura = ''
        self.contenido_archivos = ''
        self.prompt_final = ''

        # Limpiar la interfaz
        self.view.set_prompt_base_estado(False, "")
        self.view.set_project_estado(False, "")
        self.view.set_archivos_estado(False)
        self.view.mostrar_prompt_base("")
        self.view.mostrar_estructura("")
        self.view.mostrar_contenido_archivos("")
        self.view.mostrar_lista_archivos([])
        self.view.mostrar_prompt_final("")

        # Mensaje de confirmación
        messagebox.showinfo("Prompt Assistant", "Todos los campos han sido limpiados correctamente.")

