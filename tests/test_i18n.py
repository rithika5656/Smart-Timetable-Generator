"""
i18n tests.
"""
import pytest
from i18n import load_locale, get_supported_languages

def test_load_en_locale():
    data = load_locale("en")
    assert "title" in data
    assert data["btn_generate"] == "Generate Timetable"

def test_load_es_locale():
    data = load_locale("es")
    assert "title" in data
    assert data["btn_generate"] == "Generar Horario"

def test_invalid_locale():
    data = load_locale("xx")
    assert data == {}

def test_supported_languages():
    langs = get_supported_languages()
    assert "en" in langs
    assert "fr" in langs
