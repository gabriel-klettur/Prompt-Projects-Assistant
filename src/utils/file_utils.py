import os

def extrae_contenido_archivos(archivos):
    """
    Extrae el contenido de los archivos especificados.

    Args:
        archivos (list): Una lista de rutas de archivos.

    Returns:
        str: El contenido de los archivos en un formato específico.
    """
    contenido_archivos = ""
    for archivo in archivos:
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
                contenido_archivos += f"------------------------------------------------------------------------------------------------------------------------------------"
                contenido_archivos += f"\n El archivo: {os.path.basename(archivo)}, Contiene:\n'''\n{contenido}\n'''\n"
                contenido_archivos += f"------------------------------------------------------------------------------------------------------------------------------------\n"
        except Exception as e:
            print(f"Error al leer el archivo {archivo}: {e}")
    return contenido_archivos