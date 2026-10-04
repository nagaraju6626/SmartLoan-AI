import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

st.set_page_config(
    page_title="Smart Loan Risk System",
    layout="wide",
    initial_sidebar_state="expanded"
)

if not st.session_state.get("authenticated", False):
    st.switch_page("pages/00_Login.py")
else:
    st.switch_page("pages/01_Home.py")
