
# Path: src/ui/themes/classic_theme.py
import customtkinter as ctk

def apply_classic_theme(root):
    ctk.set_appearance_mode("Light")  # Mantener el modo claro para el tema clásico

    # Colores más suaves y neutros para el tema clásico
    return {
        "font": ("Segoe UI", 10),  # Fuente más pequeña y ligera
        "bg_color": "#f0f0f0",     # Fondo muy claro, pero no tan brillante como el tema claro
        "fg_color": "#444444",     # Texto en gris oscuro para dar un toque más tenue
        "entry_bg": "#ffffff",     # Fondo blanco para las entradas
        "button_bg": "#d9d9d9",    # Botones de un gris suave
        "button_fg": "black"       # Texto negro para los botones
    }