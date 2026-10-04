import re

with open('frontend/components/navigation.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('padding-bottom: 80px !important;', 'padding-bottom: 0px !important;')
content = content.replace('padding-bottom: 80px;', 'padding-bottom: 0px;')

with open('frontend/components/navigation.py', 'w', encoding='utf-8') as f:
    f.write(content)
