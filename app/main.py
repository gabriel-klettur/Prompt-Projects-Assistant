import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

from colorama import Fore

from app.utils.project_data import estructura_de_carpetas
from app.utils.handle_prompt import crea_prompt

# Variable global para almacenar los archivos seleccionados.
archivos_seleccionados = []

def main():
    # Inicializar la instancia principal de Tkinter.
    root = tk.Tk()
    root.withdraw()  # Ocultamos la ventana principal.

    directorio_script = os.path.dirname(os.path.abspath(__file__))
    path_prompt_base_txt = os.path.join(directorio_script, 'utils', 'prompt_structure.txt')

    carpeta = seleccionar_carpeta(root)
    if carpeta:
        estructura = estructura_de_carpetas(carpeta)
        mostrar_arbol_directorios(root, carpeta)

        # Procesar los archivos seleccionados después de que la ventana se cierra.
        if archivos_seleccionados:
            contenido_archivos = generar_contenido_archivos(archivos_seleccionados)

            if estructura:
                prompt_gpt = crea_prompt(path_prompt_base_txt, estructura, contenido_archivos)
                print(Fore.RED + prompt_gpt + Fore.RESET)
                copiar_al_portapapeles(root, prompt_gpt)

def seleccionar_carpeta(root):
    """Abre un diálogo para seleccionar una carpeta."""
    carpeta_seleccionada = filedialog.askdirectory(parent=root)  # Usamos 'root' como parent.
    return carpeta_seleccionada

def copiar_al_portapapeles(root, texto):
    """Copia el texto al portapapeles y muestra un mensaje."""
    root.clipboard_clear()
    root.clipboard_append(texto)
    root.update()
    messagebox.showinfo("Prompt Assistant", "Prompt copiado al portapapeles.", parent=root)

def mostrar_arbol_directorios(root, carpeta):
    ventana = tk.Toplevel(root)  # Usamos Toplevel para crear una nueva ventana.
    ventana.title("Seleccionar Archivos del Árbol de Directorios")
    
    tree = ttk.Treeview(ventana, selectmode='extended')
    tree.pack(expand=True, fill='both')
    
    nodos_rutas = {}  # Diccionario para mapear nodos a sus rutas

    def insertar_nodo(padre, texto, path):
            """Inserta un nodo en el árbol, asociándolo con su ruta."""
            nodo = tree.insert(padre, 'end', text=texto, open=False)
            if os.path.isdir(path):
                # Se inserta un placeholder para que el directorio pueda expandirse
                tree.insert(nodo, 'end')
            nodos_rutas[nodo] = path  # Asociamos el nodo con su ruta
            return nodo

    def cargar_arbol(nodo):
        """Carga los contenidos de un directorio en el árbol bajo el nodo dado."""
        path = nodos_rutas.get(nodo)  # Obtenemos la ruta del nodo
        if path and os.path.isdir(path):
            # Primero, limpia los nodos hijos existentes (incluido el placeholder)
            for hijo in tree.get_children(nodo):
                tree.delete(hijo)
            # Luego, carga los contenidos del directorio
            for p in sorted(os.listdir(path)):
                abspath = os.path.join(path, p)
                if not p.startswith('.'):  # Ignorar archivos/directorios ocultos
                    insertar_nodo(nodo, p, abspath)

    # Insertamos el nodo raíz y su ruta en el diccionario nodos_rutas
    root_nodo = insertar_nodo('', carpeta, carpeta)
    
    # Carga inicial del contenido del directorio raíz
    cargar_arbol(root_nodo)

    def on_open(event):
        """Manejador del evento de apertura de un nodo, para cargar su contenido."""
        nodo = tree.focus()  # Obtiene el nodo actualmente enfocado
        cargar_arbol(nodo)

    tree.bind('<<TreeviewOpen>>', on_open)

    btn_confirmar = tk.Button(ventana, text="Confirmar Selección", command=lambda: confirmar_seleccion(tree, nodos_rutas, ventana))
    btn_confirmar.pack(pady=10)

    ventana.wait_window()  # Espera a que la ventana 'ventana' se cierre.

def confirmar_seleccion(tree, nodos_rutas, ventana):
    global archivos_seleccionados
    seleccionados = tree.selection()
    archivos_seleccionados = [nodos_rutas[nodo] for nodo in seleccionados if os.path.isfile(nodos_rutas[nodo])]
    ventana.destroy()

def generar_contenido_archivos(archivos):
    """Genera el contenido de los archivos seleccionados para el prompt."""
    contenido_archivos = ""
    for archivo in archivos:
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
            contenido_archivos += f"\n El archivo: {os.path.basename(archivo)}, Contiene:'''{contenido}'''\n"
    return contenido_archivos

if __name__ == "__main__":
    main()