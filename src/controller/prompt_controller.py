# Path: src/controller/prompt_controller.py
from tkinter import messagebox
from src.core import FileManager
from src.config import FOLDERS_TO_IGNORE
from src.utils import i18n
import re
import json
from pathlib import Path

class PromptController:
    def __init__(self, gui_helper, view):
        self.view = view
        self.gui_helper = gui_helper
        self.file_manager = FileManager(FOLDERS_TO_IGNORE)

        self.prompt_base_path = None
        self.project_folder = None
        self.selected_files = []
        self.estructura = ''
        self.contenido_archivos = ''
        self.prompt_final = ''
        self.saved_ignore_structure = []
        self.saved_ignore_files = []
        self.saved_only_extensions = []
        try:
            settings_file = Path("settings.json")
            if settings_file.exists():
                data = settings_file.read_text(encoding="utf-8")
                obj = json.loads(data)
                self.saved_ignore_structure = obj.get("ignore_structure", [])
                self.saved_ignore_files = obj.get("ignore_files", [])
                self.saved_only_extensions = obj.get("only_extensions", [])
        except Exception as e:
            print(f"Error loading settings: {e}")

    def obtener_ignorados_estructura(self):
        texto = self.view.left_panel.entry_ignore_structure.get("1.0", "end").strip()
        return [item.strip() for item in texto.split(",") if item.strip()]

    def obtener_ignorados_archivos(self):
        texto = self.view.left_panel.entry_ignore_files.get("1.0", "end").strip()
        return [item.strip() for item in texto.split(",") if item.strip()]

    def obtener_solo_extensiones(self):
        texto = self.view.left_panel.entry_only_ext.get("1.0", "end").strip()
        return [ext.strip() for ext in texto.split(",") if ext.strip()]

    def seleccionar_prompt_base(self):
        path = self.gui_helper.seleccionar_ruta(tipo="archivo")
        if path:
            self.prompt_base_path = path
            self.view.left_panel.set_prompt_base_estado(True)
            with open(path, 'r', encoding='utf-8') as f:
                contenido = f.read()
            self.view.center_panel.mostrar_prompt_base(contenido)
            self.actualizar_prompt_final()
        else:
            messagebox.showwarning(i18n.t("warning_title"), i18n.t("no_file_selected"))

    def seleccionar_proyecto(self):
        path = self.gui_helper.seleccionar_ruta(tipo="carpeta")
        if path:
            self.project_folder = path
            self.file_manager = FileManager(self.obtener_ignorados_estructura(), self.obtener_solo_extensiones())
            self.estructura = self.file_manager.genera_estructura_de_carpetas(path)
            self.view.left_panel.set_project_estado(True)
            self.view.center_panel.mostrar_estructura(self.estructura)
            self.actualizar_prompt_final()
        else:
            messagebox.showwarning(i18n.t("warning_title"), i18n.t("no_folder_selected"))

    def seleccionar_archivos(self):
        if not self.project_folder:
            messagebox.showerror(i18n.t("error_title"), i18n.t("project_folder_required"))
            return

        self.gui_helper.folders_to_ignore = self.obtener_ignorados_archivos()
        self.gui_helper.only_extensions = self.obtener_solo_extensiones()

        self.selected_files = self.gui_helper.mostrar_arbol_directorios(self.project_folder)
        if self.selected_files:
            self.view.left_panel.set_archivos_estado(True, len(self.selected_files))
            self.view.left_panel.mostrar_lista_archivos(self.selected_files)

            self.file_manager = FileManager(self.obtener_ignorados_archivos(), self.obtener_solo_extensiones())
            self.contenido_archivos = self.file_manager.extrae_contenido_archivos(self.selected_files)
            self.view.center_panel.mostrar_contenido_archivos(self.contenido_archivos)
            self.actualizar_prompt_final()
        else:
            messagebox.showwarning(i18n.t("warning_title"), i18n.t("no_files_selected"))
            self.view.left_panel.set_archivos_estado(False)

    def actualizar_prompt_final(self):
        prompt_base = self.view.center_panel.obtener_prompt_base()
        if not prompt_base:
            return

        self.prompt_final = self.view.right_panel.construir_prompt_final(
            prompt_base,
            self.estructura,
            self.contenido_archivos
        )
        self.prompt_final = self.view.right_panel.obtener_prompt_final()

    def copiar_prompt(self):
        if self.prompt_final:
            self.gui_helper.copiar_al_portapapeles(self.prompt_final)
        else:
            messagebox.showwarning(i18n.t("warning_title"), i18n.t("prompt_empty"))

    def limpiar_todo(self):
        self.prompt_base_path = None
        self.project_folder = None
        self.selected_files = []
        self.estructura = ''
        self.contenido_archivos = ''
        self.prompt_final = ''

        self.view.left_panel.set_prompt_base_estado(False)
        self.view.left_panel.set_project_estado(False)
        self.view.left_panel.set_archivos_estado(False)
        self.view.left_panel.mostrar_lista_archivos([])

        self.view.center_panel.mostrar_prompt_base("")
        self.view.center_panel.mostrar_estructura("")
        self.view.center_panel.mostrar_contenido_archivos("")
        self.view.right_panel.mostrar_prompt_final("")
        messagebox.showinfo(i18n.t("app_name"), i18n.t("fields_cleared"))

    def on_ignore_change(self):
        if not self.project_folder:
            return

        # Update folder structure view
        fm_struct = FileManager(self.obtener_ignorados_estructura(), self.obtener_solo_extensiones())
        self.estructura = fm_struct.genera_estructura_de_carpetas(self.project_folder)
        self.view.center_panel.mostrar_estructura(self.estructura)

        # Update file contents if any files selected
        if self.selected_files:
            fm_files = FileManager(self.obtener_ignorados_archivos(), self.obtener_solo_extensiones())
            self.contenido_archivos = fm_files.extrae_contenido_archivos(self.selected_files)
            self.view.center_panel.mostrar_contenido_archivos(self.contenido_archivos)
        self.actualizar_prompt_final()

    def save_settings(self):
        ignorados_estructura = self.obtener_ignorados_estructura()
        ignorados_archivos = self.obtener_ignorados_archivos()
        only_exts = self.obtener_solo_extensiones()
        settings = {
            "ignore_structure": ignorados_estructura,
            "ignore_files": ignorados_archivos,
            "only_extensions": only_exts
        }
        settings_file = Path("settings.json")
        try:
            settings_file.write_text(json.dumps(settings, indent=2), encoding="utf-8")
            self.view.left_panel._set_estado(self.view.left_panel.status_save, True)
            messagebox.showinfo(i18n.t("app_name"), i18n.t("save_success"))
        except Exception as e:
            self.view.left_panel._set_estado(self.view.left_panel.status_save, False)
            messagebox.showerror(i18n.t("app_name"), f"{i18n.t('save_error')} {e}")

    def save_ignore_files(self):
        ignorados_archivos = self.obtener_ignorados_archivos()
        settings_file = Path("settings.json")
        try:
            if settings_file.exists():
                data = settings_file.read_text(encoding="utf-8")
                obj = json.loads(data)
            else:
                obj = {}
            obj["ignore_files"] = ignorados_archivos
            settings_file.write_text(json.dumps(obj, indent=2), encoding="utf-8")
            self.saved_ignore_files = ignorados_archivos
            self.view.left_panel._set_estado(self.view.left_panel.status_save_files, True)
            messagebox.showinfo(i18n.t("app_name"), i18n.t("save_success"))
        except Exception as e:
            self.view.left_panel._set_estado(self.view.left_panel.status_save_files, False)
            messagebox.showerror(i18n.t("app_name"), f"{i18n.t('save_error')} {e}")

    def set_path_in_files(self):
        """
        Para cada archivo seleccionado:
        1) Elimina cualquier línea '# Path: ...' existente.
        2) Inserta un único comentario '# Path: <ruta_relativa>' 
           justo antes del primer 'import' o 'from'.
        """
        if not self.selected_files:
            messagebox.showwarning(i18n.t("warning_title"), i18n.t("no_files_selected"))
            return

        root = Path(self.project_folder)
        updated_count = 0
        pattern_old = re.compile(r'^\s*#\s*Path:')

        for fp in self.selected_files:
            p = Path(fp)
            try:
                original = p.read_text(encoding="utf-8")
            except Exception as e:
                print(f"Error leyendo {p}: {e}")
                continue

            # 1) Filtrar líneas antiguas
            lines = original.splitlines()
            without_old = [ln for ln in lines if not pattern_old.match(ln)]

            # 2) Encontrar posición del primer import/from
            insert_at = next(
                (i for i, ln in enumerate(without_old)
                 if ln.startswith("import ") or ln.startswith("from ")),
                len(without_old)
            )

            # 3) Construir y añadir el comentario
            rel = p.relative_to(root).as_posix()
            comment = f"# Path: {rel}"
            new_lines = without_old[:insert_at] + [comment] + without_old[insert_at:]

            # 4) Escribir de vuelta
            try:
                p.write_text("\n".join(new_lines), encoding="utf-8")
                updated_count += 1
            except Exception as e:
                print(f"Error escribiendo {p}: {e}")

        # Indicar éxito en la UI
        self.view.left_panel._set_estado(self.view.left_panel.status_set_path, True)
        messagebox.showinfo(
            i18n.t("app_name"),
            f"Path comments updated in {updated_count} file(s)."
        )