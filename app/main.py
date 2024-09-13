import os
import tkinter as tk

from colorama import Fore

from app.utils import genera_estructura_de_carpetas, extrae_contenido_archivos
from app.utils import crea_prompt
from app.ui import seleccionar_ruta, copiar_al_portapapeles, mostrar_arbol_directorios

def main():
    """
    Main function of the PromptCodeAssistant application.
    This function initializes the Tkinter instance, prompts the user to select a base prompt file and a folder,
    displays the directory tree of the selected folder, generates the content of selected files,
    creates a GPT prompt based on the selected files and folder structure, and copies the prompt to the clipboard.
    """
    # Inicializar la instancia principal de Tkinter.
    root = tk.Tk()
    root.withdraw()  # Ocultamos la ventana principal.

    path_prompt_base_txt = seleccionar_ruta(root, tipo="archivo")
    if not path_prompt_base_txt:
        print("No se seleccionó el archivo de prompt base. Terminando el programa.")
        return

    carpeta = seleccionar_ruta(root, tipo="carpeta")
    if not carpeta:
        print("No se seleccionó la carpeta. Terminando el programa.")
        return
        
    estructura = genera_estructura_de_carpetas(carpeta)    
    archivos_seleccionados = mostrar_arbol_directorios(root, carpeta)  # Ahora captura los archivos seleccionados aquí
    
    if archivos_seleccionados:
        contenido_archivos = extrae_contenido_archivos(archivos_seleccionados)        
        prompt_gpt = crea_prompt(path_prompt_base_txt, estructura, contenido_archivos)
        print(Fore.RED + prompt_gpt + Fore.RESET)
        copiar_al_portapapeles(root, prompt_gpt)

if __name__ == "__main__":
    main()
