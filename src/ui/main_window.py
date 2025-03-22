# ui/main_window.py

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from src.ui import PromptAssistantGUI
from src.core import FileManager
from src.core import PromptGenerator
from src.config import FOLDERS_TO_IGNORE

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Prompt Code Assistant")
        self.root.state('zoomed')
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

        self.estructura = None
        self.contenido_archivos = None

    def _center_window(self, window, width, height):
        x_position = (window.winfo_screenwidth() // 2) - (width // 2)
        y_position = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x_position}+{y_position}")

    def _create_widgets(self):
        # === FRAME PRINCIPAL ===
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill='both', expand=True)

        # Configurar 3 columnas expandibles
        main_frame.columnconfigure(0, weight=1)  # Columna izquierda
        main_frame.columnconfigure(1, weight=2)  # Columna central
        main_frame.columnconfigure(2, weight=2)  # Columna derecha

        # === COLUMNA 1: Panel Izquierdo ===
        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        self.btn_select_prompt = ttk.Button(left_frame, text="Seleccionar Prompt Base", command=self.select_prompt_base)
        self.status_prompt = tk.Label(left_frame, text="No seleccionado", fg="red")

        self.btn_select_project = ttk.Button(left_frame, text="Seleccionar Carpeta Proyecto", command=self.select_project_folder)
        self.status_project = tk.Label(left_frame, text="No seleccionado", fg="red")

        self.btn_select_files = ttk.Button(left_frame, text="Seleccionar Archivos", command=self.select_files, state='disabled')
        self.status_files = tk.Label(left_frame, text="No seleccionado", fg="red")        

        for widget in [self.btn_select_prompt, self.status_prompt,
                    self.btn_select_project, self.status_project,
                    self.btn_select_files, self.status_files]:
            widget.pack(pady=10, anchor='w')
        
        # Título del Listbox
        tk.Label(left_frame, text="Archivos seleccionados:").pack(anchor='w', pady=(20, 0))

        # Listbox + Scrollbar
        listbox_frame = tk.Frame(left_frame)
        listbox_frame.pack(fill='both', expand=True)

        self.listbox_files = tk.Listbox(listbox_frame, height=10)
        self.listbox_files.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(listbox_frame, orient='vertical', command=self.listbox_files.yview)
        scrollbar.pack(side='right', fill='y')

        self.listbox_files.config(yscrollcommand=scrollbar.set)

        # === COLUMNA 2: Panel Central ===
        center_frame = tk.Frame(main_frame)
        center_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

        self.text_prompt_base = tk.Text(center_frame, wrap='word', height=10)
        self.text_directorio = tk.Text(center_frame, wrap='word', height=10)
        self.text_archivos = tk.Text(center_frame, wrap='word', height=10)

        self.text_prompt_base.tag_configure("prompt", foreground="blue")
        self.text_directorio.tag_configure("estructura", foreground="green")
        self.text_archivos.tag_configure("archivos", foreground="purple")        

        for label, text_widget in [
            ("Prompt Base:", self.text_prompt_base),
            ("Estructura de Carpetas:", self.text_directorio),
            ("Contenido Archivos Seleccionados:", self.text_archivos)
        ]:
            tk.Label(center_frame, text=label).pack(anchor='w')
            text_widget.pack(fill='both', expand=True, pady=(0, 10))

        

        # === COLUMNA 3: Panel Derecho ===
        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=2, sticky='nsew', padx=10, pady=10)

        tk.Label(right_frame, text="Prompt Final Generado:").pack(anchor='w')

        self.text_prompt_final = tk.Text(right_frame, wrap='word')
        self.text_prompt_final.pack(fill='both', expand=True)

        self.text_prompt_final.tag_configure("prompt", foreground="blue")
        self.text_prompt_final.tag_configure("estructura", foreground="green")
        self.text_prompt_final.tag_configure("archivos", foreground="purple")

        frame_botones = tk.Frame(right_frame)
        frame_botones.pack(pady=10, anchor='s')

        self.btn_copiar = ttk.Button(frame_botones, text="Copiar", command=self.copy_to_clipboard)
        self.btn_save = ttk.Button(frame_botones, text="Guardar", command=self._guardar_prompt)
        self.btn_load = ttk.Button(frame_botones, text="Cargar", command=self._cargar_prompt)
        self.btn_clean = ttk.Button(frame_botones, text="Limpiar", command=self._limpiar_prompt)

        for btn in [self.btn_copiar, self.btn_save, self.btn_load, self.btn_clean]:
            btn.pack(side='left', padx=5)

        # === OTROS AJUSTES ===
        self.text_prompt_final.tag_configure("separador", foreground="orange")

    def _insertar_separador_titulado(self, text_widget, titulo):
        text_widget.insert(tk.END, f"\n-------------------------------------------------------\n", "separador")
        text_widget.insert(tk.END, f"\n-------- {titulo.upper()} --------\n", "separador")
        text_widget.insert(tk.END, f"\n-------------------------------------------------------\n", "separador")

    def _guardar_prompt(self):
        from tkinter import filedialog
        if self.prompt_final:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.prompt_final)

    def _cargar_prompt(self):
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                contenido = f.read()
                self.text_prompt_final.delete("1.0", tk.END)
                self.text_prompt_final.insert(tk.END, contenido)
                self.prompt_final = contenido.strip()  # Actualiza la variable
                self.btn_copiar['state'] = 'normal'    # ✅ Habilita el botón copiar


    def _limpiar_prompt(self):
        # Resetear textos
        self.text_prompt_base.delete("1.0", tk.END)
        self.text_directorio.delete("1.0", tk.END)
        self.text_archivos.delete("1.0", tk.END)
        self.text_prompt_final.delete("1.0", tk.END)

        # Resetear Listbox
        self.listbox_files.delete(0, tk.END)

        # Resetear estados visuales
        self.status_prompt.config(text="No seleccionado", fg="red")
        self.status_project.config(text="No seleccionado", fg="red")
        self.status_files.config(text="No seleccionado", fg="red")

        # Deshabilitar botones
        self.btn_select_files['state'] = 'disabled'
        self.btn_copiar['state'] = 'disabled'

        # Reiniciar variables
        self.prompt_base_selected = False
        self.project_folder_selected = False
        self.files_selected = False

        self.prompt_base_path = None
        self.project_folder = None
        self.selected_files = []
        self.prompt_final = None
        self.estructura = None
        self.contenido_archivos = None
        self.prompt_generator = None



    def select_prompt_base(self):
        path = self.gui_helper.seleccionar_ruta(tipo="archivo")
        if path:
            self.prompt_base_path = path
            self.prompt_base_selected = True
            self.status_prompt.config(text="Seleccionado", fg="green")
            self._check_ready_state()
            with open(path, 'r', encoding='utf-8') as f:
                contenido = f.read()
                self.text_prompt_base.delete(1.0, tk.END)
                self.text_prompt_base.insert(tk.END, contenido, "prompt")
                self._actualizar_prompt_final()
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
            self.estructura = self.file_manager.genera_estructura_de_carpetas(self.project_folder)
            
            self.text_directorio.delete(1.0, tk.END)
            self.text_directorio.insert(tk.END, self.estructura, "estructura")
            self._actualizar_prompt_final()
                        

        else:
            messagebox.showwarning("Advertencia", "No se seleccionó ninguna carpeta.")

    def select_files(self):
        self.selected_files.clear()
        self.files_selected = False        
        self.status_files.config(text="No seleccionado", fg="red")
        self.listbox_files.delete(0, tk.END)  # Vaciar el Listbox cuando se reinician los archivos seleccionados
        self.btn_copiar['state'] = 'disabled'  # Deshabilitar botón si no hay archivos
        
        if self.project_folder:
            self.selected_files = self.gui_helper.mostrar_arbol_directorios(self.project_folder)
            if self.selected_files:
                self.files_selected = True
                self.status_files.config(text=f"{len(self.selected_files)} archivos seleccionados", fg="green")
                self._update_file_list()  # Actualizar el Listbox con los archivos seleccionados                
                self._check_ready_state()

                self.contenido_archivos = self.file_manager.extrae_contenido_archivos(self.selected_files)
                self.text_archivos.delete(1.0, tk.END)
                self.text_archivos.insert(tk.END, self.contenido_archivos, "archivos")
                self._actualizar_prompt_final()                

            else:
                messagebox.showwarning("Advertencia", "No se seleccionaron archivos.")
                self.status_files.config(text="No seleccionado", fg="red")
                self.files_selected = False
                self.btn_copiar['state'] = 'disabled'  # Deshabilitar botón si no hay archivos 
                
        else:
            messagebox.showerror("Error", "Primero seleccione una carpeta de proyecto.")        

    def _actualizar_prompt_final(self):
        prompt_base = self.text_prompt_base.get("1.0", tk.END).strip()
        estructura = self.text_directorio.get("1.0", tk.END).strip()
        contenido_archivos = self.text_archivos.get("1.0", tk.END).strip()

        if not prompt_base:
            return

        self.text_prompt_final.delete("1.0", tk.END)

        # Separador: Prompt Base
        self._insertar_separador_titulado(self.text_prompt_final, "PROMPT BASE")
        self.text_prompt_final.insert(tk.END, prompt_base + "\n", "prompt")

        # Separador: Estructura
        if estructura:
            self._insertar_separador_titulado(self.text_prompt_final, "ESTRUCTURA DE CARPETAS")
            self.text_prompt_final.insert(tk.END, estructura + "\n", "estructura")

        # Separador: Archivos
        if contenido_archivos:
            self._insertar_separador_titulado(self.text_prompt_final, "CONTENIDO DE LOS ARCHIVOS SELECCIONADOS")
            self.text_prompt_final.insert(tk.END, contenido_archivos, "archivos")

        self.prompt_final = self.text_prompt_final.get("1.0", tk.END).strip()


    def _update_file_list(self):
        """Actualizar el Listbox con los archivos seleccionados."""
        self.listbox_files.delete(0, tk.END)  # Borrar contenido previo del Listbox
        for file in self.selected_files:
            self.listbox_files.insert(tk.END, file)  # Añadir archivos al Listbox

    def copy_to_clipboard(self):
        prompt_text = self.text_prompt_final.get("1.0", tk.END).strip()
        if prompt_text:
            try:
                self.root.clipboard_clear()
                self.root.clipboard_append(prompt_text)
                self.root.update()
                messagebox.showinfo("Éxito", "Prompt copiado al portapapeles.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo copiar: {str(e)}")
        else:
            messagebox.showwarning("Advertencia", "El prompt final está vacío.")

    def _check_ready_state(self):
        # Habilitar o deshabilitar el botón de copiar según el estado
        if self.prompt_base_selected and self.project_folder_selected:
            self.btn_copiar['state'] = 'normal'
        else:
            self.btn_copiar['state'] = 'disabled'

    def run(self):
        self.root.mainloop()
