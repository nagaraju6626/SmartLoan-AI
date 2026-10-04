import re

with open('frontend/pages/04_Data_Analysis.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'st.warning("Please upload or select a dataset from the Data Upload page first.")',
    'st.warning("No dataset uploaded. Please upload a dataset first.")'
)

content = content.replace(
    'st.error("Failed to load original dataset.")',
    'st.error("Failed to load original dataset. Please return to Data Upload and upload the file again.")'
)

with open('frontend/pages/04_Data_Analysis.py', 'w', encoding='utf-8') as f:
    f.write(content)
