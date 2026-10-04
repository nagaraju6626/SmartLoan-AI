import re

with open('frontend/components/header.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the bug
content = content.replace('col1, col4 = st.columns', 'col1, col2 = st.columns')

with open('frontend/components/header.py', 'w', encoding='utf-8') as f:
    f.write(content)
