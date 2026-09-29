import streamlit as st
from frontend.components.navigation import render_sidebar
from frontend.components.header import render_header
from frontend.components.styles import load_css

def render_layout():
    # Load central CSS for the layout
    load_css()
    # Render the sidebar
    render_sidebar()
    # Render the header
    render_header()
