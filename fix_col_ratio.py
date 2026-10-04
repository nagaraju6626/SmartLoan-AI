import re

with open('frontend/pages/01_Home.py', 'r', encoding='utf-8') as f:
    content = f.read()

# I previously used [1.1, 1] which is roughly 52% 48%.
content = content.replace('col1, col2 = st.columns([1.1, 1]', 'col1, col2 = st.columns([0.45, 0.55]')

with open('frontend/pages/01_Home.py', 'w', encoding='utf-8') as f:
    f.write(content)
