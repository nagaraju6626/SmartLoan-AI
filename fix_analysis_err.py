import re

with open('frontend/pages/04_Data_Analysis.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix error message and add .empty check
old_err = '''    if raw_df is None:
        st.error("Failed to load original dataset. Please return to Data Upload and upload the file again.")
        return'''

new_err = '''    if raw_df is None or raw_df.empty:
        st.error("No dataset found. Please upload a CSV from the Data Upload page.")
        st.stop()'''

content = content.replace(old_err, new_err)

with open('frontend/pages/04_Data_Analysis.py', 'w', encoding='utf-8') as f:
    f.write(content)
