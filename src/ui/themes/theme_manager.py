
# Path: src/ui/themes/theme_manager.py
import customtkinter as ctk
from src.ui.themes.classic_theme import apply_classic_theme
from src.ui.themes.modern_theme import apply_modern_theme
from src.ui.themes.light_theme import apply_light_theme

class ThemeManager:
    def __init__(self, root, theme_name="Moderno"):
        self.root = root
        self.theme_name = theme_name
        self.theme_styles = {}

    def apply_theme(self):
        print(f"[ThemeManager] Aplicando tema: {self.theme_name}")  # ✅ Debug
        if self.theme_name == "Moderno":
            ctk.set_appearance_mode("Dark")
            self.theme_styles = apply_modern_theme(self.root)
        elif self.theme_name == "Light":
            ctk.set_appearance_mode("Light")
            self.theme_styles = apply_light_theme(self.root)
        elif self.theme_name == "Clasico":
            self.theme_styles = apply_classic_theme(self.root)
        else:
            # Fallback
            ctk.set_appearance_mode("System")
            self.theme_styles = apply_modern_theme(self.root)

    def get_styles(self):
        """Devuelve los estilos actuales como diccionario, si los paneles necesitan acceso directo."""
        return self.theme_styles