import streamlit as st

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from frontend.components.navigation import render_sidebar
from frontend.components.header import render_header
render_sidebar()
render_header()
st.title('API Documentation')

