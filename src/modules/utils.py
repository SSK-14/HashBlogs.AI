import re
import streamlit as st
import pyperclip

def init_session_state():
    state_defaults = {
        "blog_content": None,
        "blog_content_edit": False,
        "blog_banner": None,
        "blog_content_regenerate": None,
        "question": None,
        "search_context": None,
        "search_images": None,
        "blog_audio": None,
    }
    for key, value in state_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def parse_content(blog_content):
    title_match = re.search(r"^# (.+)$", blog_content, re.MULTILINE)
    title = title_match.group(1) if title_match else None
    tldr_match = re.search(r"### tl;dr\s+(.*?)\s+(?=##|$)", blog_content, re.DOTALL)
    tldr = tldr_match.group(1).strip() if tldr_match else None
    return title, tldr

def copy_to_clipboard(text):
    pyperclip.copy(text)
    st.toast("Copied to clipboard", icon="📋")
