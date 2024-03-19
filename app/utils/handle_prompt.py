import re

def crea_prompt(ruta_archivo, estructura_de_carpetas):
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()
    
    contenido_modificado = re.sub(r"(''')", lambda m: f"{m.group(1)}\n{estructura_de_carpetas}\n", contenido, count=1)
    
    return contenido_modificado
