import os

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from colorama import Fore, Back, Style

from app.utils.project_data import estructura_de_carpetas
from app.utils.handle_prompt import crea_prompt

def main():
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
    root = tk.Tk()
    root.withdraw()  # Ocultamos la ventana principal de Tkinter
    carpeta_seleccionada = filedialog.askdirectory()  # Abrimos el diálogo para seleccionar carpeta
    return carpeta_seleccionada    

def copiar_al_portapapeles(texto):
    root = tk.Tk()
    root.withdraw()
    root.clipboard_clear()                      # Limpia el portapapeles
    root.clipboard_append(texto)                # Añade el texto al portapapeles
    root.update()                               # Mantiene el portapapeles después de cerrar la ventana
    messagebox.showinfo("Prompt Assistant", "Prompt copiado al portapapeles.")
    root.destroy()                              # Cierra la ventana después de mostrar el mensaje

if __name__ == "__main__":
    main()
