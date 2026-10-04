with open('frontend/components/header.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('st.switch_page(\"pages/01_Home.py\")', 'st.switch_page(\"pages/00_Login.py\")')
with open('frontend/components/header.py', 'w', encoding='utf-8') as f:
    f.write(content)
