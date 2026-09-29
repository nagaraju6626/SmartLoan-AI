import streamlit as st

def initialize_theme():
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    # Force light theme globally
    st.session_state.theme = "light"

def toggle_theme():
    initialize_theme()
    # Dark mode is disabled as per project requirements

def apply_theme():
    initialize_theme()
    
    # Base CSS that applies to the theme (structural, shadows, radiuses)
    base_css = """
    <style>
    /* Search Bar Base Styling */
    div[data-testid="stTextInput"] > div > div > input {
        border-radius: 20px !important;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06) !important;
    }
    
    /* Buttons Base Styling */
    div[data-testid="column"] > div > div > div > div > button {
        height: 44px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06) !important;
    }
    div[data-testid="column"] > div > div > div > div[data-testid="stPopover"] > button {
        height: 44px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06) !important;
    }
    </style>
    """
    st.markdown(base_css, unsafe_allow_html=True)
    
    # Light Mode CSS explicitly coloring the search bar and inputs
    light_css = """
    <style>
    :root {
        --primary-color: #2563EB !important;
        --background-color: #F8FAFC !important;
        --secondary-background-color: #FFFFFF !important;
        --text-color: #0F172A !important;
    }
    .stApp { background-color: #F8FAFC !important; color: #0F172A !important; }
    
    /* Search Bar & Header Controls (Light) */
    div[data-testid="stTextInput"] > div > div > input {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        color: #334155 !important;
    }
    div[data-testid="stTextInput"] > div > div > input::placeholder {
        color: #64748B !important;
    }
    div[data-testid="column"] > div > div > div > div > button {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        color: #334155 !important;
    }
    div[data-testid="column"] > div > div > div > div[data-testid="stPopover"] > button {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        color: #1E293B !important;
    }
    </style>
    """
    st.markdown(light_css, unsafe_allow_html=True)
