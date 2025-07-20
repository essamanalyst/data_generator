import platform
import sys
import streamlit as st

def load_css() -> str:
    """Load custom CSS styles"""
    with open("assets/styles.css", "r") as f:
        return f"<style>{f.read()}</style>"

def get_python_version() -> str:
    """Get Python version information"""
    return sys.version

def get_os_info() -> str:
    """Get operating system information"""
    return f"{platform.system()} {platform.release()}"

def format_number(number: int) -> str:
    """Format large numbers with commas"""
    return "{:,}".format(number)
