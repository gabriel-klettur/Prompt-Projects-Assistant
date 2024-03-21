import os
import tkinter as tk

from colorama import Fore

from app.utils.project_data import estructura_de_carpetas, generar_contenido_archivos
from app.utils.handle_prompt import crea_prompt
from app.ui.gui import seleccionar_carpeta, copiar_al_portapapeles, mostrar_arbol_directorios, seleccionar_archivo

def main():
    # Inicializar la instancia principal de Tkinter.
    root = tk.Tk()
    root.withdraw()  # Ocultamos la ventana principal.

    path_prompt_base_txt = seleccionar_archivo(root)
    if not path_prompt_base_txt:
        print("No se seleccionó el archivo de prompt base. Terminando el programa.")
        return

    carpeta = seleccionar_carpeta(root)
    if not carpeta:
        print("No se seleccionó la carpeta. Terminando el programa.")
        return
        
    estructura = estructura_de_carpetas(carpeta)    
    archivos_seleccionados = mostrar_arbol_directorios(root, carpeta)  # Ahora captura los archivos seleccionados aquí
    
    if archivos_seleccionados:
        contenido_archivos = generar_contenido_archivos(archivos_seleccionados)        
        prompt_gpt = crea_prompt(path_prompt_base_txt, estructura, contenido_archivos)
        print(Fore.RED + prompt_gpt + Fore.RESET)
        copiar_al_portapapeles(root, prompt_gpt)

if __name__ == "__main__":
    main()
