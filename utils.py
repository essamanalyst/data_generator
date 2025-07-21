import platform
import sys
import streamlit as st
import time
@st.cache_data
def load_css() -> str:
    """Load CSS styles with caching"""
    try:
        with open("assets/styles.css", "r") as f:
            return f"<style>{f.read()}</style>"
    except FileNotFoundError:
        return "<style></style>"

def get_python_version() -> str:
    """Get Python version information"""
    return sys.version.split()[0]

def get_os_info() -> str:
    """Get operating system information"""
    return f"{platform.system()} {platform.release()}"

def format_number(number: int) -> str:
    """Format large numbers with commas"""
    return "{:,}".format(number)

@st.cache_data
def measure_performance(func):
    """Decorator to measure function performance"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        st.caption(f"Function '{func.__name__}' executed in {end_time-start_time:.4f} seconds")
        return result
    return wrapper
