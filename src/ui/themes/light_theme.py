# Path: src/ui/themes/light_theme.py
import customtkinter as ctk

def apply_light_theme(root):
    ctk.set_appearance_mode("Light")  # Asegura que estemos en modo "Light"
    ctk.set_default_color_theme("blue")  # Puedes cambiarlo por otro color si prefieres

    return {
        "font": ("Segoe UI", 12),  # Fuente más grande y legible
        "bg_color": "#f0f0f0",     # Fondo gris suave en modo Light
        "fg_color": "#333333",     # Texto en color oscuro para buen contraste
        "entry_bg": "#ffffff",     # Fondo blanco para las entradas
        "button_bg": "#4CAF50",    # Botones con un verde brillante
        "button_fg": "white"       # Texto blanco para los botones
    }