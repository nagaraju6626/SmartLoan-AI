import streamlit as st

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from frontend.components.navigation import render_sidebar
from frontend.components.header import render_header

# --- Authentication Check ---
if not st.session_state.get("authenticated", False):
    st.switch_page("pages/00_Login.py")
# ----------------------------

render_sidebar()
render_header()
st.title('API Documentation')

