import json
import os
from typing import Dict
import streamlit as st

@st.cache_data
def load_translations() -> dict:
    """Load translations with caching"""
    with open("assets/translations.json", "r", encoding="utf-8") as f:
        return json.load(f)

def setup_language() -> str:
    """Initialize language settings"""
    if "language" not in st.session_state:
        st.session_state.language = "en"
    return st.session_state.language

@st.cache_data
def get_translation(lang: str, key: str) -> str:
    """Get translation for specific key with caching"""
    translations = load_translations()
    lang_data = translations.get(lang, translations["en"])
    return lang_data.get(key, key)

def switch_language():
    """Toggle between English and Arabic"""
    if st.session_state.language == "en":
        st.session_state.language = "ar"
    else:
        st.session_state.language = "en"
