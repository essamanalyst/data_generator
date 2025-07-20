import json
import os
from typing import Dict
import streamlit as st

def setup_language() -> str:
    """Initialize language settings"""
    if "language" not in st.session_state:
        st.session_state.language = "en"
    return st.session_state.language

def get_translation(lang: str, key: str) -> str:  # <-- تغيير هنا
    """Load translations for the selected language and key"""
    with open("assets/translations.json", "r", encoding="utf-8") as f:
        translations = json.load(f)
    return translations.get(lang, translations["en"]).get(key, key)

def switch_language():
    """Toggle between English and Arabic"""
    if st.session_state.language == "en":
        st.session_state.language = "ar"
    else:
        st.session_state.language = "en"
