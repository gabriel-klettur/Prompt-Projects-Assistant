# src/ui/main_window.py

import tkinter as tk
from tkinter import ttk
from src.ui import PromptAssistantGUI
from src.controller.prompt_controller import PromptController
from src.config import FOLDERS_TO_IGNORE

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Prompt Code Assistant")
        self.root.state('zoomed')
        self._center_window(self.root, 500, 500)
        self.root.minsize(800, 600)  # Ancho mínimo total (3 columnas de 200), alto mínimo 400

        # Inicializar GUI helper y controlador
        self.gui_helper = PromptAssistantGUI(self.root, FOLDERS_TO_IGNORE)
        self.controller = PromptController(self.gui_helper, self)

        # Inicializar componentes visuales
        self._create_widgets()

    def _center_window(self, window, width, height):
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def _create_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("TLabel", font=("Segoe UI", 10))

        main_paned = tk.PanedWindow(self.root, orient='horizontal', sashrelief='raised', showhandle=True)
        main_paned.pack(fill='both', expand=True)

        # === COLUMNA IZQUIERDA ===
        left_frame = tk.LabelFrame(main_paned, text="Acciones", padx=10, pady=10)
        main_paned.add(left_frame, minsize=200)
        main_paned.paneconfig(left_frame, stretch="always")

        self.btn_select_prompt, self.status_prompt = self._crear_fila_boton_estado(
            left_frame, "Seleccionar Prompt Base", self.controller.seleccionar_prompt_base)

        self.btn_select_project, self.status_project = self._crear_fila_boton_estado(
            left_frame, "Seleccionar Carpeta Proyecto", self.controller.seleccionar_proyecto)

        self.btn_select_files, self.status_files = self._crear_fila_boton_estado(
            left_frame, "Seleccionar Archivos", self.controller.seleccionar_archivos)
        self.btn_select_files.config(state='disabled')

        tk.Label(left_frame, text="Archivos seleccionados:").pack(anchor='w', pady=(20, 0))
        listbox_frame = tk.Frame(left_frame)
        listbox_frame.pack(fill='both', expand=True)

        self.listbox_files = tk.Listbox(listbox_frame, height=10)
        self.listbox_files.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(listbox_frame, orient='vertical', command=self.listbox_files.yview)
        scrollbar.pack(side='right', fill='y')
        self.listbox_files.config(yscrollcommand=scrollbar.set)

        # === COLUMNA CENTRAL ===
        center_frame = tk.LabelFrame(main_paned, text="Visualización de Contexto", padx=10, pady=10)
        main_paned.add(center_frame, minsize=200)
        main_paned.paneconfig(center_frame, stretch="always")

        self.text_prompt_base = tk.Text(center_frame, wrap='word', height=10)
        self.text_directorio = tk.Text(center_frame, wrap='word', height=10)
        self.text_archivos = tk.Text(center_frame, wrap='word', height=10)

        self.text_prompt_base.tag_configure("prompt", foreground="blue")
        self.text_directorio.tag_configure("estructura", foreground="green")
        self.text_archivos.tag_configure("archivos", foreground="purple")

        for label, widget in [
            ("Prompt Base:", self.text_prompt_base),
            ("Estructura de Carpetas:", self.text_directorio),
            ("Contenido Archivos Seleccionados:", self.text_archivos)
        ]:
            tk.Label(center_frame, text=label).pack(anchor='w')
            widget.pack(fill='both', expand=True, pady=(0, 10))

        # === COLUMNA DERECHA ===
        right_frame = tk.LabelFrame(main_paned, text="Prompt Generado", padx=10, pady=10)
        main_paned.add(right_frame, minsize=200)
        main_paned.paneconfig(right_frame, stretch="always")

        tk.Label(right_frame, text="Prompt Final Generado:").pack(anchor='w')
        self.text_prompt_final = tk.Text(right_frame, wrap='word')
        self.text_prompt_final.pack(fill='both', expand=True)

        frame_botones = tk.Frame(right_frame)
        frame_botones.pack(pady=10, anchor='s')
        self.btn_copiar = ttk.Button(frame_botones, text="Copiar", command=self.controller.copiar_prompt)
        self.btn_copiar.pack(side='left', padx=5)

        self.text_prompt_final.tag_configure("prompt", foreground="blue")
        self.text_prompt_final.tag_configure("estructura", foreground="green")
        self.text_prompt_final.tag_configure("archivos", foreground="purple")
        self.text_prompt_final.tag_configure("separador", foreground="orange")

    def _crear_fila_boton_estado(self, parent, texto_boton, comando):
        frame = tk.Frame(parent)
        frame.pack(anchor='w', pady=5)
        boton = ttk.Button(frame, text=texto_boton, command=comando)
        boton.pack(side='left')
        estado = tk.Label(frame, text="❌", fg="red", width=2)
        estado.pack(side='left', padx=10)
        return boton, estado

    def set_prompt_base_estado(self, estado, ruta):
        icon = "✔️" if estado else "❌"
        color = "green" if estado else "red"
        self.status_prompt.config(text=f"{icon}", fg=color)
        self.btn_select_files['state'] = 'normal' if estado else 'disabled'

    def set_project_estado(self, estado, ruta):
        icon = "✔️" if estado else "❌"
        color = "green" if estado else "red"
        self.status_project.config(text=f"{icon}", fg=color)
        self.btn_select_files['state'] = 'normal' if estado else 'disabled'

    def set_archivos_estado(self, estado, cantidad=0):
        icon = "✔️" if estado else "❌"
        color = "green" if estado else "red"        
        self.status_files.config(text=f"{icon}", fg=color)
        self.btn_select_files.config(text=f"Seleccionar Archivos ({cantidad})" if estado else "Seleccionar Archivos")

    def mostrar_prompt_base(self, texto):
        self.text_prompt_base.delete("1.0", tk.END)
        self.text_prompt_base.insert(tk.END, texto, "prompt")

    def mostrar_estructura(self, estructura):
        self.text_directorio.delete("1.0", tk.END)
        self.text_directorio.insert(tk.END, estructura, "estructura")

    def mostrar_contenido_archivos(self, contenido):
        self.text_archivos.delete("1.0", tk.END)
        self.text_archivos.insert(tk.END, contenido, "archivos")

    def mostrar_lista_archivos(self, archivos):
        self.listbox_files.delete(0, tk.END)
        for archivo in archivos:
            self.listbox_files.insert(tk.END, archivo)

    def mostrar_prompt_final(self, prompt):
        self.text_prompt_final.delete("1.0", tk.END)
        self.text_prompt_final.insert(tk.END, prompt)

    def obtener_prompt_base(self):
        return self.text_prompt_base.get("1.0", tk.END).strip()

    def construir_prompt_final(self, prompt_base, estructura, archivos):
        self.text_prompt_final.delete("1.0", tk.END)

        if prompt_base:
            self._insertar_separador_titulado(self.text_prompt_final, "PROMPT BASE")
            self.text_prompt_final.insert(tk.END, prompt_base + "\n", "prompt")

        if estructura:
            self._insertar_separador_titulado(self.text_prompt_final, "ESTRUCTURA DE CARPETAS")
            self.text_prompt_final.insert(tk.END, estructura + "\n", "estructura")

        if archivos:
            self._insertar_separador_titulado(self.text_prompt_final, "CONTENIDO DE LOS ARCHIVOS SELECCIONADOS")
            self.text_prompt_final.insert(tk.END, archivos, "archivos")

        return self.text_prompt_final.get("1.0", tk.END).strip()

    def _insertar_separador_titulado(self, text_widget, titulo):
        text_widget.insert(tk.END, f"\n-------------------------------------------------------\n", "separador")
        text_widget.insert(tk.END, f"\n-------- {titulo.upper()} --------\n", "separador")
        text_widget.insert(tk.END, f"\n-------------------------------------------------------\n", "separador")

    def run(self):
        self.root.mainloop()
