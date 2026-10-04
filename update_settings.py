import re

with open('frontend/pages/13_Settings.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'value="Admin User"', r'value=st.session_state.get("username", "Admin User")', content)
content = re.sub(r'value="admin@smartloan.com"', r'value=st.session_state.get("email", "admin@smartloan.com")', content)

with open('frontend/pages/13_Settings.py', 'w', encoding='utf-8') as f:
    f.write(content)
