from app.utils.directory_structure import seleccionar_carpeta, estructura_de_carpetas

import re
from colorama import Fore, Back, Style
import tkinter as tk
from tkinter import messagebox
import os


def main():
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    path_prompt_base_txt = os.path.join(directorio_script, 'utils', 'prompt_Python_Helper_GPT.txt')
    
    carpeta = seleccionar_carpeta()
    if carpeta:
        estructura = ""
        
        estructura = estructura_de_carpetas(carpeta)        
        
        if estructura:
            prompt_gpt = crea_prompt(path_prompt_base_txt, estructura)
            print(Fore.RED + prompt_gpt + Fore.RESET)
            copiar_al_portapapeles(prompt_gpt)            

    

def copiar_al_portapapeles(texto):
    root = tk.Tk()
    # Esconde la ventana principal
    root.withdraw()
    root.clipboard_clear()                      # Limpia el portapapeles
    root.clipboard_append(texto)                # Añade el texto al portapapeles
    root.update()                               # Mantiene el portapapeles después de cerrar la ventana
    messagebox.showinfo("Prompt Assistant", "Prompt copiado al portapapeles.")
    root.destroy()                              # Cierra la ventana después de mostrar el mensaje

def crea_prompt(ruta_archivo, estructura_de_carpetas):
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()
    
    contenido_modificado = re.sub(r"(''')", lambda m: f"{m.group(1)}\n{estructura_de_carpetas}\n", contenido, count=1)
    
    return contenido_modificado

if __name__ == "__main__":
    main()
