import os

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from colorama import Fore, Back, Style

from app.utils.project_data import estructura_de_carpetas
from app.utils.handle_prompt import crea_prompt



def main():
    """
    This is the main function of the PromptCodeAssistant application.
    It performs the following steps:
    1. Retrieves the directory path of the script.
    2. Constructs the path to the 'prompt_structure.txt' file.
    3. Prompts the user to select a folder.
    4. If a folder is selected, generates the folder structure.
    5. If the folder structure is generated successfully, creates a prompt using the 'prompt_structure.txt' file and the generated structure.
    6. Prints the generated prompt in red color.
    7. Copies the generated prompt to the clipboard.
    """
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    path_prompt_base_txt = os.path.join(directorio_script, 'utils', 'prompt_structure.txt')
    
    carpeta = seleccionar_carpeta()
    if carpeta:
        estructura = ""        
        estructura = estructura_de_carpetas(carpeta)        
        
        if estructura:
            prompt_gpt = crea_prompt(path_prompt_base_txt, estructura)
            print(Fore.RED + prompt_gpt + Fore.RESET)
            copiar_al_portapapeles(prompt_gpt)            


def seleccionar_carpeta():
    """
    Opens a dialog to select a folder and returns the selected folder path.

    Returns:
        str: The path of the selected folder.
    """
    root = tk.Tk()
    root.withdraw()  # Ocultamos la ventana principal de Tkinter
    carpeta_seleccionada = filedialog.askdirectory()  # Abrimos el diálogo para seleccionar carpeta
    return carpeta_seleccionada

def copiar_al_portapapeles(texto):
    """
    Copia el texto proporcionado al portapapeles del sistema.

    Args:
        texto (str): El texto que se va a copiar al portapapeles.

    Returns:
        None
    """
    root = tk.Tk()
    root.withdraw()
    root.clipboard_clear()                      # Limpia el portapapeles
    root.clipboard_append(texto)                # Añade el texto al portapapeles
    root.update()                               # Mantiene el portapapeles después de cerrar la ventana
    messagebox.showinfo("Prompt Assistant", "Prompt copiado al portapapeles.")
    root.destroy()                              # Cierra la ventana después de mostrar el mensaje

if __name__ == "__main__":
    main()
