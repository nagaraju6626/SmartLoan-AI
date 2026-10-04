import streamlit as st
import sys
from pathlib import Path

# Setup path and components
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from frontend.components.navigation import render_sidebar
from frontend.components.header import render_header

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")

# --- Authentication Check ---
if not st.session_state.get("authenticated", False):
    st.switch_page("pages/00_Login.py")
# ----------------------------

render_sidebar()
render_header()

st.title("⚙️ Application Settings")
st.markdown("---")

st.subheader("Account Settings")

with st.form("settings_form"):
    new_name = st.text_input("Change Name", value=st.session_state.get("username", "Admin User"))
    new_email = st.text_input("Change Email", value=st.session_state.get("email", "admin@smartloan.com"))
    new_password = st.text_input("Change Password", type="password")
    
    submit = st.form_submit_button("Save Changes")
    
    if submit:
        st.success("Settings updated successfully!")

