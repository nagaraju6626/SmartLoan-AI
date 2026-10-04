import re

with open('frontend/components/header.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace the column definition
# col0, col1, col4 = st.columns([0.4, 6.1, 1.5], vertical_alignment="center")
pattern1 = r'col0,\s*col1,\s*col4\s*=\s*st\.columns\(\[0\.4,\s*6\.1,\s*1\.5\],\s*vertical_alignment="center"\)'
replacement1 = 'col1, col4 = st.columns([6.5, 1.5], vertical_alignment="center")'
content = re.sub(pattern1, replacement1, content)

# 2. Remove the col0 block
pattern2 = r'with col0:.*?st\.button\("[^"]*",\s*on_click=toggle_sidebar.*?key="header_sidebar_toggle"\)'
content = re.sub(pattern2, '', content, flags=re.DOTALL)

with open('frontend/components/header.py', 'w', encoding='utf-8') as f:
    f.write(content)
