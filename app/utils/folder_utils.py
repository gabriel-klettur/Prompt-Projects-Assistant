from pathlib import Path

from config import FOLDERS_TO_IGNORE

def genera_estructura_de_carpetas(directorio, prefijo=''):
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
            resultado += genera_estructura_de_carpetas(entrada, nuevo_prefijo)
        elif entrada.is_file():
            resultado += f"{prefijo}- {entrada.name}\n"
    return resultado