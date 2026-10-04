import re

with open('frontend/pages/01_Home.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace View Demo and update Get Started
pattern = r'<a href="Data_Upload" target="_self" class="btn-primary">.*?Get Started</a><a href="Dashboard" target="_self" class="btn-secondary">.*?View Demo</a>'

# Fix Get Started to use absolute path /Data_Upload so Streamlit's router intercepts it!
new_buttons = '<a href="/Data_Upload" target="_self" class="btn-primary">\U0001F680 Get Started</a>'

content = re.sub(pattern, new_buttons, content)

with open('frontend/pages/01_Home.py', 'w', encoding='utf-8') as f:
    f.write(content)
