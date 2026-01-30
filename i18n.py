"""
Internationalization backend logic.
"""
import json
import os
from typing import Dict, Optional

LOCALES_DIR = os.path.join(os.path.dirname(__file__), 'locales')
CACHE = {}

def load_locale(lang: str) -> Dict[str, str]:
    """Load locale data from JSON file."""
    if lang in CACHE:
        return CACHE[lang]
        
    try:
        file_path = os.path.join(LOCALES_DIR, f"{lang}.json")
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            CACHE[lang] = data
            return data
    except FileNotFoundError:
        return {}

def get_supported_languages() -> Dict[str, str]:
    """Return dictionary of supported languages and their names."""
    return {
        "en": "English",
        "es": "Español",
        "fr": "Français"
    }
