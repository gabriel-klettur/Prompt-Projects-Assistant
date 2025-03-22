# src/ui/main_window.py

import tkinter as tk
from tkinter import ttk
from src.ui import PromptAssistantGUI
from src.controller.prompt_controller import PromptController
from src.config import FOLDERS_TO_IGNORE
from src.utils import i18n


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(i18n.t("title"))
        self.root.state('zoomed')
        self._center_window(self.root, 500, 500)
        self.root.minsize(800, 600)

        # === SELECTOR DE IDIOMA ===
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill='x', padx=10, pady=(5, 0))

        tk.Label(top_frame, text=i18n.t("language") + ":", font=("Segoe UI", 10)).pack(side='left')

        self.language_var = tk.StringVar(value=i18n.current_language)
        language_selector = ttk.Combobox(
            top_frame,
            textvariable=self.language_var,
            values=list(i18n.AVAILABLE_LANGUAGES.keys()),
            state="readonly",
            width=5
        )
        language_selector.pack(side='left', padx=5)
        language_selector.bind("<<ComboboxSelected>>", self._on_language_change)

        self.gui_helper = PromptAssistantGUI(self.root, FOLDERS_TO_IGNORE)
        self.controller = PromptController(self.gui_helper, self)

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
        style.configure("Vertical.TScrollbar", gripcount=0, background="gray", troughcolor="white", bordercolor="gray", arrowcolor="black")

        main_paned = tk.PanedWindow(self.root, orient='horizontal', sashrelief='raised', showhandle=True)
        main_paned.pack(fill='both', expand=True)

        # === COLUMNA IZQUIERDA ===
        left_frame = tk.LabelFrame(main_paned, text=i18n.t("actions"), padx=10, pady=10)
        main_paned.add(left_frame, minsize=200)
        main_paned.paneconfig(left_frame, stretch="always")

        self.btn_select_prompt, self.status_prompt = self._crear_fila_boton_estado(
            left_frame, i18n.t("select_prompt_base"), self.controller.seleccionar_prompt_base)

        self.btn_select_project, self.status_project = self._crear_fila_boton_estado(
            left_frame, i18n.t("select_project"), self.controller.seleccionar_proyecto)

        self.btn_select_files, self.status_files = self._crear_fila_boton_estado(
            left_frame, i18n.t("select_files"), self.controller.seleccionar_archivos)
        self.btn_select_files.config(state='disabled')

        self.label_selected_files = tk.Label(left_frame, text=i18n.t("selected_files"))
        self.label_selected_files.pack(anchor='w', pady=(20, 0))

        listbox_frame = tk.Frame(left_frame)
        listbox_frame.pack(fill='both', expand=True)

        self.listbox_files = tk.Listbox(listbox_frame, height=10)
        self.listbox_files.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(listbox_frame, orient='vertical', command=self.listbox_files.yview)
        scrollbar.pack(side='right', fill='y')
        self.listbox_files.config(yscrollcommand=scrollbar.set)

        # === COLUMNA CENTRAL ===
        center_frame = tk.LabelFrame(main_paned, text=i18n.t("context_view"), padx=10, pady=10)
        main_paned.add(center_frame, minsize=200)
        main_paned.paneconfig(center_frame, stretch="always")

        self.label_prompt_base = tk.Label(center_frame, text=i18n.t("prompt_base"))
        self.label_prompt_base.pack(anchor='w')
        prompt_base_frame = tk.Frame(center_frame)
        prompt_base_frame.pack(fill='both', expand=True, pady=(0, 10))
        self.text_prompt_base = tk.Text(prompt_base_frame, wrap='word', height=10)
        self.text_prompt_base.pack(side='left', fill='both', expand=True)
        scrollbar_base = ttk.Scrollbar(prompt_base_frame, orient='vertical', command=self.text_prompt_base.yview)
        scrollbar_base.pack(side='right', fill='y')
        self.text_prompt_base.config(yscrollcommand=scrollbar_base.set)

        self.label_folder_structure = tk.Label(center_frame, text=i18n.t("folder_structure"))
        self.label_folder_structure.pack(anchor='w')
        directorio_frame = tk.Frame(center_frame)
        directorio_frame.pack(fill='both', expand=True, pady=(0, 10))
        self.text_directorio = tk.Text(directorio_frame, wrap='word', height=10)
        self.text_directorio.pack(side='left', fill='both', expand=True)
        scrollbar_directorio = ttk.Scrollbar(directorio_frame, orient='vertical', command=self.text_directorio.yview)
        scrollbar_directorio.pack(side='right', fill='y')
        self.text_directorio.config(yscrollcommand=scrollbar_directorio.set)

        self.label_file_content = tk.Label(center_frame, text=i18n.t("file_content"))
        self.label_file_content.pack(anchor='w')
        archivos_frame = tk.Frame(center_frame)
        archivos_frame.pack(fill='both', expand=True, pady=(0, 10))
        self.text_archivos = tk.Text(archivos_frame, wrap='word', height=10)
        self.text_archivos.pack(side='left', fill='both', expand=True)
        scrollbar_archivos = ttk.Scrollbar(archivos_frame, orient='vertical', command=self.text_archivos.yview)
        scrollbar_archivos.pack(side='right', fill='y')
        self.text_archivos.config(yscrollcommand=scrollbar_archivos.set)

        self.text_prompt_base.tag_configure("prompt", foreground="blue")
        self.text_directorio.tag_configure("estructura", foreground="green")
        self.text_archivos.tag_configure("archivos", foreground="purple")

        # === COLUMNA DERECHA ===
        right_frame = tk.LabelFrame(main_paned, text=i18n.t("generated_prompt"), padx=10, pady=10)
        main_paned.add(right_frame, minsize=200)
        main_paned.paneconfig(right_frame, stretch="always")

        self.label_final_prompt = tk.Label(right_frame, text=i18n.t("final_prompt"))
        self.label_final_prompt.pack(anchor='w')
        prompt_final_frame = tk.Frame(right_frame)
        prompt_final_frame.pack(fill='both', expand=True)
        self.text_prompt_final = tk.Text(prompt_final_frame, wrap='word')
        self.text_prompt_final.pack(side='left', fill='both', expand=True)
        scrollbar_final = ttk.Scrollbar(prompt_final_frame, orient='vertical', command=self.text_prompt_final.yview)
        scrollbar_final.pack(side='right', fill='y')
        self.text_prompt_final.config(yscrollcommand=scrollbar_final.set)

        frame_botones = tk.Frame(right_frame)
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
        self.btn_select_files.config(text=f"{i18n.t('select_files')} ({cantidad})" if estado else i18n.t("select_files"))

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

    def _on_language_change(self, event):
        nuevo_idioma = self.language_var.get()
        i18n.set_language(nuevo_idioma)
        self._actualizar_textos_ui()

    def _actualizar_textos_ui(self):
        self.root.title(i18n.t("title"))
        self.btn_select_prompt.config(text=i18n.t("select_prompt_base"))
        self.btn_select_project.config(text=i18n.t("select_project"))
        self.btn_select_files.config(text=i18n.t("select_files"))
        self.btn_copiar.config(text=i18n.t("copy"))
        self.btn_limpiar.config(text=i18n.t("clear"))
        self.label_selected_files.config(text=i18n.t("selected_files"))
        self.label_prompt_base.config(text=i18n.t("prompt_base"))
        self.label_folder_structure.config(text=i18n.t("folder_structure"))
        self.label_file_content.config(text=i18n.t("file_content"))
        self.label_final_prompt.config(text=i18n.t("final_prompt"))

    def run(self):
        self.root.mainloop()   