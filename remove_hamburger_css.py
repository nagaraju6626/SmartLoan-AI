import re

with open('frontend/components/theme.py', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'/\* Force Hamburger Toggle Icon Visibility in ALL states \*/.*?text-indent: 0 !important;\s*}'
content = re.sub(pattern, '', content, flags=re.DOTALL)

with open('frontend/components/theme.py', 'w', encoding='utf-8') as f:
    f.write(content)
