# Path: src/ui/panel_left.py
import customtkinter as ctk
from src.utils import i18n
import src.config as config

class LeftPanel:
    def __init__(self, parent, controller):
        self.controller = controller
        self.frame = ctk.CTkFrame(parent)
        self.frame.configure(height=600)

        # Botón para seleccionar prompt base
        self.btn_select_prompt = ctk.CTkButton(
            self.frame,
            text=i18n.t("select_prompt_base"),
            command=self.controller.seleccionar_prompt_base
        )
        self.btn_select_prompt.pack(pady=5, padx=10, fill="x")
        self.btn_select_prompt.helper_text = i18n.t("help_select_prompt_base")
        self.btn_select_prompt.bind("<Button-2>", self._show_helper)

        self.status_prompt = ctk.CTkLabel(
            self.frame,
            text="❌",
            text_color="red",
            width=20
        )
        self.status_prompt.pack(pady=2, padx=10)

        # Campos de ignore y extensiones
        # Ignore for folder structure
        self.label_ignore_structure = ctk.CTkLabel(
            self.frame,
            text=i18n.t("ignore_structure")
        )
        self.label_ignore_structure.pack(anchor='w', padx=10, pady=(15, 5))

        self.entry_ignore_structure = ctk.CTkTextbox(self.frame, height=60)
        self.entry_ignore_structure.pack(fill='x', padx=10)
        self.entry_ignore_structure.insert("0.0", ", ".join(self.controller.saved_ignore_structure if self.controller.saved_ignore_structure else config.FOLDERS_TO_IGNORE))
        self.entry_ignore_structure.bind("<KeyRelease>", lambda e: self.controller.on_ignore_change())
        self.entry_ignore_structure.helper_text = i18n.t("help_ignore_structure")
        self.entry_ignore_structure.bind("<Button-2>", self._show_helper)

        self.label_only_ext = ctk.CTkLabel(
            self.frame,
            text=i18n.t("only_extensions")
        )
        self.label_only_ext.pack(anchor='w', padx=10, pady=(15, 5))

        self.entry_only_ext = ctk.CTkTextbox(self.frame, height=40)
        self.entry_only_ext.pack(fill='x', padx=10)
        self.entry_only_ext.insert("0.0", ", ".join(self.controller.saved_only_extensions))
        self.entry_only_ext.bind("<KeyRelease>", lambda e: self.controller.on_ignore_change())
        self.entry_only_ext.helper_text = i18n.t("help_only_extensions")
        self.entry_only_ext.bind("<Button-2>", self._show_helper)

        # Campos de ignore para selección de archivos
        self.label_ignore_files = ctk.CTkLabel(
            self.frame,
            text=i18n.t("ignore_select_files")
        )
        self.label_ignore_files.pack(anchor='w', padx=10, pady=(15, 5))

        self.entry_ignore_files = ctk.CTkTextbox(self.frame, height=60)
        self.entry_ignore_files.pack(fill='x', padx=10)
        self.entry_ignore_files.insert("0.0", ", ".join(self.controller.saved_ignore_files if self.controller.saved_ignore_files else config.FOLDERS_TO_IGNORE))
        self.entry_ignore_files.bind("<KeyRelease>", lambda e: self.controller.on_ignore_change())
        self.entry_ignore_files.helper_text = i18n.t("help_ignore_select_files")
        self.entry_ignore_files.bind("<Button-2>", self._show_helper)

        # Save settings button (moved below file ignore)
        self.btn_save_settings = ctk.CTkButton(
            self.frame,
            text=i18n.t("save_settings"),
            command=self.controller.save_settings,
            fg_color="#4CAF50",
            hover_color="#45a049",
            state="normal"
        )
        self.btn_save_settings.pack(pady=5, padx=10, fill="x")
        self.btn_save_settings.helper_text = i18n.t("help_save_settings")
        self.btn_save_settings.bind("<Button-2>", self._show_helper)
        # Estado del guardado general
        self.status_save = ctk.CTkLabel(
            self.frame,
            text="❌",
            text_color="red",
            width=20
        )
        self.status_save.pack(pady=2, padx=10)

        # Botón para seleccionar carpeta de proyecto
        self.btn_select_project = ctk.CTkButton(
            self.frame,
            text=i18n.t("select_project"),
            command=self.controller.seleccionar_proyecto
        )
        self.btn_select_project.pack(pady=5, padx=10, fill="x")
        self.btn_select_project.helper_text = i18n.t("help_select_project")
        self.btn_select_project.bind("<Button-2>", self._show_helper)

        self.status_project = ctk.CTkLabel(
            self.frame,
            text="❌",
            text_color="red",
            width=20
        )
        self.status_project.pack(pady=2, padx=10)

        # Botón para seleccionar archivos
        self.btn_select_files = ctk.CTkButton(
            self.frame,
            text=i18n.t("select_files"),
            command=self.controller.seleccionar_archivos,
            state="disabled"
        )
        self.btn_select_files.pack(pady=5, padx=10, fill="x")
        self.btn_select_files.helper_text = i18n.t("help_select_files")
        self.btn_select_files.bind("<Button-2>", self._show_helper)

        self.status_files = ctk.CTkLabel(
            self.frame,
            text="❌",
            text_color="red",
            width=20
        )
        self.status_files.pack(pady=2, padx=10)

        # Nuevo botón para insertar/actualizar path en archivos seleccionados
        self.btn_set_path = ctk.CTkButton(
            self.frame,
            text="Set path in Selected Files",
            command=self.controller.set_path_in_files,
            state="disabled"
        )
        self.btn_set_path.pack(pady=5, padx=10, fill="x")
        self.btn_set_path.helper_text = i18n.t("help_set_path")
        self.btn_set_path.bind("<Button-2>", self._show_helper)

        self.status_set_path = ctk.CTkLabel(
            self.frame,
            text="❌",
            text_color="red",
            width=20
        )
        self.status_set_path.pack(pady=2, padx=10)

        # Lista de archivos seleccionados
        self.label_selected_files = ctk.CTkLabel(
            self.frame,
            text=i18n.t("selected_files")
        )
        self.label_selected_files.pack(anchor='w', padx=10, pady=(20, 5))

        self.listbox_files = ctk.CTkTextbox(self.frame, height=100)
        self.listbox_files.pack(fill="both", expand=False, padx=10, pady=(0, 10))
        self.listbox_files.helper_text = i18n.t("help_selected_files")
        self.listbox_files.bind("<Button-2>", self._show_helper)

        # Agrupamos widgets para estilos
        self.widgets = [
            self.btn_select_prompt, self.status_prompt,
            self.label_ignore_structure, self.entry_ignore_structure,
            self.label_only_ext, self.entry_only_ext,
            self.label_ignore_files, self.entry_ignore_files,
            self.btn_save_settings, self.status_save,
            self.btn_select_project, self.status_project,
            self.btn_select_files, self.status_files,
            self.btn_set_path, self.status_set_path,
            self.label_selected_files, self.listbox_files
        ]
        # Bind middle-click to show helper for any widget
        root = self.frame.winfo_toplevel()
        root.bind_all("<ButtonRelease-2>", self._show_helper)

    def set_prompt_base_estado(self, estado: bool):
        self._set_estado(self.status_prompt, estado)
        self.btn_select_files.configure(state="normal" if estado else "disabled")
        # El botón de set_path todavía debe estar deshabilitado
        self.btn_set_path.configure(state="disabled")
        self._set_estado(self.status_set_path, False)

    def set_project_estado(self, estado: bool):
        self._set_estado(self.status_project, estado)
        self.btn_select_files.configure(state="normal" if estado else "disabled")
        # El botón de set_path todavía debe estar deshabilitado
        self.btn_set_path.configure(state="disabled")
        self._set_estado(self.status_set_path, False)

    def set_archivos_estado(self, estado: bool, cantidad: int = 0):
        self._set_estado(self.status_files, estado)
        texto = f"{i18n.t('select_files')} ({cantidad})" if estado else i18n.t('select_files')
        self.btn_select_files.configure(text=texto)
        # Habilitar/deshabilitar el nuevo botón
        self.btn_set_path.configure(state="normal" if estado else "disabled")
        # Resetear estado de status_set_path
        self._set_estado(self.status_set_path, False)

    def _set_estado(self, label, estado: bool):
        # Usar botones icónicos en lugar de emojis
        icon = "✓" if estado else "✗"
        text_color = "#4CAF50" if estado else "#E74C3C"
        label.configure(text=icon, text_color=text_color)

    def mostrar_lista_archivos(self, archivos: list):
        self.listbox_files.configure(state="normal")
        self.listbox_files.delete("0.0", "end")
        for archivo in archivos:
            self.listbox_files.insert("end", f"{archivo}\n")
        self.listbox_files.configure(state="disabled")

    def update_styles(self, estilos: dict):
        for widget in self.widgets:
            # Fuente
            if "font" in estilos:
                widget.configure(font=estilos["font"])
            try:
                if isinstance(widget, ctk.CTkButton):
                    # Actualizar color de botones
                    widget.configure(
                        fg_color=estilos.get("button_bg", None),
                        text_color=estilos.get("button_fg", None)
                    )
                elif isinstance(widget, ctk.CTkLabel):
                    # Solo actualizar color de texto para evitar fondo blanco en modo Light
                    widget.configure(
                        text_color=estilos.get("fg_color", None)
                    )
                elif isinstance(widget, ctk.CTkTextbox):
                    widget.configure(
                        fg_color=estilos.get("entry_bg", None),
                        text_color=estilos.get("fg_color", None)
                    )
                elif isinstance(widget, ctk.CTkComboBox):
                    widget.configure(
                        fg_color=estilos.get("bg_color", None),
                        text_color=estilos.get("fg_color", None)
                    )
            except:
                pass

    def _show_helper(self, event):
        widget = event.widget
        # Buscar helper_text en el widget o sus ancestros
        while widget:
            text = getattr(widget, "helper_text", None)
            if text:
                # Crear popup CTk
                popup = ctk.CTkToplevel(self.frame)
                popup.title(i18n.t("app_name"))
                popup.transient(self.frame)
                popup.grab_set()
                ctk.CTkLabel(popup, text=text, wraplength=400).pack(padx=20, pady=10)
                ctk.CTkButton(popup, text="OK", command=popup.destroy).pack(pady=(0,10))
                break
            widget = getattr(widget, "master", None)