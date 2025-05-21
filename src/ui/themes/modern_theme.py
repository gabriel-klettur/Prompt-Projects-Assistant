# Path: src/ui/themes/modern_theme.py
import customtkinter as ctk

def apply_modern_theme(root):
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    return {
        "font": ("Segoe UI", 12),
        "bg_color": "#2a2d2e",
        "fg_color": "white",
        "entry_bg": "#1e1f22",
        "button_bg": "#3b8ed0",
        "button_fg": "white",
        "corner_radius": 8,
        "border_width": 1,
        "button_hover": "#5aaae0"
    }