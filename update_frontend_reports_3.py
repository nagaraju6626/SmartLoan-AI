import re

with open('frontend/pages/10_Reports.py', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'if "report_download_url" in st\.session_state:.*?st\.markdown\(st\.session_state\["report_markdown"\]\)'

new_download = '''    if st.session_state.get("report_pdf_bytes"):
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="Download Business Report",
            data=st.session_state["report_pdf_bytes"],
            file_name=f"smart_loan_business_report.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True
        )'''

content = re.sub(pattern, new_download, content, flags=re.DOTALL)

with open('frontend/pages/10_Reports.py', 'w', encoding='utf-8') as f:
    f.write(content)
