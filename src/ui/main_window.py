# ui/main_window.py

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from src.ui import PromptAssistantGUI
from src.utils import FileManager
from src.utils import PromptGenerator
from src.config import FOLDERS_TO_IGNORE

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Prompt Code Assistant")
        self.root.geometry("500x500")  # Aumentamos el tamaño de la ventana para acomodar el Listbox
        self._center_window(self.root, 500, 500)

        # Inicializar variables de estado
        self.prompt_base_selected = False
        self.project_folder_selected = False
        self.files_selected = False

        self.prompt_base_path = None
        self.project_folder = None
        self.selected_files = []
        self.prompt_final = None

        # Inicializar componentes
        self._create_widgets()

        # Inicializar clases auxiliares
        self.gui_helper = PromptAssistantGUI(self.root, FOLDERS_TO_IGNORE)
        self.file_manager = FileManager(FOLDERS_TO_IGNORE)
        self.prompt_generator = None

    def _center_window(self, window, width, height):
        x_position = (window.winfo_screenwidth() // 2) - (width // 2)
        y_position = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x_position}+{y_position}")

    def _create_widgets(self):
        # Crear botones y etiquetas de estado
        self.btn_select_prompt = ttk.Button(self.root, text="Seleccionar Prompt Base", command=self.select_prompt_base)
        self.btn_select_project = ttk.Button(self.root, text="Seleccionar Carpeta Proyecto", command=self.select_project_folder)
        self.btn_select_files = ttk.Button(self.root, text="Seleccionar Archivos", command=self.select_files)
        self.btn_copy_clipboard = ttk.Button(self.root, text="Copiar al Portapapeles", command=self.copy_to_clipboard)

        # Deshabilitar botones según el estado
        self.btn_select_files['state'] = 'disabled'
        self.btn_copy_clipboard['state'] = 'disabled'

        # Indicadores de estado
        self.status_prompt = tk.Label(self.root, text="No seleccionado", fg="red")
        self.status_project = tk.Label(self.root, text="No seleccionado", fg="red")
        self.status_files = tk.Label(self.root, text="No seleccionado", fg="red")

        # Ubicar los widgets en la ventana
        self.btn_select_prompt.pack(pady=10)
        self.status_prompt.pack()

        self.btn_select_project.pack(pady=10)
        self.status_project.pack()

        self.btn_select_files.pack(pady=10)
        self.status_files.pack()

        # Crear Listbox para mostrar los archivos seleccionados
        self.lbl_selected_files = tk.Label(self.root, text="Archivos seleccionados:")
        self.lbl_selected_files.pack(pady=(10, 0))

        self.listbox_files = tk.Listbox(self.root, height=10, width=60)
        self.listbox_files.pack(pady=5)

        # Añadir scrollbar al Listbox
        scrollbar = ttk.Scrollbar(self.root, orient='vertical', command=self.listbox_files.yview)
        self.listbox_files.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        self.btn_copy_clipboard.pack(pady=20)

    def select_prompt_base(self):
        path = self.gui_helper.seleccionar_ruta(tipo="archivo")
        if path:
            self.prompt_base_path = path
            self.prompt_base_selected = True
            self.status_prompt.config(text="Seleccionado", fg="green")
            self._check_ready_state()
        else:
            messagebox.showwarning("Advertencia", "No se seleccionó ningún archivo.")

    def select_project_folder(self):
        path = self.gui_helper.seleccionar_ruta(tipo="carpeta")
        if path:
            self.project_folder = path
            self.project_folder_selected = True
            self.status_project.config(text="Seleccionado", fg="green")
            self.btn_select_files['state'] = 'normal'  # Habilitar selección de archivos
            self._check_ready_state()
        else:
            messagebox.showwarning("Advertencia", "No se seleccionó ninguna carpeta.")

    def select_files(self):
        self.selected_files.clear()
        self.files_selected = False        
        self.status_files.config(text="No seleccionado", fg="red")
        self.listbox_files.delete(0, tk.END)  # Vaciar el Listbox cuando se reinician los archivos seleccionados
        self.btn_copy_clipboard['state'] = 'disabled'  # Deshabilitar botón si no hay archivos
        
        if self.project_folder:
            self.selected_files = self.gui_helper.mostrar_arbol_directorios(self.project_folder)
            if self.selected_files:
                self.files_selected = True
                self.status_files.config(text=f"{len(self.selected_files)} archivos seleccionados", fg="green")
                self._update_file_list()  # Actualizar el Listbox con los archivos seleccionados                
                self._check_ready_state()
            else:
                messagebox.showwarning("Advertencia", "No se seleccionaron archivos.")
                self.status_files.config(text="No seleccionado", fg="red")
                self.files_selected = False
                self.btn_copy_clipboard['state'] = 'disabled'  # Deshabilitar botón si no hay archivos 
                
        else:
            messagebox.showerror("Error", "Primero seleccione una carpeta de proyecto.")        

    def _update_file_list(self):
        """Actualizar el Listbox con los archivos seleccionados."""
        self.listbox_files.delete(0, tk.END)  # Borrar contenido previo del Listbox
        for file in self.selected_files:
            self.listbox_files.insert(tk.END, file)  # Añadir archivos al Listbox

    def copy_to_clipboard(self):
        if self.prompt_base_selected and self.project_folder_selected:
            # Crear instancia de PromptGenerator
            self.prompt_generator = PromptGenerator(self.prompt_base_path)

            # Generar la estructura de carpetas
            estructura = self.file_manager.genera_estructura_de_carpetas(self.project_folder)
            self.prompt_generator.set_estructura_de_carpetas(estructura)

            # Extraer contenido de los archivos seleccionados
            if self.files_selected:
                contenido_archivos = self.file_manager.extrae_contenido_archivos(self.selected_files)
                self.prompt_generator.set_contenido_archivos(contenido_archivos)
            else:
                self.prompt_generator.set_contenido_archivos('')

            # Crear el prompt final
            self.prompt_final = self.prompt_generator.crear_prompt()

            # Copiar al portapapeles y mostrar mensaje
            self.gui_helper.copiar_al_portapapeles(self.prompt_final)
        else:
            messagebox.showerror("Error", "Asegúrese de haber seleccionado el prompt base y la carpeta del proyecto.")

    def _check_ready_state(self):
        # Habilitar o deshabilitar el botón de copiar según el estado
        if self.prompt_base_selected and self.project_folder_selected:
            self.btn_copy_clipboard['state'] = 'normal'
        else:
            self.btn_copy_clipboard['state'] = 'disabled'

    def run(self):
        self.root.mainloop()
