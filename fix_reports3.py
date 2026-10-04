import re

with open('frontend/pages/10_Reports.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the file_path checks inside "Generate Report" button
pattern = r'# 1\. Validate dataset existence.*?# 2\. Validate dataset readability and content'
replacement = '# 1. Validate dataset existence in session state\n        '

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('frontend/pages/10_Reports.py', 'w', encoding='utf-8') as f:
    f.write(content)
