import re

with open('frontend/pages/10_Reports.py', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'if st\.session_state\.get\("report_pdf_bytes"\):\s*st\.markdown\("<br>", unsafe_allow_html=True\)\s*st\.download_button\('

new_download = '''    if st.session_state.get("report_pdf_bytes"):
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button('''

content = re.sub(pattern, new_download, content, flags=re.DOTALL)

with open('frontend/pages/10_Reports.py', 'w', encoding='utf-8') as f:
    f.write(content)
