import re

with open('frontend/pages/01_Home.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the hero-right div styling
old_div = '<div class="hero-right" style="padding:0; width: 100%; margin:0;">'
new_div = '<div class="hero-right" style="padding:0; width: 450px; max-width: 100%; margin: 0;">'

content = content.replace(old_div, new_div)

# And if I want it even closer, I can remove the "gap='large'" from columns
# Let's also check the st.columns definition
content = content.replace('col1, col2 = st.columns([1.1, 1], gap="large")', 'col1, col2 = st.columns([1.1, 1], gap="medium")')

with open('frontend/pages/01_Home.py', 'w', encoding='utf-8') as f:
    f.write(content)
