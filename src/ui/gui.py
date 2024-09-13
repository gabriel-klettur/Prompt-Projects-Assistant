import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

from pathlib import Path

import os

from src.config import FOLDERS_TO_IGNORE

def seleccionar_ruta(root, tipo="archivo"):
    """
    Permite al usuario seleccionar un archivo o carpeta mediante un cuadro de diálogo.

    Args:
        root: La raíz de la ventana de Tkinter.
        tipo: Tipo de selección ("archivo" o "carpeta").

    Returns:
        La ruta seleccionada o None si no se selecciona nada.
    """
    if tipo == "archivo":
        ruta_seleccionada = filedialog.askopenfilename(parent=root, title="Seleccionar archivo")
    elif tipo == "carpeta":
        ruta_seleccionada = filedialog.askdirectory(parent=root, title="Seleccionar carpeta")
    
    return ruta_seleccionada

def copiar_al_portapapeles(root, texto):
    """
    Copia el texto dado al portapapeles y maneja errores de forma segura.

    Args:
        root (Tk): La ventana raíz de Tkinter.
        texto (str): El texto a copiar al portapapeles.
    """
    try:
        root.clipboard_clear()
        root.clipboard_append(texto)
        root.update()
        messagebox.showinfo("Prompt Assistant", "Prompt copiado al portapapeles.", parent=root)
    except Exception as e:
        messagebox.showerror("Error", f"Error copiando al portapapeles: {str(e)}")


#!--------------------------------------------------------------------------------------------------------------------
#!------------------------------------------- Ventana Arbol de Directorios -------------------------------------------
#!--------------------------------------------------------------------------------------------------------------------

def crear_ventana_arbol_directorios(root):
    """
    Crea y devuelve una nueva ventana para seleccionar archivos del árbol de directorios.

    Args:
        root: La ventana raíz a la que se asociará la nueva ventana.

    Returns:
        La nueva ventana creada.

    """
    ventana = tk.Toplevel(root)
    ventana.title("Seleccionar Archivos del Árbol de Directorios")
    ancho_ventana, alto_ventana = 800, 600
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}")
    centro_ventana(ventana, ancho_ventana, alto_ventana)
    return ventana

def centro_ventana(ventana, ancho_ventana, alto_ventana):
    """
    Centers a window on the screen.

    Args:
        ventana: The window to be centered.
        ancho_ventana: The width of the window.
        alto_ventana: The height of the window.
    """
    posicion_x = (ventana.winfo_screenwidth() // 2) - (ancho_ventana // 2)
    posicion_y = (ventana.winfo_screenheight() // 2) - (alto_ventana // 2)
    ventana.geometry(f"+{posicion_x}+{posicion_y}")

def insertar_nodo(tree, padre, texto, path, nodos_rutas):
    path = Path(path)  # Convierte la ruta a un objeto Path
    nodo = tree.insert(padre, 'end', text=texto, open=False)
    nodos_rutas[nodo] = str(path)  # Almacena la ruta como cadena para mantener la consistencia
    if path.is_dir():
        tree.insert(nodo, 'end')  # El resto del código permanece igual
    return nodo

def expandir_todo(tree, nodo, nodos_rutas):
    """
    Expande recursivamente todos los nodos hijos del nodo dado.

    Args:
        tree (ttk.Treeview): El widget de Treeview.
        nodo (str): El identificador del nodo padre.
        nodos_rutas (dict): Un diccionario que mapea identificadores de nodos a sus rutas de archivos/directorios.
    """
    tree.item(nodo, open=True)  # Expande el nodo actual.
    path = nodos_rutas.get(nodo)
    if path and os.path.isdir(path):
        for hijo in tree.get_children(nodo):
            expandir_todo(tree, hijo, nodos_rutas)  # Llamada recursiva para expandir los nodos hijos.

def cargar_arbol(tree, nodo, nodos_rutas):
    """
    Carga el contenido de un directorio en un árbol de tkinter usando os.scandir para mayor eficiencia.

    Args:
        tree (tkinter.ttk.Treeview): El árbol de tkinter en el que se cargará el contenido.
        nodo (str): El nodo del árbol en el que se cargará el contenido.
        nodos_rutas (dict): Un diccionario que mapea nodos del árbol a rutas de directorio.

    Returns:
        None
    """
    path = nodos_rutas.get(nodo, '')
    if path and os.path.isdir(path):
        for hijo in tree.get_children(nodo):
            tree.delete(hijo)
        
        with os.scandir(path) as it:
            elementos = sorted(it, key=lambda e: (not e.is_dir(), e.name))
            for elemento in elementos:
                if elemento.name.startswith('.') or elemento.name in FOLDERS_TO_IGNORE:
                    continue
                abspath = os.path.join(path, elemento.name)
                hijo = insertar_nodo(tree, nodo, elemento.name, abspath, nodos_rutas)
                if elemento.is_dir():
                    cargar_arbol(tree, hijo, nodos_rutas)  # Carga recursiva de contenido.


def preparar_arbol(tree, carpeta, nodos_rutas):
    """
    Prepara el árbol de visualización con los nodos y rutas proporcionados.

    Args:
        tree (tkinter.ttk.Treeview): El objeto Treeview en el que se mostrará el árbol.
        carpeta (str): El nombre de la carpeta raíz del árbol.
        nodos_rutas (dict): Un diccionario que contiene los nodos y rutas del árbol.

    Returns:
        None
    """
    root_nodo = insertar_nodo(tree, '', carpeta, carpeta, nodos_rutas)
    cargar_arbol(tree, root_nodo, nodos_rutas)
    expandir_todo(tree, root_nodo, nodos_rutas)
    tree.bind('<<TreeviewOpen>>', lambda event: on_open(event, tree, nodos_rutas))

def on_open(event, tree, nodos_rutas):
    """
    Event handler for the 'open' event.

    Args:
        event: The event object triggered by the 'open' event.
        tree: The tree widget object.
        nodos_rutas: The list of nodes and paths.

    Returns:
        None
    """
    nodo = tree.focus()
    cargar_arbol(tree, nodo, nodos_rutas)

def mostrar_arbol_directorios(root, carpeta):
    """
    Displays a directory tree in a GUI window and allows the user to select files.

    Args:
        root: The root Tkinter object.
        carpeta: The path of the folder to display in the tree.

    Returns:
        A list of selected files.
    """
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
    """
    Add selected files to the list of selected files and close the window.

    Parameters:
    - tree: The tree widget containing the selected files.
    - nodos_rutas: A dictionary mapping tree nodes to file paths.
    - archivos_seleccionados_temp: A list to store the selected file paths.
    - ventana: The window to be closed.

    Returns:
    None
    """
    seleccionados = tree.selection()
    for nodo in seleccionados:
        if os.path.isfile(nodos_rutas[nodo]):
            archivos_seleccionados_temp.append(nodos_rutas[nodo])
    ventana.destroy()