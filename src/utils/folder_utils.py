import os

from src.config import FOLDERS_TO_IGNORE

def genera_estructura_de_carpetas(directorio):
    """
    Genera una representación de la estructura de directorios usando os.walk.

    Args:
        directorio (str): La ruta al directorio raíz.

    Returns:
        str: La representación de la estructura de directorios.
    """
    estructura = ''
    directorio = os.path.abspath(directorio)
    for root, dirs, files in os.walk(directorio):
        # Filtrar directorios y archivos que empiezan con '.' o están en FOLDERS_TO_IGNORE
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in FOLDERS_TO_IGNORE]
        files = [f for f in files if not f.startswith('.')]

        # Calcular el nivel de profundidad
        nivel = root.replace(directorio, '').count(os.sep)
        indent = '|  ' * nivel

        # Añadir el directorio actual
        if nivel == 0:
            estructura += f"+ {os.path.basename(root)}/\n"
        else:
            estructura += f"{indent}+ {os.path.basename(root)}/\n"

        # Añadir los archivos en el directorio actual
        subindent = '|  ' * (nivel + 1)
        for f in files:
            estructura += f"{subindent}- {f}\n"

    return estructura