import re

with open('frontend/components/header.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace column structure
old_cols = '''    col0, col1, col4 = st.columns([0.4, 6.1, 1.5], vertical_alignment="center")
    
    with col0:
        st.button("☰", on_click=toggle_sidebar, use_container_width=True, key="header_sidebar_toggle")
        
    with col1:'''

new_cols = '''    col1, col2 = st.columns([6.5, 1.5], vertical_alignment="center")
    
    with col1:'''

content = content.replace(old_cols, new_cols)

# Also need to replace the col4 usage
content = content.replace('    with col4:', '    with col2:')

with open('frontend/components/header.py', 'w', encoding='utf-8') as f:
    f.write(content)
