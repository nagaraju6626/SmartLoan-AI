import re

files = ['frontend/components/navigation.py', 'frontend/components/styles.py']

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Find the [data-testid="stSidebar"] block and add padding-bottom
    # Specifically looking for overflow-x: hidden;
    if 'overflow-x: hidden;' in content:
        content = content.replace('overflow-x: hidden;', 'overflow-x: hidden;\n        padding-bottom: 80px !important;')
        
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("CSS updated.")
