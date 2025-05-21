# Path: src/ui/panel_right.py
import tkinter as tk
import customtkinter as ctk
from src.utils import i18n
import tiktoken

class RightPanel:
    def __init__(self, parent, controller):
        self.controller = controller
        self.frame = ctk.CTkFrame(parent)

        self.title_label = ctk.CTkLabel(self.frame, text=i18n.t("generated_prompt"), font=("Segoe UI", 14, "bold"))
        self.title_label.pack(anchor='w', padx=10, pady=(10, 5))

        self.text_prompt_final = ctk.CTkTextbox(self.frame, height=400)
        self.text_prompt_final.pack(fill="both", expand=True, padx=10, pady=5)

        botones_frame = ctk.CTkFrame(self.frame)
        botones_frame.pack(pady=10, padx=10)

        self.btn_copiar = ctk.CTkButton(botones_frame, text=i18n.t("copy"), command=self.controller.copiar_prompt, width=150)
        self.btn_copiar.pack(side="left", padx=10)

        self.btn_limpiar = ctk.CTkButton(botones_frame, text=i18n.t("clear"), command=self.controller.limpiar_todo, width=150)
        self.btn_limpiar.pack(side="left", padx=10)

        # Label para contador de tokens
        self.label_token_count = ctk.CTkLabel(self.frame, text="Tokens: 0")
        self.label_token_count.pack(anchor='w', padx=10)

        # Frame para separar el prompt en partes
        self.split_frame = ctk.CTkFrame(self.frame)
        self.split_frame.pack(pady=5, padx=10, fill="x")

        # Campo para tamaño de separación (tokens por parte)
        self.size_label = ctk.CTkLabel(self.split_frame, text=i18n.t("tokens_per_part"))
        self.size_label.pack(side="left", padx=5)
        self.chunk_size_entry = ctk.CTkEntry(self.split_frame, width=100)
        self.chunk_size_entry.insert(0, "50000")
        self.chunk_size_entry.pack(side="left", padx=5)

        # Botón para separar el prompt en partes
        self.btn_split = ctk.CTkButton(self.split_frame, text=f"{i18n.t('split_into')}: 0", command=self.split_prompt, width=150)
        self.btn_split.pack(side="left", padx=10)

        # Menú de opciones para seleccionar la parte a copiar
        self.part_optionmenu = ctk.CTkComboBox(self.split_frame, values=[i18n.t("copy")], command=self.on_part_selected, width=150)
        self.part_optionmenu.pack(side="left", padx=10)
        # Valor inicial 'copy' para mostrar y luego deshabilitar
        self.part_optionmenu.set(i18n.t("copy"))
        self.part_optionmenu.configure(state="disabled")

        # Lista de partes del prompt
        self.prompt_parts = []

        self.widgets = [
            self.title_label, self.text_prompt_final, self.btn_copiar, self.btn_limpiar, self.label_token_count,
            self.btn_split, self.part_optionmenu, self.size_label, self.chunk_size_entry
        ]

    def mostrar_prompt_final(self, prompt):
        self.text_prompt_final.delete("1.0", tk.END)
        self.text_prompt_final.insert(tk.END, prompt)
        # Actualizar contador de tokens
        self.update_token_count()

    def construir_prompt_final(self, prompt_base, estructura, archivos):
        self.text_prompt_final.delete("1.0", tk.END)

        if prompt_base:
            self._insertar_separador_titulado(i18n.t("section_prompt_base"))
            self.text_prompt_final.insert(tk.END, prompt_base + "\n", "prompt")

        if estructura:
            self._insertar_separador_titulado(i18n.t("section_structure"))
            self.text_prompt_final.insert(tk.END, estructura + "\n", "estructura")

        if archivos:
            self._insertar_separador_titulado(i18n.t("section_file_contents"))
            self.text_prompt_final.insert(tk.END, archivos, "archivos")
        # Actualizar contador de tokens
        self.update_token_count()
        return self.text_prompt_final.get("1.0", tk.END).strip()

    def _insertar_separador_titulado(self, titulo):
        self.text_prompt_final.insert(tk.END, f"\n-------------------------------------------------------\n", "separador")
        self.text_prompt_final.insert(tk.END, f"\n-------- {titulo.upper()} --------\n", "separador")
        self.text_prompt_final.insert(tk.END, f"\n-------------------------------------------------------\n", "separador")

    def obtener_prompt_final(self):
        return self.text_prompt_final.get("1.0", tk.END).strip()

    def update_token_count(self):
        """Actualiza la etiqueta con el número de tokens del prompt generado."""
        prompt = self.obtener_prompt_final()
        try:
            enc = tiktoken.get_encoding("cl100k_base")
        except AttributeError:
            enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
        count = len(enc.encode(prompt))
        self.label_token_count.configure(text=f"Tokens: {count}")
        # Actualizar etiqueta del botón según número de partes
        try:
            size = int(self.chunk_size_entry.get())
        except ValueError:
            size = 50000
        num_parts = (count + size - 1) // size if count > 0 else 0
        self.btn_split.configure(text=f"{i18n.t('split_into')}: {num_parts}")

    def update_styles(self, estilos: dict):
        for widget in self.widgets:
            if isinstance(widget, (ctk.CTkLabel, ctk.CTkTextbox, ctk.CTkButton)):
                if "font" in estilos:
                    widget.configure(font=estilos["font"])
            try:
                if "fg_color" in estilos:
                    widget.configure(fg_color=estilos["bg_color"])
                if "text_color" in estilos:
                    widget.configure(text_color=estilos["fg_color"])
            except:
                pass

    # -------- Métodos para separar el prompt en partes --------
    def split_prompt(self):
        prompt = self.obtener_prompt_final()
        if not prompt:
            return
        try:
            enc = tiktoken.get_encoding("cl100k_base")
        except AttributeError:
            enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
        tokens = enc.encode(prompt)
        try:
            size = int(self.chunk_size_entry.get())
        except ValueError:
            size = 50000
        chunk_size = size
        parts = [enc.decode(tokens[i:i+chunk_size]) for i in range(0, len(tokens), chunk_size)]
        self.prompt_parts = parts
        values = [f"{i18n.t('part')} {i+1}" for i in range(len(parts))]
        self.part_optionmenu.configure(values=values)
        self.part_optionmenu.configure(state="normal")
        if values:
            self.part_optionmenu.set(values[0])

    def on_part_selected(self, choice):
        try:
            index = int(choice.split()[-1]) - 1
            part = self.prompt_parts[index]
            # Preparar mensaje con comillas quintuple y etiqueta de parte
            context_intro = i18n.t("context_intro")
            part_label = i18n.t("part")
            if index == 0:
                message = f"{context_intro}\n{part_label} 1: '''''{part}'''''"
            else:
                message = f"{part_label} {index+1}: '''''{part}'''''"
            self.controller.copiar_parte_prompt(message)
        except Exception:
            pass