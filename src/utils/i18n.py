# src/utils/i18n.py

from src.utils import translations_en, translations_es, translations_is

AVAILABLE_LANGUAGES = {
    "EN": translations_en.translations,
    "ES": translations_es.translations,
    "IS": translations_is.translations,
}

current_language = "EN"

def set_language(lang_code):
    global current_language
    if lang_code in AVAILABLE_LANGUAGES:
        current_language = lang_code

def t(key):
    return AVAILABLE_LANGUAGES[current_language].get(key, key)
