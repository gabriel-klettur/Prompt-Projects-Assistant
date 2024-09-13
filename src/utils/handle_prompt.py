import re

def crea_prompt(ruta_archivo, estructura_de_carpetas, contenido_archivos):
    """
    Modifies the content of a file by adding the folder structure at the specified location.

    Args:
        ruta_archivo (str): The path of the file to be modified.
        estructura_de_carpetas (str): The folder structure to be added.

    Returns:
        str: The modified content of the file with the folder structure added.
    """
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()
    
    contenido_modificado = re.sub(r"(''')", lambda m: f"{m.group(1)}\n{estructura_de_carpetas}\n", contenido, count=1)
    
    contenido_modificado = contenido_modificado + contenido_archivos
    
    return contenido_modificado
