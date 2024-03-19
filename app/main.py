import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

from colorama import Fore

from app.utils.project_data import estructura_de_carpetas, generar_contenido_archivos
from app.utils.handle_prompt import crea_prompt

def main():
    # Inicializar la instancia principal de Tkinter.
    root = tk.Tk()
    root.withdraw()  # Ocultamos la ventana principal.

    directorio_script = os.path.dirname(os.path.abspath(__file__))
    path_prompt_base_txt = os.path.join(directorio_script, 'utils', 'prompt_structure.txt')

    carpeta = seleccionar_carpeta(root)
    if carpeta:
        estructura = estructura_de_carpetas(carpeta)
        
        archivos_seleccionados = mostrar_arbol_directorios(root, carpeta)  # Ahora captura los archivos seleccionados aquí
        
        if archivos_seleccionados:
            contenido_archivos = generar_contenido_archivos(archivos_seleccionados)
            
            if estructura:
                prompt_gpt = crea_prompt(path_prompt_base_txt, estructura, contenido_archivos)
                print(Fore.RED + prompt_gpt + Fore.RESET)
                copiar_al_portapapeles(root, prompt_gpt)

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
    archivos_seleccionados_temp = []  # Lista temporal para almacenar los archivos seleccionados
    
    tree = ttk.Treeview(ventana, selectmode='extended')
    tree.pack(expand=True, fill='both')
    
    nodos_rutas = {}

    def insertar_nodo(padre, texto, path):
        nodo = tree.insert(padre, 'end', text=texto, open=False)
        if os.path.isdir(path):
            tree.insert(nodo, 'end')
        nodos_rutas[nodo] = path
        return nodo

    def cargar_arbol(nodo):
        path = nodos_rutas.get(nodo)
        if path and os.path.isdir(path):
            for hijo in tree.get_children(nodo):
                tree.delete(hijo)
            for p in sorted(os.listdir(path)):
                abspath = os.path.join(path, p)
                if not p.startswith('.'):
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


if __name__ == "__main__":
    main()
