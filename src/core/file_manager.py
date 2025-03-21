# utils/file_manager.py

import os

class FileManager:
    def __init__(self, folders_to_ignore=None):
        if folders_to_ignore is None:
            folders_to_ignore = []
        self.folders_to_ignore = folders_to_ignore

    def genera_estructura_de_carpetas(self, directorio):
        """
        Genera una representación de la estructura de directorios.

        Args:
            directorio (str): La ruta al directorio raíz.

        Returns:
            str: La representación de la estructura de directorios.
        """
        estructura = ''
        directorio = os.path.abspath(directorio)
        for root, dirs, files in os.walk(directorio):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in self.folders_to_ignore]
            files = [f for f in files if not f.startswith('.')]

            nivel = root.replace(directorio, '').count(os.sep)
            indent = '|  ' * nivel

            if nivel == 0:
                estructura += f"+ {os.path.basename(root)}/\n"
            else:
                estructura += f"{indent}+ {os.path.basename(root)}/\n"

            subindent = '|  ' * (nivel + 1)
            for f in files:
                estructura += f"{subindent}- {f}\n"

        return estructura

    def extrae_contenido_archivos(self, archivos):
        """
        Extrae y formatea el contenido de los archivos seleccionados.

        Args:
            archivos (list): Lista de rutas de archivos.

        Returns:
            str: El contenido formateado de los archivos.
        """
        contenido_archivos = ""
        for archivo in archivos:
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                    contenido_archivos += "------------------------------------------------------------------------------------------------------------------------------------\n"
                    contenido_archivos += f" El archivo: {os.path.basename(archivo)}, Contiene:\n'''\n{contenido}\n'''\n"
                    contenido_archivos += "------------------------------------------------------------------------------------------------------------------------------------\n"
            except Exception as e:
                print(f"Error al leer el archivo {archivo}: {e}")
        return contenido_archivos
