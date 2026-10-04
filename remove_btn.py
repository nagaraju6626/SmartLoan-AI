import re

with open("frontend/components/header.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("from frontend.components.theme import toggle_theme, apply_theme", "from frontend.components.theme import apply_theme")
content = content.replace("col0, col1, col2, col3, col4 = st.columns([0.4, 5, 0.7, 0.7, 1.2]", "col0, col1, col_spacer, col4 = st.columns([0.4, 5.0, 1.4, 1.2]")

pattern = re.compile(r'    with col2:.*?    with col4:', re.DOTALL)
content = pattern.sub('    with col_spacer:\n        st.empty()\n        \n    with col4:', content)

with open("frontend/components/header.py", "w", encoding="utf-8") as f:
    f.write(content)
