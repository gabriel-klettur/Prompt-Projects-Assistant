import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

import os

def seleccionar_archivo(root):
    """
    Permite al usuario seleccionar un archivo mediante un cuadro de diálogo.

    Args:
        root: La raíz de la ventana de Tkinter.

    Returns:
        La ruta del archivo seleccionado o None si no se selecciona ningún archivo.
    """
    archivo_seleccionado = filedialog.askopenfilename(parent=root, title="Seleccionar archivo de prompt base")
    return archivo_seleccionado

def seleccionar_carpeta(root):
    """
    Opens a dialog box to select a folder/directory.

    Parameters:
        root (Tk): The root window object.

    Returns:
        str: The path of the selected folder/directory.
    """
    carpeta_seleccionada = filedialog.askdirectory(parent=root)  # Usamos 'root' como parent.
    return carpeta_seleccionada

def copiar_al_portapapeles(root, texto):
    """
    Copies the given text to the clipboard.

    Args:
        root (Tk): The root Tkinter window.
        texto (str): The text to be copied to the clipboard.
    """
    root.clipboard_clear()
    root.clipboard_append(texto)
    root.update()
    messagebox.showinfo("Prompt Assistant", "Prompt copiado al portapapeles.", parent=root)

#!--------------------------------------------------------------------------------------------------------------------
#!------------------------------------------- Ventana Arbol de Directorios -------------------------------------------
#!--------------------------------------------------------------------------------------------------------------------

def crear_ventana_arbol_directorios(root):
    ventana = tk.Toplevel(root)
    ventana.title("Seleccionar Archivos del Árbol de Directorios")
    ancho_ventana, alto_ventana = 800, 600
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}")
    centro_ventana(ventana, ancho_ventana, alto_ventana)
    return ventana

def centro_ventana(ventana, ancho_ventana, alto_ventana):
    posicion_x = (ventana.winfo_screenwidth() // 2) - (ancho_ventana // 2)
    posicion_y = (ventana.winfo_screenheight() // 2) - (alto_ventana // 2)
    ventana.geometry(f"+{posicion_x}+{posicion_y}")

def insertar_nodo(tree, padre, texto, path, nodos_rutas):
    if os.path.isdir(path) and texto in ["__pycache__", "venv"]:
        return None
    nodo = tree.insert(padre, 'end', text=texto, open=False)
    if os.path.isdir(path):
        tree.insert(nodo, 'end')
    nodos_rutas[nodo] = path
    return nodo

def cargar_arbol(tree, nodo, nodos_rutas):
    path = nodos_rutas.get(nodo)
    if path and os.path.isdir(path):
        for hijo in tree.get_children(nodo):
            tree.delete(hijo)
        for p in sorted(os.listdir(path)):
            if not p.startswith('.') and p not in ["__pycache__", "venv"]:
                abspath = os.path.join(path, p)
                insertar_nodo(tree, nodo, p, abspath, nodos_rutas)

def preparar_arbol(tree, carpeta, nodos_rutas):
    root_nodo = insertar_nodo(tree, '', carpeta, carpeta, nodos_rutas)
    cargar_arbol(tree, root_nodo, nodos_rutas)
    tree.bind('<<TreeviewOpen>>', lambda event: on_open(event, tree, nodos_rutas))

def on_open(event, tree, nodos_rutas):
    nodo = tree.focus()
    cargar_arbol(tree, nodo, nodos_rutas)

def mostrar_arbol_directorios(root, carpeta):
    ventana = crear_ventana_arbol_directorios(root)
    archivos_seleccionados_temp = []
    nodos_rutas = {}

    tree = ttk.Treeview(ventana, selectmode='extended')
    tree.pack(expand=True, fill='both')
    preparar_arbol(tree, carpeta, nodos_rutas)

    btn_confirmar = tk.Button(ventana, text="Confirmar Selección", command=lambda: on_confirmar(tree, nodos_rutas, archivos_seleccionados_temp, ventana))
    btn_confirmar.pack(pady=10)

    ventana.wait_window()
    return archivos_seleccionados_temp

def on_confirmar(tree, nodos_rutas, archivos_seleccionados_temp, ventana):
    seleccionados = tree.selection()
    for nodo in seleccionados:
        if os.path.isfile(nodos_rutas[nodo]):
            archivos_seleccionados_temp.append(nodos_rutas[nodo])
    ventana.destroy()