import os
import re

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'st.dataframe(' in content and 'apply_dataframe_style' not in content:
        # Add import
        import_stmt = "from frontend.components.theme import apply_dataframe_style\n"
        
        # We find the place to insert the import
        # Usually after 'import streamlit as st'
        content = re.sub(r'(import streamlit as st\n)', r'\1' + import_stmt, content)
        
        # Now replace st.dataframe(X, ...) with st.dataframe(apply_dataframe_style(X), ...)
        # We need a robust regex for this
        # It's easier to just do a simple replacement for the specific usages we found.
        # But a regex that captures the first argument to st.dataframe is:
        # st.dataframe(arg, ...) -> st.dataframe(apply_dataframe_style(arg), ...)
        
        # Let's do a simple regex since most arguments are separated by commas
        content = re.sub(
            r'st\.dataframe\(([^,]+),\s*use_container_width', 
            r'st.dataframe(apply_dataframe_style(\1), use_container_width', 
            content
        )
        content = re.sub(
            r'st\.dataframe\((pd\.DataFrame\([^)]+\)),\s*use_container_width', 
            r'st.dataframe(apply_dataframe_style(\1), use_container_width', 
            content
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

pages_dir = 'frontend/pages'
for filename in os.listdir(pages_dir):
    if filename.endswith('.py'):
        update_file(os.path.join(pages_dir, filename))
