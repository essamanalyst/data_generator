import json
import streamlit as st

@st.cache_data
def load_translations():
    """تحميل ملفات الترجمة مع التخزين المؤقت"""
    try:
        with open("assets/translations.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"en": {}, "ar": {}}

def setup_language():
    """تهيئة إعدادات اللغة"""
    if "language" not in st.session_state:
        st.session_state.language = "en"
    return st.session_state.language

def get_translation(lang: str, key: str) -> str:
    """الحصول على الترجمة مع التعامل مع الأخطاء"""
    translations = load_translations()
    lang_dict = translations.get(lang, translations.get("en", {}))
    return lang_dict.get(key, key)

def switch_language():
    """تبديل اللغة بين الإنجليزية والعربية"""
    if "language" not in st.session_state:
        st.session_state.language = "en"
    else:
        st.session_state.language = "ar" if st.session_state.language == "en" else "en"
