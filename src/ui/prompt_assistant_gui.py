# ui/prompt_assistant_gui.py

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from pathlib import Path

class PromptAssistantGUI:
    def __init__(self, root, folders_to_ignore=None):
        self.root = root
        self.folders_to_ignore = folders_to_ignore if folders_to_ignore else []
        self.archivos_seleccionados = []

    def seleccionar_ruta(self, tipo="archivo"):
        """
        Permite al usuario seleccionar un archivo o carpeta.

        Args:
            tipo (str): "archivo" o "carpeta".

        Returns:
            str: Ruta seleccionada.
        """
        if tipo == "archivo":
            ruta_seleccionada = filedialog.askopenfilename(parent=self.root, title="Seleccionar archivo")
        elif tipo == "carpeta":
            ruta_seleccionada = filedialog.askdirectory(parent=self.root, title="Seleccionar carpeta")
        else:
            ruta_seleccionada = None
        return ruta_seleccionada

    def copiar_al_portapapeles(self, texto):
        """
        Copia el texto al portapapeles.

        Args:
            texto (str): Texto a copiar.
        """
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(texto)
            self.root.update()
            messagebox.showinfo("Prompt Assistant", "Prompt copiado al portapapeles.", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Error copiando al portapapeles: {str(e)}")

    def mostrar_arbol_directorios(self, carpeta):
        """
        Muestra una ventana con el árbol de directorios para seleccionar archivos.

        Args:
            carpeta (str): Ruta de la carpeta raíz.

        Returns:
            list: Lista de archivos seleccionados.
        """

        self.archivos_seleccionados = []

        ventana = tk.Toplevel(self.root)
        ventana.title("Seleccionar Archivos del Árbol de Directorios")
        ancho_ventana, alto_ventana = 800, 600
        ventana.geometry(f"{ancho_ventana}x{alto_ventana}")
        self._centro_ventana(ventana, ancho_ventana, alto_ventana)

        tree = ttk.Treeview(ventana, selectmode='extended')
        tree.pack(expand=True, fill='both')

        nodos_rutas = {}
        self._preparar_arbol(tree, carpeta, nodos_rutas)

        btn_confirmar = tk.Button(
            ventana,
            text="Confirmar Selección",
            command=lambda: self._on_confirmar(tree, nodos_rutas, ventana)
        )
        btn_confirmar.pack(pady=10)

        ventana.wait_window()
        return self.archivos_seleccionados

    # Métodos auxiliares
    def _centro_ventana(self, ventana, ancho_ventana, alto_ventana):
        posicion_x = (ventana.winfo_screenwidth() // 2) - (ancho_ventana // 2)
        posicion_y = (ventana.winfo_screenheight() // 2) - (alto_ventana // 2)
        ventana.geometry(f"+{posicion_x}+{posicion_y}")

    def _insertar_nodo(self, tree, padre, texto, path, nodos_rutas):
        path = Path(path)
        nodo = tree.insert(padre, 'end', text=texto, open=False)
        nodos_rutas[nodo] = str(path)
        if path.is_dir():
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
            for hijo in tree.get_children(nodo):
                tree.delete(hijo)
            with os.scandir(path) as it:
                elementos = sorted(it, key=lambda e: (not e.is_dir(), e.name))
                for elemento in elementos:
                    if elemento.name.startswith('.') or elemento.name in self.folders_to_ignore:
                        continue
                    abspath = os.path.join(path, elemento.name)
                    hijo = self._insertar_nodo(tree, nodo, elemento.name, abspath, nodos_rutas)
                    if elemento.is_dir():
                        self._cargar_arbol(tree, hijo, nodos_rutas)

    def _preparar_arbol(self, tree, carpeta, nodos_rutas):
        root_nodo = self._insertar_nodo(tree, '', carpeta, carpeta, nodos_rutas)
        self._cargar_arbol(tree, root_nodo, nodos_rutas)
        self._expandir_todo(tree, root_nodo, nodos_rutas)
        tree.bind('<<TreeviewOpen>>', lambda event: self._on_open(event, tree, nodos_rutas))

    def _on_open(self, event, tree, nodos_rutas):
        nodo = tree.focus()
        self._cargar_arbol(tree, nodo, nodos_rutas)

    def _on_confirmar(self, tree, nodos_rutas, ventana):
        seleccionados = tree.selection()
        for nodo in seleccionados:
            path = nodos_rutas[nodo]
            if os.path.isfile(path):
                self.archivos_seleccionados.append(path)
        ventana.destroy()
