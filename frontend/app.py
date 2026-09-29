import streamlit as st

st.set_page_config(
    page_title="Smart Loan Risk System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Redirect to the actual Home page
st.switch_page("pages/01_Home.py")
