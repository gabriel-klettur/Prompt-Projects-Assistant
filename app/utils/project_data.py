import os

from pathlib import Path

def estructura_de_carpetas(directorio, prefijo=''):
    directorio = Path(directorio)
    resultado = ''
    for entrada in directorio.iterdir():
        if entrada.is_dir() and not entrada.name.startswith(('.', 'env', 'venv', '__pycache__')):
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
            contenido_archivos += f"\n El archivo: {os.path.basename(archivo)}, Contiene:'''{contenido}'''\n"
    return contenido_archivos