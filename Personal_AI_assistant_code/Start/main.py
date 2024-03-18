from directory_structure import seleccionar_carpeta, estructura_de_carpetas
import re
from colorama import Fore, Back, Style
import tkinter as tk
from tkinter import messagebox
from modelos_db import Archivo, Session
from operaciones_db import guardar_archivo
import os
from sqlalchemy import create_engine
import pandas as pd

def main():
    path_prompt_base_txt = 'prompt_Python_Helper_GPT.txt'
    
    carpeta = seleccionar_carpeta()
    if carpeta:
        estructura = ""
        
        estructura = estructura_de_carpetas(carpeta)        
        
        if estructura:
            prompt_gpt = crea_prompt(path_prompt_base_txt, estructura)
            print(Fore.RED + prompt_gpt + Fore.RESET)
            copiar_al_portapapeles(prompt_gpt)            
            #guardar_archivos_en_db(carpeta)
            #database_to_csv()

def database_to_csv():
    # Crear motor de conexión a la base de datos SQLite
    engine = create_engine('sqlite:///bd_project_python.db')

    # Leer datos de la tabla 'archivos'
    df = pd.read_sql_table('archivos', con=engine)

    # Guardar los datos en un archivo CSV
    df.to_csv('bd_project_python.csv', index=False)
    

def guardar_archivos_en_db(carpeta_raiz):
    carpetas_excluidas = {'env', 'venv', '.git', '.vscode', '__pycache__'}
    extensiones_excluidas = {'.png'}  # Conjunto de extensiones de archivo para excluir
    for raiz, dirs, archivos in os.walk(carpeta_raiz, topdown=True):
        dirs[:] = [d for d in dirs if d not in carpetas_excluidas]
        for nombre_archivo in archivos:
            if not any(nombre_archivo.endswith(ext) for ext in extensiones_excluidas):
                ruta_completa = os.path.join(raiz, nombre_archivo)
                with open(ruta_completa, 'rb') as archivo:  # Usar 'rb' para leer en modo binario
                    contenido_archivo = archivo.read()
                    # Aquí llamarías a guardar_archivo(nombre_archivo, contenido_archivo)
                    guardar_archivo(ruta_completa, contenido_archivo)

def copiar_al_portapapeles(texto):
    root = tk.Tk()
    # Esconde la ventana principal
    root.withdraw()
    root.clipboard_clear()  # Limpia el portapapeles
    root.clipboard_append(texto)  # Añade el texto al portapapeles
    root.update()  # Mantiene el portapapeles después de cerrar la ventana
    messagebox.showinfo("Información", "Texto copiado al portapapeles.")
    root.destroy()  # Cierra la ventana después de mostrar el mensaje

def crea_prompt(ruta_archivo, estructura_de_carpetas):
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()
    
    contenido_modificado = re.sub(r"(''')", lambda m: f"{m.group(1)}\n{estructura_de_carpetas}\n", contenido, count=1)
    
    return contenido_modificado

if __name__ == "__main__":
    main()
