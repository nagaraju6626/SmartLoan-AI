import streamlit as st
import sys
from pathlib import Path

# Setup path and components
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from frontend.components.navigation import render_sidebar
from frontend.components.header import render_header

st.set_page_config(page_title="Profile", page_icon="👤", layout="wide")


# --- Authentication Check ---
if not st.session_state.get("authenticated", False):
    st.switch_page("pages/00_Login.py")
# ----------------------------

render_sidebar()
render_header()

st.title("👤 Profile")
st.markdown("---")

st.subheader(st.session_state.get("username", "Admin User"))
role = "Administrator" if st.session_state.get("email") == "admin@smartloan.com" else "User"
st.write(f"**Email:** {st.session_state.get('email', 'admin@smartloan.com')}")
st.write(f"**Role:** {role}")


if role == "Administrator":
    st.info("This is the system administrator profile. You have full access to all Data Analysis, Model Training, and Applicant Risk Assessment tools within the Smart Loan platform.")
else:
    st.info("This is your user profile. You can access the available Smart Loan tools from the sidebar.")
