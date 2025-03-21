# utils/prompt_generator.py

import re

class PromptGenerator:
    
    # Constructor
    def __init__(self, prompt_base_path):
        self.prompt_base_path = prompt_base_path
        self.prompt_base_content = ''
        self.estructura_de_carpetas = ''
        self.contenido_archivos = ''
        self.prompt_final = ''

        self._cargar_prompt_base()
    
    def _cargar_prompt_base(self):
        """Carga el contenido del prompt base desde el archivo especificado."""
        with open(self.prompt_base_path, 'r', encoding='utf-8') as f:
            self.prompt_base_content = f.read()

    def set_estructura_de_carpetas(self, estructura):
        """Establece la estructura de carpetas para el prompt."""
        self.estructura_de_carpetas = estructura

    def set_contenido_archivos(self, contenido):
        """Establece el contenido de los archivos seleccionados para el prompt."""
        self.contenido_archivos = contenido

    def crear_prompt(self):
        """Genera el prompt final combinando todos los elementos."""
        # Insertar la estructura de carpetas en el lugar apropiado
        contenido_modificado = re.sub(
            r"(''')",
            lambda m: f"{m.group(1)}\n{self.estructura_de_carpetas}\n",
            self.prompt_base_content,
            count=1
        )
        # Añadir el contenido de los archivos al final
        self.prompt_final = contenido_modificado + self.contenido_archivos
        return self.prompt_final
