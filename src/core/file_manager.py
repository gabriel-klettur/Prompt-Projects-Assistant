# src/core/file_manager.py

import os
from src.utils import i18n

class FileManager:
    def __init__(self, folders_to_ignore=None):
        if folders_to_ignore is None:
            folders_to_ignore = []
        self.folders_to_ignore = folders_to_ignore

    def genera_estructura_de_carpetas(self, directorio):
        estructura = ''
        directorio = os.path.abspath(directorio)
        for root, dirs, files in os.walk(directorio):
            dirs[:] = [
                d for d in dirs
                if not d.startswith('.') and
                d not in self.folders_to_ignore and
                not any(d.endswith(ext) for ext in self.folders_to_ignore)
            ]
            files = [
                f for f in files
                if not f.startswith('.') and
                not any(f.endswith(ext) for ext in self.folders_to_ignore)
            ]

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
        contenido_archivos = ""
        for archivo in archivos:
            try:
                if any(archivo.endswith(ext) for ext in self.folders_to_ignore):
                    continue
                with open(archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                    contenido_archivos += "------------------------------------------------------------------------------------------------------------------------------------\n"
                    contenido_archivos += f" {i18n.t('file_label')}: {os.path.basename(archivo)}, {i18n.t('contains_label')}:\n'''\n{contenido}\n'''\n"
                    contenido_archivos += "------------------------------------------------------------------------------------------------------------------------------------\n"
            except Exception as e:
                print(f"Error al leer el archivo {archivo}: {e}")
        return contenido_archivos
