import os

from pathlib import Path

from pathlib import Path

from config import FOLDERS_TO_IGNORE

def estructura_de_carpetas(directorio, prefijo=''):
    """
    Recursively generates a directory structure representation.

    Args:
        directorio (str): The path to the directory.
        prefijo (str, optional): The prefix to be added to each line. Defaults to ''.

    Returns:
        str: The directory structure representation.
    """
    directorio = Path(directorio)
    resultado = ''
    for entrada in directorio.iterdir():
        if entrada.is_dir() and not any(entrada.name.startswith(prefix) or entrada.name in FOLDERS_TO_IGNORE for prefix in ['.']):
            resultado += f"{prefijo}+ {entrada.name}\n"
            nuevo_prefijo = prefijo + "|  "
            resultado += estructura_de_carpetas(entrada, nuevo_prefijo)
        elif entrada.is_file():
            resultado += f"{prefijo}- {entrada.name}\n"
    return resultado


def generar_contenido_archivos(archivos):
    """
    Genera el contenido de los archivos especificados.

    Args:
        archivos (list): Una lista de rutas de archivos.

    Returns:
        str: El contenido de los archivos en un formato específico.
    """
    contenido_archivos = ""
    for archivo in archivos:
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
            contenido_archivos += f"------------------------------------------------------------------------------------------------------------------------------------"
            contenido_archivos += f"\n El archivo: {os.path.basename(archivo)}, Contiene:\n'''\n{contenido}\n'''\n"
            contenido_archivos += f"------------------------------------------------------------------------------------------------------------------------------------\n"
    return contenido_archivos