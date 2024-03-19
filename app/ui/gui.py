import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

import os

def seleccionar_carpeta(root):    
    carpeta_seleccionada = filedialog.askdirectory(parent=root)  # Usamos 'root' como parent.
    return carpeta_seleccionada

def copiar_al_portapapeles(root, texto):
    root.clipboard_clear()
    root.clipboard_append(texto)
    root.update()
    messagebox.showinfo("Prompt Assistant", "Prompt copiado al portapapeles.", parent=root)

def mostrar_arbol_directorios(root, carpeta):
    ventana = tk.Toplevel(root)
    ventana.title("Seleccionar Archivos del Árbol de Directorios")
    
    # Ajustar el tamaño de la ventana (p. ej., 800x600).
    ancho_ventana = 800
    alto_ventana = 600
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}")

    # Calcular la posición x y y para centrar la ventana.
    posicion_x = (ventana.winfo_screenwidth() // 2) - (ancho_ventana // 2)
    posicion_y = (ventana.winfo_screenheight() // 2) - (alto_ventana // 2)
    
    # Actualizar la geometría de la ventana para que aparezca centrada.
    ventana.geometry(f"+{posicion_x}+{posicion_y}")
    
    archivos_seleccionados_temp = []  # Lista temporal para almacenar los archivos seleccionados
    
    tree = ttk.Treeview(ventana, selectmode='extended')
    tree.pack(expand=True, fill='both')
    
    nodos_rutas = {}

    def insertar_nodo(padre, texto, path):
        # Omitir la inserción si el directorio es __pycache__
        if os.path.isdir(path) and texto == "__pycache__":
            return None  # No se crea un nodo para __pycache__
        nodo = tree.insert(padre, 'end', text=texto, open=False)
        if os.path.isdir(path):
            tree.insert(nodo, 'end')  # Insertar un nodo ficticio para forzar la expansión
        nodos_rutas[nodo] = path
        return nodo

    def cargar_arbol(nodo):
        path = nodos_rutas.get(nodo)
        if path and os.path.isdir(path):
            for hijo in tree.get_children(nodo):
                tree.delete(hijo)
            for p in sorted(os.listdir(path)):
                abspath = os.path.join(path, p)
                if not p.startswith('.') and p != "__pycache__":  # Omitir directorios que no deseamos mostrar
                    insertar_nodo(nodo, p, abspath)

    root_nodo = insertar_nodo('', carpeta, carpeta)
    cargar_arbol(root_nodo)

    def on_open(event):
        nodo = tree.focus()
        cargar_arbol(nodo)

    tree.bind('<<TreeviewOpen>>', on_open)

    def confirmar_seleccion():
        seleccionados = tree.selection()
        for nodo in seleccionados:
            if os.path.isfile(nodos_rutas[nodo]):
                archivos_seleccionados_temp.append(nodos_rutas[nodo])

    def on_confirmar():
        confirmar_seleccion()  # Captura los archivos seleccionados
        ventana.destroy()

    btn_confirmar = tk.Button(ventana, text="Confirmar Selección", command=on_confirmar)
    btn_confirmar.pack(pady=10)

    ventana.wait_window()  # Espera que la ventana se cierre antes de continuar

    return archivos_seleccionados_temp  # Retorna la lista de archivos seleccionados