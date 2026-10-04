import streamlit as st
from streamlit.source_util import get_pages
pages = get_pages("")
for page_hash, page in pages.items():
    print(page["page_name"], page["script_path"])
