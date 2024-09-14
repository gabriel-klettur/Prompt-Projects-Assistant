# main.py

import tkinter as tk
from colorama import Fore
from src.config import FOLDERS_TO_IGNORE

from src.utils import FileManager
from src.utils import PromptGenerator
from src.ui import PromptAssistantGUI


def main():
    root = tk.Tk()
    root.withdraw()

    gui = PromptAssistantGUI(root, FOLDERS_TO_IGNORE)
    file_manager = FileManager(FOLDERS_TO_IGNORE)

    # Seleccionar el archivo de prompt base
    path_prompt_base_txt = gui.seleccionar_ruta(tipo="archivo")
    if not path_prompt_base_txt:
        print("No se seleccionó el archivo de prompt base. Terminando el programa.")
        return

    # Seleccionar la carpeta
    carpeta = gui.seleccionar_ruta(tipo="carpeta")
    if not carpeta:
        print("No se seleccionó la carpeta. Terminando el programa.")
        return

    # Crear instancia de PromptGenerator
    prompt_generator = PromptGenerator(path_prompt_base_txt)

    # Generar la estructura de carpetas
    estructura = file_manager.genera_estructura_de_carpetas(carpeta)
    prompt_generator.set_estructura_de_carpetas(estructura)

    # Mostrar árbol de directorios y obtener archivos seleccionados
    archivos_seleccionados = gui.mostrar_arbol_directorios(carpeta)

    # Extraer contenido de los archivos seleccionados
    contenido_archivos = file_manager.extrae_contenido_archivos(archivos_seleccionados)
    prompt_generator.set_contenido_archivos(contenido_archivos)

    # Crear el prompt final
    prompt_final = prompt_generator.crear_prompt()

    # Mostrar y copiar el prompt
    print(Fore.RED + prompt_final + Fore.RESET)
    gui.copiar_al_portapapeles(prompt_final)

if __name__ == "__main__":
    main()
