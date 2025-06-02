# Path: src/ui/prompt_assistant_gui.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from pathlib import Path
from src.utils import i18n

import tkinter as tk
from tkinter import ttk


class PromptAssistantGUI:
    def __init__(self, root, folders_to_ignore=None, only_extensions=None, theme_styles=None, only_folders=None):
        self.root = root
        self.folders_to_ignore = folders_to_ignore if folders_to_ignore else []
        self.only_extensions = only_extensions if only_extensions else []
        self.archivos_seleccionados = []
        self.theme_styles = theme_styles or {}
        self.only_folders = only_folders if only_folders else []

    def seleccionar_ruta(self, tipo="archivo"):
        if tipo == "archivo":
            return filedialog.askopenfilename(parent=self.root, title=i18n.t("select_file"))
        elif tipo == "carpeta":
            return filedialog.askdirectory(parent=self.root, title=i18n.t("select_folder"))
        return None

    def copiar_al_portapapeles(self, texto):
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(texto)
            self.root.update()
            messagebox.showinfo(i18n.t("app_name"), i18n.t("copied_to_clipboard"), parent=self.root)
        except Exception as e:
            messagebox.showerror(i18n.t("app_name"), f"{i18n.t('clipboard_error')} {str(e)}")

    def mostrar_arbol_directorios(self, carpeta):
        self.archivos_seleccionados = []
        # Mostrar sólo las carpetas indicadas en only_folders, o toda la estructura si está vacío
        ventana = ctk.CTkToplevel(self.root)
        ventana.title(i18n.t("select_files_title"))

        # Dimensiones y centrar en pantalla
        ancho_ventana, alto_ventana = 800, 600
        ventana.geometry(f"{ancho_ventana}x{alto_ventana}")
        self._centro_ventana(ventana, ancho_ventana, alto_ventana)

        # Frame superior donde colocamos la sección de extensiones
        top_frame = ctk.CTkFrame(ventana)
        top_frame.pack(fill="x", padx=10, pady=5)

        extension_label = ctk.CTkLabel(
            top_frame,
            text=i18n.t("only_extensions"),
            font=("Segoe UI", 10, "bold")
        )
        extension_label.pack(anchor="w")

        # Obtener colores del tema actual
        bg_color = self.theme_styles.get("bg_color", "#2a2d2e")
        fg_color = self.theme_styles.get("fg_color", "white")
        highlight_color = self.theme_styles.get("button_bg", "#1f538d")
        selected_fg = self.theme_styles.get("button_fg", "white")

        # --- Canvas con fondo adaptado y CTkScrollbar horizontal ---
        canvas_ext = tk.Canvas(
            top_frame,
            height=35,
            bg=bg_color,           # Ahora usa el color del tema
            highlightthickness=0,
            borderwidth=0
        )
        canvas_ext.pack(fill='x', side='top')

        scroll_x = ctk.CTkScrollbar(
            master=top_frame,
            orientation="horizontal",
            command=canvas_ext.xview
        )
        scroll_x.pack(fill='x', side='bottom')
        canvas_ext.configure(xscrollcommand=scroll_x.set)

        # Frame interior donde van los CheckBoxes de extensiones
        inner_frame = ctk.CTkFrame(canvas_ext, fg_color=bg_color)
        canvas_ext.create_window((0, 0), window=inner_frame, anchor='nw')

        def on_configure(event):
            canvas_ext.configure(scrollregion=canvas_ext.bbox("all"))
        inner_frame.bind("<Configure>", on_configure)

        extensions = self._extraer_extensiones_disponibles(carpeta)
        self.extension_vars = {}

        for ext in sorted(extensions):
            var = tk.BooleanVar()
            cb = ctk.CTkCheckBox(
                inner_frame,
                text=ext,
                variable=var,
                command=self._on_extension_checkbox_change,
                fg_color=bg_color,       # Fondo igual que el tema
                text_color=fg_color      # Texto según tema
            )
            cb.pack(side='left', padx=5)
            self.extension_vars[ext] = var

        # --- Sección del árbol de directorios con un CTkFrame ---
        tree_frame = ctk.CTkFrame(ventana)
        tree_frame.pack(expand=True, fill='both', padx=10, pady=5)

        # Estilo para el Treeview
        style = ttk.Style(tree_frame)
        style.theme_use("clam")
        style.configure("Treeview",
                        background=bg_color,
                        fieldbackground=bg_color,
                        foreground=fg_color,
                        borderwidth=0)
        style.configure("Treeview.Heading",
                        background=bg_color,
                        foreground=fg_color)
        style.map("Treeview",
                  background=[("selected", highlight_color)],
                  foreground=[("selected", selected_fg)])

        self.tree = ttk.Treeview(tree_frame, selectmode='extended')
        self.tree.pack(expand=True, fill='both')

        # Eventos en el Treeview
        self.tree.bind("<Button-1>", self._interceptar_click)
        self.tree.bind("<ButtonRelease-1>", self._on_tree_click)

        self.nodos_rutas = {}
        self._preparar_arbol(self.tree, carpeta, self.nodos_rutas)

        # Botón de confirmación
        btn_confirmar = ctk.CTkButton(
            ventana,
            text=i18n.t("confirm_selection"),
            command=lambda: self._on_confirmar(self.tree, self.nodos_rutas, ventana)
        )
        btn_confirmar.pack(pady=10)

        ventana.wait_window()
        return self.archivos_seleccionados

    def _centro_ventana(self, ventana, ancho_ventana, alto_ventana):
        posicion_x = (ventana.winfo_screenwidth() // 2) - (ancho_ventana // 2)
        posicion_y = (ventana.winfo_screenheight() // 2) - (alto_ventana // 2)
        ventana.geometry(f"+{posicion_x}+{posicion_y}")

    def _extraer_extensiones_disponibles(self, carpeta):
        extensiones = set()
        carpeta = os.path.abspath(carpeta)
        for root, dirs, files in os.walk(carpeta):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in self.folders_to_ignore]
            for file in files:
                if file.startswith(".") or any(file.endswith(ext) for ext in self.folders_to_ignore):
                    continue
                ext = Path(file).suffix
                if ext:
                    extensiones.add(ext)
        return extensiones

    def _insertar_nodo(self, tree, padre, texto, path, nodos_rutas):
        path_obj = Path(path)
        name = path_obj.name
        if (
            name.startswith('.') or
            name in self.folders_to_ignore or
            any(name.endswith(ext) for ext in self.folders_to_ignore)
        ):
            return None

        nodo = tree.insert(padre, 'end', text=texto, open=False)
        nodos_rutas[nodo] = str(path_obj)

        if path_obj.is_dir():
            tree.insert(nodo, 'end')
        return nodo

    def _expandir_todo(self, tree, nodo, nodos_rutas):
        tree.item(nodo, open=True)
        path = nodos_rutas.get(nodo)
        if path and os.path.isdir(path):
            for hijo in tree.get_children(nodo):
                self._expandir_todo(tree, hijo, nodos_rutas)

    def _cargar_arbol(self, tree, nodo, nodos_rutas):
        path = nodos_rutas.get(nodo, '')
        if path and os.path.isdir(path):
            # Limpiar hijos actuales del nodo
            for hijo in tree.get_children(nodo):
                tree.delete(hijo)

            with os.scandir(path) as it:
                elementos = sorted(it, key=lambda e: (not e.is_dir(), e.name))
                for elemento in elementos:
                    abspath = os.path.join(path, elemento.name)
                    hijo = self._insertar_nodo(tree, nodo, elemento.name, abspath, nodos_rutas)
                    if hijo and elemento.is_dir():
                        self._cargar_arbol(tree, hijo, nodos_rutas)

    def _preparar_arbol(self, tree, carpeta, nodos_rutas):
        # Si se especificaron only_folders, incluir carpetas coincidentes en cualquier nivel
        if self.only_folders:
            matched = []
            for root, dirs, files in os.walk(carpeta):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in self.folders_to_ignore]
                for d in dirs:
                    if d in self.only_folders:
                        matched.append(os.path.join(root, d))
            for folder_path in matched:
                rel = os.path.relpath(folder_path, carpeta)
                node = tree.insert('', 'end', text=rel, open=True)
                nodos_rutas[node] = folder_path
                self._cargar_arbol(tree, node, nodos_rutas)
                self._expandir_todo(tree, node, nodos_rutas)
            return
        # Caso por defecto: toda la estructura del proyecto
        root_nodo = self._insertar_nodo(tree, '', carpeta, carpeta, nodos_rutas)
        if root_nodo:
            self._cargar_arbol(tree, root_nodo, nodos_rutas)
            self._expandir_todo(tree, root_nodo, nodos_rutas)
            tree.bind('<<TreeviewOpen>>', lambda event: self._on_open(event, tree, nodos_rutas))

    def _on_open(self, event, tree, nodos_rutas):
        nodo = tree.focus()
        self._cargar_arbol(tree, nodo, nodos_rutas)

    def _on_confirmar(self, tree, nodos_rutas, ventana):
        seleccionados = tree.selection()
        for nodo in seleccionados:
            path = nodos_rutas.get(nodo)
            if path and os.path.isfile(path):
                self.archivos_seleccionados.append(path)
        ventana.destroy()

    def _on_extension_checkbox_change(self):
        extensiones_seleccionadas = [ext for ext, var in self.extension_vars.items() if var.get()]
        for nodo, path in self.nodos_rutas.items():
            if os.path.isfile(path):
                ext = Path(path).suffix
                if ext in extensiones_seleccionadas:
                    self.tree.selection_add(nodo)
                else:
                    self.tree.selection_remove(nodo)

    def _interceptar_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "tree":
            return "break"

    def _on_tree_click(self, event):
        item = self.tree.identify_row(event.y)
        if not item:
            return
        if item in self.tree.selection():
            self.tree.selection_remove(item)
        else:
            self.tree.selection_add(item)